# Technique 9: conversation memory (2026-11-18)

In the OpenAI format every request carries the **whole conversation so far**, so input tokens
grow with every turn. Memory trimming keeps the last 2 exchanges word for word and shrinks
everything older. Built and measured in mock mode (token counts are real; answers are stand-ins
of realistic length). **Quality needs real runs (pending credit).**

## What was built

- **TechStore is multi-turn** (`agent.ask(question, history=...)`, the CLI's `--conversations`,
  and the Streamlit demo). Follow-ups search documents with the previous question too ("what
  about the Y500?"), and order numbers from any earlier turn stay available. Follow-ups never use
  the FAQ shortcut or the cache: "can I still cancel it?" means nothing on its own.
- **Memory modes** (`techniques.apply_memory`, works on any OpenAI-style request):

| Mode | Older turns become | Extra cost |
|---|---|---|
| `off` | resent in full every turn | — |
| `window` | dropped | none |
| `facts` | a note: the customer's earlier questions + every order number, amount, email and date mentioned | none |
| `summary` | a summary by the cheap model (Luna, no reasoning), **rolling**: each older turn is summarised once and the summary extended, never redone | one small call per turn that ages out; counted in that answer's cost |

## Measured on 8 dev conversations (36 turns, `data/conversations_dev.jsonl`)

| Mode | Input tokens | vs off | Avg. input from turn 4 |
|---|---|---|---|
| off | 34,327 | — | 1,098 |
| window | 32,401 | −5.6% | 938 |
| facts | 32,713 | −4.7% | 964 |
| summary (mock summary) | 32,714 | −4.7% | 964 |

Small in total because these chats are short (4–6 turns) and trimming starts at turn 4. Per
turn it is clear: conversation c08 grows 678 → 1,191 input tokens without trimming, and stays
at **about 880** with it (turn 6: −26%).

**Projection** from the measured growth (~100 tokens per turn, flat at ~890 with trimming):

| Chat length | Saving on input tokens |
|---|---|
| 5 turns | −6% |
| 10 turns | −24% |
| 20 turns | −46% |

## Still to know (needs credit; in `runs/PENDING_CREDITS.md`)

Does shrinking older turns lose anything the model needs? `window` forgets what was said
early on (order records are re-attached, but other details are not); `facts` keeps numbers
and questions but not the agent's explanations; `summary` keeps meaning but costs a call.
Run all four on Sol, check quality per turn against `off`, and include the summary calls'
real cost.

Also open: the final proof originally planned 60 multi-turn conversations. These 8 are
dev-only (written by Claude, used for building); fresh ones would be needed for a fair final
number.
