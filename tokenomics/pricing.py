"""Model prices and the cost of one call.

$ per 1M tokens, Standard tier, short context. Verified 2026-10-03 against
developers.openai.com/api/docs/pricing; model ids verified on the account's Limits page.
Batch and Flex tiers are 50% of these rates.

Prompt caching (developers.openai.com/api/docs/guides/prompt-caching, read 2026-11-18):
prompts of 1,024+ tokens can be cached by exact prefix; writing a prefix costs 1.25x input
(30-minute cache), reading it 0.05x for GPT-6.1 Sol and 0.1x for others. price() bills
both when the response reports them; whether Chat Completions reports cache writes is
still to be confirmed with a real call (techstore/runs/PENDING_CREDITS.md).
"""
PRICING = {
    "gpt-6.1-sol": {"input": 2.00,  "cached_input": 0.10, "cache_write": 2.50,  "output": 10.00},
    "gpt-6-luna":  {"input": 0.10,  "cached_input": 0.01, "cache_write": 0.125, "output": 0.50},
    "gpt-6-astra": {"input": 10.00, "cached_input": 1.00, "cache_write": 12.50, "output": 50.00},
}
PRICING_AS_OF = "2026-10-03"


def price(model: str, prompt_tokens: int, completion_tokens: int,
          cached_prompt_tokens: int = 0, cache_write_tokens: int = 0) -> float:
    """USD cost of one call. Unknown models cost 0 and are flagged by the caller.

    `prompt_tokens` is the provider's total, which includes cached and newly written
    tokens: cached ones are billed at the cheap read rate, written ones at the write rate
    (1.25x), the rest at the normal input rate.
    """
    p = PRICING.get(model)
    if not p:
        return 0.0
    cached = min(max(cached_prompt_tokens, 0), prompt_tokens)
    written = min(max(cache_write_tokens, 0), prompt_tokens - cached)
    return ((prompt_tokens - cached - written) * p["input"]
            + cached * p.get("cached_input", p["input"])
            + written * p.get("cache_write", p["input"])
            + completion_tokens * p["output"]) / 1e6
