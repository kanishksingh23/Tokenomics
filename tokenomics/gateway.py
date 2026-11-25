"""Tokenomics gateway: an OpenAI-compatible endpoint that applies the techniques to any app.

    TOKENOMICS_UPSTREAM=mock uvicorn tokenomics.gateway:create_app --factory --port 8000
    OPENAI_API_KEY=sk-...    uvicorn tokenomics.gateway:create_app --factory --port 8000

An app switches by changing two settings, nothing else:
    OPENAI_BASE_URL=http://localhost:8000/v1
    OPENAI_API_KEY=<a Tokenomics key from `python -m tokenomics.keys create --client NAME`>

Per request: check the key -> safe response cache -> conversation memory -> spending limits ->
provider call -> record the actual cost, store the answer for reuse, trace it. GPT-6 requests
without a `verbosity` get "low" (TOKENOMICS_VERBOSITY, "off" to disable).

Optional request headers (each ignored if absent):
    X-Tokenomics-Question   the end user's own words, for cache matching
                            (default: the last user message)
    X-Tokenomics-Namespace  what else changes the right answer, e.g. the app's knowledge-base
                            version (default: a fingerprint of the system messages)
    X-Tokenomics-Private    "true" when the prompt holds personal data: never cached
    X-Tokenomics-Client     the end user, for per-user budgets under the app's key
Every response carries a "tokenomics" object: who answered, the model, the cost, and what each
technique did. Streaming is not supported (out of scope, Tokenomics.md v2.9).
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from tokenomics import techniques, tracing
from tokenomics.keys import KeyStore
from tokenomics.pricing import PRICING, price
from tokenomics.response_cache import ResponseCache, namespace_key
from tokenomics.spending_limits import SpendingLimits, estimate_cost
from tokenomics.tokens import count_tokens, prompt_tokens

# Request parameters that change the right answer, so they belong in the cache namespace.
_ANSWER_PARAMS = ("temperature", "top_p", "max_tokens", "max_completion_tokens", "stop", "seed",
                  "tools", "tool_choice", "response_format", "reasoning_effort", "verbosity", "n")


def _env(name: str, default):
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    if isinstance(default, bool):
        return raw.strip().lower() in ("1", "true", "on", "yes")
    return type(default)(raw)


@dataclass
class Settings:
    upstream: str = "openai"                  # "openai" or "mock" (no provider calls)
    upstream_base_url: str = "https://api.openai.com/v1"
    upstream_api_key: str = ""
    keys_path: str = "gateway_keys.json"
    state_dir: str = ".tokenomics"
    cache: bool = True
    cache_threshold: float = 0.88
    cache_ttl_hours: float = 24.0
    limits: bool = True
    global_daily_usd: float = 5.0
    client_daily_usd: float = 1.0             # per key, unless the key sets its own
    end_user_daily_usd: float = 0.05          # per X-Tokenomics-Client end user
    soft_ratio: float = 0.8
    rpm: float = 60.0
    downgrade_model: str = "gpt-6-luna"
    memory: str = "off"                       # off | window | facts | summary
    # Provider length setting added when the app sends none ("off" = never). "low" cut Sol's
    # cost 5.5% with every answer still correct (real runs, 2026-11-25). GPT-6 models only:
    # the parameter was checked on Sol and Luna; other providers may reject it.
    verbosity: str = "low"
    keep_turns: int = 2
    expected_output_tokens: int = 200
    default_max_tokens: int = 2000
    mock_output_tokens: int = 93
    extra: dict = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> Settings:
        s = cls()
        for name in s.__dataclass_fields__:
            if name != "extra":
                setattr(s, name, _env(f"TOKENOMICS_{name.upper()}", getattr(s, name)))
        s.upstream_api_key = os.getenv("OPENAI_API_KEY", s.upstream_api_key)
        s.keys_path = os.getenv("TOKENOMICS_KEYS", s.keys_path)   # same name as tokenomics.keys
        return s


def _error(status: int, message: str, kind: str, headers: dict | None = None):
    return JSONResponse({"error": {"message": message, "type": kind, "code": status}},
                        status_code=status, headers=headers)


def _completion(model: str, text: str, usage: dict, finish: str = "stop") -> dict:
    """A chat.completion object, for answers that did not come from the provider."""
    return {"id": f"chatcmpl-tk-{uuid.uuid4().hex[:20]}", "object": "chat.completion",
            "created": int(time.time()), "model": model,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": text},
                         "finish_reason": finish}],
            "usage": usage}


def mock_upstream(settings: Settings):
    """Provider stand-in: answers instantly, counts real input tokens, no network, no cost."""
    def call(request: dict) -> dict:
        question = next((m["content"] for m in reversed(request["messages"]) if m["role"] == "user"), "")
        text = f"[MOCK RESPONSE via Tokenomics gateway] A real answer to: {question[-200:]}"
        filler = " (placeholder standing in for a real answer)"
        while count_tokens(text) < settings.mock_output_tokens:
            text += filler
        pt = prompt_tokens(request["messages"])
        return _completion(request["model"], text, {"prompt_tokens": pt,
                                                    "completion_tokens": settings.mock_output_tokens,
                                                    "total_tokens": pt + settings.mock_output_tokens})
    return call


def openai_upstream(settings: Settings):
    """The real provider, through the OpenAI SDK, adapting to each model's parameter quirks."""
    from openai import OpenAI  # noqa: PLC0415

    from tokenomics.upstream import chat_completion  # noqa: PLC0415
    client = OpenAI(api_key=settings.upstream_api_key, base_url=settings.upstream_base_url)

    def call(request: dict) -> dict:
        extra = {k: request[k] for k in ("verbosity", "response_format", "tools", "tool_choice",
                                          "stop", "seed", "top_p") if k in request}
        resp, _ = chat_completion(
            client, request["model"], request["messages"],
            max_tokens=request.get("max_completion_tokens") or request.get("max_tokens")
            or settings.default_max_tokens,
            temperature=request.get("temperature"), reasoning_effort=request.get("reasoning_effort"),
            **extra)
        return resp.model_dump()
    return call


