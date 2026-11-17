# Token-saving step 1: short system prompt, and Luna with no reasoning (2026-10-15)

Same 64 dev questions and settings as `../2026-10-15_baseline/` (embedding retrieval, top_k 4).
Only the system prompt and the reasoning effort change.

- `system_prompt_short.txt` keeps every rule and all three exact refusal wordings; it only
  cuts phrasing: 436 → 283 tokens. **Since 2026-11-17 it is the default `system_prompt.txt`;**
  the original is `system_prompt_original.txt`. (The commands below use the old file name.)
  **New baseline** for later experiments: `sol_short.jsonl` with grades `sol_short.check.csv`.
- `reasoning_effort`: how much hidden thinking the model does. Checked 2026-10-15:
  Luna accepts none/low/medium/high (default behaves like medium); Sol accepts
  low/medium/high (no "none"). Neither accepts "minimal".

```
python cli.py --batch data/questions_dev.jsonl --out runs/2026-10-15_shortprompt/sol_short.jsonl  --model gpt-6.1-sol --system-prompt system_prompt_short.txt
python cli.py --batch data/questions_dev.jsonl --out runs/2026-10-15_shortprompt/luna_short.jsonl --model gpt-6-luna  --system-prompt system_prompt_short.txt
python cli.py --batch data/questions_dev.jsonl --out runs/2026-10-15_shortprompt/luna_short_effortnone.jsonl --model gpt-6-luna --system-prompt system_prompt_short.txt --reasoning-effort none
```

## Tokens and cost (per question, means)

| Run | Input | Output | of which thinking | **Total tokens** | Cost / 64 q |
|---|---|---|---|---|---|
| Sol baseline | 877 | 93.5 | 5.6 | 970 | $0.1721 |
| Sol short prompt | 724 | 87.2 | 5.6 | **811 (−16%)** | $0.1485 (−14%) |
| Luna baseline | 877 | 146.9 | 84.2 | 1024 | $0.0103 |
| Luna short prompt | 724 | 155.5 | 92.8 | 879 (−14%) | $0.0096 |
| Luna short + effort none | 724 | 55.5 | **0** | **779 (−24%)** | $0.0064 (−38%) |

Against the Sol baseline, Luna short + effort none uses **20% fewer tokens** and costs
**96% less**. 0 errors, 0 answers cut off, 0 cached tokens in all runs.

## Quality: automatic check (2026-11-17)

Checked with `quality_check.py`: each answer is compared with its baseline answer; it keeps the
baseline's grade only if the reply type, every number and the meaning (MiniLM similarity ≥ 0.90)
all match. Changed answers were graded by an AI grader (Claude helper agents, draft); baselines
were draft-graded the same way. **No human has confirmed these yet.**

| Run | Same as baseline | Changed → AI-graded | Final verdicts | vs baseline | Cost per correct answer |
|---|---|---|---|---|---|
| Sol short prompt | 40 | 24 | **64 correct** | 63 correct, 1 wrong | \$0.002731 → **\$0.002320 (−15%)** |
| Luna short prompt | 29 | 35 | 62 correct, 2 partial | 60 / 3 partial / 1 wrong | \$0.000172 → \$0.000155 (−10%) |
| Luna short + effort none | 27 | 37 | 57 correct, **7 partial** | 60 / 3 partial / 1 wrong | \$0.000172 → **\$0.000112 (−35%)** |

**Reading it.**
- **Short prompt: keep.** No quality loss on either model; Sol even fixed q006 (the baseline called
  an order due *today* "overdue").
- **No thinking on Luna: cheaper, slightly worse.** Three fewer correct answers and four more
  partial ones (q009 invented a refund date; q055 missed warranties that were in the evidence),
  no wrong ones. A good candidate for *simple* questions only (adaptive thinking), not everywhere.
- **Answers vary between runs anyway.** GPT-6 rejects temperature, so part of the 24–37
  "changed" answers is natural run-to-run variation. Measuring that needs one re-run of the
  baseline (≈ \$0.18), pending OpenAI credit.
- **Rubric gap found and fixed (rule 4, 2026-11-17):** an answerable question whose reply opens
  with a refusal line but then answers is at best **partial**. Applied in `quality_check.py` and to
  all existing grades (changed one: q059 in the no-thinking run, correct → partial).
- For humans (optional, at the end): q009, q020, q025, q029, q032, q035, q036, q048, q050, q053,
  q055, q059. Details per answer: `*.check.csv`, grader notes in `*.judge.csv`.

## Automatic checks before grading (2026-10-15)

Automatic checks only (not grades):

| Run | Out-of-scope handled | Answerable questions refused outright |
|---|---|---|
| Sol baseline / short | 10/10 / 10/10 | 0 / 0 |
| Luna baseline / short / short+none | 8/10 / 9/10 / 8/10 | 1 / 1 / **2** |

Removing Luna's thinking may cost some quality (one more outright refusal). Grading pages: `*.grading.html` here.
