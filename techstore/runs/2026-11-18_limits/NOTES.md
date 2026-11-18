# Technique 12: spending limits (2026-11-18)

Check each client's budget **before** a request is sent, like a prepaid balance. Langfuse
records spending afterwards and can't stop anything; this can. Built and tested without
OpenAI credit (the logic is deterministic; mock scenarios below use estimated costs).

## How it decides (`spending_limits.py`)

| Situation | Action |
|---|---|
| Whole app over its daily cap (default **$5**) | **Refuse**, for every caller including scripts: the runaway-loop guard |
| Client over its daily budget (default **$0.05**, ~20 Sol answers) and even the cheap model won't fit | **Refuse** politely; no model call, nothing spent |
| Client past the soft limit (default **80%** of budget) | **Downgrade** to the cheap model (Luna), if that still fits |
| Client sending more than **20 requests per minute** | Refuse that request ("please wait a moment"), via a token bucket |
| Otherwise | Allow |

- The cost is **estimated before** the call (real input tokens + an expected 200 output tokens)
  and the **actual** cost recorded after, so the ledger matches the bill.
- FAQ-shortcut and cache answers cost nothing and never count.
- Spend lives in `techstore/.cache/spend.sqlite` (not in git); mock runs use memory, so
  estimates never count against the real budget. Days are UTC.
- Clients: each Streamlit browser session; `--client` in the CLI; API keys at the gateway.
  Without a client, only the app-wide cap applies.
- Each decision is a `spending-limit` step in the Langfuse trace.

## Scenarios (mock costs)

1. **Runaway loop** (one question repeated; app cap set to $1 for the test): stopped at call
   348 with $0.9987 spent. Without the cap, 10,000 overnight calls would cost about $28.78.
2. **Heavy demo visitor** (120 questions, $0.05 budget): 17 answers on Sol, then 103 on Luna;
   $0.0494 spent, never over budget.
3. **Burst** (30 messages at once, 20/minute): 20 answered, 10 asked to wait.

## Later

At the gateway (roadmap step 13) the same checks run per API key, and the per-minute bucket
moves to a shared store so several gateway processes agree on the count.

## Bug found while testing

The demo app crashed on the **second message** of a session: Streamlit answers each message on
a new thread, and a SQLite connection refuses to be shared across threads by default. The
response cache had the same latent bug. Both stores now share their connection safely behind
a lock; a test uses them from several threads at once.
