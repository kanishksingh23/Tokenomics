# Credit checks: the tests that waited for OpenAI credit (2026-11-25)

New OpenAI key (…dlkA). `check_setup.py --ping` passed. Rows 1–4 and 6–9 of
`../PENDING_CREDITS.md` were run today; row 5 (response cache on repeat traffic) still needs Rahul's
repeat-traffic set. **Total spend ≈ $1.50** (runs $1.34, caching probe $0.006, one-off checks
$0.005, combination runs ≈ $0.13).

Baseline for the 64-question runs: `../2026-10-15_shortprompt/sol_short.jsonl` and `luna_short.jsonl`
with their graded `*.check.csv`. Quality: `quality_check.py` (answers unchanged in type, numbers
and meaning inherit the baseline grade; changed answers graded by an AI grader: Claude helper
agents, no access to earlier grades; **drafts, not human-confirmed**). Files per run: `<run>.jsonl`
(answers), `<run>.check.csv` (verdict per question), `<run>.judge.md` / `.judge.csv` (graded
changed answers). Script: `run_batches.sh`, `run_chats.sh`, `summarize.py`.

**Reproducing after this commit:** these runs used the *old* defaults. Since 2026-11-25
`verbosity=low`, adaptive context 0.25 and (for `--conversations` with memory off) the cache
layout are defaults, so to reproduce a reference run add `--verbosity off --context-margin off`
(and `--layout classic` for the chat runs).

## #7 How prompt caching behaves in Chat Completions (`probe_caching.py`, `caching_probe.json`)

One 1,491-token prompt sent three times to Sol:

| Call | cached_tokens | cache_write_tokens | Cost |
|---|---|---|---|
| 1 (new prompt) | 0 | 1,488 | $0.004376 |
| 2 (same prompt) | 1,488 | 0 | $0.000795 (−82%) |
| 3 (same prefix, new question) | 1,480 | 10 | $0.000929 |

- **Caching is on by default** in Chat Completions; no setting needed.
- Usage reports both `prompt_tokens_details.cached_tokens` and `cache_write_tokens` (our code reads both).
- Writes are reported, so **"writes billed" is the realistic simulator column**. The 1.25× write
  price is from OpenAI's docs; only the usage dashboard can confirm the bill itself.
- A new question on a cached prefix writes only its new tokens (call 3).

## #1 Does GPT-6 accept `verbosity`? Yes, both models.

