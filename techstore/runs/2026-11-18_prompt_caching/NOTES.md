# Technique 10: provider prompt caching (2026-11-18)

OpenAI can reuse the beginning of a prompt it saw recently and bill it far cheaper. Built
and simulated without OpenAI credit; **the real behaviour in our API must be confirmed
with real calls** (`runs/PENDING_CREDITS.md`, rows 7–8).

## The official rules (developers.openai.com/api/docs/guides/prompt-caching, read 2026-11-18)

For GPT-5.6 and later, including GPT-6.x:
- Only prompts of **1,024+ tokens** are cached, and only by **exact prefix** from the first token.
- **Writing** new tokens into the cache costs **1.25×** the input price (30-minute cache;
  a 12-hour cache costs 2.5×, Responses API only).
- **Reading** cached tokens costs **0.05×** for GPT-6.1 Sol and **0.1×** for other models
  (our `cached_input` prices: $0.10 for Sol, $0.01 for Luna).
- Caching is on by default. With explicit mode and no breakpoints, nothing is cached or written.
- Summarising, compacting or truncating earlier turns resets reuse.
- **Not documented:** whether the Chat Completions API (which we use) behaves the same, its
  usage field names, and whether a write is billed when it is never reused.

## What was built

- **Honest billing:** `config.price()` and the Langfuse cost split now bill cached reads at the
  read rate and cache writes at 1.25×, reading `cached_tokens` / `cache_write_tokens` from either
  `prompt_tokens_details` (Chat Completions) or `input_tokens_details` (Responses).
- **Cache-friendly layout** (`--layout cache`): fixed instructions first, the conversation
  exactly as sent, and this turn's documents with the question at the end. Each turn's prompt
  then starts with the previous turn's prompt. Not combinable with memory trimming yet
  (trimming rewrites earlier turns, which resets reuse).
- **Simulator** (`prompt_cache_sim.py`): replays chats through the agent, captures the exact
  prompts, and prices them under the rules above, both if writes are billed and if they are free.

## Simulated results (Sol, input side only; output identical across setups)

**8 dev chats, 4–6 turns** (`data/conversations_dev.jsonl`):

| Setup | Input tokens | Writes billed | Writes free |
|---|---|---|---|
| classic (current) | 34,327 | **+10%** | 0% |
| classic + facts memory | 32,713 | +1% | −5% |
| cache layout | 63,356 | +1% | −15% |

**3 long chats, 13–14 turns** (dev chats joined end to end):

| Setup | Input tokens | Writes billed | Writes free |
|---|---|---|---|
| classic (current) | 59,970 | **+22%** | 0% |
| classic + facts memory | 42,435 | −22% | −29% |
| **cache layout** | 176,581 | **−31%** | **−42%** |

## What it means

1. **Single questions are unaffected:** our prompts are ~600–900 tokens, under the 1,024 minimum.
   That's why the October baseline showed 0 cached tokens.
2. **A real risk:** if writes are billed by default, long chats in the classic layout pay up to
   +22% for cache writes that are never reused (the documents near the top change every turn).
   Tokenomics should control caching (explicit mode, write only where reuse is likely) rather
   than leave it to chance.
3. **Techniques interact.** The cache layout triples tokens but cuts cost most on long chats;
   memory trimming cuts tokens but blocks cache reuse. Short chats → trim; long chats → cache
   layout (if writes are billed). A later refinement: trim only every N turns ("compaction"),
   so the prefix stays stable between trims.
4. **Tokens vs cost again:** the cache layout sends ~3× more tokens and costs 31–42% less.
   Cost is the headline measure; tokens alone would call this a failure.
5. **Quality unknown:** the cache layout moves documents from the instructions message into the
   user's message. Needs a real-run quality check.
