"""Langfuse tracing: one trace per question, with a `retrieve` step and an `llm` step.

Optional. Without the langfuse package or its keys in .env, every function here
is a no-op, so tests, CI and anyone without an account run unchanged.
Set LANGFUSE_TRACING=off to disable it even when the keys are present.

Costs are sent explicitly (from config.PRICING) rather than left for Langfuse to
infer, because its built-in price list may not know our models.
"""
from __future__ import annotations

import os
from contextlib import contextmanager

_client = None
_checked = False


def client():
    """The Langfuse client, or None when tracing is off or not configured."""
    global _client, _checked
    if not _checked:
        _checked = True
        if (os.getenv("LANGFUSE_TRACING", "on").lower() != "off"
                and os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")):
            try:
                from langfuse import get_client  # noqa: PLC0415
                _client = get_client()
            except ImportError:
                _client = None
    return _client


def enabled() -> bool:
    return client() is not None


class _Null:
    """Stands in for a Langfuse observation when tracing is off."""
    id = None
    trace_id = None

    def update(self, **_):
        return self


@contextmanager
def observation(name: str, **kwargs):
    """A step inside the current trace (or a new trace, if none is open)."""
    lf = client()
    if lf is None:
        yield _Null()
        return
    with lf.start_as_current_observation(name=name, **kwargs) as obs:
        yield obs


@contextmanager
def question_trace(question: str, *, model: str, retriever: str, top_k: int,
                   mock: bool, session_id: str | None = None):
    """Root of one question's trace. Attributes set here are copied onto every step."""
    lf = client()
    if lf is None:
        yield _Null()
        return
    from langfuse import propagate_attributes  # noqa: PLC0415
    with lf.start_as_current_observation(name="techstore-question", input=question) as root:
        with propagate_attributes(
            trace_name="techstore-question",
            session_id=session_id,
            # Mock runs go to their own environment so they never mix with real data.
            environment="mock" if mock else "development",
            tags=[model, f"retriever:{retriever}", f"top_k:{top_k}"],
            metadata={"model": model, "retriever": retriever, "top_k": str(top_k)},
        ):
            yield root


def usage_and_cost(model: str, prompt_tokens: int, completion_tokens: int,
                   cached_tokens: int = 0, reasoning_tokens: int = 0) -> tuple[dict, dict]:
    """Token counts and USD cost in Langfuse's format, split the way they are billed."""
    import config  # noqa: PLC0415
    cached = min(max(cached_tokens, 0), prompt_tokens)
    reasoning = min(max(reasoning_tokens, 0), completion_tokens)
    usage = {
        "input": prompt_tokens - cached,
        "input_cached_tokens": cached,
        "output": completion_tokens - reasoning,
        "output_reasoning_tokens": reasoning,
    }
    usage["total"] = sum(usage.values())
    p = config.PRICING.get(model)
    if not p:
        return usage, {}
    cost = {
        "input": usage["input"] * p["input"] / 1e6,
        "input_cached_tokens": cached * p.get("cached_input", p["input"]) / 1e6,
        # Reasoning tokens are billed at the output rate.
        "output": usage["output"] * p["output"] / 1e6,
        "output_reasoning_tokens": reasoning * p["output"] / 1e6,
    }
    cost["total"] = sum(cost.values())
    return usage, cost


def trace_url(trace_id: str | None) -> str | None:
    lf = client()
    if lf is None or not trace_id:
        return None
    try:
        return lf.get_trace_url(trace_id=trace_id)
    except Exception:                                   # noqa: BLE001
        return None


def flush() -> None:
    """Send buffered traces now. Short-lived scripts must call this before exiting."""
    lf = client()
    if lf is not None:
        lf.flush()
