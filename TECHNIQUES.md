# Tokenomics: every cost and token technique, explained

What each technique attacks, how it works, what we measured, and where it stands.
Status as of **19 November 2026**. Numbers come from the run notes in `techstore/runs/`;
terms are explained in [LEARNING.md](LEARNING.md).

---

## Part 0: Where the money goes

Every answer is billed in **tokens** (pieces of words, about ¾ of a word each):

| | GPT-6.1 Sol (expensive) | GPT-6 Luna (cheap) |
|---|---|---|
| **Input** (what we send), per 1M tokens | $2.00 | $0.10 |
| **Output** (what it writes), per 1M tokens | $10.00 | $0.50 |

Two facts shape everything:
- **Output costs 5× input.** One saved output token is worth five saved input tokens.
- **Sol costs 20× Luna** for the same token.

The measured "before" picture (Sol, 64 dev questions, 15 Oct 2026):

```
One question ≈ 877 input tokens + 94 output tokens ≈ $0.0027
  877 input = 436 instructions (50%)   ← identical on every call
            + 381 documents    (44%)   ← changes per question
            +  26 order records (3%)
            +  ~25 question and date (3%)
```

The bill has distinct parts: instructions, documents, conversation history, hidden thinking,
the visible answer, the price per token, and repeated questions. **Each technique attacks one
part.** Savings **multiply** rather than add: a 16% cut then a 10% cut is about 24%, because the
second cut applies to what is left.

**The yardstick is cost per correct answer** (total cost ÷ answers graded correct). A trick that
saves money but breaks answers makes this number worse, so it can't fool us.

---

## 1. Shorter instructions ✅ adopted

**Attacks:** the 436 instruction tokens sent with every question.

**How it works:** the system prompt (the fixed instructions) was rewritten with **every rule
kept**, including the three exact refusal sentences, in fewer words:

> Before: "For billing disputes, list every charge you can see and explain the resolution step by step, including amounts."
> After: "Billing disputes: list every charge with its amount, then the resolution step by step."

**436 → 283 tokens.** A cut to something sent every time saves on every request.

**Measured (Sol):** −16% tokens per question (970 → 811), **−15% cost per correct answer**.
Quality held: 64/64 correct, against 63 correct and 1 wrong before.

**Status:** the default since 17 Nov 2026 (`system_prompt.txt`; the original is kept as
`system_prompt_original.txt`). An app-side lesson, not something the gateway applies for others.

---

## 2. Reasoning-effort control ✅ measured; for simple questions only

**Attacks:** hidden thinking. Newer models think privately before answering; those tokens are
billed as output (the 5× price) although nobody sees them.

**Discovery:** Luna thinks **84 hidden tokens per question**, Sol about 6. That's why Luna wrote
147 output tokens when only 63 were the visible answer.

**How it works:** the `reasoning_effort` setting. Luna accepts `none / low / medium / high`; Sol's
lowest is `low`. Simple questions don't need thinking; comparisons may.

**Measured (Luna, `none`):** output 155 → 55 tokens; **cost per correct answer −35%**. Quality
dipped: 57 correct + 7 partial, against 60 + 3 + 1 wrong (e.g. an invented refund date in q009,
missed warranty facts in q055).

**Status:** a real lever, but only for simple questions, which is why it pairs with routing.
On Sol it barely matters.

---

## 3. Answer-length control ✅ adopted (`verbosity=low`)

**Attacks:** the visible answer, the most expensive kind of token.

**How it works, two ways:**
1. A "be brief" rule added to the instructions: start with the direct answer in one or two
   sentences, lists only when needed, no greeting or closing offer.
2. OpenAI's `verbosity` setting (low/medium/high). Both GPT-6 models accept it.

**The break-even:** the rule costs 55 input tokens per call (on Sol: 55 × $2/1M = $0.00011).
Each output token saved is worth $0.00001, so answers must shrink by **at least ~11 tokens** on
average. `verbosity` costs no input at all.

**Why it's promising:** Sol's answers average 88 visible tokens, often with greetings and
"let me know if you need anything else". Cutting 30% would save about 10% of Sol's cost.

**Measured (real runs, 64 questions, 2026-11-25):** the rule cut Sol's output 15% but its 55
extra input tokens ate the saving (−0.5% cost). `verbosity=low` cut output just as much with no
extra input: **Sol −5.5% cost, 64/64 correct**. Luna −3% (its output is mostly hidden thinking).

