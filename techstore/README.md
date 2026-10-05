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
python cli.py --batch data/questions_dev.jsonl --out results_real.jsonl
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
├── validate_data.py     corpus integrity; dev/test progress; --freeze locks the test set
├── check_setup.py       pre-flight: packages, key, model ids exist, prices present
├── review_results.py    batch review: cost, output length, flags, grading sheet
├── eval_retrieval.py    keyword vs embedding vs hybrid, per-category recall
├── system_prompt.txt
├── data/
│   ├── knowledge_base.jsonl    84 policy / product / billing / API documents
│   ├── orders.jsonl            40 orders incl. the multi-charge dispute case
│   ├── questions_dev.jsonl     dev set (target 100): tuning only
│   └── questions_test.jsonl    test set (target 200): frozen, final results only
└── tests/test_agent.py  12 tests, no API calls, free to run in CI
```

## Design decisions worth knowing

**Retrieval is not optional.** Sending all 85 documents in every prompt costs
~7,700 prompt tokens instead of ~500 — 7x the cost (measured with the real
tokenizer), growing with every document added. `test_prompt_stays_within_budget`
guards this.

**Measured prompt size**: the first real run averaged 639 prompt and 93 output
tokens per question, \$0.0022 on GPT-6.1 Sol. Re-measure on the test set.

**Embedding search is the default.** On 14 questions the system had never seen,
embedding search found the right document 14/14 and keyword search 8/14:
customers say "earphones", "blinking" or "paid twice" where the documents say
earbuds, flicker and duplicate charge. Keyword search had looked better on the
first 50 questions only because document tags had been written in their exact
wording. Choosing the method per question (keyword for technical questions)
was tested and matched embedding alone, so it is kept in reserve.

**Embeddings are pinned to CPU.** On Apple Silicon the library defaults to the
MPS GPU, which recompiles per input length: p95 144 ms on unseen queries versus
9.8 ms on CPU.

**Known retrieval gaps** (from `eval_retrieval.py --misses`): "Standard Warranty
Terms" is the most-missed document and is central to policy edge cases; and
comparisons naming two products often retrieve only one of them.

**Named products are always retrieved.** Product pages carry an `aliases` list;
when a question names a product ("PulseBook 14", "X200"), its page is included
first and retrieval fills the remaining slots.

**Category questions get the product catalogue.** `catalogue_summary` lists all
16 products on one line each (name, type, price, key specs). It is never returned
by search; it is added, on top of the usual documents, when a question names a
category and asks to compare, choose or buy ("which of your headphones is
lighter?"). `validate_data.py` checks every price and spec number in it against
the product pages, so it cannot drift from them.

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
| 4 | Seed questions, manual review, mentor demo | 50 seeds answered for real and graded by two people |

**Status: days 1–3 complete.** Day 4 is the manual review pass, which needs an
API key and human judgement.

The corpus carries 86 documents (including the catalogue and About TechStore)
and 40 orders — enough breadth for all 300 questions. Products hold a canonical `price` field and every order is checked
against it, so a billing answer can never cite a price the catalogue contradicts.

## Writing the remaining questions (Weeks 3–6)

**Full guide for writers: [WRITING_TEST_QUESTIONS.md](WRITING_TEST_QUESTIONS.md)** — categories, question types, key points, using AI, the format, and every document and order id.

There are two sets, and they must never mix:

| Set | File | Target | Use |
|:---|:---|---:|:---|
| Dev | `data/questions_dev.jsonl` (ids `q…`) | 100 | Finding problems and tuning anything |
| Test | `data/questions_test.jsonl` (ids `t…`) | 200 | Final results only |

**Why:** every fix made after looking at results fits the system to those
questions, training or not. On 14 new questions keyword search found the right
document 8 times out of 14, against 100% on the questions it had been tuned on.

**Write the test set first**, before any more tuning, then freeze it:

    python validate_data.py --freeze     # writes questions_test.sha256; commit both

After that, any edit to the test set fails validation, and so does any question
that appears in both files. Use the current dev questions as examples of tone and
difficulty, and **check every question by hand** against the knowledge base for
answer correctness and category label: that review decides whether the benchmark
measures anything. Include questions the knowledge base cannot answer, two
questions in one message, hostile phrasing, and the customer's own words rather
than the documents' wording.

`python validate_data.py` shows progress against both targets per category.

## Handover to the router

| Week | Change |
|:--|:---|
| 4 | `OPENAI_BASE_URL` → `http://localhost:8000/v1`. One line. |
| 10 | `benchmarks/run_baseline.py` wraps `SupportAgent` for the always-frontier arm |
| 12 | The inspector panel gains routing rows; this becomes the demo UI |
