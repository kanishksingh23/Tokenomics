"""Configuration for the TechStore support agent (Phase 0)."""
import os
from pathlib import Path

try:
    from tokenomics.pricing import PRICING, PRICING_AS_OF, price  # noqa: F401  (re-exported)
except ImportError as exc:      # the package lives at the repo root since 2026-11-18
    raise ImportError(
        "The Tokenomics package isn't installed. Run this once from the repo root:\n"
        "    pip install -e \".[gateway,embeddings]\"\n"
        "(or `pip install -e ..` from inside techstore/), then try again.") from exc

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
KB_PATH = DATA_DIR / "knowledge_base.jsonl"
ORDERS_PATH = DATA_DIR / "orders.jsonl"
# system_prompt.txt is the short version since 2026-11-17 (same rules, 436 -> 283 tokens; no quality
# loss on the 64 dev questions). The original is kept as system_prompt_original.txt.
SYSTEM_PROMPT_PATH = BASE_DIR / os.getenv("SYSTEM_PROMPT", "system_prompt.txt")

# Two question sets that must never mix. DEV is for finding problems and tuning
# anything (prompt, documents, search, thresholds). TEST is written once, frozen
# (see TEST_LOCK_PATH) and used only for final claims: results on questions the
# system was tuned on overstate how it does on new ones.
DEV_QUESTIONS_PATH = DATA_DIR / "questions_dev.jsonl"
TEST_QUESTIONS_PATH = DATA_DIR / "questions_test.jsonl"
TEST_LOCK_PATH = DATA_DIR / "questions_test.sha256"
# Variants of 12 test questions for measuring the answer cache (WRITING_TEST_QUESTIONS.md):
# "same" = same answer in other words, "different" = look-alike needing another answer.
REPEAT_QUESTIONS_PATH = DATA_DIR / "questions_repeat.jsonl"

API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
# Through the Tokenomics gateway: OPENAI_BASE_URL=http://localhost:8000/v1 and a Tokenomics key
# ("tk-..."). The gateway then runs the cache and spending limits, so the agent doesn't.
VIA_GATEWAY = API_KEY.startswith("tk-")

# NOTE: verify these exact strings against your provider's model list before the
# Week 10 benchmark. Pricing below is $ per 1M tokens, as of 2026-09.
FRONTIER_MODEL = os.getenv("FRONTIER_MODEL", "gpt-6.1-sol")
ECONOMY_MODEL = os.getenv("ECONOMY_MODEL", "gpt-6-luna")
# Technique 14, model routing (tokenomics/routing.py): with model "auto", answer with the
# economy model first and escalate to the frontier model only when the answer looks weak.
ROUTING_THRESHOLD = float(os.getenv("ROUTING_THRESHOLD", "0.5"))

# Prices and the cost formula belong to the product (tokenomics/pricing.py).

# Embeddings: on 14 questions the system had never seen, embedding search found the
# right document 14/14 and keyword search 8/14. Keyword had looked better on the
# 50 seed questions only because document tags had been fitted to their wording.
# Re-check on the frozen test set.
RETRIEVER = os.getenv("RETRIEVER", "embedding")   # embedding | keyword | auto
# 4 documents per question. With 3, a needed document ranked 4th by a hair was
# cut (q036: Standard Warranty Terms 0.481 vs 0.487). Dev-set recall 83.3% -> 87.5%
# for ~7% more cost per question, paid equally by every arm of the benchmark.
TOP_K = int(os.getenv("TOP_K", "4"))

# Technique 8, the FAQ shortcut (faq_shortcut.py). Only human-approved answers in
# data/faq.jsonl are ever served. 0.75 gave 0 wrong matches on the dev set with a safety
# margin; at 0.70 one question sat on the edge of the wrong FAQ.
FAQ_SHORTCUT = os.getenv("FAQ_SHORTCUT", "on").strip().lower() != "off"
FAQ_THRESHOLD = float(os.getenv("FAQ_THRESHOLD", "0.75"))

# Technique 7, the safe response cache (response_cache.py). OFF by default here: experiment
# runs must call the model every time, or a repeated run would just replay saved answers.
# The gateway will switch it on. 0.88 sits between the most similar dangerous pair in the
# safety suite (0.79) and the least similar true paraphrase (0.86).
RESPONSE_CACHE = os.getenv("RESPONSE_CACHE", "off").strip().lower() == "on"
CACHE_THRESHOLD = float(os.getenv("CACHE_THRESHOLD", "0.88"))
CACHE_TTL_HOURS = float(os.getenv("CACHE_TTL_HOURS", "24"))

# Technique 9, conversation memory (techniques.py): off | window | facts | summary.
# Keeps the last MEMORY_KEEP_TURNS exchanges word for word and shrinks everything older.
MEMORY_MODE = os.getenv("MEMORY_MODE", "off").strip().lower() or "off"
MEMORY_KEEP_TURNS = int(os.getenv("MEMORY_KEEP_TURNS", "2"))