**Status:** **`verbosity=low` is the default** in TechStore and in the gateway (for GPT-6 requests
that don't set it). The "be brief" rule is dropped.

---

## 4. Sentence-level trimming ❌ rejected

**Attacked:** the documents, by sending only the sentences relevant to the question.

**Why it failed:** checked for free with a **proxy measure**: do the 207 numbers Sol quoted in
its correct answers still appear after trimming? Even the gentlest setting lost **11%** of them,
from documents the questions needed: the **Y500's price and specs** in a headphone comparison,
**express delivery's ₹149**. Our documents are short (94 tokens on average), so the sentence that
looks less related often holds the key number. The saving on offer was only −13% document tokens.

**Status:** kept in the code, switched off (`--passage-margin`). Rejecting a technique with
evidence, before spending anything, is itself a result.

---

## 5. Adaptive context ✅ adopted (default)

**Attacks:** the documents, by sending fewer *whole* documents (never cutting inside one).

**How it works:** we always sent the 4 best matches, but often one is a clear winner:

```
"Can I return earbuds I already opened?"
  Non-Returnable Items      0.71   ← clear winner
  Earbuds troubleshooting   0.42
  Studio Buds product page  0.39
```

Keep only documents scoring within **0.25** of the best (at least 1, at most 4). Named products
and order records are always kept.

**Measured (free, against each dev question's needed documents):** 4.03 → **3.41 documents**,
−15% document tokens (381 → 322), about −8% input and −5% of Sol's cost. **No needed document
was dropped**; the only losses were extra details Sol had borrowed from documents the question
didn't need.

**Real runs (2026-11-25):** **Sol −12.4% cost, 64/64 correct**; Luna −11%, 60 correct + 4
partial vs 61 + 3 (within run-to-run noise). With `verbosity=low` on top: **Sol −16%**, 64/64.

**Status:** **default, margin 0.25** with the embedding retriever (`--context-margin off` to
disable). App-side only: the gateway never sees how an app picks its documents.

---

## 6. Prompt compression ❓ waiting for the mentor's decision

**Would attack:** the documents, by squeezing out words. A small free model (Microsoft's
LLMLingua) runs on our side: "TechStore accepts returns within 30 days of delivery" becomes
"Returns within 30 days of delivery".

**The risk for us:** technique 4 showed our short documents are fragile; compression could drop
"not" or a number. It would go through the same proxy measure first.

**Status:** not built.

---

## 7. Safe response cache ✅ built

**Attacks:** repeated questions. A reused answer costs zero tokens.

**How it works, two levels:**
1. **Exact:** the same question again (ignoring capitals, spaces, end punctuation).
2. **Same meaning:** "How do I reset my password?" ≈ "How can I reset my password?", via
   embeddings (meaning as numbers) with a similarity threshold of **0.88**.

**The hard part is safety.** A meaning match is reused only if every check passes:

| Check | Stops |
|---|---|
| Same numbers, amounts, dates, product names | Order 48213's answer reaching order 48217; ₹500 vs ₹1,500; AuraWatch vs Studio Buds |
| No meaning flip (negations, opposite pairs, both directions) | "turn **on**" answered with "turn **off**"; enable/disable; with/without |
| Same namespace (instructions, knowledge version, model, settings) | Old answers surviving a policy edit |
| Never personal or time-sensitive | "my order", order numbers, "today", "in stock", anything using order records |

**Measured:** **45/45** dangerous look-alike pairs blocked; 27/30 true rephrasings reused. The
most similar dangerous pair scores 0.79, the least similar rephrasing 0.86, so 0.88 keeps a
margin. **CI runs this suite with the real model on every push**; one wrong reuse fails the build.

**The saving equals how often customers repeat themselves.** On our question sets it is 0, by
design (no repeats). Rahul's repeat-traffic set will measure it fairly.

**Status:** `tokenomics/response_cache.py`, inside the gateway.

---

## 8. FAQ shortcut ✅ built; waiting for approval

**Attacks:** common questions, from the **first** time they're asked (a cache helps only from
the second).

**How it works:** 22 answers to top questions, written in advance from the documents. They reach
customers without any model checking them, so **a person must approve each one**; until then
nothing is served. A question qualifies only if it clearly matches one FAQ (≥ 0.75 and clearly
closer than any other), has no numbers, is a single question, and names no specific product.

**Measured:** 3 of 64 dev questions answered, in **~8 ms instead of ~3 s**, with **0 wrong
matches**: −3.8% tokens on a deliberately hard question set (real traffic has more FAQs).

**Status:** `tokenomics/faq.py` (matcher) + `techstore/data/faq.jsonl`; waiting for Rahul's
approval (`techstore/FAQ_REVIEW.md`).

---

## 9. Conversation memory ✅ built; quality checked

**Attacks:** conversation history. Every new message is sent with the whole chat so far:

```
Turn 1:  [instructions][Q1]                              678 tokens
Turn 4:  [instructions][Q1][A1][Q2][A2][Q3][A3][Q4]       983 tokens
Turn 6:  ...                                            1,191 tokens   (+~100 per turn)
```

**How it works:** keep the last 2 exchanges word for word; shrink older ones by
- **window:** drop them (free; forgets early details),
- **facts:** a note of earlier questions plus every order number, amount and date (free),
- **summary:** a short Luna summary, **rolling** (each old turn summarised once, never redone).

**Measured:** input stays **flat at ~880 tokens** after turn 3; turn 6 already −26%. Projected
**−24% over a 10-turn chat, −46% over 20**.

**Real runs (8 chats, 36 turns, Sol, 2026-11-25):** **no context lost** in any mode. On these
short 4–6-turn chats it saved almost nothing (−4% to +1%): trimming starts late, and an
untrimmed chat gets reused by provider caching.

**Status:** `techniques.apply_memory`; TechStore is multi-turn. Available, but **off by default**:
for chats the cache layout (§10) is the default, and the two can't be combined yet (trimming
rewrites the beginning). Later: trim only every N turns ("compaction").

