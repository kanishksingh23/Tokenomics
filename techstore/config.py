"""Configuration for the TechStore support agent (Phase 0)."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
KB_PATH = DATA_DIR / "knowledge_base.jsonl"
ORDERS_PATH = DATA_DIR / "orders.jsonl"
SYSTEM_PROMPT_PATH = BASE_DIR / "system_prompt.txt"

API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# NOTE: verify these exact strings against your provider's model list before the
# Week 10 benchmark. Pricing below is $ per 1M tokens, as of 2026-09.
FRONTIER_MODEL = os.getenv("FRONTIER_MODEL", "gpt-5.6-sol")
ECONOMY_MODEL = os.getenv("ECONOMY_MODEL", "gpt-5.6-luna")

# $ per 1M tokens. cached_input applies to prompt tokens the provider served
# from its own prompt cache (billed at 10% of input). Unverified against the
# provider's live pricing page -- check before the benchmark.
PRICING = {
    "gpt-5.6-sol":  {"input": 4.00,  "cached_input": 0.40, "output": 20.00},
    "gpt-5.6-luna": {"input": 0.20,  "cached_input": 0.02, "output": 1.20},
    "gpt-6-astra":  {"input": 10.00, "cached_input": 1.00, "output": 50.00},
}
PRICING_AS_OF = "2026-09-23"

# keyword measured 81.8% context recall@3 vs 76.4% for embeddings on the labelled
# seed set (see eval_retrieval.py). Re-evaluate on the full 500 questions.
RETRIEVER = os.getenv("RETRIEVER", "keyword")   # keyword | embedding | auto
TOP_K = int(os.getenv("TOP_K", "3"))
MAX_TOKENS = 600

# Fixed refusal wordings. system_prompt.txt instructs the model to use these
# verbatim, and review_results.py detects them; a test keeps the two in sync.
REFUSAL_UNKNOWN = "I don't have that information. I can connect you with a human agent who can help."
REFUSAL_OFF_TOPIC = "I can only help with TechStore orders, products, and support."

# Mock mode cannot know how long a real answer is, so it assumes this many
# output tokens (the section 2 planning figure). Output costs 5x input on Sol,
# so this assumption dominates the estimate.
MOCK_OUTPUT_TOKENS = 150
TEMPERATURE = 0.0


def price(model: str, prompt_tokens: int, completion_tokens: int,
          cached_prompt_tokens: int = 0) -> float:
    """USD cost of one call. Unknown models cost 0 and are flagged by the caller.

    `prompt_tokens` is the provider's total, which includes any cached tokens;
    those are billed at the cached rate instead of the full input rate.
    """
    p = PRICING.get(model)
    if not p:
        return 0.0
    cached = min(max(cached_prompt_tokens, 0), prompt_tokens)
    return ((prompt_tokens - cached) * p["input"]
            + cached * p.get("cached_input", p["input"])
            + completion_tokens * p["output"]) / 1e6
