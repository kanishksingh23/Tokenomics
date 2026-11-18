"""Token- and cost-saving techniques that act on an OpenAI-style request.

Each function takes the request (model, messages, parameters) and returns a changed copy;
nothing here knows about TechStore. The gateway (roadmap step 13, Tokenomics.md §10) will
apply the same functions to any app's requests. Until it exists, the TechStore agent
applies them itself, so every technique can be measured now.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re

# Technique 3, answer-length control. Output tokens cost 5x input on both GPT-6 models, so
# shorter visible answers save the most per token. The rule costs about 60 input tokens on
# every call, so it pays off only if answers shrink by more than ~12 tokens on average.
CONCISE_RULE = (
    "Answer length: start with the direct answer in one or two sentences. Add a short list "
    "or numbered steps only when the question needs them (troubleshooting, billing "
    "breakdowns, comparisons). No greeting, no restating the question, and no closing offer "
    "of more help."
)
LENGTH_MODES = ("default", "concise")


def apply_length(request: dict, mode: str | None = None, verbosity: str | None = None) -> dict:
    """Answer-length control.
    mode="concise" appends CONCISE_RULE to the system message (works on any model).
    verbosity="low|medium|high" sets the provider's own length setting, which adds no input
    tokens but only some models accept (an unsupported value fails loudly, never silently)."""
    if (mode or "default") not in LENGTH_MODES:
        raise ValueError(f"unknown answer-length mode {mode!r}; choose from {LENGTH_MODES}")
    out = copy.deepcopy(request)
    if mode == "concise":
        msgs = out["messages"]
        if msgs and msgs[0]["role"] == "system":
            msgs[0]["content"] = f"{msgs[0]['content']}\n\n{CONCISE_RULE}"
        else:
            msgs.insert(0, {"role": "system", "content": CONCISE_RULE})
    if verbosity:
        out["verbosity"] = verbosity
    return out


def apply_reasoning(request: dict, effort: str | None = None) -> dict:
    """Technique 2, reasoning-effort control: how much hidden thinking the model does.
    GPT-6 Luna accepts none/low/medium/high, Sol low/medium/high (checked 2026-10-15)."""
    out = copy.deepcopy(request)
    if effort:
        out["reasoning_effort"] = effort
    return out


# Technique 9, conversation memory. In the OpenAI format every request carries the WHOLE
# conversation so far, so input tokens grow with every turn. These modes keep the last
# `keep_turns` exchanges word for word and shrink everything older:
#   window   drop older turns entirely (free; forgets what was said early on)
#   facts    replace them with a short note of their facts: numbers, amounts, emails and the
#            customer's earlier questions (free; no model call)
#   summary  replace them with a model-written summary (one small extra call, cached so each
#            older turn is summarised once, not on every new turn)
MEMORY_MODES = ("off", "window", "facts", "summary")
_FACT = re.compile(r"₹\s?[\d,]+(?:\.\d+)?|#?\b\d{5}\b|[\w.+-]+@[\w-]+\.[\w.]+|"
                   r"\b\d{1,2} (?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b", re.I)


def _split(messages: list[dict]) -> tuple[list[dict], list[list[dict]], dict]:
    """(leading system messages, earlier turns as [user, assistant...] groups, final user msg)."""
    head = [m for m in messages[: next((i for i, m in enumerate(messages) if m["role"] != "system"),
                                        len(messages))]]
    body = messages[len(head):]
    final, earlier = body[-1], body[:-1]
    turns: list[list[dict]] = []
    for m in earlier:
        if m["role"] == "user" or not turns:
            turns.append([m])
        else:
            turns[-1].append(m)
    return head, turns, final


def facts_note(turns: list[list[dict]]) -> str:
    """No-model memory: what the customer asked earlier, and every number/amount/email/date
    mentioned by either side, with nothing invented."""
    asked = [t[0]["content"].strip() for t in turns if t and t[0]["role"] == "user"]
    found: list[str] = []
    for t in turns:
        for m in t:
            for f in _FACT.findall(m["content"]):
                f = f.strip()
                if f not in found:
                    found.append(f)
    note = "Earlier in this conversation the customer asked: " + " | ".join(
        q if len(q) <= 160 else q[:157] + "..." for q in asked) + "."
    if found:
        note += " Details mentioned: " + ", ".join(found) + "."
    return note


def _key(messages: list[dict]) -> str:
    return hashlib.sha256(json.dumps(messages, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def apply_memory(request: dict, mode: str = "off", keep_turns: int = 2, summarise=None,
                 summary_cache: dict | None = None) -> tuple[dict, dict]:
    """Returns (changed request, info). `summarise(previous_summary, messages) -> str` is
    needed for mode "summary"; `summary_cache` (any dict) makes it a rolling summary."""
    if mode not in MEMORY_MODES:
        raise ValueError(f"unknown memory mode {mode!r}; choose from {MEMORY_MODES}")
    out = copy.deepcopy(request)
    head, turns, final = _split(out["messages"])
    info = {"mode": mode, "turns_before": len(turns), "dropped_turns": 0, "summary_calls": 0}
    if mode == "off" or len(turns) <= keep_turns:
        return out, info
    old, recent = turns[:-keep_turns] if keep_turns else turns, turns[-keep_turns:] if keep_turns else []
    info["dropped_turns"] = len(old)
    note = None
    if mode == "facts":
        note = facts_note(old)
    elif mode == "summary":
        if summarise is None:
            raise ValueError("memory mode 'summary' needs a summarise function")
        cache = summary_cache if summary_cache is not None else {}
        flat = [m for t in old for m in t]
        note = cache.get(_key(flat))
        if note is None:
            # Rolling: start from the longest already-summarised prefix, add only the rest.
            prev, start = None, 0
            for cut in range(len(old) - 1, 0, -1):
                prefix = [m for t in old[:cut] for m in t]
                if _key(prefix) in cache:
                    prev, start = cache[_key(prefix)], cut
                    break
            note = summarise(prev, [m for t in old[start:] for m in t])
            cache[_key(flat)] = note
            info["summary_calls"] = 1
        note = "Summary of the earlier conversation: " + note
    messages = list(head)
    if note:
        messages.append({"role": "system", "content": note})
    for t in recent:
        messages.extend(t)
    messages.append(final)
    out["messages"] = messages
    return out, info
