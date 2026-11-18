# Techniques 4 and 5: how much context each question gets (2026-11-18)

Documents are 44% of every prompt (381 of 877 input tokens in the October baseline). Two ways
to send less, both measured for free on the 64 dev questions; real-run quality pending credit.

**How quality was judged without model calls:**
1. **Needed documents kept:** each dev question lists the documents it needs (`context_ids`).
2. **Facts kept:** Sol's October answers were graded 64/64 correct. Every number they quote
   that appears in the documents (207 numbers: prices, days, amounts) should still be there.
   This over-counts slightly: generic step numbers ("1", "2", "3") look like losses.

## Technique 5, adaptive context: candidate (margin 0.25)

Keep documents whose search score is within a margin of the best match (at least 1, at most 4);
named products and order records are always kept. `--context-margin 0.25`.

| Margin | Needed docs kept | Docs/question | Doc tokens | Numbers kept |
|---|---|---|---|---|
| off (always 4) | 87.5% | 4.03 | 381 | 207/207 |
| 0.30 | 87.5% | 3.69 | 348 | 96.6% |
| **0.25** | **87.5%** | **3.41** | **322 (−15%)** | 92.8% |
| 0.20 | 86.1% | 3.06 | 293 (−23%) | 92.8% |
| 0.10 | 83.3% | 2.36 | 232 (−39%) | — |

At 0.25 no needed document is lost (the 9 misses are the same as with 4 documents: existing
retrieval gaps). The numbers lost are mostly step numbers, plus a few extra details Sol borrowed
from documents the question didn't strictly need (e.g. "48 hours" in q052). Extra detail isn't
required by the rubric, so this likely doesn't hurt correctness. Saving: about −8% of input
tokens, −5% of Sol's cost per question. **Real-run check pending.**

## Technique 4, sentence-level trimming: rejected (kept in code, off)

Inside each document keep only sentences close to the question (first sentence always kept).
`--passage-margin`.

| Margin | Doc tokens | Numbers kept |
|---|---|---|
| off | 381 | 207/207 |
| 0.30 | 333 (−13%) | 184/207 (**−11%**) |
| 0.20 | 284 | 170/207 |
| 0.10 | 230 | 139/207 |

It cuts facts **out of the documents the question needs**: the Y500's price and specs in a
headphone comparison (q016), express delivery's ₹149 (q002). Our documents are short (94 tokens
on average), and the sentence that looks least like the question often holds the key number.
It may suit long documents; not ours.

**Also noticed:** 9 of 56 questions miss a needed document even with 4 documents (q008, q020,
q025, q026, q029, q032, q036, q037, q038). Improving search there would help quality more than
any trimming.
