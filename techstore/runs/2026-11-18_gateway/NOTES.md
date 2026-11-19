# Step 13: the Tokenomics gateway (2026-11-18)

The techniques became a product: an OpenAI-compatible server (`tokenomics/gateway.py`, docs in
`tokenomics/README.md`). Built and tested without OpenAI credit (mock provider).

## Restructure first

The technique code lived inside `techstore/` (the test app). It moved into a new installable
package, `tokenomics/` (`pip install -e .`), with no behaviour change: same 51 TechStore tests,
same numbers from the CLI, cache safety suite, FAQ check and caching simulator. TechStore now
uses the package like any other app would.

## End-to-end check (TechStore → gateway, mock provider)

TechStore changed only `OPENAI_BASE_URL` and `OPENAI_API_KEY` (a Tokenomics key):

| Question | Result |
|---|---|
| "Is delivery free?" | model |
| "How do I reset my password?" | model |
| "is delivery free" | **cache, exact**: $0, 4 ms |
| "What is happening with order 48712?" ×2 | model both times: the agent marks requests with order records private, so they're never cached |
| "How can I reset my password?" | **cache, same meaning**: $0, 14 ms |
| Key with a $0.003/day budget | switched to Luna immediately (Sol wouldn't fit under 80%) |
| Key with a near-zero budget | HTTP 429 → TechStore showed its polite "usage limit" message |

The agent recognises a Tokenomics key (`tk-...`), switches off its own cache and limits (the
gateway runs them), sends the hint headers, and reads the gateway's report of who answered and
the true cost.

## Bugs found and fixed while building

1. A refactor edit to spending limits silently didn't apply (the text no longer matched after
   re-indenting): with no cheap model configured it "downgraded" to no model, so the budget was
   never reached. Fixed, with a test; every other refactor edit verified.
2. FastAPI read `request` as a missing URL parameter, because the `Request` type was imported
   inside a function while annotations are strings (`from __future__ import annotations`).
3. Per-key budgets were set on a shared object before checking: two requests at once could mix
   budgets. The budget is now passed into each check.
4. The provider call blocked the server's event loop; it now runs in a worker thread.
5. The key tool and the gateway used different setting names for the keys file; `/ready`
   reported "no client keys", which is how it was caught.
6. The first request took 6.7 s (embedding model loaded lazily); it now loads at startup.

## Not yet done

- Real provider run through the gateway (needs credit; `runs/PENDING_CREDITS.md`).
- Several gateway processes sharing one cache/ledger (needs a shared store such as Redis).
- Model routing (roadmap step 14) plugs in at step 4 of the request flow.