---

## 10. Provider prompt caching ✅ verified; cache layout is the chat default

**Attacks:** the price of repeated prompt beginnings (tokens unchanged, cost lower).

**OpenAI's rules for GPT-6:** a prompt of 1,024+ tokens that starts exactly like one sent in
the last 30 minutes has the repeated part billed at **0.05×** on Sol (0.1× on Luna). But
**writing** a prompt into that cache costs **1.25×**, so it pays only if what's written is reused.

**Findings:**
- **Single questions: no effect.** Our prompts (~600–900 tokens) are under the 1,024 minimum,
  which is why October showed 0 cached tokens.
- **A hidden risk:** in long chats our classic layout puts each turn's documents near the top,
  so the beginning changes every turn. Prompts would be written at 1.25× and never reused: up
  to **+22% for nothing**.
- **The fix, a cache layout:** fixed instructions first, the conversation exactly as sent, this
  turn's documents last, so each turn starts exactly like the previous one.

**Simulated with our real prompts (3 chats of 13–14 turns), input cost:**

| Setup | Tokens | If writes are billed | If writes are free |
|---|---|---|---|
| Classic layout | 59,970 | **+22%** | 0% |
| Classic + facts memory | 42,435 | −22% | −29% |
| **Cache layout** | 176,581 (3×) | **−31%** | **−42%** |

**Two lessons:** techniques **interact** (trimming memory changes the beginning and blocks cache
reuse), and **the cheapest setup sends the most tokens**, which is why cost, not tokens, is the
headline measure.

**Real runs (2026-11-25):** caching is on by default in Chat Completions, and usage reports
both cached and written tokens. The simulator was within 1% of the real bill. On 2 long chats
(13 turns each, Sol): classic paid **+14%** for writes never reused; the **cache layout cost
26.5% less and got 26/26 turns right vs 23/26**. Classic made the agent **take back its own
correct earlier answers** when a turn's documents no longer held the policy it had quoted; the
cache layout keeps earlier documents in the conversation.

**Status:** **cache layout is the default for chats** (CLI `--conversations`, the demo) when
memory is off; single questions keep the classic layout their 64-question results used.

---

## 11. Batch API ⏳ not built

**Attacks:** the price of non-urgent work: OpenAI charges **50% less** for requests sent in bulk
with answers within hours. Not for live chat, but ideal for our own test runs and the final
benchmark. Built when credits return.

---

## 12. Spending limits ✅ built

**Attacks:** runaway or excessive spending. No single answer gets cheaper; the total gets a ceiling.

**How it works:** like a prepaid balance, checked **before** each call (Langfuse only records after):

| Situation | Action |
|---|---|
| Whole app over $5 today | Stop everything, scripts included |
| A client past 80% of its daily budget | Switch to Luna (still answered, 20× cheaper) |
| A client at its budget | Polite refusal, no model call, $0 |
| More than 20 messages a minute | "Please wait a moment" |

**Measured (mock):** a looping bug was stopped at $1 (10,000 overnight calls would have cost
≈ $29); a 120-question visitor got 17 Sol answers then 103 on Luna and never exceeded the budget.

**Status:** `tokenomics/spending_limits.py`, in the agent and the gateway.

---

## 14. Model routing ✅ built; evaluated on real answers (replay)

**Attacks:** the **price per token**, the biggest lever: Sol costs 20× more than Luna.

**What the data said first:** Luna was **never wrong** on the 64 dev questions (57–62 correct, the rest
partial, over 7 graded runs), including the billing and API questions we expected to need Sol. Its weak answers
had visible patterns: a refusal line before a real answer, or "I don't have information" when the documents had it.

