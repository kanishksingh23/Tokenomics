# Technique 8: FAQ shortcut (2026-11-17)

Common questions are answered from **human-approved** answers in `data/faq.jsonl`, with no
model call: zero tokens, zero cost, about 8 ms instead of about 3 s. No OpenAI credit needed.

**Status: built; 22 answers drafted, none approved yet.** Until a person approves an answer
(`python faq_shortcut.py --review`, then `--approve`), the shortcut serves nothing.

## How a question qualifies (all must hold)

1. Meaning close to one FAQ: MiniLM similarity ≥ **0.75** (closest of the FAQ's question and examples).
2. Clearly closer to that FAQ than to any other (gap ≥ 0.05).
3. No digits: order numbers and amounts need a personal answer.
4. A single question.
5. Doesn't name a product (it may need that product's page).

## Calibration on the 64 dev questions (drafts included, measuring only)

| Similarity threshold | Served | Right FAQ | Wrong FAQ |
|---|---|---|---|
| 0.60 (gap 0.05) | 7 | 6 | 1 (q064 → tracking; it was about changing the address) |
| 0.65 (gap 0.05) | 7 | 6 | 1 |
| 0.70 | 6 | 6 | 0, but q001 sat at 0.70 pointing at the *wrong* FAQ (refund time) |
| **0.75 (chosen)** | **3** | **3** | **0** |

A wrong saved answer reaches a customer unchecked; a missed match only costs a normal model
call. So the threshold is set on the safe side.

Served at 0.75: q002 "Is delivery free?" (0.78), q003 payment methods (0.99), q004 "Do you ship
outside India?" (0.82). Missed but fine: q005, q051, q053, q059 (scores 0.63–0.75); the model
answers them as usual.

**Saving on this set**, using the real measured costs of the Sol short-prompt run: 1,994 of
51,915 tokens (**−3.8%**) and \$0.0052 of \$0.1485 (**−3.5%**). The dev set is deliberately
weighted towards hard questions (only 12 of 64 are simple FAQs); real support traffic has many
more, so this understates real-world savings. Rahul's 36 fresh questions give the fair figure.

## Known limits

- MiniLM's sense of "same meaning" is rough: "Do you sell washing machines?" scored closer to
  "Do you have a physical store?" (0.48) than to "What products do you sell?". The safety gates
  and the high threshold are what keep this safe.
- Coverage grows by adding example phrasings, ideally real customer wordings taken from
  Langfuse traces, each approved by a person.

## Update 2026-11-26: a gap found while reviewing the approvals (PR #1)

With all 22 answers approved, "you dropped the price after I ordered, will you refund the price
difference?" was served the **price-match** answer (0.81), which is about competitors' prices;
TechStore's own price drops follow a different rule (`bill_price_drop`). The matcher only
compared questions with approved answers, so a topic without an approved answer fell to its
nearest approved neighbour. Two fixes:

1. **Unapproved answers now count when matching, but are never served.** A question closest to
   an answer that isn't approved yet gets no saved answer and goes to the model.
2. **New draft answer `faq_price_drop`** (source `bill_price_drop`), waiting for Rahul's approval.

Dev-set evaluation unchanged (3/64 served, 0 wrong). Tests now build agents with the FAQ
shortcut off (`tests/conftest.py`): with approved answers, questions like "Is delivery free?"
were answered without a model request, which broke four tests on machines with the embedding
model. CI did not notice because it does not install that model.
