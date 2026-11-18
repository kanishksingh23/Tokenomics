# Technique 7: safe response cache (2026-11-18)

Reuses a model's earlier answer when the same question (or one with the same meaning) comes
again: zero tokens, zero cost, a few milliseconds. Built and tested without OpenAI credit.

**Status: built and safety-tested.** Off by default in experiment runs (`--cache` turns it on)
so repeated runs always call the model; the gateway will switch it on.

## How it decides

1. **Exact tier:** same question after trimming case, spaces and end punctuation, *and* the same
   entities.
2. **Semantic tier:** MiniLM similarity ≥ **0.88**, plus all the safety checks.

| Safety check | Stops |
|---|---|
| Namespace (app instructions, knowledge-base version, model, settings) in the key | Reuse after the documents, prompt or settings change |
| Same entities (numbers, amounts, dates, emails, product names) | Order-number, amount and product swaps |
| Meaning flips: negations (not, can't, without) and opposite pairs (enable/disable, on/off, before/after, credit/debit, ...) | "How do I turn **on** ..." answered with "turn **off**" |
| Length ratio ≤ 3.5, length ≤ 150 words | Truncation collisions in the embedding |
| Never cache personal or time-varying questions (order numbers, "my order", "today", "in stock", ...) or any answer built from a customer's order records | One customer's data reaching another; stale answers |

## Safety suite: `data/cache_pairs.jsonl`, 75 pairs

45 dangerous look-alikes (6 order/personal, 6 amount/date, 11 negation/antonym, 6 product
swap, 13 different intent, 3 time-varying) and 30 true rephrasings.

| Threshold | Dangerous pairs blocked | Rephrasings reused |
|---|---|---|
| 0.86 | 45/45 | 30/30 |
| **0.88 (chosen)** | **45/45** | **27/30** |
| 0.90 | 45/45 | 24/30 |
| 0.92 | 45/45 | 23/30 |

The most similar dangerous pair that only the threshold can stop ("Do you sell gaming
consoles?" / "...gaming laptops?") scores **0.79**; the least similar true rephrasing scores
**0.86**. 0.88 keeps a margin from the danger side. **CI runs this suite with the real model
on every push and fails on any false hit.**

Bugs the tests caught while building: (1) the meaning-flip check worked in only one direction
("on → off" blocked, "off → on" not); (2) the exact tier ignored entities known from outside
the text. Both fixed, both covered by tests.

## Saving on our questions: 0, and why

Replaying the 64 dev questions with Sol's real answers: **0 reused**, 11 never cacheable
(personal). Our question sets contain no repeats by design: related dev questions
("How long do I have to return something?" / "What's the last day I can send an item back?")
score only 0.33–0.64, and several need different answers ("payment methods" vs "Paytm wallet").
The cache's saving equals the **repeat rate of real traffic**, which our sets can't show.
The spec plans about 8%; real support traffic often repeats far more.

**To measure it fairly:** a small "repeat traffic" set, e.g. 2–3 rephrasings of about 12 of the
test questions, written by Rahul (not by whoever tuned the threshold), run through the cache
with real model answers. Logged in `runs/PENDING_CREDITS.md`.
