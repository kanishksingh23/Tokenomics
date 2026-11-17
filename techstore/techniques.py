"""Token- and cost-saving techniques that act on an OpenAI-style request.

Each function takes the request (model, messages, parameters) and returns a changed copy;
nothing here knows about TechStore. The gateway (roadmap step 13, Tokenomics.md §10) will
apply the same functions to any app's requests. Until it exists, the TechStore agent
applies them itself, so every technique can be measured now.
"""
from __future__ import annotations

import copy

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
