# Baseline: 64 dev questions on Sol and on Luna (2026-10-15)

The "before" numbers every token-saving step is measured against.
Both runs: embedding retrieval, top_k 4, MAX_TOKENS 2000, same 64 questions
(`data/questions_dev.jsonl`), traced in Langfuse (sessions `sol_baseline`, `luna_baseline`).

```
python cli.py --batch data/questions_dev.jsonl --out runs/2026-10-15_baseline/sol_baseline.jsonl  --model gpt-6.1-sol
python cli.py --batch data/questions_dev.jsonl --out runs/2026-10-15_baseline/luna_baseline.jsonl --model gpt-6-luna
```

## Numbers

| | Sol (gpt-6.1-sol) | Luna (gpt-6-luna) |
|---|---|---|
| Errors | 0 / 64 | 0 / 64 |
| **Total cost** | **$0.1721** | **$0.0103** (6.0% of Sol) |
| Cost per question | $0.002689 | $0.000161 |
| Input tokens / question (mean) | 877 | 877 |
| Output tokens / question (mean) | 93.5 | **146.9** |
| …of which hidden reasoning | 5.6 | **84.2** |
| Visible answer tokens (mean) | 87.8 | 62.6 |
| Cached input tokens | 0 | 0 |
| Cut off (`finish_reason=length`) | 0 | 0 |
| Latency p50 / p95 | 3.2 s / 6.4 s | 2.7 s / 8.7 s |

Langfuse totals match these files exactly ($0.1721 and $0.0103).

## Where the 877 input tokens go

| Part | Tokens | Share |
|---|---|---|
| System prompt (instructions, identical every call) | 436 | 50% |
| Retrieved documents (4 per question) | 381 | 44% |
| Order records | 26 | 3% |
| Question + date line | 25 | 3% |

Largest single document: `catalogue_summary`, 602 tokens (added only for category questions).
Average document: 94 tokens.

## Findings

1. **Input is the main cost.** On Sol, input is 90% of tokens and 65% of cost
   ($0.112 of $0.172). Cutting the prompt is the biggest lever for tokens *and* money.
2. **Half the prompt is our own instructions,** sent unchanged 64 times.
3. **No provider prompt caching happened** (0 cached tokens in 128 calls). The likely
   reason: the prompts are short (877 tokens on average), and OpenAI has historically
   cached only prompts of 1,024+ tokens. Not verified for GPT-6.
4. **Luna is cheaper but uses more tokens.** It spends 84 hidden reasoning tokens per
   question (57% of its output) against Sol's 6. Routing to Luna cuts **cost** about 17×,
   but **output tokens rise** by ~57%. That matters if the goal is counted in tokens.
5. **Neither GPT-6 model accepts `logprobs`** (HTTP 400 "Unsupported parameter").
   Escalation signal 1 (30% weight) is unavailable; Layer 3 must rely on the other four
   signals with the weights renormalised.
6. **Automatic checks (not grades):** Sol handled 10/10 out-of-scope questions correctly;
   Luna 8/10, and refused one answerable question outright. Human grading decides.

## Still to do

- Grade both runs: `sol_baseline.grading.html` and `luna_baseline.grading.html`
  (verdict CSVs: `sol_grades.csv`, `luna_grades.csv`). Luna's grades tell us how often
  the cheap model is good enough on its own, the upper limit of what routing can save.
