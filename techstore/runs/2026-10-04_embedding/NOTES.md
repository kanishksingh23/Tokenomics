# Switching the default search to embeddings (2026-10-04)

On 14 newly written questions (now q051–q064 in the dev set) the right document was
found by keyword search 8/14, hybrid 12/14, embedding 14/14. On the 50 seed
questions, where document tags had been fitted to the exact wording, keyword had
looked best. Embeddings became the default.

`embedding_check_8.jsonl`: real answers (gpt-6.1-sol, embedding search) for the 4
questions where embeddings find FEWER needed documents than keyword (q008, q026,
q036, q038) and 4 where they find more (q052, q056, q057, q061). Cost $0.0253.

| Result | Questions |
|:---|:---|
| Improved: now answered correctly | q052, q056, q057, q061 |
| Lost a "needed" document but still answered fully and correctly | q008, q026, q038 |
| **Worse**: lost Standard Warranty Terms, could not explain the warranty | **q036** |

For q036 the warranty document ranks 4th (0.481) just behind 3rd (0.487).
Retrieving 4 documents instead of 3 raises dev-set recall from 83.3% to 87.5% for
about 7% more cost per question. Decision pending.

**Decision (same day): 4 documents per question.** Re-run of q036 with top_k=4: the
warranty document is retrieved and the answer explains that warranty is independent
of the return window. Cost $0.0036.
