"""Counting tokens without calling a model (for estimates and mock runs)."""
from __future__ import annotations

# Per-message framing the chat format adds around each message, and the reply priming.
MSG_OVERHEAD = 3
REPLY_PRIMING = 3


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


def prompt_tokens(messages: list[dict]) -> int:
    """What the API would count for these messages."""
    return sum(count_tokens(m["content"]) + MSG_OVERHEAD for m in messages) + REPLY_PRIMING
