# Category questions — catalogue check (2026-10-04)

Model: gpt-6.1-sol. After adding the product catalogue (`catalogue_summary`),
which is included when a question names a product category and asks to compare,
choose or buy.

| Question | Before (baseline_50) | After |
|:---|:---|:---|
| q019 "Which of your headphones is lighter…" | Could not compare: X200 page not retrieved | X200 250 g vs Y500 268 g, correct |
| q020 "A tablet and a laptop under 1 lakh" | No laptop page retrieved; laptop half handed to a human | Full recommendation; all totals verified (₹82,998 / ₹94,998 / ₹99,997) |
| q021 "My headphones will not pair" (control) | — | Unchanged; catalogue correctly not included |

Cost: $0.0144.
