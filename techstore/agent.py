"""TechStore support agent (Phase 0).

Deliberately has NO router, cache, classifier or circuit breaker. It answers a
question by retrieving relevant knowledge-base documents and calling one model.

This is (a) the application the router will sit underneath, and (b) the
always-frontier baseline arm of the Week 10 benchmark. `benchmarks/run_baseline.py`
is this class in a loop.

Week 4: set OPENAI_BASE_URL to the router and change nothing else.
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

import config
from retriever import Doc, build_retriever, load_docs

ORDER_ID = re.compile(r"\b(?:order\s*#?\s*)?(\d{5})\b", re.I)

# Chat formatting overhead: ~3 tokens per message plus 3 to prime the reply.
_MSG_OVERHEAD = 3
_REPLY_PRIMING = 3


def _make_counter():
    """Real tokenizer when available; otherwise a word-count heuristic.
    Measured on the seed set, words x 4/3 undercounts by ~14%, so the
    fallback uses 1.5 tokens per word."""
    try:
        import tiktoken  # noqa: PLC0415
        enc = tiktoken.get_encoding("o200k_base")
        return (lambda t: len(enc.encode(t))), "tiktoken/o200k_base"
    except Exception:                                   # noqa: BLE001
        return (lambda t: (len(t.split()) * 3 + 1) // 2), "heuristic/1.5-per-word"


count_tokens, TOKEN_COUNTER = _make_counter()


# Parameter quirks, learned at runtime per model. Newer OpenAI reasoning models
# reject `temperature` and `max_tokens` (wanting `max_completion_tokens`); some
# OpenAI-compatible servers reject `max_completion_tokens`. Each quirk costs one
# rejected request (400s are not billed) and is then remembered.
_QUIRKS: dict[str, dict] = {}


def chat_completion(client, model: str, messages: list[dict], max_tokens: int,
                    temperature: float | None):
    """Returns (response, temperature actually sent or None)."""
    q = _QUIRKS.setdefault(model, {"temperature": True, "limit": "max_completion_tokens"})
    for _ in range(4):
        kwargs = {"model": model, "messages": messages, q["limit"]: max_tokens}
        if q["temperature"] and temperature is not None:
            kwargs["temperature"] = temperature
        try:
            return client.chat.completions.create(**kwargs), kwargs.get("temperature")
        except Exception as exc:                        # noqa: BLE001
            if getattr(exc, "status_code", None) != 400:
                raise
            msg = str(exc).lower()
            if q["temperature"] and "temperature" in msg:
                q["temperature"] = False
                continue
            if f"'{q['limit']}'" in msg or f'"{q["limit"]}"' in msg or f" {q['limit']} " in f" {msg} ":
                q["limit"] = ("max_tokens" if q["limit"] == "max_completion_tokens"
                              else "max_completion_tokens")
                continue
            raise
    raise RuntimeError(f"{model}: could not find request parameters the model accepts")


@dataclass
class Answer:
    """One interaction. This record is the seed of the spec's accounting ledger."""
    question: str
    answer: str
    model: str
    retriever: str = ""
    retrieved: list[str] = field(default_factory=list)
    orders_used: list[str] = field(default_factory=list)
    prompt_tokens: int = 0
    cached_prompt_tokens: int = 0
    completion_tokens: int = 0
    reasoning_tokens: int = 0         # hidden, billed as output; 0 for non-reasoning models
    finish_reason: str | None = None  # "length" means the answer was cut off at MAX_TOKENS
    temperature_used: float | None = None  # None: the model rejected temperature (not reproducible at T=0)
    cost_usd: float = 0.0
    # True in mock mode: tokens are counted locally and output length is
    # assumed. Never mix estimated rows into benchmark results.
    cost_is_estimate: bool = False
    latency_ms: float = 0.0
    retrieval_ms: float = 0.0
    error: str | None = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


def _load_orders(path: Path) -> dict[str, dict]:
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                o = json.loads(line)
                out[o["order_id"]] = o
    return out


class MockCompletion:
    """Offline stand-in for the model. Echoes the retrieved documents so the
    retrieval and accounting path can be exercised with no API key and no spend.
    Used by --mock and available to tests."""

    def __init__(self, agent: "SupportAgent"):
        self.agent = agent

    def respond(self, question: str, context: str, retrieved: list[str]) -> tuple[str, int, int]:
        titles = [d.title for d in self.agent.docs if d.id in retrieved]
        body = (
            "[MOCK RESPONSE - no model was called]\n\n"
            f"A real answer to {question!r} would be composed from:\n"
            + "\n".join(f"  - {t}" for t in titles)
        )
        # Count what the API would actually receive: two messages plus overhead.
        system = f"{self.agent.system_prompt}\n\n{context}"
        prompt_tokens = (count_tokens(system) + count_tokens(question)
                         + 2 * _MSG_OVERHEAD + _REPLY_PRIMING)
        # The placeholder text says nothing about a real answer's length.
        return body, prompt_tokens, config.MOCK_OUTPUT_TOKENS


