# Tokenomics: the package and the gateway

Cut what an app pays for LLM calls without making answers worse. Every technique here works
on an OpenAI-style request and knows nothing about any particular app; the **gateway** applies
them to any app's traffic. (TechStore, in `../techstore`, is the test app.)

## Install

```bash
pip install -e ".[gateway,embeddings]"     # from the repo root; add ,tracing for Langfuse
```

## Run the gateway

```bash
python -m tokenomics.keys create --client myapp --daily-budget 1.00   # prints a key once: tk-...
TOKENOMICS_UPSTREAM=mock uvicorn tokenomics.gateway:create_app --factory --port 8000   # no provider calls
OPENAI_API_KEY=sk-...    uvicorn tokenomics.gateway:create_app --factory --port 8000   # real provider
```

Or with Docker, from the repo root: `docker compose up --build gateway`.

**Switching an app over** takes two settings and no code changes:

```
OPENAI_BASE_URL=http://localhost:8000/v1
OPENAI_API_KEY=tk-...            # the Tokenomics key, not the provider key
```

The app never sees the provider key. Only a SHA-256 fingerprint of each Tokenomics key is stored.

## What happens to each request

| Step | Technique | Module |
|---|---|---|
| 1 | Check the key → 401 if unknown; 403 if the model isn't allowed for it | `keys.py` |
| 2 | **Safe response cache:** a first question asked before (same words or same meaning) is answered for free. Never for follow-ups or private requests; never across keys. | `response_cache.py` |
| 3 | **Conversation memory:** older turns shrunk (`window`, `facts` or `summary`) | `techniques.py` |
| 4 | **Spending limits:** app-wide daily cap; per key (or per end user) past 80% → cheap model; at 100% → 429 | `spending_limits.py` |
| 5 | The provider call, adapting to each model's parameter quirks | `upstream.py` |
| 6 | Record the actual cost; keep the answer for reuse; Langfuse trace | `pricing.py`, `tracing.py` |

Other techniques live with the app because they need its knowledge: the FAQ shortcut's
answers (`faq.py` is the matcher), adaptive context, prompt layout.

## Optional request headers

| Header | Purpose |
|---|---|
| `X-Tokenomics-Question` | The end user's own words, for cache matching (default: the last user message) |
| `X-Tokenomics-Namespace` | What else changes the right answer, e.g. the knowledge-base version (default: a fingerprint of the system messages) |
| `X-Tokenomics-Private: true` | The prompt holds personal data: never cached |
| `X-Tokenomics-Client` | The end user, for per-user budgets under the app's key |

## What comes back

A normal `chat.completion`, plus a `tokenomics` object (also summarised in `X-Tokenomics-*`
response headers):

```json
"tokenomics": {"served_by": "cache", "model": "gpt-6.1-sol", "cost_usd": 0.0,
               "cache_kind": "semantic", "cache_score": 0.91,
               "memory": {"mode": "off", "dropped_turns": 0},
               "limit": {"action": "allow", "reason": "within budget"}}
```

Refusals by the spending limit are HTTP 429 with an OpenAI-style error. Streaming isn't
supported (out of scope, Tokenomics.md v2.9).

## Endpoints

`POST /v1/chat/completions` · `GET /v1/models` · `GET /health` (alive) · `GET /ready` (provider
key and client keys configured: 503 with the problems listed if not).

## Settings

Environment variables `TOKENOMICS_<NAME>` for every field of `gateway.Settings`, e.g.
`TOKENOMICS_UPSTREAM` (`openai`/`mock`), `TOKENOMICS_CACHE` (`true`/`false`),
`TOKENOMICS_CACHE_THRESHOLD` (0.88), `TOKENOMICS_GLOBAL_DAILY_USD` (5.0),
`TOKENOMICS_CLIENT_DAILY_USD` (1.0 per key), `TOKENOMICS_END_USER_DAILY_USD` (0.05),
`TOKENOMICS_RPM` (60), `TOKENOMICS_MEMORY` (`off`), `TOKENOMICS_VERBOSITY` (`low`, added to
GPT-6 requests that set none; `off` to disable), `TOKENOMICS_STATE_DIR` (`.tokenomics`),
`TOKENOMICS_KEYS` (`gateway_keys.json`), plus `OPENAI_API_KEY` for the provider.

## Tests

`python -m pytest tests` from the repo root: the gateway is called in-process with a stand-in
provider (no network, no cost). CI also builds the Docker image and health-checks the gateway.
