"""TechStore support agent (Phase 0).

Deliberately has NO router, cache, classifier or circuit breaker. It answers a
question by retrieving relevant knowledge-base documents and calling one model.

This is (a) the application the router will sit underneath, and (b) the
always-frontier baseline arm of the Week 10 benchmark. `benchmarks/run_baseline.py`
is this class in a loop.

Week 4: set OPENAI_BASE_URL to the router and change nothing else.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import config
import techniques
import tracing
from retriever import Doc, build_retriever, load_docs

ORDER_ID = re.compile(r"\b(?:order\s*#?\s*)?(\d{5})\b", re.I)


def _alias_pattern(alias: str) -> re.Pattern:
    words = [re.escape(w) for w in alias.lower().split()]
    return re.compile(r"\b" + r"\s*".join(words) + r"\b")


# A question gets the product catalogue when it names a product CATEGORY and asks
# to compare, choose or buy. Questions naming a category alone ("my headphones
# will not pair") are about one item the customer already owns and do not.
_CATEGORY = re.compile(r"\b(headphones?|earbuds?|buds|laptops?|notebooks?|tablets?|smart\s?watch(es)?|"
                       r"watch(es)?|monitors?|chargers?|power\s?banks?|products?)\b", re.I)
_INTENT = re.compile(r"\b(which|compare|comparison|vs\.?|versus|best|recommend|suggest|cheapest|cheaper|"
                     r"lightest|lighter|heaviest|longest|difference|options|choose|should i (buy|get)|"
                     r"do you (sell|have|offer)|budget|lakh)\b|\bunder\s+(₹|rs\.?\s*)?\d", re.I)


def wants_catalogue(question: str) -> bool:
    return bool(_CATEGORY.search(question) and _INTENT.search(question))


QUESTION_MARK = "CUSTOMER QUESTION:"
# Spending limits: what the customer sees instead of an answer (no model call, nothing spent).
LIMIT_REACHED = ("Sorry, this assistant has reached its usage limit for today. Please try again "
                 "tomorrow, or contact TechStore support by chat or email (9 AM to 9 PM IST).")
LIMIT_SLOW_DOWN = "You're sending messages very quickly. Please wait a moment and try again."


def _question_of(user_message: str) -> str:
    """The customer's words from a user message (layout "cache" puts documents before them)."""
    i = user_message.rfind(QUESTION_MARK)
    return user_message[i + len(QUESTION_MARK):].strip() if i >= 0 else user_message


