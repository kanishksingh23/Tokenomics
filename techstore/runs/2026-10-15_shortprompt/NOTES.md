# Token-saving step 1: short system prompt, and Luna with no reasoning (2026-10-15)

Same 64 dev questions and settings as `../2026-10-15_baseline/` (embedding retrieval, top_k 4).
Only the system prompt and the reasoning effort change.

- `system_prompt_short.txt` keeps every rule and all three exact refusal wordings; it only
  cuts phrasing: 436 → 283 tokens.
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

## Quality: not known yet

Automatic checks only (not grades):

| Run | Out-of-scope handled | Answerable questions refused outright |
|---|---|---|
| Sol baseline / short | 10/10 / 10/10 | 0 / 0 |
| Luna baseline / short / short+none | 8/10 / 9/10 / 8/10 | 1 / 1 / **2** |

Removing Luna's thinking may cost some quality (one more outright refusal). These runs need
grading before any of the changes is adopted. Grading pages: `*.grading.html` here.
