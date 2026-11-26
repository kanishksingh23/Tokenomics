# Technique 14: model routing (2026-11-26)

Built in mock mode and evaluated **for free** on real answers we already had: every dev
question was answered by both Sol and Luna in the 2026-10-15 and 2026-11-25 runs, and every
answer is graded. No new API calls were made. A live check is in `../PENDING_CREDITS.md` (row 10).

## What the data said first

Luna (20× cheaper than Sol) was **never wrong** on the 64 dev questions: across 7 graded runs
it got 57–62 correct and the rest partial, including the billing and API questions the plan
expected to need Sol. Its partials had three patterns:

| Pattern | Example | Visible in the answer? |
|---|---|---|
| Refusal line before a real answer | q053 "I can only help with TechStore… Paytm wallet payments aren't accepted" | ✅ yes |
| "I don't have information about…" although the documents had it | q035, q052 | ⚠ yes, but the prompt also tells the model to say this when something *is* missing |
| An option left out of a comparison | q020 | ❌ no |

So the plan's trained neural classifier has nothing to learn here (2–7 weak answers in 64), and
the design that fits the evidence is **cheap-first**: Luna answers, simple checks look at the
answer, and Sol is asked once only if it looks weak.

## What was built

- `tokenomics/routing.py` (generic, used by TechStore and the gateway):
  - **choose**: economy unless a hard rule says frontier: code in the question, a question over
    250 tokens, tools / strict JSON schema, or a chat that escalated in the last 3 turns
    ("sticky"). A concrete model name is always honoured; only `model="auto"` is routed.
  - **check**: signals with strengths, combined as independent evidence
    (U = 1 − Π(1 − sᵢ), escalate at U ≥ 0.5): refusal line followed by a real answer (0.8),
    generic hedges (0.35 each: "not sure", "might be", "I think"), too short for a "compare /
    explain / why" question (0.6), repetition, unfinished text (0.4), missing-info phrase (0.3).
  - **guards** (no escalation): answer cut off by the length limit (Sol would be too); a plain
    decline or refusal (Sol would decline too); the spending limit would be crossed.
  - One escalation at most; both calls' cost, tokens and latency are added up.
- TechStore: `--model auto` (CLI), "auto" in the demo (shows the decision and the discarded
  cheap answer), `make_router()` with TechStore's fixed sentences.
- Gateway: `"model": "auto"`; optional `X-Tokenomics-Conversation` header for stickiness; the
  response's `tokenomics.route` says what happened.
- `routing_replay.py`: the five-arm comparison on real graded answers (below).

## Results: replay on 6 pairs of real runs (64 questions each)

Full table: `replay.txt`; per-question decisions: `replay_detail_combo.txt`. Current defaults (combo pair):

| Arm | Cost | vs always-Sol | Correct / partial / wrong | Cost per correct | Sent to Sol | p50 / p90 latency |
|---|---|---|---|---|---|---|
| always Sol | $0.1242 | — | 64 / 0 / 0 | $0.001940 | 64 | 2.50 / 3.78 s |
| always Luna | $0.0085 | −93% | 62 / 2 / 0 | $0.000137 | 0 | 1.88 / 3.03 s |
| **router** | **$0.0104** | **−92%** | **63 / 1 / 0** | **$0.000165** | 1 | 1.89 / 3.12 s |
| router, careful variant | $0.0370 | −70% | 64 / 0 / 0 | $0.000578 | 14 | 1.92 / 5.38 s |
| random, same # to Sol | $0.0104 | −92% | 62 / 2 / 0 | $0.000168 | 1 | 1.88 / 3.09 s |
| oracle (knows the grades) | $0.0113 | −91% | 64 / 0 / 0 | $0.000177 | 2 | 1.89 / 3.03 s |

Across all 6 pairs the router cost **−88% to −92%** vs always-Sol with **62–64 correct and 0
wrong**, sent 1–3 questions to Sol, and was correct as often as or more often than random
escalation (62–64 vs 60–62), close to the oracle.

**The "careful" variant** treats "I don't have information about" as a strong signal. It reaches
64/64 everywhere but escalates 13–17 questions, because the phrase is right far more often than
wrong (on the combo pair, 1 of 12 answers using it was actually partial). It costs ~3.5× more
for at most 1–2 extra correct answers, and its p90 latency rises to ~5.5 s. **Default: the
standard router**; the careful variant is one setting away (`missing_info_weight=0.6`).

## What this means

1. **Most of the saving comes from Luna being good enough**, not from clever routing: always-Luna
   is already −93%. The router is a cheap **safety net** (+1–2% cost) that repairs the weak
   answers it can see. On a harder question set the safety net matters more.
2. **Cheap-first is also faster** here: Luna's median is 1.9 s vs Sol's 2.5 s; escalated
   questions wait for both, but there are few.
3. **Caveat: these checks were designed while looking at the dev answers.** The fair number
   comes from Rahul's 36 fresh test questions, written before any router tuning.
4. Not built (from the original plan), and why: the trained neural classifier and calibration
   (too few weak answers to learn from), per-token log-probabilities (unknown for GPT-6
   reasoning models; the formula works without them), the learning loop (mentor decision
   pending), and a third, open-weight model on Groq (optional; needs a free key).
