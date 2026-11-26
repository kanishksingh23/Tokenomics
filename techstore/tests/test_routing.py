"""Technique 14, model routing. No API calls: the router's checks run on fixed texts (several
taken from real Luna answers) and the agent runs in mock mode."""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ["LANGFUSE_TRACING"] = "off"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import agent as agent_mod  # noqa: E402
import config  # noqa: E402
from agent import REFUSAL_LINE, SupportAgent, make_router  # noqa: E402


def test_real_weak_patterns_escalate():
    r = make_router()
    # Real Luna partial (q053): a refusal line before a correct answer.
    c = r.check("Can I pay with my Paytm wallet?",
                f"{REFUSAL_LINE} Paytm wallet payments aren't accepted; TechStore accepts UPI.")
    assert c.escalate and "refusal_then_answer" in c.signals
    # Generic hedging: two weak signs together escalate.
    c = r.check("What's the warranty?", "I'm not sure, but it might be 2 years.")
    assert c.escalate and c.signals["hedge"] >= 0.7


def test_correct_answers_and_plain_declines_stay():
    r = make_router()
    assert not r.check("Is delivery free?", "Delivery is free on orders above ₹499.").escalate
    # "I don't have information about" is legitimate in TechStore answers: weak on its own.
    c = r.check("X200 battery and student discount?",
                "The SoundWave X200 has up to 40-hour battery life. "
                "I don't have information about student discounts.")
    assert not c.escalate and c.signals == {"missing_info": 0.3}
    # A plain off-topic refusal (plus the allowed offer of help) is not a weak answer.
    c = r.check("Weather in Delhi?", f"{REFUSAL_LINE} I can help with orders, returns and products.")
    assert not c.escalate and not c.signals
    # Cut off by the length limit: the frontier model would be cut off too.
    c = r.check("Explain the EMI rules", "I'm not sure, it might be that the EMI", finish_reason="length")
    assert not c.escalate and c.suppressed_by.startswith("truncated")


def test_choose_rules_and_stickiness():
    r = make_router()
    assert r.choose("Is delivery free?").tier == "economy"
    assert r.choose("Why does this fail?\n```python\nclient.get()\n```").tier == "frontier"
    assert r.choose("word " * 400).reason.startswith("long question")
    assert r.choose("hi", {"tools": [{"type": "function"}]}).tier == "frontier"
    r.record("chat-1", escalated=True)
    assert [r.choose("next?", conversation_id="chat-1").tier for _ in range(1)] == ["frontier"]
    for _ in range(3):
        r.record("chat-1", escalated=False)
    assert r.choose("next?", conversation_id="chat-1").tier == "economy"   # decayed after 3 turns
    assert r.choose("next?", conversation_id="chat-2").tier == "economy"   # other chats unaffected


def test_agent_auto_escalates_once_and_adds_both_costs(monkeypatch):
    def respond(self, question, context, retrieved, messages=None, model=None):
        text = ("I'm not sure, I think it might be 30 days." if model == config.ECONOMY_MODEL
                else "You can return items within the 30-day return window.")
        return text, 600, 40
    monkeypatch.setattr(agent_mod.MockCompletion, "respond", respond)
    a = SupportAgent(model="auto", retriever_mode="keyword", mock=True, faq=False)
    res = a.ask("How long do I have to return something?")
    assert res.route_tier == "economy" and res.escalated
    assert res.first_model == config.ECONOMY_MODEL and res.model == config.FRONTIER_MODEL
    assert res.answer.startswith("You can return") and res.first_answer.startswith("I'm not sure")
    assert res.prompt_tokens == 1200                                     # both calls counted
    expected = config.price(config.ECONOMY_MODEL, 600, 40) + config.price(config.FRONTIER_MODEL, 600, 40)
    assert abs(res.cost_usd - expected) < 2e-6
    # Batch questions share a session id but are not a conversation: no stickiness.
    nxt = a.ask("Is delivery free?", session_id="batch")
    assert nxt.route_tier == "economy"


def test_agent_auto_keeps_good_cheap_answers():
    a = SupportAgent(model="auto", retriever_mode="keyword", mock=True, faq=False)
    res = a.ask("Is delivery free?")
    assert res.model == config.ECONOMY_MODEL and not res.escalated and res.route_tier == "economy"
    fixed = SupportAgent(model=config.FRONTIER_MODEL, retriever_mode="keyword", mock=True, faq=False)
    assert fixed.router is None and fixed.ask("Is delivery free?").route_tier is None


def test_replay_on_real_graded_answers():
    """Guard against a change that makes routing worse on the real (already paid for) runs:
    the router must stay far cheaper than always-Sol, never lose quality vs always-Luna, and
    not escalate more than a handful of questions."""
    from routing_replay import PAIRS, evaluate
    for name, luna_run, sol_run in PAIRS:
        arms = {a["arm"]: a for a in evaluate(luna_run, sol_run, seeds=20)[0]}
        sol, luna, router = arms["always Sol"], arms["always Luna"], arms["router"]
        assert router["cost"] < 0.15 * sol["cost"], name
        assert router["score"] >= luna["score"] and router["wrong"] == 0, name
        assert router["to_sol"] <= 4, name
