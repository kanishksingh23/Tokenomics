# TechStore Support Agent — Phase 0

The application the cost router will sit underneath, and the **always-frontier
baseline arm** of the Week 10 benchmark.

No router, no cache, no classifier, no circuit breaker. A question comes in,
relevant knowledge-base documents are retrieved, one model is called, an answer
comes back — with tokens, cost and latency recorded for every call.

## Why this exists first

1. **It is the baseline.** `benchmarks/run_baseline.py` is `SupportAgent` in a loop.
2. **It validates the corpus while fixing is cheap.** Retrieval bugs and gaps in
   the knowledge base surface now, not in the benchmark week.
3. **It makes before/after real.** "Same agent, one line changed, 60% cheaper"
   beats comparing two benchmark scripts.
4. **It gives the router a drop-in target.** In Week 4, set `OPENAI_BASE_URL`
   to the gateway. Nothing else changes.

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env          # add your API key

python check_setup.py                                # free pre-flight: key, model ids, pricing, data
python check_setup.py --ping                         # plus one tiny real call (< $0.001)

python cli.py --mock "Can I return opened headphones?"   # full pipeline, no key, no spend
python cli.py "Can I return opened headphones?"          # calls the model
python cli.py --batch data/questions_seed.jsonl --out results_real.jsonl
python review_results.py results_real.jsonl --sheet review.csv   # read, grade, calibrate
streamlit run app.py                                     # the demo
```

**Set a hard spend limit on the provider account before the first real call.**

Retrieval and context assembly work with **zero dependencies and no API key** —
`--dry-run` and `validate_data.py` are the loop to iterate on the corpus in.

## Layout

```
techstore/
├── config.py            model ids, pricing table (as-of dated), paths
├── retriever.py         BM25-lite (stdlib) + MiniLM backends, auto-selected
├── agent.py             retrieve -> assemble context -> call model -> Answer record
├── cli.py               single question, --dry-run, or --batch over JSONL
├── app.py               Streamlit chat + inspector panel
├── validate_data.py     corpus integrity + progress against the 500 target
├── check_setup.py       pre-flight: packages, key, model ids exist, prices present
├── review_results.py    batch review: cost, output length, flags, grading sheet
├── eval_retrieval.py    keyword vs embedding vs hybrid, per-category recall
├── system_prompt.txt
├── data/
│   ├── knowledge_base.jsonl    84 policy / product / billing / API documents
│   ├── orders.jsonl            40 orders incl. the multi-charge dispute case
│   └── questions_seed.jsonl    40 seed questions, 5 per category
└── tests/test_agent.py  12 tests, no API calls, free to run in CI
```

## Design decisions worth knowing

**Retrieval is not optional.** Sending all 85 documents in every prompt costs
~7,700 prompt tokens instead of ~500 — 7x the cost (measured with the real
tokenizer), growing with every document added. `test_prompt_stays_within_budget`
guards this.

**Measured prompt size is ~451 tokens** (max 613), against the 400 the spec
assumes. Per-request cost on Sol is \$0.00480 rather than \$0.00460. Re-measure
once the full 500 questions exist.

**Keyword is the default retriever, on measurement.** `python eval_retrieval.py`
reports context recall@3 on the labelled seed questions: keyword 81.8%, hybrid
80.0%, embedding 76.4%. Keyword is also ~150x faster (0.05 ms vs 7.9 ms).
Caveat: some KB tags were tuned while diagnosing seed questions, which favours
keyword on this set. Re-run on the full 500, and report absolute retrieval
numbers only from questions not used for tuning.

**Embeddings are pinned to CPU.** On Apple Silicon the library defaults to the
MPS GPU, which recompiles per input length: p95 144 ms on unseen queries versus
9.8 ms on CPU.

**Known retrieval gaps** (from `eval_retrieval.py --misses`): "Standard Warranty
Terms" is the most-missed document and is central to policy edge cases; and
comparisons naming two products often retrieve only one of them.

**Named products are always retrieved.** Product pages carry an `aliases` list;
when a question names a product ("PulseBook 14", "X200"), its page is included
first and retrieval fills the remaining slots.

**The store has a fixed "today"** (`SIMULATED_TODAY` in `config.py`, stated in
every prompt). The model knows the real date, so against frozen order records
answers would otherwise drift with the calendar. `validate_data.py` checks that
no fixture event is after today and no due date is already past.

**Two retrieval backends.** `keyword` is pure stdlib so the agent is testable
before anything is installed; `embedding` uses the same MiniLM model the router
needs for Layer 1B and Layer 2, so this validates that pipeline early. `auto`
prefers embeddings and falls back silently.

**Orders 48213 and 48217 hold different products on purpose.** Near-identical
questions, completely different correct answers — the fixture for the Week 2
semantic-cache safety suite and for the blocked-attack demo moment.

**The inspector panel is the point of the UI.** It currently shows retrieval,
tokens, cost and latency. From Week 4 it gains cache status, tier, uncertainty
signals and savings. Building it now means the response schema grows with it
rather than being retrofitted during the recording week.

## The four-day plan

| Day | Work | Done when |
|:--|:---|:---|
| 1 | Knowledge base + system prompt + order fixtures | `validate_data.py` passes; 84 docs, 40 orders |
| 2 | Retriever + agent + context assembly | `--dry-run` shows correct docs; recall tests pass |
| 3 | Model call, cost accounting, CLI, Streamlit | Real answers with cost and latency logged |
| 4 | Seed questions, manual review, mentor demo | 40 seeds validate; agent answers all 8 categories sensibly |

**Status: days 1–3 complete.** Day 4 is the manual review pass, which needs an
API key and human judgement.

The corpus now carries 84 documents and 40 orders — enough breadth to support all
500 questions. Products hold a canonical `price` field and every order is checked
against it, so a billing answer can never cite a price the catalogue contradicts.

## Expanding to 500 questions (Weeks 3–6)

The 40 seeds are the exemplars — 5 per category, fixing tone and difficulty.
Generate ~55 more per category from those plus the knowledge base, then **review
every one by hand** against the KB for answer correctness and category label.
The 84 documents and 40 orders are sized to support this without further
authoring; if a generated question has no supporting document, add the document
rather than dropping the question.
That review is the step that decides whether the benchmark measures anything.

Run `python validate_data.py` after each batch; it reports per-category progress
against the 500 target and fails on any dangling `context_ids` or `order_ids`.

Deliberately include: questions with no answer in the knowledge base (does the
model hallucinate or admit it?), two questions in one message, and hostile
phrasing.

## Handover to the router

| Week | Change |
|:--|:---|
| 4 | `OPENAI_BASE_URL` → `http://localhost:8000/v1`. One line. |
| 10 | `benchmarks/run_baseline.py` wraps `SupportAgent` for the always-frontier arm |
| 12 | The inspector panel gains routing rows; this becomes the demo UI |
