"""Phase 0 tests. None of these call an API, so they are free and run in CI."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Tests must never send traces, even on a machine whose .env has Langfuse keys.
os.environ["LANGFUSE_TRACING"] = "off"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import config  # noqa: E402
from agent import SupportAgent  # noqa: E402
from retriever import build_retriever, load_docs  # noqa: E402

RECALL_CASES = [
    ("How long do I have to return something?", "pol_return_window"),
    ("Can I return headphones I already opened?", "pol_return_exclusions"),
    ("Where is my order?", "ship_tracking"),
    ("When will I get my money back?", "pol_refund_timeline"),
    ("I was charged three times", "bill_duplicate_charge"),
    ("My headphones will not pair", "tsg_headphone_pairing"),
    ("webhook 403 HMAC signature", "api_webhook_signature"),
    ("I dropped my laptop", "svc_accidental_damage"),
    ("laptop faulty after 35 days what are my rights", "pol_warranty_terms"),
    ("only one earbud is working", "tsg_earbuds_one_side"),
    ("my laptop is overheating", "tsg_laptop_overheating"),
    ("my monitor keeps flickering", "tsg_monitor_flicker"),
    ("how do I paginate the orders endpoint", "api_pagination"),
    ("my webhook endpoint was disabled", "api_webhook_retries"),
    ("403 insufficient_scope error", "api_scopes"),
    ("refund to a card I closed", "bill_refund_to_closed_card"),
    ("I paid cash on delivery how do I get refunded", "bill_cod_refund"),
    ("can I use two coupons together", "bill_promo_codes"),
    ("the price dropped after I bought it", "bill_price_drop"),
    ("does the replacement get a new warranty", "pol_replacement_warranty"),
    ("I want to buy 20 units for my company", "pol_bulk_orders"),
    ("can I inspect the package before accepting", "ship_open_box"),
    ("how do I turn on two factor authentication", "acc_two_factor"),
    ("my power bank will not charge my laptop", "tsg_powerbank_not_charging"),
]


def test_kb_wellformed():
    docs = load_docs(config.KB_PATH)
    assert len(docs) >= 80
    ids = [d.id for d in docs]
    assert len(ids) == len(set(ids)), "duplicate document id"
    for d in docs:
        assert d.title and d.text and d.tags
        assert len(d.text.split()) >= 25, f"{d.id} is too thin to be useful"


def test_orders_wellformed():
    rows = [json.loads(line) for line in open(config.ORDERS_PATH, encoding="utf-8") if line.strip()]
    assert len(rows) >= 40
    assert len({r["order_id"] for r in rows}) == len(rows)
    for r in rows:
        assert r["total"] == sum(i["qty"] * i["unit_price"] for i in r["items"])


def test_order_prices_match_catalogue():
    """An order quoting a price the product document does not state would make
    every billing-dispute answer unverifiable."""
    catalogue = {d.id: d.price for d in load_docs(config.KB_PATH) if d.price}
    rows = [json.loads(line) for line in open(config.ORDERS_PATH, encoding="utf-8") if line.strip()]
    for r in rows:
        for item in r["items"]:
            assert catalogue.get(item["sku"]) == item["unit_price"], (
                f"{r['order_id']}: {item['sku']} priced {item['unit_price']}, "
                f"catalogue says {catalogue.get(item['sku'])}"
            )


def test_orders_respect_stated_business_rules():
    """Fixtures must not contradict the knowledge base, or the agent is being
    graded against an inconsistent world."""
    rows = [json.loads(line) for line in open(config.ORDERS_PATH, encoding="utf-8") if line.strip()]
    for r in rows:
        if r["payment_method"] == "Cash on Delivery":
            assert r["total"] <= 20000, f"{r['order_id']}: COD above the stated cap"
        if r["payment_method"].startswith("No-Cost EMI"):
            assert r["total"] >= 5000, f"{r['order_id']}: EMI below the stated floor"
        if r["status"] in ("Delivered", "Shipped", "Returned"):
            assert r.get("tracking_id"), f"{r['order_id']}: {r['status']} without tracking"


def test_retrieval_recall_keyword():
    r = build_retriever(load_docs(config.KB_PATH), "keyword")
    misses = [q for q, want in RECALL_CASES
              if want not in [d.id for d, _ in r.search(q, 3)]]
    assert not misses, f"top-3 recall failures: {misses}"


def test_order_id_extraction():
    a = SupportAgent(retriever_mode="keyword")
    _, _, orders, _ = a.build_context("Where is my order #48213?")
    assert orders == ["48213"]
    _, _, orders, _ = a.build_context("Compare order 48213 and order 48217")
    assert orders == ["48213", "48217"]
    _, _, orders, _ = a.build_context("Do you ship to 560034?")
    assert orders == [], "a pin code must not be read as an order id"


def test_prompt_stays_within_budget():
    """Section 2's cost model assumes a ~400-token prompt. Sending the whole KB
    would be ~7,700 tokens and 7x the cost, so this guards the economics."""
    a = SupportAgent(retriever_mode="keyword")
    for q, _ in RECALL_CASES:
        ctx, _, _, _ = a.build_context(q)
        approx = (len(a.system_prompt.split()) + len(ctx.split())) * 4 // 3
        assert approx < 900, f"prompt too large ({approx} tok) for: {q}"


def test_mock_cost_is_flagged_as_estimate():
    """A mock row must never be mistaken for a measured cost."""
    r = SupportAgent(retriever_mode="keyword", mock=True).ask("Can I return opened headphones?")
    assert r.cost_is_estimate
    assert r.completion_tokens == config.MOCK_OUTPUT_TOKENS


def test_cached_tokens_are_discounted():
    p = config.PRICING["gpt-6.1-sol"]
    full = config.price("gpt-6.1-sol", 1000, 0)
    half_cached = config.price("gpt-6.1-sol", 1000, 0, cached_prompt_tokens=500)
    assert abs(full - 1000 * p["input"] / 1e6) < 1e-12
    assert abs(half_cached - (500 * p["input"] + 500 * p["cached_input"]) / 1e6) < 1e-12
    # cached count can never exceed the prompt it belongs to
    assert config.price("gpt-6.1-sol", 100, 0, cached_prompt_tokens=10_000) == config.price(
        "gpt-6.1-sol", 100, 0, cached_prompt_tokens=100)


def test_near_identical_order_queries_differ():
    """48213 and 48217 are different products. The router's semantic cache must
    never serve one for the other -- this fixture is the Week 2 safety test."""
    a = SupportAgent(retriever_mode="keyword")
    c1, _, _, _ = a.build_context("Where is my order #48213?")
    c2, _, _, _ = a.build_context("Where is my order #48217?")
    assert "SoundWave X200" in c1 and "NovaTab 11" in c2
    assert c1 != c2


def test_model_id_suggestions():
    """check_setup.py must point at the right id when the configured one is a
    near-miss, and must not invent a match when nothing is close."""
    from check_setup import match_models
    available = ["gpt-5.6-sol-2026-08-01", "gpt-5.6-luna", "gpt-4.1-mini", "whisper-1"]
    missing = match_models(available, ["gpt-5.6-sol", "gpt-5.6-luna", "claude-opus-5"])
    assert "gpt-5.6-luna" not in missing                 # exact match is not missing
    assert missing["gpt-5.6-sol"][0] == "gpt-5.6-sol-2026-08-01"
    assert missing["claude-opus-5"] == []                # nothing similar -> no suggestion


def test_review_flags_invented_rupee_amounts():
    from review_results import known_amounts
    amounts = known_amounts()
    assert 12999 in amounts and 134999 in amounts        # catalogue prices
    assert 49 in amounts                                  # COD fee quoted in the KB text
    assert 9999 not in amounts


def test_system_prompt_carries_the_exact_refusals():
    """review_results.py detects these sentences; if the prompt drifts from
    config, every refusal is silently misgraded."""
    prompt = config.SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    assert config.REFUSAL_UNKNOWN in prompt
    assert config.REFUSAL_OFF_TOPIC in prompt
    assert config.REFUSAL_PARTIAL in prompt


def test_no_match_is_stated_explicitly():
    ctx, docs, _, _ = SupportAgent(retriever_mode="keyword").build_context(
        "What is the capital of France?")
    assert docs == []
    assert "No reference documents matched this question." in ctx


def test_about_document_answers_catalogue_questions():
    a = SupportAgent(retriever_mode="keyword")
    for q in ["Do you sell washing machines?", "What time does your Bangalore store open?"]:
        assert "about_techstore" in [d.id for d, _ in a.retriever.search(q, 3)], q


def test_refusal_behaviour_grading():
    from review_results import behavior_problem as bp
    off, unk = config.REFUSAL_OFF_TOPIC, config.REFUSAL_UNKNOWN
    curly = unk.replace("'", "’")                     # models often emit curly quotes
    assert bp("decline_off_topic", off) is None
    assert "ANSWERED" in bp("decline_off_topic", "The capital of France is Paris.")
    assert "wording" in bp("decline_off_topic", unk)
    assert bp("admit_unknown", curly + " Anything else?") is None
    assert "invented" in bp("admit_unknown", "Yes, students get 10% off.")
    assert bp("answer_from_about", "TechStore does not sell washing machines.") is None
    assert "About" in bp("answer_from_about", unk)
    assert bp("partial", "The X200 lasts 40 hours. " + unk) is None
    assert "unanswerable half" in bp("partial", "The X200 lasts 40 hours.")
    assert bp(None, "The return window is 30 days.") is None
    assert "REFUSED" in bp(None, unk)
    hedge = "Your order shipped with BlueDart. " + unk
    assert bp(None, hedge, missing_gold=True) is None        # retrieval's fault, not the model's
    assert "unnecessary hedge" in bp(None, hedge, missing_gold=False)
    assert bp("decline_off_topic", "**" + off + "**") is None    # markdown-wrapped refusal
    assert bp("partial", "The X200 lasts 40 hours. "
              + config.REFUSAL_PARTIAL + " student discounts.") is None
    assert "whole question" in bp("partial", unk)



class _ApiError(Exception):
    def __init__(self, status, msg):
        super().__init__(msg)
        self.status_code = status


class _FakeClient:
    """Rejects parameters the way real models do, and records every request."""
    def __init__(self, reject):
        self.reject, self.calls = reject, []
        self.chat = type("C", (), {"completions": self})()

    def create(self, **kw):
        self.calls.append(kw)
        for param, (status, msg) in self.reject.items():
            if param in kw:
                raise _ApiError(status, msg)
        return "RESPONSE"


def _fresh(model):
    from agent import _QUIRKS
    _QUIRKS.pop(model, None)


def test_reasoning_model_rejecting_temperature_is_retried_without_it():
    from agent import chat_completion
    _fresh("m-reason")
    c = _FakeClient({"temperature": (400, "Unsupported value: 'temperature' does not support 0")})
    resp, temp = chat_completion(c, "m-reason", [], 2000, 0.0)
    assert resp == "RESPONSE" and temp is None
    assert len(c.calls) == 2 and "temperature" not in c.calls[1]
    assert c.calls[1]["max_completion_tokens"] == 2000
    chat_completion(c, "m-reason", [], 2000, 0.0)       # quirk remembered:
    assert len(c.calls) == 3                             # one request, not two


def test_server_rejecting_max_completion_tokens_falls_back():
    from agent import chat_completion
    _fresh("m-compat")
    c = _FakeClient({"max_completion_tokens":
                     (400, "Unrecognized request argument supplied: 'max_completion_tokens'")})
    resp, temp = chat_completion(c, "m-compat", [], 2000, 0.0)
    assert resp == "RESPONSE" and temp == 0.0
    assert c.calls[-1]["max_tokens"] == 2000 and "max_completion_tokens" not in c.calls[-1]


def test_unrelated_errors_are_not_retried():
    from agent import chat_completion
    for status, msg in [(429, "Rate limit: temperature"), (400, "Invalid 'messages': empty")]:
        _fresh("m-err")
        c = _FakeClient({"model": (status, msg)})
        try:
            chat_completion(c, "m-err", [], 2000, 0.0)
            raise AssertionError("should have raised")
        except _ApiError:
            pass
        assert len(c.calls) == 1, f"{status} must not be retried (would waste money)"



def test_named_products_are_always_retrieved():
    a = SupportAgent(retriever_mode="keyword")
    _, docs, _, _ = a.build_context(
        "Is the PulseBook Pro 16 worth twice the price of the PulseBook 14 for video editing?")
    assert {"prod_pulsebook14", "prod_pulsebook_pro16"} <= set(docs)
    assert len(docs) == a.top_k
    _, docs, _, _ = a.build_context("Does the AuraWatch 3 have GPS?")
    assert docs[0] == "prod_aurawatch3" and "prod_aurawatch_pro" not in docs[:1]
    _, docs, _, _ = a.build_context("Is delivery free?")      # names nothing: plain retrieval
    assert not any(d.startswith("prod_") for d in docs)


def test_every_product_has_aliases():
    for d in load_docs(config.KB_PATH):
        if d.category == "product":
            assert d.meta.get("aliases"), f"{d.id} has no aliases"


def test_simulated_date_reaches_the_model_and_fits_the_fixtures():
    import validate_data
    a = SupportAgent(retriever_mode="keyword")
    assert "Today's date: 30 September 2026." in a.system_message("ctx")
    assert validate_data.main() == 0          # includes the date-consistency rule


def test_rupee_amounts_with_paise_parse():
    from review_results import RUPEES, _amount
    found = RUPEES.findall("contribution is ₹6,499.90, total ₹1,34,999")
    assert [_amount(m) for m in found] == [6499.90, 134999.0]


def test_catalogue_only_for_category_comparisons():
    from agent import wants_catalogue
    for q in ["Which of your headphones is lighter?", "What is your cheapest pair of headphones?",
              "Which charger do I need for the Pro 16 laptop?",
              "I want a tablet and a laptop. What should I buy under 1 lakh?"]:
        assert wants_catalogue(q), q
    for q in ["My headphones will not pair with my phone.", "Is my laptop under warranty?",
              "My monitor says no signal.", "Does the ClearView 27 support USB-C?"]:
        assert not wants_catalogue(q), q
    a = SupportAgent(retriever_mode="keyword")
    _, docs, _, _ = a.build_context("Which of your headphones is lighter?")
    assert docs[-1] == "catalogue_summary" and len(docs) == a.top_k + 1   # extra, not a slot


def test_catalogue_is_never_returned_by_search():
    r = build_retriever(load_docs(config.KB_PATH), "keyword")
    for q in ["product catalogue", "all products and prices", "product range"]:
        assert "catalogue_summary" not in [d.id for d, _ in r.search(q, 10)]


def test_catalogue_agrees_with_product_pages():
    docs = {d.id: d for d in load_docs(config.KB_PATH)}
    cat = docs["catalogue_summary"]
    lines = [line for line in cat.text.split("\n")[1:] if line.strip()]
    products = [d for d in docs.values() if d.category == "product"]
    assert len(lines) == len(products)
    for pid, line in zip(cat.meta["sources"], lines, strict=False):
        name, _, price, _ = [x.strip() for x in line.split("|")]
        assert name == docs[pid].title
        assert int(price.replace("₹", "").replace(",", "")) == docs[pid].price


def test_tracing_off_is_a_no_op():
    from tokenomics import tracing
    assert not tracing.enabled()
    with tracing.observation("x", as_type="span") as step:
        step.update(output="ignored")
    tracing.flush()
    res = SupportAgent(retriever_mode="keyword", mock=True).ask("Can I return opened headphones?",
                                                          session_id="t")
    assert res.answer and res.trace_id is None and tracing.trace_url(res.trace_id) is None


def test_trace_cost_split_matches_billing():
    from tokenomics import tracing
    model = config.FRONTIER_MODEL
    usage, cost = tracing.usage_and_cost(model, prompt_tokens=1000, completion_tokens=300,
                                         cached_tokens=400, reasoning_tokens=100)
    assert usage["input"] == 600 and usage["input_cached_tokens"] == 400
    assert usage["output"] == 200 and usage["output_reasoning_tokens"] == 100
    assert usage["total"] == 1300
    assert abs(cost["total"] - config.price(model, 1000, 300, 400)) < 1e-12
    assert tracing.usage_and_cost("unknown-model", 10, 5)[1] == {}


def test_quality_check_numbers_are_normalised():
    from quality_check import numbers
    assert numbers("₹1,34,999.00 within 30 days, order #48712") == {"134999", "30", "48712"}
    assert numbers("₹134999 in 30 days for order 48712") == {"134999", "30", "48712"}


def test_quality_check_compare_rules():
    from quality_check import compare
    near = lambda a, b: 0.97  # noqa: E731  (meaning treated as nearly identical)
    base = {"answer": "You can return it within the 30-day return window, counted from delivery."}
    same, _, why = compare(base, {"answer": "Returns are accepted within the 30-day window, from delivery."},
                           near, 0.90)
    assert same and not why
    # one number differs -> changed, even when the meaning looks the same
    same, _, why = compare(base, {"answer": "You can return it within the 31-day return window."}, near, 0.90)
    assert not same and any("numbers" in w for w in why)
    # an answer that turns into a refusal -> changed
    same, _, why = compare(base, {"answer": config.REFUSAL_UNKNOWN + " Within 30 days."}, near, 0.90)
    assert not same and any("reply kind" in w for w in why)
    # meaning drifted
    same, _, why = compare(base, base | {"answer": base["answer"] + " "}, lambda a, b: 0.5, 0.90)
    assert not same and any("similarity" in w for w in why)
    # errors are never "same"
    assert not compare(base, {"answer": "", "error": "RateLimitError"}, near, 0.90)[0]


def test_cost_per_correct():
    from quality_check import cost_per_correct
    rows = [{"id": "a", "cost_usd": 0.002}, {"id": "b", "cost_usd": 0.002}]
    assert cost_per_correct(rows, {"a": "correct", "b": "partial"}) == 0.004
    assert cost_per_correct(rows, {"a": "correct"}) is None   # ungraded answer -> no figure


def test_answer_length_technique():
    from tokenomics import techniques
    req = {"model": "m", "messages": [{"role": "system", "content": "Rules."},
                                      {"role": "user", "content": "hi"}]}
    out = techniques.apply_length(req, "concise", verbosity="low")
    assert out["messages"][0]["content"].endswith(techniques.CONCISE_RULE)
    assert out["verbosity"] == "low"
    assert req["messages"][0]["content"] == "Rules."          # the original request is untouched
    assert techniques.apply_length(req, "default") == req
    try:
        techniques.apply_length(req, "tiny")
        raise AssertionError("unknown mode accepted")
    except ValueError:
        pass
    # the rule is counted in the prompt, so its input cost shows up in every measurement
    plain = SupportAgent(retriever_mode="keyword", mock=True).ask("Is delivery free?")
    concise = SupportAgent(retriever_mode="keyword", mock=True,
                           answer_length="concise").ask("Is delivery free?")
    assert concise.prompt_tokens > plain.prompt_tokens and concise.answer_length == "concise"


def test_refusal_opening_rule():
    from quality_check import refusal_opening_cap as cap
    ans = config.REFUSAL_OFF_TOPIC + " TechStore ships within India only and not to Dubai."
    assert cap(ans, None, "correct") == "partial"                 # answerable question
    assert cap(ans, "answer_from_about", "correct") == "partial"
    assert cap(config.REFUSAL_OFF_TOPIC, "decline_off_topic", "correct") == "correct"
    assert cap("TechStore ships within India only.", None, "correct") == "correct"
    assert cap(ans, None, "wrong") == "wrong"                    # never raises a verdict


def _bow_encoder():
    """Tiny stand-in for MiniLM: bag-of-words unit vectors, so tests need no model."""
    import numpy as np
    vocab = {}

    def encode(texts):
        rows = []
        for t in texts:
            words = [w.strip("?.,!").lower() for w in t.split()]
            for w in words:
                vocab.setdefault(w, len(vocab))
            rows.append(words)
        out = np.zeros((len(texts), 512))
        for i, words in enumerate(rows):
            for w in words:
                out[i, vocab[w] % 512] += 1
        return out / np.maximum(np.linalg.norm(out, axis=1, keepdims=True), 1e-9)
    return encode


def test_faq_shortcut_gates():
    from tokenomics.faq import FaqShortcut
    entries = [
        {"id": "faq_ship", "question": "do you ship internationally", "examples": [],
         "answer": "India only.", "sources": ["ship_international"], "status": "approved"},
        {"id": "faq_pay", "question": "which payment methods do you accept", "examples": [],
         "answer": "UPI, cards.", "sources": ["bill_payment_methods"], "status": "approved"},
        {"id": "faq_draft", "question": "what are your store hours", "examples": [],
         "answer": "None.", "sources": ["about_techstore"], "status": "draft"},
    ]
    sc = FaqShortcut(entries, encode=_bow_encoder(), threshold=0.6, margin=0.05,
                     block=lambda q: "names a product" if "pulsebook" in q.lower() else None)
    assert [e["id"] for e in sc.entries] == ["faq_ship", "faq_pay"]      # drafts never served
    assert sc.lookup("Do you ship internationally?").entry["id"] == "faq_ship"
    assert sc.lookup("Do you ship internationally? Which payment methods?").entry is None
    assert "number" in sc.lookup("do you ship internationally to 48712").reason
    assert sc.lookup("do you ship the pulsebook internationally").reason == "names a product"
    assert sc.lookup("my laptop screen flickers").entry is None           # not close enough
    only_drafts = FaqShortcut([entries[2]], encode=_bow_encoder())
    assert only_drafts.lookup("what are your store hours").reason == "no approved FAQ entries"


def test_faq_answers_cite_real_documents():
    from faq_shortcut import load_faq
    from review_results import load_jsonl
    kb = {d["id"] for d in load_jsonl(config.KB_PATH)}
    dev = {q["question"].strip().lower() for q in load_jsonl(config.DEV_QUESTIONS_PATH)}
    faq = load_faq()
    assert len({e["id"] for e in faq}) == len(faq)
    for e in faq:
        assert e["status"] in ("draft", "approved") and e["answer"] and e["sources"]
        assert set(e["sources"]) <= kb, e["id"]
        assert not ({e["question"].lower(), *map(str.lower, e["examples"])} & dev), e["id"]
        if e["status"] == "approved":
            assert e["approved_by"] and e["approved_on"], e["id"]


def test_response_cache_safety_rules():
    from tokenomics import response_cache as rc
    cache = rc.ResponseCache(":memory:", encode=_bow_encoder(), threshold=0.6)
    ns = "ns"
    assert cache.store("Is delivery free?", "Free above 999.", ns, "m") == "stored"
    hit = cache.lookup("is delivery free", ns).hit                       # exact (normalised)
    assert hit and hit.kind == "exact"
    assert cache.lookup("Is delivery free?", "other-namespace").hit is None   # never crosses apps/settings
    # meaning flips are refused in BOTH directions
    cache.store("How do I turn on noise cancellation?", "A", ns, "m")
    assert cache.lookup("How do I turn off noise cancellation?", ns).hit is None
    cache.store("How do I disable two-factor authentication?", "B", ns, "m")
    assert cache.lookup("How do I enable two-factor authentication?", ns).hit is None
    # different numbers or products -> different entities -> no reuse
    cache.store("How much is delivery on a ₹500 order?", "C", ns, "m")
    assert "entities" in cache.lookup("How much is delivery on a ₹1500 order?", ns).reason
    cache.store("Is it good for video editing?", "D", ns, "m", frozenset({"prod_pulsebook_air13"}))
    assert cache.lookup("Is it good for video editing?", ns, frozenset({"prod_novatab_mini8"})).hit is None
    # personal / time-varying / private: never stored, never served
    assert cache.store("Where is my order 48213?", "E", ns, "m").startswith("not stored")
    assert cache.store("Will my refund arrive today?", "F", ns, "m").startswith("not stored")
    assert cache.store("Why was I charged twice?", "G", ns, "m", private=True).startswith("not stored")
    assert cache.lookup("Why was I charged twice?", ns).hit is None


def test_response_cache_expiry():
    from tokenomics import response_cache as rc
    cache = rc.ResponseCache(":memory:", encode=_bow_encoder(), ttl_hours=-1)   # already expired
    cache.store("Is delivery free?", "Free above 999.", "ns", "m")
    assert cache.lookup("Is delivery free?", "ns").hit is None


def test_agent_reuses_cached_answer(monkeypatch):
    from tokenomics import response_cache as rc
    monkeypatch.setattr(rc, "_minilm", _bow_encoder)          # no model download in CI
    agent = SupportAgent(retriever_mode="keyword", mock=True, faq=False, cache=True)
    first = agent.ask("Is delivery free?")
    again = agent.ask("Is delivery free?")
    assert first.served_by == "model" and "stored" in first.cache_note
    assert again.served_by == "cache" and again.cache_kind == "exact" and again.cost_usd == 0
    order = agent.ask("Where is my order 48213?")
    assert order.served_by == "model" and "not stored" in order.cache_note


def _chat(n):
    msgs = [{"role": "system", "content": "Rules and documents."}]
    for i in range(1, n):
        msgs += [{"role": "user", "content": f"question {i} about order 48712 and ₹12,999"},
                 {"role": "assistant", "content": f"answer {i}"}]
    return msgs + [{"role": "user", "content": f"question {n}"}]


def test_memory_modes():
    from tokenomics import techniques as t
    req = {"model": "m", "messages": _chat(5)}             # 4 earlier turns + the new question
    same, info = t.apply_memory(req, "off")
    assert same == req and info["dropped_turns"] == 0
    short, _ = t.apply_memory({"model": "m", "messages": _chat(3)}, "window", keep_turns=2)
    assert short["messages"] == _chat(3)                   # nothing older than 2 turns yet
    win, info = t.apply_memory(req, "window", keep_turns=2)
    assert info["dropped_turns"] == 2
    assert [m["content"] for m in win["messages"]][1:] == [
        "question 3 about order 48712 and ₹12,999", "answer 3",
        "question 4 about order 48712 and ₹12,999", "answer 4", "question 5"]
    facts, _ = t.apply_memory(req, "facts", keep_turns=2)
    note = facts["messages"][1]
    assert note["role"] == "system" and "48712" in note["content"] and "₹12,999" in note["content"]
    assert "question 1" in note["content"] and req["messages"] == _chat(5)   # input untouched


def test_memory_summary_is_rolling():
    from tokenomics import techniques as t
    calls, cache = [], {}

    def summarise(prev, msgs):
        calls.append((prev, len(msgs)))
        return (prev or "") + f"+{len(msgs)}"
    for n in (4, 5, 6):                                    # three successive turns of one chat
        t.apply_memory({"model": "m", "messages": _chat(n)}, "summary", 2, summarise, cache)
    # each turn summarises only the turn that newly aged out, extending the previous summary
    assert calls == [(None, 2), ("+2", 2), ("+2+2", 2)]
    t.apply_memory({"model": "m", "messages": _chat(6)}, "summary", 2, summarise, cache)
    assert len(calls) == 3                                 # same history again: no new call


def test_agent_conversation():
    agent = SupportAgent(retriever_mode="keyword", mock=True, memory="window", keep_turns=1)
    history = []
    for q in ["What's happening with order 48712?", "Why are there three charges?",
              "Can I still cancel it?"]:
        res = agent.ask(q, history=history)
        history += [{"role": "user", "content": q}, {"role": "assistant", "content": res.answer}]
    assert res.turn == 3 and res.memory_dropped_turns == 1
    assert res.orders_used == ["48712"]        # the order from turn 1 is still looked up at turn 3
    assert res.served_by == "model"            # follow-ups never use the FAQ or cache


def test_cache_write_and_read_billing():
    from tokenomics import tracing
    m = config.FRONTIER_MODEL                      # Sol: input $2, write $2.50, read $0.10 per 1M
    p = config.PRICING[m]
    cost = config.price(m, 2000, 100, cached_prompt_tokens=1200, cache_write_tokens=500)
    expect = (300 * p["input"] + 1200 * p["cached_input"] + 500 * p["cache_write"] + 100 * p["output"]) / 1e6
    assert abs(cost - expect) < 1e-12
    usage, c = tracing.usage_and_cost(m, 2000, 100, cached_tokens=1200, cache_write_tokens=500)
    assert usage["input"] == 300 and usage["input_cache_write_tokens"] == 500
    assert abs(c["total"] - cost) < 1e-12


def test_cache_layout():
    import pytest

    from agent import QUESTION_MARK, _question_of
    agent = SupportAgent(retriever_mode="keyword", mock=True, layout="cache")
    first = agent.ask("Is delivery free?")
    system, user = agent.last_request["messages"][0], agent.last_request["messages"][-1]
    assert "REFERENCE DOCUMENTS" not in system["content"]          # fixed instructions only
    assert "REFERENCE DOCUMENTS" in user["content"] and user["content"] == first.sent_user_message
    assert _question_of(first.sent_user_message) == "Is delivery free?"
    history = [{"role": "user", "content": first.sent_user_message},
               {"role": "assistant", "content": first.answer}]
    agent.ask("And for express?", history=history)
    # the new prompt starts with the previous prompt, word for word: reusable by the provider
    assert agent.last_request["messages"][:2] == [system, history[0]]
    assert QUESTION_MARK not in _question_of("plain question")
    with pytest.raises(ValueError):
        SupportAgent(retriever_mode="keyword", mock=True, layout="cache", memory="facts")


def test_prompt_cache_simulation_rules():
    from prompt_cache_sim import price_requests
    big = "word " * 1500                                    # comfortably over 1,024 tokens
    sys_msg = {"role": "system", "content": "instructions"}
    t1 = [sys_msg, {"role": "user", "content": big + "first"}]
    t2 = t1 + [{"role": "assistant", "content": "answer"}, {"role": "user", "content": "second"}]
    grows = price_requests([t1, t2], config.FRONTIER_MODEL, writes_billed=True)
    assert grows["cached_tokens"] > 1024 and grows["written_tokens"] > 1024   # turn 2 reuses turn 1
    changing = price_requests([t1, [{"role": "system", "content": "other"}, *t1[1:]]],
                              config.FRONTIER_MODEL, writes_billed=True)
    assert changing["cached_tokens"] == 0                   # a different start: no reuse
    assert changing["cost_with_cache"] > changing["cost_no_cache"]        # writes wasted
    small = price_requests([[sys_msg, {"role": "user", "content": "hi"}]] * 2, config.FRONTIER_MODEL, True)
    assert small["cached_tokens"] == small["written_tokens"] == 0          # under 1,024: never cached


def test_adaptive_context():
    q = "Can I compare the PulseBook 14 with the Pro 16 for video editing?"
    fixed = SupportAgent(retriever_mode="keyword", mock=True)
    tight = SupportAgent(retriever_mode="keyword", mock=True, context_margin=0.0)
    loose = SupportAgent(retriever_mode="keyword", mock=True, context_margin=1e9)
    _, docs_fixed, _, _ = fixed.build_context(q)
    _, docs_tight, _, _ = tight.build_context(q)
    _, docs_loose, _, _ = loose.build_context(q)
    named = {"prod_pulsebook14", "prod_pulsebook_pro16"}
    assert named <= set(docs_tight)                      # named products are always kept
    assert len(docs_tight) < len(docs_fixed) and docs_loose == docs_fixed
    _, one, _, _ = tight.build_context("How long do I have to return something?")
    assert len(one) == 1                                 # a clear winner travels alone


def test_passage_keeps_first_sentence():
    import pytest
    pytest.importorskip("sentence_transformers")
    agent = SupportAgent(retriever_mode="keyword", mock=True, passage_margin=0.0)
    doc = next(d for d in agent.docs if d.id == "pol_refund_timeline")
    text = agent.passage(doc, "Can a refund go to a different card?")
    assert text.startswith(doc.text.split(". ")[0]) and len(text) < len(doc.text)


def test_token_bucket():
    from tokenomics.spending_limits import TokenBucket
    now = [0.0]
    bucket = TokenBucket(2, clock=lambda: now[0])           # 2 requests per minute
    assert bucket.take() and bucket.take() and not bucket.take()
    now[0] = 30                                             # half a minute refills one
    assert bucket.take() and not bucket.take()


def test_spending_limit_decisions():
    from tokenomics.spending_limits import SpendingLimits
    now = [1_800_000_000.0]
    lim = SpendingLimits(":memory:", client_daily_usd=1.0, global_daily_usd=5.0, soft_ratio=0.8,
                         rpm=0, downgrade_model="cheap", clock=lambda: now[0])
    est = {"big": 0.10, "cheap": 0.01}.get
    assert lim.check("a", "big", est).action == "allow"
    lim.record("a", 0.75)
    d = lim.check("a", "big", est)                          # 0.75 + 0.10 > 0.80 soft limit
    assert d.action == "downgrade" and d.model == "cheap"
    lim.record("a", 0.985)                                  # now 1.735 > budget even for cheap
    assert lim.check("a", "big", est).action == "refuse"
    assert lim.check("b", "big", est).action == "allow"     # other clients unaffected
    lim.record("b", 3.3)                                    # app total now 5.035
    assert "app daily cap" in lim.check("c", "big", est).reason
    assert "app daily cap" in lim.check(None, "big", est).reason   # scripts too
    now[0] += 86_400                                        # next day: everything resets
    assert lim.check("a", "big", est).action == "allow"


def test_agent_spending_limits():
    from agent import LIMIT_REACHED
    from tokenomics.spending_limits import SpendingLimits
    agent = SupportAgent(retriever_mode="keyword", mock=True, faq=False)
    agent.limits = SpendingLimits(":memory:", client_daily_usd=0.006, global_daily_usd=1.0, rpm=0,
                                  downgrade_model=config.ECONOMY_MODEL)
    seen = []
    for _ in range(60):          # after the downgrade, cheap answers stretch the budget a long way
        r = agent.ask("How do I reset my password?", client_id="visitor-1")
        seen.append((r.limit_action, r.model, r.cost_usd))
    actions = [a for a, _, _ in seen]
    assert actions[0] == "allow" and "downgrade" in actions and actions[-1] == "refuse"
    assert all(m == config.ECONOMY_MODEL for a, m, _ in seen if a == "downgrade")
    assert all(c == 0 for a, _, c in seen if a == "refuse")       # refusals cost nothing
    assert r.answer == LIMIT_REACHED and r.served_by == "limit"
    assert agent.limits.spent("visitor-1") <= 0.006 + 1e-9         # never over budget


def test_stores_work_across_threads():
    """Streamlit answers each message on a new thread; the stores must allow that."""
    import threading

    from tokenomics import response_cache as rc
    from tokenomics.spending_limits import SpendingLimits
    lim = SpendingLimits(":memory:", rpm=0)
    cache = rc.ResponseCache(":memory:", encode=_bow_encoder())
    errors = []

    def worker():
        try:
            lim.record("visitor", 0.01)
            lim.check("visitor", "m", lambda m: 0.001)
            cache.store("Is delivery free?", "Free above 999.", "ns", "m")
            cache.lookup("Is delivery free?", "ns")
        except Exception as exc:                      # noqa: BLE001
            errors.append(exc)
    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors and abs(lim.spent("visitor") - 0.04) < 1e-9


def test_spending_limit_without_cheap_model():
    """No downgrade model configured: allow up to the budget, then refuse; never 'downgrade'."""
    from tokenomics.spending_limits import SpendingLimits
    lim = SpendingLimits(":memory:", client_daily_usd=1.0, soft_ratio=0.5, rpm=0)
    est = {"big": 0.10}.get
    lim.record("a", 0.85)                                   # past the soft limit, room left
    assert lim.check("a", "big", est).action == "allow"
    lim.record("a", 0.10)
    assert lim.check("a", "big", est).action == "refuse"    # 0.95 + 0.10 > 1.00