# Technique 10, prompt layout for provider caching. "classic": documents inside the first
# (system) message. "cache": fixed instructions first, then the conversation exactly as sent,
# then this turn's documents with the question, so each turn's prompt starts with the
# previous turn's prompt and OpenAI's prefix cache can reuse it.
PROMPT_LAYOUT = os.getenv("PROMPT_LAYOUT", "classic").strip().lower() or "classic"
# Layout for multi-turn chats (CLI --conversations, the demo) when memory is "off". Default
# "cache" since 2026-11-25: on 2 real 13-turn chats it cost 26.5% less than classic and got
# 26/26 turns right vs 23/26 (classic made the agent take back its own earlier answers).
# Single questions keep PROMPT_LAYOUT (classic), the setting all 64-question results used.
CHAT_LAYOUT = os.getenv("CHAT_LAYOUT", "cache").strip().lower() or "cache"

# Technique 5, adaptive context: instead of always sending TOP_K documents, keep only those
# whose search score is within CONTEXT_MARGIN of the best one (at least 1, at most TOP_K).
# Default 0.25 since 2026-11-25 (real runs: Sol -12.4% cost, 64/64 correct). "off" = always
# TOP_K. Scores are cosine similarities, so the default applies only to the embedding
# retriever; keyword (BM25) scores are on another scale.
_margin = os.getenv("CONTEXT_MARGIN", "0.25").strip().lower()
CONTEXT_MARGIN = None if _margin in ("", "off", "none") else float(_margin)

# Technique 4, smaller context: inside each document, keep only sentences (catalogue: product
# lines) whose similarity to the question is within PASSAGE_MARGIN of the document's best
# sentence; the first sentence always stays. Empty = off (whole documents).
PASSAGE_MARGIN = float(os.getenv("PASSAGE_MARGIN")) if os.getenv("PASSAGE_MARGIN") else None

# Technique 12, spending limits (spending_limits.py), checked BEFORE each model call.
# The app-wide daily cap is the runaway-loop guard and applies to everything, scripts too;
# per-client limits apply when a client is known (each demo visitor, later each API key).
SPEND_LIMITS = os.getenv("SPEND_LIMITS", "on").strip().lower() != "off"
GLOBAL_DAILY_BUDGET_USD = float(os.getenv("GLOBAL_DAILY_BUDGET_USD", "5.00"))
CLIENT_DAILY_BUDGET_USD = float(os.getenv("CLIENT_DAILY_BUDGET_USD", "0.05"))   # ~20 Sol answers
SOFT_LIMIT_RATIO = float(os.getenv("SOFT_LIMIT_RATIO", "0.8"))    # past this: cheap model
CLIENT_RPM = float(os.getenv("CLIENT_RPM", "20"))                  # requests per minute
EXPECTED_OUTPUT_TOKENS = int(os.getenv("EXPECTED_OUTPUT_TOKENS", "200"))  # for the estimate
# Upper bound on output tokens, including any hidden reasoning tokens. Reasoning
# models can spend hundreds of tokens thinking before writing; a low cap yields an
# EMPTY answer that is still billed. You pay only for tokens actually produced,
# so a generous cap costs nothing extra (worst case: 2000 x $10/1M = $0.02).
MAX_TOKENS = 2000

# The store's "today". Fixed so answers do not change with the real calendar:
# the model knows the real date, and against frozen order records a later run
# would see every delivery as overdue. validate_data.py checks the fixtures
# agree with it (nothing happened after today; nothing due is already past).
SIMULATED_TODAY = "2026-09-30"

# Fixed refusal wordings. system_prompt.txt instructs the model to use these
# verbatim, and review_results.py detects them; a test keeps the two in sync.
REFUSAL_UNKNOWN = "I don't have that information. I can connect you with a human agent who can help."
REFUSAL_OFF_TOPIC = "I can only help with TechStore orders, products, and support."
# Opening of the one sentence used when only PART of a question can be answered.
REFUSAL_PARTIAL = "I don't have information about"

# Mock mode cannot know how long a real answer is, so it assumes this many
# output tokens (the section 2 planning figure). Output costs 5x input on Sol,
# so this assumption dominates the estimate.
MOCK_OUTPUT_TOKENS = 93   # calibrated: mean billed output over the 50-question real run, 2026-10-03
TEMPERATURE = 0.0

# How much hidden "thinking" the model does before answering (billed as output).
# Empty = the model's default. GPT-6 Luna accepts none/low/medium/high; Sol accepts
# low/medium/high (checked 2026-10-15). Luna's default spent 84 tokens per question.
REASONING_EFFORT = os.getenv("REASONING_EFFORT", "").strip() or None

# Answer-length control (techniques.py). "concise" adds a short-answer rule to the system
# message; VERBOSITY sends the provider's own length setting (low/medium/high).
# VERBOSITY default "low" since 2026-11-25 (real runs: Sol -5.5% cost, 64/64 correct; the
# concise rule saved nothing because it adds input). "off" = don't send it.
ANSWER_LENGTH = os.getenv("ANSWER_LENGTH", "default").strip() or "default"
_verbosity = os.getenv("VERBOSITY", "low").strip().lower()
VERBOSITY = None if _verbosity in ("", "off", "none", "default") else _verbosity