def _pretty_date(iso: str) -> str:
    y, m, d = (int(x) for x in iso.split("-"))
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    return f"{d} {months[m - 1]} {y}"

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
                    temperature: float | None, reasoning_effort: str | None = None, **extra):
    """Returns (response, temperature actually sent or None). `extra` passes provider
    parameters such as verbosity through unchanged; unsupported ones fail loudly."""
    q = _QUIRKS.setdefault(model, {"temperature": True, "limit": "max_completion_tokens"})
    for _ in range(4):
        kwargs = {"model": model, "messages": messages, q["limit"]: max_tokens}
        if q["temperature"] and temperature is not None:
            kwargs["temperature"] = temperature
        if reasoning_effort:
            # Never dropped silently: an unsupported value fails loudly.
            kwargs["reasoning_effort"] = reasoning_effort
        kwargs.update({k: v for k, v in extra.items() if v is not None})
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
    cache_write_tokens: int = 0       # prompt tokens written into the provider's cache (1.25x)
    completion_tokens: int = 0
    reasoning_tokens: int = 0         # hidden, billed as output; 0 for non-reasoning models
    finish_reason: str | None = None  # "length" means the answer was cut off at MAX_TOKENS
    temperature_used: float | None = None  # None: the model rejected temperature (not reproducible at T=0)
    reasoning_effort: str | None = None    # None: the model's default
    answer_length: str = "default"          # "concise" adds the answer-length rule (techniques.py)
    verbosity: str | None = None           # provider length setting, if sent
    system_prompt: str = ""                # file name, so runs with different prompts stay comparable
    system_prompt_sha: str = ""            # first 8 hex of its sha256: the file name alone is ambiguous
                                           # (system_prompt.txt was the 436-token version until 2026-11-17)
    cost_usd: float = 0.0
    # True in mock mode: tokens are counted locally and output length is
    # assumed. Never mix estimated rows into benchmark results.
    cost_is_estimate: bool = False
    latency_ms: float = 0.0
    retrieval_ms: float = 0.0
    error: str | None = None
    trace_id: str | None = None       # Langfuse trace, when tracing is on
    served_by: str = "model"          # "faq" / "cache": answered without a model call
    faq_id: str | None = None
    faq_score: float | None = None
    cache_kind: str | None = None     # "exact" or "semantic" when served_by == "cache"
    cache_score: float | None = None
    cached_question: str | None = None
    cache_note: str | None = None     # why the cache missed, skipped, or did not store
    turn: int = 1                     # position in the conversation (1 = first question)
    memory_mode: str = "off"          # conversation-memory technique applied (techniques.py)
    memory_dropped_turns: int = 0     # earlier turns shrunk into a note/summary or dropped
    memory_cost_usd: float = 0.0      # cost of writing the summary (summary mode); in cost_usd too
    client_id: str | None = None      # whose budget this counts against (None: app cap only)
    limit_action: str | None = None   # spending limits: allow / downgrade / refuse
    limit_reason: str | None = None
    prompt_layout: str = "classic"
    sent_user_message: str = ""       # the final user message as sent; with layout "cache", put
                                      # THIS in the history so the next prompt reuses the prefix

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

    def respond(self, question: str, context: str, retrieved: list[str],
                messages: list[dict] | None = None) -> tuple[str, int, int]:
        titles = [d.title for d in self.agent.docs if d.id in retrieved]
        body = (
            "[MOCK RESPONSE - no model was called]\n\n"
            f"A real answer to {question!r} would be composed from:\n"
            + "\n".join(f"  - {t}" for t in titles)
        )
        # Pad to the assumed answer length, so conversation history grows like a real one.
        filler = " (placeholder standing in for a real answer)"
        while count_tokens(body) < config.MOCK_OUTPUT_TOKENS:
            body += filler
        # Count what the API would actually receive: the messages plus overhead.
        if messages is None:
            messages = [{"role": "system", "content": self.agent.system_message(context)},
                        {"role": "user", "content": question}]
        prompt_tokens = (sum(count_tokens(m["content"]) for m in messages)
                         + len(messages) * _MSG_OVERHEAD + _REPLY_PRIMING)
        # The placeholder text says nothing about a real answer's length.
        return body, prompt_tokens, config.MOCK_OUTPUT_TOKENS


