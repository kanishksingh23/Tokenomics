"""Calling the AI provider (any OpenAI-compatible API), adapting to what each model accepts."""
from __future__ import annotations

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
