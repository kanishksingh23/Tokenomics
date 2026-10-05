"""Phase 0 tests. None of these call an API, so they are free and run in CI."""
from __future__ import annotations

import json
import sys
from pathlib import Path

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
