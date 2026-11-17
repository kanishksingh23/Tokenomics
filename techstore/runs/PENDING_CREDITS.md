# Tests waiting for OpenAI credit

OpenAI credit ran out (found 2026-11-17; ≈ $0.57 recorded spend, the $50 grant most likely
expired). Everything below is built and ready; it only needs real model calls.
**Add each new item here the moment it is built.** Tick it off with the run folder when done.

Before the first run: `python check_setup.py --ping` (catches key, model-id and parameter
problems for under $0.001).

| # | Test | Why | Command(s) | Est. cost | Done |
|---|---|---|---|---|---|
| 1 | **`verbosity` support check** | Does GPT-6 accept OpenAI's built-in length setting? It saves the 55 input tokens the concise rule costs. | `python cli.py --verbosity low "Is delivery free?"` (Luna and Sol) | < $0.01 | |
| 2 | **Run-to-run variation** | How many answers change by chance alone, with nothing changed (GPT-6 rejects temperature). Tells us how much of an experiment's "changed" answers is noise. | `python cli.py --batch data/questions_dev.jsonl --out runs/<date>_variation/sol_rerun.jsonl --model gpt-6.1-sol` and the same with `--model gpt-6-luna` | ≈ $0.18 | |
| 3 | **Answer-length control** (technique 3) | Do concise answers cut output tokens by more than the rule adds (55 input tokens)? | Sol and Luna, short prompt, `--answer-length concise`; if #1 passes, also `--verbosity low` | ≈ $0.16 (×2 with verbosity) | |
| 4 | Sol `reasoning_effort=low` (technique 2) | Optional: Sol thinks only ~6 tokens per question, so little to gain | `--model gpt-6.1-sol --reasoning-effort low` | ≈ $0.15 | |

Then run `quality_check.py` against the graded baseline for each, and record the result in the
run folder's NOTES.md and in `Tokenomics.md` §10.

## Later (built when we reach them)

- Each new technique: one 64-question run on Sol and one on Luna (≈ $0.18 per technique).
- Hosted open-weight model (routing stage): free Groq key, ≈ $0.003 per 64 questions.
- **Final proof** on the 36 test questions: always-Sol, always-Luna, random, oracle, Tokenomics.
  About $0.10 per arm on Sol, cents on Luna; use the Batch API (−50%).
