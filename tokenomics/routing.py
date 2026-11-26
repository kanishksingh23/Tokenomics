"""Technique 14, model routing: answer with the cheap model first, escalate only when needed.

Two steps, both cheap and explainable:

1. **Choose** (before any call): a request goes to the economy model unless a hard rule says it
   needs the frontier model (code in the question, a very long question, tools or a strict JSON
   schema, or a conversation that recently escalated). A client asking for a concrete model is
   always honoured; only `model="auto"` is routed.
2. **Check** (after the economy answer): look for signs the answer is weak. If the combined
   uncertainty reaches the threshold, the answer is discarded and the same request is sent once
   to the frontier model. Never more than one escalation.

Why cheap-first: an escalated request costs economy + frontier, but with a 20x price gap
(Luna vs Sol) cheap-first stays cheaper than always-frontier unless more than ~95% of requests
escalate. Real TechStore runs: Luna was never wrong on the 64 dev questions; its few partial
answers showed visible patterns (a refusal line before a real answer, "I don't have
information" when the documents had it), which is what the checks below look for.

Uncertainty: each signal gives a strength in [0, 1]; they combine as independent evidence,
U = 1 - (1 - s1)(1 - s2)..., so one strong signal or two weak ones can escalate.
Suppression guards: no escalation when the answer was cut off by the length limit (the
frontier model would be cut off too) or when the answer is purely a decline/refusal (the
frontier model would decline too).
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field

# Generic hedges: the model saying it is unsure. Weak alone (0.35 each), so two are needed.
HEDGE_PATTERNS = [
    r"\bi('m| am) not (entirely |completely |totally )?sure\b",
    r"\bit (might|could|may) be\b",
    r"\bi (cannot|can't|am unable to) (verify|confirm)\b",
    r"\bas an ai( language model)?\b",
    r"\bactually, (wait|let me reconsider)\b",
    r"\bi (think|believe|guess)\b",
]
# The question asks for depth; a very short answer to it is suspicious.
DEPTH_WORDS = re.compile(r"\b(explain|compare|comparison|versus|vs\.?|troubleshoot|step by step|"
                         r"why|difference|which (one|should)|recommend)\b", re.I)
CODE_MARKERS = re.compile(r"```|\bTraceback\b|\bdef \w+\(|\bfunction\s*\(|\{\s*\"", re.I)


@dataclass
class RouteDecision:
    model: str
    tier: str                 # "economy" or "frontier"
    reason: str


@dataclass
class Check:
    """Uncertainty of an economy answer."""
    escalate: bool
    uncertainty: float
    signals: dict = field(default_factory=dict)    # name -> strength (only those that fired)
    suppressed_by: str | None = None               # guard that blocked an escalation


@dataclass
class Router:
    economy: str = "gpt-6-luna"
    frontier: str = "gpt-6.1-sol"
    threshold: float = 0.5
    max_question_tokens: int = 250        # longer questions go straight to frontier
    sticky_turns: int = 3                 # after an escalation, the next N turns stay frontier
    # App-specific fixed sentences (from the app's own instructions). Optional.
    decline_lines: tuple = ()             # "the documents don't cover this" replies
    refusal_lines: tuple = ()             # "not my topic" replies
    missing_info_phrases: tuple = ()      # "I don't have information about ..."
    # How strongly "something is missing" counts. Weak by default: apps often tell the model to
    # say it when part of an answer is genuinely missing (TechStore does), so it is right more
    # often than wrong; 0.3 needs a second signal to escalate.
    missing_info_weight: float = 0.3
    _sticky: dict = field(default_factory=dict)    # conversation id -> (turns left, last used)

    # ------------------------------------------------------------------ step 1: choose
    def choose(self, question: str, request: dict | None = None,
               conversation_id: str | None = None) -> RouteDecision:
        request = request or {}
        if conversation_id and self._sticky_left(conversation_id) > 0:
            return RouteDecision(self.frontier, "frontier", "sticky: this conversation escalated recently")
        if request.get("tools") or (request.get("response_format") or {}).get("type") == "json_schema":
            return RouteDecision(self.frontier, "frontier", "capability: tools or strict JSON schema")
        if CODE_MARKERS.search(question or ""):
            return RouteDecision(self.frontier, "frontier", "code in the question")
        if _approx_tokens(question) > self.max_question_tokens:
            return RouteDecision(self.frontier, "frontier",
                                 f"long question (> {self.max_question_tokens} tokens)")
        return RouteDecision(self.economy, "economy", "default: cheap model first")

    # ------------------------------------------------------------------ step 2: check
    def check(self, question: str, answer: str, finish_reason: str | None = None,
              completion_tokens: int | None = None) -> Check:
        text = (answer or "").strip()
        low = text.lower()
        signals: dict[str, float] = {}
        if not text:
            signals["empty"] = 1.0
        # A fixed refusal/decline line followed by a real answer: the model answered but
        # opened as if it couldn't (graded partial at best; rubric rule 4).
        opener = _starts_with(low, self.refusal_lines + self.decline_lines)
        if opener is not None:
            rest = text[len(opener):].strip()
            if _sentences(rest) and not _only_offers_help(rest):
                signals["refusal_then_answer"] = 0.8
        # Says something is missing although it answered: often the documents had it.
        if opener is None and any(p.lower() in low for p in self.missing_info_phrases):
            signals["missing_info"] = self.missing_info_weight
        hedges = sum(bool(re.search(p, low)) for p in HEDGE_PATTERNS)
        if hedges:
            signals["hedge"] = min(1.0, 0.35 * hedges)
        words = len(text.split())
        if DEPTH_WORDS.search(question or "") and 0 < words < 25 and opener is None:
            signals["too_short"] = 0.6
        sents = _sentences(text)
        if len(sents) >= 4:
            rep = 1 - len({s.lower() for s in sents}) / len(sents)
            if rep > 0:
                signals["repetition"] = round(min(1.0, rep * 2), 2)
        if text and (text.count("```") % 2 == 1 or text[-1] not in ".!?)\"'*`:|]"
                     and not re.search(r"\d$", text)):
            signals["unfinished"] = 0.4
        u = 1.0
        for s in signals.values():
            u *= 1 - s
        u = round(1 - u, 3)
        # Suppression guards: escalating cannot help here.
        guard = None
        if finish_reason == "length":
            guard = "truncated by the length limit (frontier would be too)"
        elif opener is not None and "refusal_then_answer" not in signals:
            guard = "a plain decline or refusal (frontier would decline too)"
        escalate = u >= self.threshold and guard is None
        return Check(escalate, u, signals, guard if u >= self.threshold else None)

    # ------------------------------------------------------------------ stickiness
    def record(self, conversation_id: str | None, escalated: bool) -> None:
        """Call once per answered turn. An escalation makes the next turns frontier."""
        if not conversation_id:
            return
        if escalated:
            self._sticky[conversation_id] = (self.sticky_turns, time.time())
        elif conversation_id in self._sticky:
            left, _ = self._sticky[conversation_id]
            if left <= 1:
                del self._sticky[conversation_id]
            else:
                self._sticky[conversation_id] = (left - 1, time.time())
        if len(self._sticky) > 10_000:                      # forget the oldest
            for k in sorted(self._sticky, key=lambda k: self._sticky[k][1])[:1000]:
                del self._sticky[k]

    def _sticky_left(self, conversation_id: str) -> int:
        return self._sticky.get(conversation_id, (0, 0))[0]


def _approx_tokens(text: str) -> int:
    return int(len((text or "").split()) * 1.35)


def _starts_with(low: str, lines: tuple) -> str | None:
    for line in lines:
        if low.startswith(line.lower()):
            return line
    return None


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if len(s.strip()) > 3]


def _only_offers_help(rest: str) -> bool:
    """The instructions allow one short sentence on what the agent *can* help with."""
    s = _sentences(rest)
    return len(s) == 1 and bool(re.search(r"\b(i can|i'd be happy|happy to|i can help|"
                                          r"feel free|let me know|connect you)\b", s[0], re.I))
