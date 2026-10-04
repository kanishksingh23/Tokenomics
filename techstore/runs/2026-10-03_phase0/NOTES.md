# Phase 0 — first runs against the real model (2026-10-03)

Model: gpt-6.1-sol (rejects temperature, so answers vary between runs). Retriever: keyword.

| File | What | Code |
|:---|:---|:---|
| `baseline_50.jsonl` | All 50 seed questions. The Phase 0 baseline: $0.1104, 0 hallucinations, 10/10 out-of-scope | commit b6fa1a1 |
| `rerun_17_after_fixes.jsonl` | 12 questions targeted by the fixes + 5 unchanged controls | this commit |
| `date_check_5.jsonl` | q006 three times, q008, q009 — after the explicit date rule | this commit |

## Grades for `baseline_50.jsonl`

| File | Who | Result |
|:---|:---|:---|
| `grades_human.csv` | Rahul (46 questions), Kanishk (4: q026, q031, q032, q033) | 42 correct · 8 partial · 0 wrong · 0 hallucinated |
| `grades_claude_provisional.csv` | Claude — not independent: it wrote the knowledge base and questions | 44 correct · 6 partial · 0 wrong · 0 hallucinated |

Agreement, humans vs Claude: 44/50 = 88%, Cohen's kappa 0.50. Grading was done in
`baseline_50.grading.html` (open it in a browser), built by `grading_view.py`.
The grading rubric was tightened afterwards; see the spec, section 7, Grading Rubric.

Re-grade any file with:

    python review_results.py runs/2026-10-03_phase0/baseline_50.jsonl --sheet my_review.csv