One question, Sol: output 106 → 84 tokens with `verbosity=low`, still complete and correct.
Measured properly below (#3).

## #2 Run-to-run variation (the noise floor)

Same settings as the 15 Oct short-prompt run, nothing changed:

| Model | "Changed" answers by chance alone | Final verdicts | Cost / 64 q |
|---|---|---|---|
| Sol | **19 / 64 (30%)** | 64 correct (= baseline) | $0.1479 (Oct: $0.1485) |
| Luna | **29 / 64 (45%)** | 61 correct, 3 partial (Oct: 62 / 2) | $0.0096 (same) |

**How to read every other result:** about 30% of Sol's answers and 45% of Luna's change wording or
numbers between identical runs (GPT-6 rejects `temperature`). A difference of ±1 correct answer
is noise. Cost per 64 questions is stable to within ~0.5%. So cost results are below compared with
**today's rerun**, the fairest same-day reference.

## #3, #4, #9 Single-question techniques (64 dev questions)

| Run | Input | Output | Thinking | Cost / 64 q | vs rerun | Verdicts | Cost per correct |
|---|---|---|---|---|---|---|---|
| **Sol rerun** (reference) | 724 | 83.5 | 3.5 | $0.1479 | — | 64 correct | $0.002312 |
| Sol concise rule (#3) | 779 | 71.2 | 1.2 | $0.1472 | −0.5% | 64 correct | $0.002300 |
| Sol `verbosity=low` (#3) | 724 | 70.8 | 2.5 | $0.1398 | **−5.5%** | 64 correct | $0.002185 |
| Sol reasoning effort low (#4) | 724 | 82.2 | 0.0 | $0.1472 | −0.5% | 64 correct | $0.002299 |
| Sol adaptive context 0.25 (#9) | 665 | 80.4 | 1.5 | $0.1295 | **−12.4%** | 64 correct | $0.002024 |
| Sol `verbosity=low` + adaptive | 665 | 72.1 | 4.1 | $0.1242 | **−16.0%** | 64 correct | **$0.001940** |
| **Luna rerun** (reference) | 724 | 153.6 | 89.0 | $0.0096 | — | 61 correct, 3 partial | $0.000158 |
| Luna concise rule | 779 | 151.8 | 93.5 | $0.0099 | +3% | 61 / 3 | $0.000163 |
| Luna `verbosity=low` | 724 | 144.2 | 83.4 | $0.0093 | −3% | 61 / 3 | $0.000153 |
| Luna adaptive context 0.25 | 665 | 143.6 | 81.2 | $0.0085 | −11% | 60 / 4 | $0.000142 |
| Luna `verbosity=low` + adaptive | 665 | 142.8 | 82.8 | $0.0085 | −11% | 62 correct, 2 partial | **$0.000137** |

No answer was wrong, hallucinated or cut off in any run.

**Decisions.**
- **Adaptive context (#9): adopt** for both models. −12% cost, quality unchanged (Sol 64/64;
  Luna 60 vs 61 correct is within the noise floor). The few needed documents it drops (q020's
  PulseBook 14 page) were covered by the catalogue line. (It also produced 58 cached tokens per
  question on average, a side effect of shorter, more uniform prompts.)
- **Answer length (#3): use `verbosity=low`, drop the concise rule.** The rule cuts Sol's output
  by 15% but adds 55 input tokens, so it saves nothing (−0.5%). `verbosity=low` cuts output just
  as much with no extra input: −5.5% on Sol, 64/64 correct. On Luna, output is mostly hidden
  thinking, so neither helps much (−3%).
- **Sol reasoning effort low (#4): not worth it.** Sol thinks only ~3 tokens per question; −0.5%.
- **Together:** `verbosity=low` + adaptive context cut Sol's cost **16%**, about the product of
  the two (0.945 × 0.876 = 0.83).

## #6 Conversation memory quality (8 dev chats, 36 turns, Sol)

| Mode | Answer cost | Memory calls | Total | vs off | Graded turns (12 where trimming acted): correct / partial |
|---|---|---|---|---|---|
| off | $0.0987 | — | $0.0987 | — | 9 / 3 |
| window | $0.0949 | — | $0.0949 | −4% | 8 / 4 |
| facts | $0.0998 | — | $0.0998 | +1% | 9 / 3 |
| summary | $0.0944 | $0.0006 | $0.0950 | −4% | 10 / 2 |

- **No context was lost** by trimming. Every mode resolved "it" / "that order" to the right
  order or product on every turn. One `window` partial (c02 t4) may be a trimming side effect,
  low confidence.
- **No saving on short chats** (4–6 turns): trimming starts at turn 4, and `off` keeps a stable
  prefix that provider caching reuses (105 cached tokens per turn vs 29 for `facts`). The saving
  shows on long chats (−24% at 10 turns, −46% at 20, simulated 2026-11-18).
- **A different quality problem found (all modes, `off` included):** when a turn's documents
  don't include a policy the agent cited earlier, it **takes back its own correct earlier answer**
  ("I'm sorry, I don't have information about the 30-day window"). c03 t4, c06 t4, c07 t4. Cause:
  in the classic layout only the current turn's documents are shown, and the prompt says to answer
  only from them. See #8: the cache layout fixes it.
- First grading pass used a pack missing the customer's message per turn (formatting bug, caught
  by the grader); re-graded with the fixed pack. The first pass is kept as `memory.judge.v1_noquestion.csv`.

## #8 Cache layout vs classic, real (2 long chats, 13 turns each, Sol, `long_chats.jsonl`)

| Input side | Simulated (`prompt_cache_sim.py`) | Real |
|---|---|---|
| Classic: cached / written tokens | 0 / 36,366 | 2,748 / 32,369 |
| Classic: input cost vs no caching | +22% | **+14%** |
| Cache layout: cached / written tokens | 104,803 / 18,548 | 106,124 / 18,623 |
| Cache layout: input cost | $0.0602 | **$0.0605** |

| Layout | Total cost (26 turns) | Quality (26 turns) |
|---|---|---|
| classic | $0.1162 | 23 correct, 3 partial |
| **cache** | **$0.0854 (−26.5%)** | **26 correct** |

- **The simulator is validated:** within 1% on the cache layout.
- **Default caching costs money in the classic layout:** +14% input cost from writes never reused.
- **The cache layout is cheaper and better:** its 3 fewer partials are exactly the take-back
  problem above. Earlier turns' documents stay in the conversation, so the agent never disowns
  what it said. **Recommendation: cache layout as the default for multi-turn chats.** Open:
  it cannot yet be combined with memory trimming (trimming rewrites the prefix); for very long
  chats, trim only every N turns ("compaction").

## For humans (optional, at the end)

Not-confident AI grades: q017, q020, q029, q035, q036, q049, q052 (Luna runs), q029, q035, q036 (Sol).
All `*.check.csv` rows with `needs_human = yes`.