class SupportAgent:
    def __init__(self, model: str | None = None, retriever_mode: str | None = None,
                 top_k: int | None = None, mock: bool = False,
                 reasoning_effort: str | None = None, system_prompt: str | None = None,
                 answer_length: str | None = None, verbosity: str | None = None,
                 faq: bool | None = None, faq_drafts: bool = False, cache: bool | None = None,
                 memory: str | None = None, keep_turns: int | None = None,
                 layout: str | None = None, context_margin: float | None = None,
                 passage_margin: float | None = None, limits: bool | None = None):
        self.model = model or config.FRONTIER_MODEL
        self.reasoning_effort = reasoning_effort or config.REASONING_EFFORT
        self.answer_length = answer_length or config.ANSWER_LENGTH
        self.memory_mode = memory or config.MEMORY_MODE
        self.keep_turns = config.MEMORY_KEEP_TURNS if keep_turns is None else keep_turns
        self._summary_cache: dict = {}
        self.context_margin = config.CONTEXT_MARGIN if context_margin is None else context_margin
        self.passage_margin = config.PASSAGE_MARGIN if passage_margin is None else passage_margin
        self._sentences: dict[str, tuple[list[str], object]] = {}
        # Spending limits. Mock runs use a throwaway in-memory ledger: estimated costs must
        # never count against the real budget.
        self.limits = None
        if config.SPEND_LIMITS if limits is None else limits:
            import spending_limits  # noqa: PLC0415
            self.limits = spending_limits.SpendingLimits(
                ":memory:" if mock else spending_limits.SPEND_PATH)
        self.prompt_layout = layout or config.PROMPT_LAYOUT
        if self.prompt_layout not in ("classic", "cache"):
            raise ValueError("layout must be 'classic' or 'cache'")
        if self.prompt_layout == "cache" and self.memory_mode != "off":
            # Trimming rewrites earlier turns, which changes the prompt's beginning and
            # stops the provider reusing its cache. Combining the two is a later step.
            raise ValueError("layout 'cache' needs memory 'off' (trimming resets cache reuse)")
        self.verbosity = verbosity or config.VERBOSITY
        self.top_k = top_k or config.TOP_K
        self.docs: list[Doc] = load_docs(config.KB_PATH)
        self.retriever = build_retriever(self.docs, retriever_mode or config.RETRIEVER)
        self.orders = _load_orders(config.ORDERS_PATH)
        # Product pages are always included when a question names the product.
        # Retrieval alone missed the PulseBook 14 page in "Is the Pro 16 worth
        # twice the PulseBook 14?", because the Pro 16 page outscored it.
        self._product_patterns = [(d, [_alias_pattern(a) for a in d.meta.get("aliases", [])])
                                  for d in self.docs if d.meta.get("aliases")]
        prompt_path = config.BASE_DIR / system_prompt if system_prompt else config.SYSTEM_PROMPT_PATH
        self.system_prompt_name = prompt_path.name
        self.system_prompt = prompt_path.read_text(encoding="utf-8").strip()
        self.system_prompt_sha = hashlib.sha256(self.system_prompt.encode()).hexdigest()[:8]
        self.mock = mock
        self._client = None
        # FAQ shortcut: off if disabled or if the embedding library is missing (e.g. in CI).
        # faq_drafts serves unapproved answers too: for measuring only, never for customers.
        self.faq = None
        if (config.FAQ_SHORTCUT if faq is None else faq):
            try:
                from faq_shortcut import FaqShortcut, load_faq  # noqa: PLC0415
                self.faq = FaqShortcut(
                    load_faq(), threshold=config.FAQ_THRESHOLD, include_drafts=faq_drafts,
                    block=lambda q: "names a product" if self.named_products(q) else None)
            except ImportError:
                self.faq = None
        # Safe response cache. Mock runs use a throwaway in-memory cache so fake answers
        # are never saved where a real run could reuse them.
        self.cache = None
        if (config.RESPONSE_CACHE if cache is None else cache):
            try:
                from response_cache import ResponseCache, namespace_key  # noqa: PLC0415
                self.cache = ResponseCache(":memory:" if mock else config.BASE_DIR / ".cache" /
                                           "responses.sqlite", threshold=config.CACHE_THRESHOLD,
                                           ttl_hours=config.CACHE_TTL_HOURS)
                kb_version = hashlib.sha256(config.KB_PATH.read_bytes()).hexdigest()[:12]
                # Everything except the question that changes the right answer.
                self.cache_namespace = namespace_key(
                    app="techstore", prompt=self.system_prompt_sha, kb=kb_version,
                    model=self.model, effort=self.reasoning_effort, length=self.answer_length,
                    verbosity=self.verbosity, top_k=self.top_k, retriever=self.retriever.name)
            except ImportError:
                self.cache = None

    # -- context assembly -------------------------------------------------
    def _orders_in(self, question: str) -> list[dict]:
        ids = {m.group(1) for m in ORDER_ID.finditer(question)}
        return [self.orders[i] for i in sorted(ids) if i in self.orders]

    def named_products(self, question: str) -> list[Doc]:
        q = question.lower()
        return [d for d, pats in self._product_patterns if any(p.search(q) for p in pats)]

    def system_message(self, context: str = "") -> str:
        base = f"{self.system_prompt}\n\nToday's date: {_pretty_date(config.SIMULATED_TODAY)}."
        return f"{base}\n\n{context}" if context else base

    def build_context(self, question: str, history: list[dict] | None = None
                      ) -> tuple[str, list[str], list[str], float]:
        t0 = time.perf_counter()
        # A follow-up ("what about the Y500?") means little alone: search with the previous
        # question too. Order numbers stay available for the whole conversation.
        asked = [_question_of(m["content"]) for m in (history or []) if m["role"] == "user"]
        search_text = f"{asked[-1]} {question}" if asked else question
        named = self.named_products(search_text)[: self.top_k]
        named_ids = {d.id for d in named}
        searched = [(d, s) for d, s in self.retriever.search(search_text, self.top_k + len(named))
                    if d.id not in named_ids]
        if self.context_margin is not None and searched:
            # Adaptive context: keep documents scoring close to the best match; a clear winner
            # travels alone. Named products (above) are always kept.
            best = searched[0][1]
            close = [(d, s) for d, s in searched if s >= best - self.context_margin]
            searched = close or searched[:1]
        hits = [(d, None) for d in named] + searched[: self.top_k - len(named)]
        # The catalogue is extra: it never takes one of the top_k slots.
        catalogue = next((d for d in self.docs if d.id == "catalogue_summary"), None)
        if catalogue and wants_catalogue(search_text):
            hits.append((catalogue, None))
        orders = self._orders_in(" ".join([*asked, question]))
        retrieval_ms = (time.perf_counter() - t0) * 1000

        parts = ["REFERENCE DOCUMENTS", ""]
        for doc, _ in hits:
            text = doc.text if self.passage_margin is None else self.passage(doc, search_text)
            parts.append(f"[{doc.id}] {doc.title}\n{text}\n")
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

    def ask(self, question: str, session_id: str | None = None,
            history: list[dict] | None = None, client_id: str | None = None) -> Answer:
        """Answer one question. `history` is the conversation so far, as OpenAI-style
        {"role": "user"|"assistant", "content": ...} messages. With Langfuse configured,
        also records a trace; `session_id` groups traces (one batch run, one chat)."""
        with tracing.question_trace(question, model=self.model, retriever=self.retriever.name,
                                    top_k=self.top_k, mock=self.mock,
                                    reasoning_effort=self.reasoning_effort,
                                    system_prompt=self.system_prompt_name,
                                    answer_length=self.answer_length,
                                    session_id=session_id) as root:
            result = self._answer(question, history or [], client_id)
            result.trace_id = root.trace_id
            root.update(
                output=result.answer if not result.error else None,
                level="ERROR" if result.error else "DEFAULT",
                status_message=result.error,
                metadata={"cost_usd": result.cost_usd, "cost_is_estimate": result.cost_is_estimate,
                          "retrieved": result.retrieved, "orders_used": result.orders_used,
                          "finish_reason": result.finish_reason},
            )
        return result

    SUMMARY_PROMPT = (
        "Summarise this part of a customer-support chat in at most 3 short sentences, for the "
        "agent who continues it. Keep every order number, amount, date, product name and "
        "decision exactly as written; never add anything that was not said.")

    def _summarise(self, previous: str | None, messages: list[dict], spent: list[float]) -> str:
        """Memory mode "summary": the cheap model condenses older turns (rolling: it extends
        the previous summary instead of re-reading everything). Its cost is added to `spent`."""
        convo = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        if previous:
            convo = f"Summary so far: {previous}\n{convo}"
        if self.mock:
            asked = [m["content"] for m in messages if m["role"] == "user"]
            return "[mock summary] The customer asked: " + " | ".join(asked)
        model = config.ECONOMY_MODEL
        resp, _ = chat_completion(self.client, model,
                                  [{"role": "system", "content": self.SUMMARY_PROMPT},
                                   {"role": "user", "content": convo}],
                                  max_tokens=400, temperature=None, reasoning_effort="none")
        u = resp.usage
        if u:
            spent[0] += config.price(model, u.prompt_tokens, u.completion_tokens)
        return (resp.choices[0].message.content or "").strip()

    def _encode(self, texts: list[str]):
        model = getattr(self.retriever, "model", None)
        if model is None:                       # keyword retriever: load MiniLM once
            from sentence_transformers import SentenceTransformer  # noqa: PLC0415
            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
            self.retriever.model = model
        return model.encode(texts, normalize_embeddings=True)

    def passage(self, doc: Doc, question: str) -> str:
        """Technique 4: the parts of `doc` relevant to `question`. Sentences (catalogue:
        product lines) within passage_margin of the best one are kept, in order; the first
        always stays because it says what the document is about."""
        if doc.id not in self._sentences:
            if doc.id == "catalogue_summary":
                parts = [line for line in doc.text.split("\n") if line.strip()]
            else:
                parts = [p for p in re.split(r"(?<=[.!?])\s+", doc.text.strip()) if p]
            self._sentences[doc.id] = (parts, self._encode(parts))
        parts, vecs = self._sentences[doc.id]
        if len(parts) <= 2:
            return doc.text
        sims = vecs @ self._encode([question])[0]
        floor = float(sims.max()) - self.passage_margin
        keep = [p for i, (p, s) in enumerate(zip(parts, sims, strict=True)) if i == 0 or s >= floor]
        joiner = "\n" if doc.id == "catalogue_summary" else " "
        return joiner.join(keep)

    def _product_entities(self, question: str) -> frozenset:
        return frozenset(d.id for d in self.named_products(question))

    def _answer(self, question: str, history: list[dict], client_id: str | None = None) -> Answer:
        result = self._answer_uncached(question, history, client_id)
        if history:
            # A follow-up depends on what came before ("and how long would that take?"), so it
            # is never stored or served on its own. FAQ and cache apply to first questions only.
            return result
        if self.cache is not None and result.served_by == "model":
            ok = not result.error and result.finish_reason != "length" and not result.cost_is_estimate
            if ok or self.mock:
                stored = self.cache.store(
                    question, result.answer, self.cache_namespace, self.model,
                    self._product_entities(question), private=bool(result.orders_used))
            else:
                stored = "not stored: error or cut-off answer"
            result.cache_note = "; ".join(filter(None, [result.cache_note, stored]))
        return result

    def _answer_uncached(self, question: str, history: list[dict] | None = None,
                         client_id: str | None = None) -> Answer:
        history = history or []
        if self.faq is not None and self.faq.entries and not history:
            with tracing.observation("faq-shortcut", as_type="span", input=question) as step:
                t0 = time.perf_counter()
                match = self.faq.lookup(question)
                lookup_ms = round((time.perf_counter() - t0) * 1000, 1)
                step.update(output=match.entry["answer"] if match.entry else None,
                            metadata={"served": bool(match.entry), "faq_id": match.best_id,
                                      "score": round(match.score, 3), "reason": match.reason})
            if match.entry:
                # No model call: zero tokens, zero cost.
                return Answer(question=question, answer=match.entry["answer"], model=self.model,
                              retriever="faq", retrieved=list(match.entry["sources"]),
                              served_by="faq", faq_id=match.entry["id"],
                              faq_score=round(match.score, 3), latency_ms=lookup_ms,
                              system_prompt=self.system_prompt_name,
                              system_prompt_sha=self.system_prompt_sha)
        cache_note = None
        if self.cache is not None and not history:
            with tracing.observation("response-cache", as_type="span", input=question) as step:
                t0 = time.perf_counter()
                look = self.cache.lookup(question, self.cache_namespace,
                                         self._product_entities(question))
                lookup_ms = round((time.perf_counter() - t0) * 1000, 1)
                hit = look.hit
                step.update(output=hit.answer if hit else None,
                            metadata={"result": look.reason, "kind": hit.kind if hit else None,
                                      "score": round(hit.score, 3) if hit else None,
                                      "cached_question": hit.cached_question if hit else None})
            if hit:
                # No model call: zero tokens, zero cost.
                return Answer(question=question, answer=hit.answer, model=hit.model,
                              retriever="cache", served_by="cache", cache_kind=hit.kind,
                              cache_score=round(hit.score, 3), cached_question=hit.cached_question,
                              cache_note=look.reason, latency_ms=lookup_ms,
                              system_prompt=self.system_prompt_name,
                              system_prompt_sha=self.system_prompt_sha)
            cache_note = look.reason
        with tracing.observation("retrieve", as_type="retriever", input=question) as step:
            context, retrieved, orders_used, retrieval_ms = self.build_context(question, history)
            step.update(output={"documents": retrieved, "orders": orders_used},
                        metadata={"retrieval_ms": round(retrieval_ms, 2), "top_k": self.top_k})
        result = Answer(question=question, answer="", model=self.model,
                        reasoning_effort=self.reasoning_effort,
                        answer_length=self.answer_length, verbosity=self.verbosity,
                        system_prompt=self.system_prompt_name,
                        system_prompt_sha=self.system_prompt_sha,
                        retriever=self.retriever.name,
                        retrieved=retrieved, orders_used=orders_used,
                        retrieval_ms=round(retrieval_ms, 2))
        result.cache_note = cache_note
        # The request passes through the token-saving techniques exactly as the gateway
        # will apply them to any app's request (techniques.py).
        if self.prompt_layout == "cache":
            # Fixed instructions first; this turn's documents travel with the question at the end.
            user = f"{context}\n{QUESTION_MARK} {question}"
            request = {"model": self.model,
                       "messages": [{"role": "system", "content": self.system_message()},
                                    *history, {"role": "user", "content": user}]}
        else:
            user = question
            request = {"model": self.model,
                       "messages": [{"role": "system", "content": self.system_message(context)},
                                    *history, {"role": "user", "content": question}]}
        result.prompt_layout, result.sent_user_message = self.prompt_layout, user
        result.turn = sum(1 for m in history if m["role"] == "user") + 1
        summary_cost = [0.0]
        request, memory = techniques.apply_memory(
            request, self.memory_mode, self.keep_turns,
            summarise=lambda prev, msgs: self._summarise(prev, msgs, summary_cost),
            summary_cache=self._summary_cache)
        result.memory_mode = self.memory_mode
        result.memory_dropped_turns = memory["dropped_turns"]
        request = techniques.apply_length(request, self.answer_length, self.verbosity)
        request = techniques.apply_reasoning(request, self.reasoning_effort)
        messages = request["messages"]
        result.client_id = client_id
        if self.limits is not None:
            import spending_limits  # noqa: PLC0415
            def estimate(m):
                return spending_limits.estimate_cost(m, messages)
            with tracing.observation("spending-limit", as_type="guardrail", input=client_id) as step:
                decision = self.limits.check(client_id, request["model"], estimate)
                step.update(output=decision.action,
                            metadata={"reason": decision.reason,
                                      "estimate_usd": round(estimate(request["model"]), 6),
                                      "spent_today": round(decision.client_spent, 6)})
            result.limit_action, result.limit_reason = decision.action, decision.reason
            if decision.action == "refuse":
                # No model call: nothing spent.
                result.answer = (LIMIT_SLOW_DOWN if "per minute" in decision.reason
                                 else LIMIT_REACHED)
                result.served_by = "limit"
                return result
            if decision.action == "downgrade":
                request["model"] = result.model = decision.model
        model = request["model"]
        self.last_request = request        # exactly what is sent (used by prompt_cache_sim.py)
        with tracing.observation("llm", as_type="generation", model=model, input=messages,
                                 model_parameters={"max_tokens": config.MAX_TOKENS,
                                                   "reasoning_effort": self.reasoning_effort or "default",
                                                   "answer_length": self.answer_length,
                                                   "verbosity": self.verbosity or "default",
                                                   "system_prompt": self.system_prompt_name}) as gen:
            t0 = time.perf_counter()
            if self.mock:
                answer, pt, ct = MockCompletion(self).respond(question, context, retrieved, messages)
                result.answer = answer
                result.prompt_tokens, result.completion_tokens = pt, ct
                result.cost_usd = round(config.price(model, pt, ct), 6)
                result.cost_is_estimate = True
            else:
                self._call_model(request, result)
            result.latency_ms = round((time.perf_counter() - t0) * 1000, 1)
            # The summary call (memory mode "summary") is part of what this answer cost.
            result.memory_cost_usd = round(summary_cost[0], 6)
            result.cost_usd = round(result.cost_usd + summary_cost[0], 6)
            if self.limits is not None:
                self.limits.record(client_id, result.cost_usd)      # the actual cost
            usage, cost = tracing.usage_and_cost(
                model, result.prompt_tokens, result.completion_tokens,
                result.cached_prompt_tokens, result.reasoning_tokens, result.cache_write_tokens)
            gen.update(output=result.answer if not result.error else None,
                       usage_details=usage, cost_details=cost or None,
                       level="ERROR" if result.error else "DEFAULT",
                       status_message=result.error,
                       metadata={"finish_reason": result.finish_reason,
                                 "temperature_used": result.temperature_used})
        return result

    def _call_model(self, request: dict, result: Answer) -> None:
        try:
            resp, result.temperature_used = chat_completion(
                self.client, request["model"], request["messages"],
                max_tokens=config.MAX_TOKENS, temperature=config.TEMPERATURE,
                reasoning_effort=request.get("reasoning_effort"),
                verbosity=request.get("verbosity"),
            )
            result.answer = (resp.choices[0].message.content or "").strip()
            result.finish_reason = resp.choices[0].finish_reason
            u = resp.usage
            if u:
                # Provider-reported counts: these are what is billed. For
                # reasoning models completion_tokens includes hidden reasoning
                # tokens, which is why it can far exceed the visible answer.
                # Chat Completions says prompt_tokens_details, the Responses API
                # input_tokens_details; read whichever is present.
                details = (getattr(u, "prompt_tokens_details", None)
                           or getattr(u, "input_tokens_details", None))
                cached = getattr(details, "cached_tokens", 0) or 0
                written = getattr(details, "cache_write_tokens", 0) or 0
                result.cache_write_tokens = written
                out_details = getattr(u, "completion_tokens_details", None)
                result.reasoning_tokens = getattr(out_details, "reasoning_tokens", 0) or 0
                result.prompt_tokens = u.prompt_tokens
                result.cached_prompt_tokens = cached
                result.completion_tokens = u.completion_tokens
                result.cost_usd = round(config.price(
                    request["model"], u.prompt_tokens, u.completion_tokens, cached, written), 6)
        except Exception as exc:                       # noqa: BLE001
            result.error = f"{type(exc).__name__}: {exc}"