**How it works (cheap-first):**
1. **Choose:** Luna, unless a hard rule says Sol: code in the question, a very long question, tools or a strict
   JSON schema, or a chat that escalated in its last 3 turns.
2. **Check Luna's answer:** warning signs (a refusal line followed by an answer, hedging such as "I'm not sure",
   too short for a "compare/explain" question, unfinished or repeated text). If they add up to 0.5 or more,
   **ask Sol once** and pay for both. No escalation when the answer was cut off by the length limit, when it is
   a plain refusal (Sol would refuse too), or when the spending limit would be crossed.

**Measured for free (replay of real, graded answers; 6 run pairs × 64 questions):**

| Arm | Cost vs always-Sol | Correct (of 64) | Sent to Sol |
|---|---|---|---|
| Always Luna | −93% | 60–62 | 0 |
| **Router** | **−88% to −92%** | **62–64, 0 wrong** | 1–3 |
| Random, same number to Sol | −89% to −92% | 60–62 | 1–3 |
| Oracle (knows the grades) | −87% to −91% | 64 | 2–4 |

**The honest reading:** most of the saving is "Luna is good enough here"; the router is a cheap safety net
(+1–2% cost) that repairs the weak answers it can see. A "careful" setting reaches 64/64 everywhere but costs
~3.5× more (it escalates on a phrase that is usually legitimate). The checks were designed on the dev answers, so
the fair number comes from Rahul's fresh test questions.

**Status:** `tokenomics/routing.py`; `--model auto` in TechStore (CLI and demo), `"model": "auto"` in the
gateway; `routing_replay.py`. A live run is in `techstore/runs/PENDING_CREDITS.md` (row 10).

---

## The gateway: how the techniques reach any app ✅ built

Not a technique itself but the delivery vehicle. An app changes two settings (the server address
and a Tokenomics key) and its requests flow through:

```
key check → cache (free answers) → memory trimming → spending limits → provider → true cost recorded
```

Proven end to end with TechStore: repeated questions came back free in 4–14 ms, order questions
were never cached, and limit refusals reached the customer as a polite message.
(`tokenomics/gateway.py`, docs in `tokenomics/README.md`.)

## What makes the savings trustworthy

- **Langfuse:** every request's tokens and cost, matching our files to the cent.
- **Automatic quality check:** each new answer compared with an already-graded one; unchanged
  answers keep their grade and only changed ones are graded (`quality_check.py`).
- **Mock mode:** the whole system runs and is tested without spending anything.

---

## Summary

| # | Technique | Part of the bill | Saving (measured or simulated) | Status |
|---|---|---|---|---|
| 1 | Shorter instructions | Input, every call | −16% tokens, −15% cost per correct (Sol) | ✅ Default |
| 2 | Reasoning control | Hidden output | Luna output −65%; −35% cost per correct; small quality dip | ✅ Simple questions only |
| 3 | Answer-length control | Visible output | `verbosity=low`: Sol −5.5% cost, 64/64 | ✅ Default |
| 4 | Sentence trimming | Documents | −13% doc tokens but lost facts | ❌ Rejected |
| 5 | Adaptive context | Documents | Sol −12.4% cost, 64/64 (−16% with #3) | ✅ Default |
| 6 | Prompt compression | Documents | — | ❓ Mentor |
| 7 | Safe response cache | Repeated questions | = repeat rate; 45/45 safety | ✅ Built |
| 8 | FAQ shortcut | Common questions | −3.8% tokens on a hard set; 8 ms | ✅ Awaiting approval |
| 9 | Conversation memory | Chat history | −24% at 10 turns, −46% at 20 (simulated); no context lost | ✅ Available, off |
| 10 | Prompt caching | Price of repeats | Cache layout −26.5% on long chats (real), 26/26 | ✅ Chat default |
| 11 | Batch API | Price, offline work | −50% on test runs | ⏳ |
| 12 | Spending limits | Runaway total | Caps the bill ($29 bug → $1) | ✅ Built |
| 14 | **Model routing** (cheap-first + escalation) | **Price per token** | −88% to −92% cost vs always-Sol, 0 wrong (replay) | ✅ Built; live run pending |

Techniques 1–12 mostly cut **tokens**; together their saving is meaningful but moderate (Sol −16% from
adaptive context + `verbosity=low`). **Routing** attacks the largest lever, the **20× price gap** between Sol
and Luna: on the dev set it cut cost ~90% with no wrong answers, because Luna turned out good enough for almost
every question. Rahul's fresh test questions will show whether that holds on questions nobody tuned for.