class SupportAgent:
    def __init__(self, model: str | None = None, retriever_mode: str | None = None,
                 top_k: int | None = None, mock: bool = False):
        self.model = model or config.FRONTIER_MODEL
        self.top_k = top_k or config.TOP_K
        self.docs: list[Doc] = load_docs(config.KB_PATH)
        self.retriever = build_retriever(self.docs, retriever_mode or config.RETRIEVER)
        self.orders = _load_orders(config.ORDERS_PATH)
        self.system_prompt = config.SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()
        self.mock = mock
        self._client = None

    # -- context assembly -------------------------------------------------
    def _orders_in(self, question: str) -> list[dict]:
        ids = {m.group(1) for m in ORDER_ID.finditer(question)}
        return [self.orders[i] for i in sorted(ids) if i in self.orders]

    def build_context(self, question: str) -> tuple[str, list[str], list[str], float]:
        t0 = time.perf_counter()
        hits = self.retriever.search(question, self.top_k)
        orders = self._orders_in(question)
        retrieval_ms = (time.perf_counter() - t0) * 1000

        parts = ["REFERENCE DOCUMENTS", ""]
        for doc, _ in hits:
            parts.append(f"[{doc.id}] {doc.title}\n{doc.text}\n")
        if not hits:
            # Say it explicitly. An empty heading leaves the model to infer that
            # nothing matched, and some models fill the silence from memory.
            parts.append("No reference documents matched this question.\n")
        if orders:
            parts.append("CUSTOMER ORDER RECORDS")
            parts.append("")
            for o in orders:
                parts.append(json.dumps(o, ensure_ascii=False, indent=2))
                parts.append("")
        return ("\n".join(parts),
                [d.id for d, _ in hits],
                [o["order_id"] for o in orders],
                retrieval_ms)

    # -- model call -------------------------------------------------------
    @property
    def client(self):
        if self._client is None:
            from openai import OpenAI  # noqa: PLC0415
            if not config.API_KEY:
                raise RuntimeError(
                    "OPENAI_API_KEY is not set. Copy .env.example to .env and fill it in."
                )
            self._client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)
        return self._client

    def ask(self, question: str) -> Answer:
        context, retrieved, orders_used, retrieval_ms = self.build_context(question)
        result = Answer(question=question, answer="", model=self.model,
                        retriever=self.retriever.name,
                        retrieved=retrieved, orders_used=orders_used,
                        retrieval_ms=round(retrieval_ms, 2))
        t0 = time.perf_counter()
        if self.mock:
            answer, pt, ct = MockCompletion(self).respond(question, context, retrieved)
            result.answer = answer
            result.prompt_tokens, result.completion_tokens = pt, ct
            result.cost_usd = round(config.price(self.model, pt, ct), 6)
            result.cost_is_estimate = True
            result.latency_ms = round((time.perf_counter() - t0) * 1000, 1)
            return result
        try:
            resp, result.temperature_used = chat_completion(
                self.client, self.model,
                [{"role": "system", "content": f"{self.system_prompt}\n\n{context}"},
                 {"role": "user", "content": question}],
                max_tokens=config.MAX_TOKENS, temperature=config.TEMPERATURE,
            )
            result.answer = (resp.choices[0].message.content or "").strip()
            result.finish_reason = resp.choices[0].finish_reason
            u = resp.usage
            if u:
                # Provider-reported counts: these are what is billed. For
                # reasoning models completion_tokens includes hidden reasoning
                # tokens, which is why it can far exceed the visible answer.
                details = getattr(u, "prompt_tokens_details", None)
                cached = getattr(details, "cached_tokens", 0) or 0
                out_details = getattr(u, "completion_tokens_details", None)
                result.reasoning_tokens = getattr(out_details, "reasoning_tokens", 0) or 0
                result.prompt_tokens = u.prompt_tokens
                result.cached_prompt_tokens = cached
                result.completion_tokens = u.completion_tokens
                result.cost_usd = round(config.price(
                    self.model, u.prompt_tokens, u.completion_tokens, cached), 6)
        except Exception as exc:                       # noqa: BLE001
            result.error = f"{type(exc).__name__}: {exc}"
        result.latency_ms = round((time.perf_counter() - t0) * 1000, 1)
        return result