def _usage_numbers(usage: dict) -> tuple[int, int, int, int, int]:
    """prompt, completion, cached, cache-written, reasoning tokens from either API's usage."""
    details = usage.get("prompt_tokens_details") or usage.get("input_tokens_details") or {}
    out = usage.get("completion_tokens_details") or usage.get("output_tokens_details") or {}
    return (usage.get("prompt_tokens") or usage.get("input_tokens") or 0,
            usage.get("completion_tokens") or usage.get("output_tokens") or 0,
            details.get("cached_tokens") or 0, details.get("cache_write_tokens") or 0,
            out.get("reasoning_tokens") or 0)


def create_app(settings: Settings | None = None, upstream=None, keys: KeyStore | None = None):
    """The FastAPI app. Tests pass their own settings, upstream and keys."""
    s = settings or Settings.from_env()
    state = Path(s.state_dir)
    in_memory = s.state_dir == ":memory:"
    if not in_memory:
        state.mkdir(parents=True, exist_ok=True)
    keys = keys or KeyStore(s.keys_path)
    upstream = upstream or (mock_upstream(s) if s.upstream == "mock" else openai_upstream(s))
    cache = (ResponseCache(":memory:" if in_memory else state / "responses.sqlite",
                           threshold=s.cache_threshold, ttl_hours=s.cache_ttl_hours)
             if s.cache else None)
    limits = (SpendingLimits(":memory:" if in_memory else state / "spend.sqlite",
                             client_daily_usd=s.end_user_daily_usd, global_daily_usd=s.global_daily_usd,
                             soft_ratio=s.soft_ratio, rpm=s.rpm, downgrade_model=s.downgrade_model)
              if s.limits else None)
    if cache is not None:
        cache.encode(["warm up"])     # load the embedding model now, not on the first request
    summary_cache: dict = {}
    app = FastAPI(title="Tokenomics gateway", version="0.1.0")
    app.state.settings, app.state.cache, app.state.limits = s, cache, limits

    def client_for(request: Request):
        auth = request.headers.get("authorization", "")
        return keys.lookup(auth[7:].strip() if auth.lower().startswith("bearer ") else None)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/ready")
    def ready():
        problems = []
        if s.upstream != "mock" and not s.upstream_api_key:
            problems.append("no provider key (OPENAI_API_KEY)")
        if not keys.clients():
            problems.append("no client keys yet (python -m tokenomics.keys create --client NAME)")
        status = 200 if not problems else 503
        return JSONResponse({"ready": not problems, "upstream": s.upstream, "problems": problems},
                            status_code=status)

    @app.get("/v1/models")
    def models(request: Request):
        client = client_for(request)
        if client is None:
            return _error(401, "missing or unknown Tokenomics API key", "invalid_api_key")
        ids = client.allowed_models or sorted(PRICING)
        return {"object": "list", "data": [{"id": m, "object": "model", "owned_by": "tokenomics"}
                                           for m in ids]}

    @app.post("/v1/chat/completions")
    async def chat(request: Request):
        from starlette.concurrency import run_in_threadpool  # noqa: PLC0415
        client = client_for(request)
        if client is None:
            return _error(401, "missing or unknown Tokenomics API key", "invalid_api_key")
        try:
            body = await request.json()
        except json.JSONDecodeError:
            return _error(400, "request body is not valid JSON", "invalid_request_error")
        # The provider call blocks; run it in a worker thread so other requests keep moving.
        return await run_in_threadpool(handle, client, body, dict(request.headers))

    def handle(client, body: dict, h: dict):
        if body.get("stream"):
            return _error(400, "streaming is not supported by this gateway", "invalid_request_error")
        model, messages = body.get("model"), body.get("messages")
        if not model or not isinstance(messages, list) or not messages:
            return _error(400, "model and messages are required", "invalid_request_error")
        if client.allowed_models and model not in client.allowed_models:
            return _error(403, f"model {model!r} is not allowed for this key", "permission_error")
        verbosity_note = None
        if (s.verbosity.strip().lower() not in ("", "off", "none") and "verbosity" not in body
                and str(model).startswith("gpt-6")):
            body = {**body, "verbosity": s.verbosity}
            verbosity_note = f"{s.verbosity} (gateway default)"
        end_user = h.get("x-tokenomics-client")
        spender = f"{client.client_id}:{end_user}" if end_user else client.client_id
        private = h.get("x-tokenomics-private", "").lower() in ("1", "true", "yes")
        question = h.get("x-tokenomics-question") or next(
            (m.get("content") or "" for m in reversed(messages) if m.get("role") == "user"), "")
        single_turn = not any(m.get("role") == "assistant" for m in messages)
        system = [m.get("content") for m in messages if m.get("role") == "system"]
        ns = namespace_key(client=client.client_id, model=model,
                           context=h.get("x-tokenomics-namespace")
                           or hashlib.sha256(json.dumps(system).encode()).hexdigest()[:16],
                           **{k: body.get(k) for k in _ANSWER_PARAMS})
        note = {"served_by": "model", "requested_model": model}
        if verbosity_note:
            note["verbosity"] = verbosity_note
        with tracing.observation("tokenomics-gateway", as_type="span", input=question) as root:
            # 1. safe response cache: first questions only (a follow-up means nothing alone)
            if cache is not None and single_turn and not private:
                with tracing.observation("response-cache", as_type="span", input=question) as step:
                    look = cache.lookup(question, ns)
                    step.update(output=look.reason)
                note["cache"] = look.reason
                if look.hit:
                    note.update(served_by="cache", model=look.hit.model, cost_usd=0.0,
                                cache_kind=look.hit.kind, cache_score=round(look.hit.score, 3))
                    root.update(output=look.hit.answer, metadata=note)
                    body_out = _completion(model, look.hit.answer,
                                           {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0})
                    body_out["tokenomics"] = note
                    return JSONResponse(body_out, headers={"X-Tokenomics-Served-By": "cache"})
            elif private:
                note["cache"] = "skipped: private request"
            # 2. conversation memory
            req = {k: v for k, v in body.items() if k not in ("stream", "user", "metadata")}
            summary_cost = [0.0]

            def summarise(prev, msgs):
                convo = "\n".join(f"{m['role']}: {m['content']}" for m in msgs)
                sreq = {"model": s.downgrade_model, "max_tokens": 400, "reasoning_effort": "none",
                        "messages": [{"role": "system", "content": "Summarise this part of a "
                                      "customer chat in at most 3 short sentences. Keep every number, "
                                      "amount, date and product name exactly; add nothing."},
                                     {"role": "user", "content": (f"Summary so far: {prev}\n" if prev else "")
                                      + convo}]}
                out = upstream(sreq)
                pt, ct, ca, cw, _ = _usage_numbers(out.get("usage") or {})
                summary_cost[0] += price(s.downgrade_model, pt, ct, ca, cw)
                return out["choices"][0]["message"]["content"]
            req, mem = techniques.apply_memory(req, s.memory, s.keep_turns, summarise, summary_cache)
            note["memory"] = {"mode": s.memory, "dropped_turns": mem["dropped_turns"]}
            # 3. spending limits, before anything is spent
            if limits is not None:
                # The key's own budget, or the defaults; end users get the per-user budget.
                budget = (s.end_user_daily_usd if end_user else
                          client.daily_budget_usd if client.daily_budget_usd is not None
                          else s.client_daily_usd)
                expected = s.expected_output_tokens

                def est(m):
                    return estimate_cost(m, req["messages"], expected)
                with tracing.observation("spending-limit", as_type="guardrail", input=spender) as step:
                    decision = limits.check(spender, model, est, budget)
                    step.update(output=decision.action, metadata={"reason": decision.reason})
                note["limit"] = {"action": decision.action, "reason": decision.reason}
                if decision.action == "refuse":
                    root.update(output=None, metadata=note, level="WARNING")
                    return _error(429, f"Tokenomics spending limit: {decision.reason}",
                                  "rate_limit_exceeded", {"X-Tokenomics-Served-By": "limit"})
                if decision.action == "downgrade":
                    req["model"] = decision.model
            # 4. the provider
            with tracing.observation("llm", as_type="generation", model=req["model"],
                                     input=req["messages"]) as gen:
                try:
                    out = upstream(req)
                except Exception as exc:                       # noqa: BLE001
                    status = getattr(exc, "status_code", 502) or 502
                    gen.update(level="ERROR", status_message=str(exc)[:300])
                    return _error(status, f"provider error: {str(exc)[:300]}", "upstream_error")
                pt, ct, ca, cw, rt = _usage_numbers(out.get("usage") or {})
                cost = price(req["model"], pt, ct, ca, cw) + summary_cost[0]
                usage, cost_split = tracing.usage_and_cost(req["model"], pt, ct, ca, rt, cw)
                gen.update(output=out["choices"][0]["message"].get("content"), usage_details=usage,
                           cost_details=cost_split or None)
            if limits is not None:
                limits.record(spender, cost)
            answer = out["choices"][0]["message"].get("content") or ""
            finish = out["choices"][0].get("finish_reason")
            # 5. keep the answer for reuse
            if cache is not None and single_turn and not private and finish != "length" and answer:
                note["cache_store"] = cache.store(question, answer, ns, req["model"])
            note.update(model=req["model"], cost_usd=round(cost, 8),
                        summary_cost_usd=round(summary_cost[0], 8))
            root.update(output=answer, metadata=note)
        out["tokenomics"] = note
        return JSONResponse(out, headers={"X-Tokenomics-Served-By": "model",
                                          "X-Tokenomics-Model": req["model"],
                                          "X-Tokenomics-Cost-USD": f"{cost:.8f}"})

    return app
