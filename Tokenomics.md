# Project Master Specification: LLM Cost-Optimized Model Router
 
**Project Title**: Cost/Latency Optimised Model Router (LLM Cost-Optimized Model Router)  
**Track**: AI/ML Infrastructure, LLM Cost Engineering & Model Routing (AI-11)  
**Authors**: Kanishk Vikram Singh, Rahul Kumar  
**Target Delivery**: 6–8 Week Core Build expanded into a full 12-Week Production-Grade Roadmap  
**Repository**: [`kanishksingh23/Tokenomics`](https://github.com/kanishksingh23/Tokenomics)  
**License**: MIT (see [§9](#licensing--distribution-strategy))  
**Spec Version**: 2.7 — product catalogue for category questions; knowledge base freed of claims about real-world law  

---

## Table of Contents

1. [Executive Summary & Core Mission](#1-executive-summary--core-mission)
2. [The Fundamental Problem & Mathematical Reality](#2-the-fundamental-problem--mathematical-reality)
   - [Sensitivity Analysis & the Committed Claim](#sensitivity-analysis-why-we-commit-to-4060-not-67)
   - [Tier-Pair Selection: Cheapest ≠ Best](#-tier-pair-selection-why-the-cheapest-economy-model-is-not-the-best-one)
   - [Open-Weight Models: Where They Fit](#open-weight-models-where-they-fit)
3. [System Architecture & The Three Core Layers](#3-system-architecture--the-three-core-layers)
   - [Layer 1: Two-Tier Caching System (Exact & Semantic)](#layer-1-two-tier-caching-system)
   - [Layer 2: Dynamic Complexity Classification & Tier Selection](#layer-2-dynamic-complexity-classification)
   - [Layer 3: Confidence-Based Escalation (The Safety Net)](#layer-3-confidence-based-escalation)
4. [Production Infrastructure & Gateway Resilience](#4-production-infrastructure--gateway-resilience)
   - [Circuit Breaker Pattern & Jittered Exponential Backoff](#circuit-breaker-pattern)
   - [Token-Bucket Rate Limiter (Distributed Redis Lua)](#token-bucket-rate-limiter)
   - [SLA-Aware Multi-Provider Load Balancing](#sla-aware-load-balancing)
   - [SSE Streaming Pass-Through Engine](#sse-streaming-pass-through-engine)
5. [The Learning Loop: Offline Policy Retraining](#5-the-learning-loop-offline-policy-retraining)
6. [Observability, Metrics & Telemetry Stack](#6-observability-metrics--telemetry-stack)
   - [Per-Request Accounting Ledger](#per-request-accounting-ledger)
   - [Prometheus Instrumentation & Grafana Dashboard](#prometheus-instrumentation--grafana-dashboard)
   - [OpenTelemetry Distributed Tracing (Jaeger)](#opentelemetry-distributed-tracing)
7. [The Proof Engine: Benchmark & Evaluation Suite](#7-the-proof-engine-benchmark--evaluation-suite)
   - [Dual-Track Evaluation Corpora](#dual-track-evaluation-corpora)
   - [The Five-Arm Comparative Harness](#the-five-arm-comparative-harness)
   - [Statistical Protocol: Non-Inferiority by TOST](#statistical-protocol-non-inferiority-by-tost)
8. [Competitive Landscape & Market Differentiation](#8-competitive-landscape--market-differentiation)
9. [Selected Use Case: AI Customer Support Agent](#9-selected-use-case-ai-customer-support-agent)
   - [What TechStore Is — and Is Not](#-what-techstore-is--and-what-it-is-not)
   - [Phase 0: The TechStore Support Agent](#phase-0-the-techstore-support-agent-built-first)
   - [The Three Datasets](#the-three-datasets-these-are-routinely-confused)
   - [Demonstration Strategy & Demo Script](#demonstration-strategy)
   - [Licensing & Distribution Strategy](#licensing--distribution-strategy)
10. [End-to-End 12-Week Phased Delivery Roadmap](#10-end-to-end-12-week-phased-delivery-roadmap)
11. [Repository Structure & GitHub Setup](#11-repository-structure--github-setup)
12. [Critical Engineering Nuances & FAQs](#12-critical-engineering-nuances--faqs)
13. [Failure Semantics, Edge Cases & Degradation Policy](#13-failure-semantics-edge-cases--degradation-policy)
14. [Total Cost of Ownership & Project Budget](#14-total-cost-of-ownership--project-budget)

---

# 1. Executive Summary & Core Mission

The **LLM Cost-Optimized Model Router** is an intelligent, high-throughput API gateway built with Python and FastAPI. It sits transparently between client applications and heterogeneous LLM providers (e.g., OpenAI, Anthropic, open-source endpoints).

### The Mission
To automatically inspect, classify, and route incoming requests to the cheapest model capable of answering them accurately, backed by empirical proof: **a 40–60% total reduction in inference expenditure against an always-use-frontier baseline, with response quality demonstrated non-inferior by a pre-registered equivalence test (TOST, margin $\delta = 0.25$ on a 5-point scale).**

> **Claim discipline.** We never claim "no quality loss because $p > 0.05$." That is an absence of evidence, not evidence of absence. We claim *demonstrated non-inferiority within a declared margin*. See [§7](#statistical-protocol-non-inferiority-by-tost).

### What the Router Is and Isn't
* **It is NOT a simple reverse proxy or load balancer**: It does not merely distribute traffic round-robin or blindly relay prompts.
* **It is NOT a consumer-facing web application**: It is an infrastructure-grade API service exposing a standard OpenAI-compatible endpoint (`/v1/chat/completions`).
* **It IS an active decision system**: For every single query, it checks semantic similarity, evaluates prompt complexity, verifies output confidence, initiates fallback during outages, and optimizes its own routing policy over time using historical performance data — including deliberate exploration so that the policy keeps learning rather than ratcheting.

### The Four Claims We Defend
| # | Claim | Instrument of Proof |
|:--|:---|:---|
| C1 | 40–60% cost reduction vs. always-frontier | Five-arm benchmark, both arms actually executed ([§7](#the-five-arm-comparative-harness)) |
| C2 | Quality non-inferior within $\delta = 0.25$ | Pre-registered TOST + objective-ground-truth tracks |
| C3 | Routing overhead $< 20$ ms at P95 | Single-embedding pipeline, traced end-to-end ([§6](#opentelemetry-distributed-tracing)) |
| C4 | Safe under provider failure and cache collision | Chaos suite + cache-safety test suite ([§13](#13-failure-semantics-edge-cases--degradation-policy)) |

---

# 2. The Fundamental Problem & Mathematical Reality

### The Pricing Asymmetry
In production environments, engineering teams face a false trilemma between cost, latency, and capability. Market pricing per 1M tokens, October 2026:

| Class | Model | Input | Output | Cost / typical request* | Source |
|:---|:---|---:|---:|---:|:---|
| **Frontier** | GPT-6 Astra | \$10.00 | \$50.00 | \$0.011500 | OpenAI pricing page ✔ |
| **Frontier** | Claude Fable 5.1 | \$10.00 | \$50.00 | \$0.011500 | Anthropic list price |
| **Frontier** | Claude Opus 5 | \$5.00 | \$25.00 | \$0.005750 | Anthropic list price |
| **Frontier** ⭐ | **GPT-6.1 Sol** | **\$2.00** | **\$10.00** | **\$0.002300** | **OpenAI pricing page ✔** |
| Mid | Claude Sonnet 5 | \$2.00 | \$10.00 | \$0.002300 | Anthropic list price |
| **Economy** | Claude Haiku 4.5 | \$1.00 | \$5.00 | \$0.001150 | Anthropic list price |
| **Economy** | Gemini 3.8 Flash | \$0.75 | \$3.75 | \$0.000862 | third-party, Sept 2026 |
| **Economy** | DeepSeek V3.1 (open) | \$0.60 | \$1.70 | \$0.000495 | third-party, Sept 2026 |
| **Economy** | Llama 3.3 70B / Groq (open) | \$0.59 | \$0.79 | \$0.000354 | third-party, Sept 2026 |
| **Economy** ⭐ | **GPT-6 Luna** | **\$0.10** | **\$0.50** | **\$0.000115** | **OpenAI pricing page ✔** |
| **Economy** | Llama 3.1 8B / Groq (open) | \$0.05 | \$0.08 | \$0.000032 | third-party, Sept 2026 |

\* 400 prompt tokens + 150 completion tokens — the representative support request used throughout this document. **This figure is only achievable with retrieval; see below.**

**Selected pair: GPT-6.1 Sol (frontier) + GPT-6 Luna (economy).** Both model ids are confirmed on the project's OpenAI account (Limits page) and both prices on OpenAI's official pricing page, 2026-10-03. The economy choice is re-tested empirically in Week 7 (below). **Measured latency** (50 real support questions, 2026-10-03): GPT-6.1 Sol median **2.9 s**, p90 **5.0 s** — slower than the 1.2–2 s assumed in earlier revisions. GPT-6 Luna's latency is not yet measured (Week 7).

> **Naming convention.** We say **Economy** and **Frontier** throughout, never "Tier 1 / Tier 2" — readers reflexively parse "Tier 1" as *best*, which inverts the meaning. Code uses the enum `ModelTier.ECONOMY | ModelTier.FRONTIER`.
>
> **Pricing details that matter.** *Cached input* bills at 5–10% of input, but *writing* a prompt into OpenAI's cache costs 1.25× input, and our only stable prefix (the 170-token system prompt) is likely below the caching threshold — so no saving is budgeted from caching. *Batch* and *Flex* tiers are 50% of standard: every benchmark run uses Batch. *Long-context* rates (double) apply only above ~272K prompt tokens; ours are ~500. Gemini 3.8 Flash's price is introductory and doubles on 1 Jan 2027, mid-evaluation — one reason it is not selected. Authoritative prices live in `techstore/config.py` (later `app/providers/pricing.yaml`) with a mandatory `as_of` date; CI fails if it is more than 90 days old.

### The Traffic Reality
In real-world enterprise traffic, **60% to 80% of queries are routine**:
* Factual lookups, FAQ queries, status inquiries
* Summaries of clean text, basic reformatting, boilerplate code
* Categorization, simple sentiment detection

Sending 100% of queries to the Frontier tier wastes budget. Sending 100% to the Economy tier degrades user experience and introduces hallucinations.

> **A note on how this argument has  changed.** Economy-tier models in 2026 are dramatically more capable than the 2024 generation. This cuts both ways: our escalation rate $\gamma$ should be *lower* than historical routing work reports, but our **always-economy baseline arm is correspondingly stronger**. The naive objection — *"why not just use the cheap model for everything?"* — is now the serious one, and it is answered not by the aggregate saving but by the specific stratum of queries where economy fails and our escalation layer catches it. See [§7](#the-five-arm-comparative-harness).

### The Cost Reduction Equation
Let $N$ be total queries, $C_f$ the cost of a frontier call, $C_e$ the cost of an economy call, $\alpha$ the cache hit ratio, $\beta$ the proportion routed directly to economy and *accepted*, $\gamma$ the escalation rate (economy attempted, then escalated to frontier), and $\delta$ the proportion routed directly to frontier:

$$\text{Total Cost} = N \cdot \left[ 0 \cdot \alpha + C_e \cdot \beta + (C_e + C_f) \cdot \gamma + C_f \cdot \delta \right], \qquad \alpha + \beta + \gamma + \delta = 1$$

**Deriving the price ratio $\rho = C_e / C_f$ (this assumption must be stated, not smuggled in):**

| | Input | Output | Total |
|:---|:---|:---|:---|
| Frontier — GPT-6.1 Sol @ \$2 / \$10 | $400 \times 2.0\text{e-}6 = \$0.000800$ | $150 \times 10.0\text{e-}6 = \$0.001500$ | $\mathbf{\$0.002300}$ |
| Economy — GPT-6 Luna @ \$0.10 / \$0.50 | $400 \times 0.1\text{e-}6 = \$0.000040$ | $150 \times 0.5\text{e-}6 = \$0.000075$ | $\mathbf{\$0.000115}$ |

$$\rho = \frac{C_e}{C_f} = \frac{0.000115}{0.002300} = \mathbf{0.050} \qquad \text{(a 20}\times\text{ spread)}$$

Normalising by $C_f$, the **Router Cost Ratio** is:

$$R = \rho\beta + (1 + \rho)\gamma + \delta$$

### ⚠ The 400-Token Assumption Requires a Retriever

The cost model above rests on a ~400-token prompt, and that number is **not free** — it presupposes that only the *relevant* knowledge-base documents reach the model. Earlier revisions of this specification never stated a retrieval component, which silently left the alternative open:

| How the knowledge base reaches the model | Prompt tokens | Cost/req (Sol) | One 500-query arm |
|:---|---:|---:|---:|
| **Retrieve top-3 relevant documents** | ~507 (measured) | \$0.00251 | **\$1.26** |
| Concatenate all 85 documents into every prompt | ~7,659 (measured) | \$0.01682 | **\$8.41** |

Full-context concatenation is **7× more expensive** at today's 85 documents, and the multiplier grows with every document added — a real retailer's knowledge base runs to thousands. The price ratio is unaffected, because both tiers pay the same inflated input, so the extra cost is invisible in the savings percentage and large in the absolute bill. *(Revision v2.2 stated 21×, from an unmeasured word-count estimate; 7× is measured with the real tokenizer.)*

**Therefore retrieval is a required component of the application layer**, specified in [§9](#phase-0-the-techstore-support-agent-built-first) and guarded by `techstore/tests/test_agent.py::test_prompt_stays_within_budget`.

**Measured correction**: on the first real run (50 questions, 2026-10-03) the agent sent **639 prompt tokens** and received **93 output tokens** per question on average — more input than the 400 assumed here (the refusal rules lengthened the system prompt) but less output than 150, so measured cost was **\$0.0022 per question** against \$0.0023 projected. Before the refusal rules it sent ~507. $\rho$ is unchanged at 0.050 (both tiers scale together; the 40–60% claim is unaffected) but absolute cost per request is ~9% higher. Figures in this document retain 400 for arithmetic legibility; the benchmark report uses measured values. **Re-measure once the full 500-question corpus exists.**

### Sensitivity Analysis (why we commit to 40–60%, not 67%)

| Scenario | $\alpha$ | $\beta$ | $\gamma$ | $\delta$ | $R$ | Reduction |
|:---|:--|:--|:--|:--|:--|:--|
| Optimistic (high cacheability, accurate classifier) | 0.10 | 0.60 | 0.05 | 0.25 | 0.333 | **66.8%** |
| **Expected (planning target)** | 0.08 | 0.55 | 0.07 | 0.30 | 0.401 | **59.9%** |
| Conservative (low cache hit, cautious classifier) | 0.05 | 0.45 | 0.10 | 0.40 | 0.528 | **47.2%** |
| Pessimistic (adversarial traffic mix) | 0.03 | 0.35 | 0.12 | 0.50 | 0.643 | **35.7%** |

**Result**: The committed headline claim is **40–60%**, which brackets the Expected and Conservative scenarios. The optimistic 67% is reported as a ceiling, never as the promise. Under-promising here is strategically correct: the benchmark only has to clear a bar we are confident of clearing.

### ⚠ Tier-Pair Selection: Why the Cheapest Economy Model Is Not the Best One

**The choice of model pair determines whether the headline claim is achievable at all — independently of code quality.** Two current, perfectly reasonable models can sit so close in price that no routing strategy can reach 40%:

| Frontier / Economy pair | $\rho$ | Spread | Reduction (Expected scenario) |
|:---|---:|---:|---:|
| GPT-6 Astra / GPT-6 Luna | 0.010 | 100× | 62.4% ✅ |
| Claude Opus 5 / GPT-6 Luna | 0.020 | 50× | 61.8% ✅ |
| **GPT-6.1 Sol / GPT-6 Luna** | **0.050** | **20×** | **59.9% ✅** |
| GPT-6 Astra / Gemini 3.8 Flash | 0.075 | 13× | 58.4% ✅ |
| Claude Fable 5.1 / Claude Haiku 4.5 | 0.100 | 10× | 56.8% ✅ |
| Claude Opus 5 / Claude Haiku 4.5 | 0.200 | 5× | 50.6% ✅ |
| **Claude Sonnet 5 / Claude Haiku 4.5** | **0.500** | **2×** | **32.0% ❌ fails the claim** |
| **GPT-6.1 Sol / Claude Haiku 4.5** | **0.500** | **2×** | **32.0% ❌ fails the claim** |

Had we paired Sonnet 5 with Haiku 4.5 — both current, both defensible choices — the project would return 32% with a flawless implementation, and the cause would have been invisible. The last row matters for **failover design**: if the economy provider fails and economy traffic falls back to Claude Haiku while the frontier stays on Sol, the price gap collapses to 2× and savings fall below the claim. Cross-provider failover must therefore move *both* tiers together (Sol+Luna → Opus 5+Haiku 4.5, 50.6%), never one tier alone.

**But price spread is only half the story, and it is the half you can look up.** A cheaper economy model escalates more often, and every escalation pays *both* tiers. Holding the frontier at GPT-6.1 Sol:

| Economy candidate | \$/req | $\rho$ | Spread | @ $\gamma$=5% | @ $\gamma$=10% | @ $\gamma$=20% |
|:---|---:|---:|---:|---:|---:|---:|
| Llama 3.1 8B (Groq) | \$0.000032 | 0.014 | 72× | **64.1%** | 59.1% | 49.1% |
| **GPT-6 Luna** | \$0.000115 | 0.050 | 20× | 61.9% | 56.9% | 46.9% |
| Llama 3.3 70B (Groq) | \$0.000354 | 0.154 | 6.5× | 55.4% | 50.4% | 40.4% |
| DeepSeek V3.1 | \$0.000495 | 0.215 | 4.6× | 51.7% | 46.7% | 36.7% |
| Gemini 3.8 Flash | \$0.000862 | 0.375 | 2.7× | 41.8% | 36.7% | 26.8% |
| Claude Haiku 4.5 | \$0.001150 | 0.500 | 2.0× | 34.0% | 29.0% | 19.0% |

**Read across the rows, not down the first column.** Llama 3.1 8B at $\gamma$=20% (49.1%) is *worse* than GPT-6 Luna at $\gamma$=5% (61.9%), despite being 3.6× cheaper per token. **Escalation rate dominates price ratio.** The cheapest model is the best choice only if it is also good enough to rarely need escalating — an empirical question, not a pricing-page lookup.

A second effect of the GPT-6 generation: because Sol now costs half what its predecessor did, every *other* economy model is relatively more expensive beside it. Llama 3.3 70B's advantage shrank from 13× to 6.5×, and DeepSeek and Gemini Flash fall below 5× — too narrow to be worth testing.

**Therefore the tier pair is measured, not assumed.** `benchmarks/select_tier_pair.py` (Week 7, ~\$1, one afternoon) runs the 50-query development subset against three economy candidates — GPT-6 Luna, Llama 3.3 70B via Groq, and Llama 3.1 8B via Groq — reporting for each the realised $\gamma$, the resulting saving, and quality. The winner is adopted and the table above is republished with measured rather than projected columns.

### Open-Weight Models: Where They Fit

Open models (Llama, Qwen, DeepSeek, Mistral) appear in this project in three distinct roles, and conflating them is a mistake:

| Role | Decision | Rationale |
|:---|:---|:---|
| **Development backend** (Ollama, local) | ✅ **Adopt** | Weeks 1–9 test that requests flow, caches hit, breakers trip — none of which needs a frontier model. Reduces development API spend to ~zero and exercises the provider abstraction against a genuinely different backend. |
| **Hosted economy tier** (Groq / Together / Fireworks) | ✅ **Candidate** — decided by the Week 7 experiment | Real per-token pricing preserves the cost claim; open weights are permanently reproducible, unlike a closed model that may be deprecated or repriced. Against GPT-6.1 Sol, only Llama 3.1 8B remains clearly cheaper than GPT-6 Luna. |
| **Fully local benchmark** (both tiers on-device) | ❌ **Reject** | **The project's claim is denominated in dollars.** A locally-hosted model has no marginal per-token price, so the headline result degenerates to "60% of \$0". Restating it in GPU-seconds is weaker, harder to measure honestly, and unrelatable to the stakeholder audience the use case was chosen for. Separately, a student-grade GPU cannot host a genuinely frontier-class open model, so the quality gap that justifies routing would not exist. |

**Reproducibility dividend**: retaining at least one open-weight tier means a third party can re-run our benchmark in three years against identical weights. Closed frontier models carry no such guarantee. This is stated as an explicit advantage in the benchmark report.

### The Escalation Break-Even (a result that reframes the whole design)
Trying the economy model first and escalating with probability $p$ costs $C_f(\rho + p)$ in expectation. This beats always-frontier whenever:

$$\rho + p < 1 \quad \Longrightarrow \quad p < 1 - \rho = \mathbf{0.95}$$

**On cost alone, cheap-first is almost always correct.** The binding constraint is *latency*. With the measured frontier median $L_f = 2900$ ms and an assumed $L_e = 300$ ms (economy latency is not yet measured), expected latency $L_e + p \cdot L_f < L_f$ requires:

$$p < 1 - \frac{L_e}{L_f} = \mathbf{0.897} \quad \text{(provisional until } L_e \text{ is measured)}$$

and the P99 tail is far tighter still, because an escalated request pays *both* latencies serially.

**Design consequence**: the classifier threshold is **not** a cost-optimisation parameter. It is a point on a cost–latency–quality Pareto frontier, and it must be *derived from an SLA*, not hardcoded at 0.50. `benchmarks/tune_threshold.py` sweeps $\tau \in [0.2, 0.8]$ and emits the frontier plot; we then select $\tau$ as the cheapest point whose P95 latency is **no worse than the always-frontier baseline's** and whose quality is within the TOST margin. *(Earlier revisions used an absolute P95 ≤ 2,000 ms target; GPT-6.1 Sol alone measures p90 5.0 s, so an absolute target that the baseline itself misses would be meaningless.)*

---

# 3. System Architecture & The Three Core Layers

```
                           +------------------------+
                           |   Client Application   |
                           +-----------+------------+
                                       | POST /v1/chat/completions
                                       v
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FASTAPI ROUTING GATEWAY                           │
│                                                                              │
│  [ Step 0: Auth (API key -> client_id) & Idempotency Check ]                │
│                      │                                                      │
│  [ Step 1: Token-Bucket Rate Limiter ] ─── (Reject 429 if quota exceeded)   │
│                      │                                                      │
│                      ▼                                                      │
│  [ Step 2: Exact-Match Cache (Redis) ] ─── (Hit? Return response in <1ms)   │
│                      │                                                      │
│                      ▼                                                      │
│  [ Step 3: SHARED EMBED (MiniLM, computed ONCE) ]  ~11ms                    │
│                      │                                                      │
│         ┌────────────┴────────────┐                                         │
│         ▼                         ▼                                         │
│  [ Step 3a: Semantic Cache ]   [ Step 4: Complexity Classifier ]            │
│   + Entity Admission Gate       ├── Fast Rule Filter (<0.1ms)               │
│   (Hit? Return in <3ms)         └── MLP head on shared vector (~1ms)        │
│                      │                                                      │
│                      ▼                                                      │
│         ┌────────────┴────────────┐                                         │
│         ▼                         ▼                                         │
│   [ Score < τ ]              [ Score >= τ ]                                 │
│     Economy                    Frontier                                     │
│         │                         │                                         │
│         ▼                         │    (+ context-window feasibility filter) │
│  [ Provider Execution ]           │                                         │
│   (with Circuit Breaker)          │                                         │
│         │                         │                                         │
│         ▼                         │                                         │
│  [ Step 5: Uncertainty Checker ]  │                                         │
│    Signals: Logprobs, Hedging,    │                                         │
│      Length, Repetition, Struct   │                                         │
│    + finish_reason & refusal guards│                                        │
│    + latency-budget guard          │                                        │
│         │                         │                                         │
│    ┌────┴────┐                    │                                         │
│   PASS      FAIL (Escalate)       │                                         │
│    │         │                    │                                         │
│    │         ▼                    │                                         │
│    │     [ Retry on Frontier ] ───┘                                         │
│    │         │                                                              │
│    ▼         ▼                                                              │
│  [ Step 6: Telemetry Ledger & Cache Store ]                                 │
│    - Record Tokens, Latency, Real Cost vs Calibrated Baseline               │
│    - Populate Redis & ChromaDB (subject to admission policy)                │
│    - Export OpenTelemetry Spans & Prometheus Metrics                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       v
                           +------------------------+
                           | Response + X-Router-*  |
                           +------------------------+
```

> **Key architectural change from v1**: the `all-MiniLM-L6-v2` embedding is computed **exactly once** per request in `app/embeddings.py` and handed to both the semantic cache and the complexity classifier. v1 computed it twice (~11 ms + ~12 ms). This alone halves routing overhead and is the difference between hitting and missing claim C3.

---

## Layer 1: Two-Tier Caching System

The cheapest and fastest LLM call is the one that is never made. Caching reduces cost to \$0.00, cuts latency to <15ms, and preserves provider rate limits.

### Tier 1A: Exact-Match Cache (Redis)
* **Underlying Engine**: In-memory Redis 7+ using atomic GET/SET operations.
* **Lookup Overhead**: sub-millisecond (~0.5ms).
* **Hash Fingerprint Generation**: SHA-256 computed over **every field that can change the response**:

$$\text{Key} = \text{"cache:exact:"} + \text{tenant} + \text{":"} + \text{SHA256}\big(\text{canonical}(messages) \,\|\, \text{routing\_profile} \,\|\, T \,\|\, \text{top\_p} \,\|\, \text{max\_tokens} \,\|\, \text{stop} \,\|\, \text{seed} \,\|\, \text{tools} \,\|\, \text{tool\_choice} \,\|\, \text{response\_format}\big)$$

  **Two corrections against the v1 key, both of which were correctness bugs:**
  1. **`tools`, `tool_choice`, `response_format`, `max_tokens`, `stop` and `seed` are now included.** v1 hashed only model + messages + temperature + top_p + system prompt. Two requests with identical messages but different `tools` arrays have *completely different* correct responses; v1 would have served one for the other. Since we expose an OpenAI-compatible endpoint, clients *will* send these fields.
  2. **The client's `model` field is replaced by a `routing_profile` identifier.** If the chosen model were part of the key, an economy-served response could never be reused for a request the router would have sent to frontier — which defeats the purpose. The cache keys on *what was asked*, not *who answered*. The served model is stored in the value and surfaced via `X-Router-Cache-Source-Model`.
* **Exclusion List**: Caller IP, API authentication tokens, timestamps, streaming format flags (`stream: true/false`), and request IDs are explicitly stripped before hashing.
* **Stochastic Guardrail (Temperature Handling)**:
  * $T \le 0.1$: Cached aggressively with TTL = 24 to 72 hours (deterministic).
  * $0.1 < T \le 0.4$: Cached with TTL = 1 to 4 hours.
  * $T > 0.4$: Caching is completely bypassed — the caller explicitly requested variety.
  * `n > 1` or `seed` absent with $T > 0$: bypass. Returning one sample where several were requested is a protocol violation.
* **Cache Stampede Protection (singleflight)**: On a cold key, $k$ concurrent identical requests would each miss and each hit the provider — paying $k\times$ for one answer. The first misser acquires `SET cache:lock:<key> <req_id> NX PX 5000`; losers poll the key for up to 2 s, then fall through to their own provider call (fail-open, never deadlock). Lock release is a Lua compare-and-delete so a slow request cannot free a successor's lock.
* **Serving a cache hit to a streaming client**: a `stream: true` request that hits cache must not return a monolithic body. The gateway re-chunks the cached text into synthetic SSE `data:` frames (~8 tokens per frame, ~4 ms apart) and terminates with `[DONE]`, so the client's parser sees a normal stream. Header `X-Router-Cache: exact` marks it.

### Tier 1B: Semantic Similarity Cache (ChromaDB + all-MiniLM-L6-v2)
Humans rarely formulate queries with identical strings. Semantic caching matches prompts based on vector similarity.

```
"What is the capital of France?"  ──► [0.023, -0.118, ..., 0.091]
                                              │  Cosine Distance: 0.03
"France's capital city?"          ──► [0.025, -0.112, ..., 0.088]
```

* **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
  * Dimension: 384. Local CPU inference (~10–15ms), footprint < 120MB, zero GPU.
  * **⚠ Hard limit: `max_seq_length = 256` word-pieces.** Anything beyond token 256 is silently **truncated**, so two long prompts that are identical for 256 tokens and then diverge completely will embed to the *same vector*. This is a real false-positive channel that v1 did not account for. Mitigation: prompts exceeding 256 word-pieces are (a) never admitted to the semantic cache, and (b) fingerprinted with a SHA-256 of the *tail* beyond token 256, which must match exactly for any candidate hit.
* **Vector Store**: ChromaDB configured with HNSW indexing and Cosine distance metric. (Beyond ~1M vectors, migrate to Qdrant or `pgvector`; the `VectorStore` interface is written so this is a one-file change.)
* **Threshold Calibration**:
  $$d(u, v) = 1 - \frac{u \cdot v}{\|u\|_2 \|v\|_2}$$
  * **$d < 0.04$**: Near-identical phrasing $\rightarrow$ Hit.
  * **$0.04 \le d \le 0.08$**: Semantically equivalent $\rightarrow$ Hit (default threshold `0.08`).
  * **$d > 0.08$**: Distinct intent $\rightarrow$ Miss.
  * The threshold is **calibrated, not assumed**: `benchmarks/calibrate_cache.py` builds a labelled set of 400 prompt pairs (200 truly-equivalent, 200 adversarial near-misses) and selects the $d$ maximising $F_\beta$ with $\beta = 0.5$ — i.e. **precision weighted double recall**, because a false hit is far worse than a missed hit.

### ⚠ Semantic Cache Admission Control (the most important safety control in the system)

A naive semantic cache is **actively dangerous** in the domain we chose. Consider two requests from *different customers*:

```
  "Where is my order #48213?"   →  embed  →  cache the answer
  "Where is my order #48217?"   →  embed  →  cosine distance ≈ 0.01  →  HIT
```

Customer B receives Customer A's order details. Neither v1 guardrail catches this: the system prompt is identical for both, and the token-length ratio is ~1.0. Given that **12% of our benchmark corpus is "Order Status & Account"**, this is not a theoretical concern — it is a live data-leak and correctness bug that a reviewer can trigger in thirty seconds at the demo.

Semantic cache admission therefore requires **all five** of the following to pass:

1. **Tenant / principal namespacing** — the ChromaDB collection is partitioned by `(tenant_id, system_prompt_hash, kb_version)`. A response is *never* eligible for reuse across principals. Cross-user reuse is opt-in per deployment and off by default.
2. **Entity-set equality gate** — extract the entity set $E(q)$ from the prompt via regex (digit runs $\ge 4$, order/invoice/ticket IDs, emails, phone numbers, currency amounts, dates) plus spaCy `en_core_web_sm` NER (`PERSON`, `ORG`, `GPE`, `MONEY`, `DATE`, `CARDINAL`). A candidate hit is invalidated unless $E(q_{\text{new}}) = E(q_{\text{cached}})$ **exactly**. If $E(q) \ne \varnothing$ and the intent is user-scoped, bypass the semantic cache entirely.
3. **Volatility blocklist** — intents whose correct answer is time-varying (order status, shipment tracking, account balance, stock level, current price, "today", "now", "latest") are tagged `no_semantic_cache` at classification time. A correct answer that is correct *only for 20 minutes* must not be stored for 24 hours.
4. **Negation & antonym guard** — MiniLM embeddings are famously weak on negation ("how to *enable* 2FA" vs "how to *disable* 2FA" sit at $d \approx 0.05$). Candidate pairs are rejected if their token sets differ by any member of a curated antonym/negation lexicon (`enable/disable`, `add/remove`, `reverse a string/reverse a list`, `not`, `without`, `except`, `cancel`, `undo`).
5. **Token length ratio sanity check** — invalidate if query token length deviates by $> 3.5\times$ from the matched document.

Every rejection increments `llm_cache_admission_rejected_total{reason="..."}`, so the Grafana dashboard shows exactly how often the safety net fires — which is itself a compelling demo artifact.

**Test obligation**: `tests/test_cache_safety.py` contains ≥40 adversarial pairs (order-number swaps, negation flips, tenant crossovers, 256-token-truncation collisions) and **CI fails on a single false positive**. This test file is, frankly, the most persuasive file in the repository.

---

## Layer 2: Dynamic Complexity Classification

Layer 2 determines whether a cache-miss query can be satisfied by an Economy model or requires Frontier.

```
                     Incoming Prompt
                           │
                           ▼
                ┌──────────────────────┐
                │ Context-Fit Filter    │ ── (Hard constraint, not a score)
                └──────────┬───────────┘
                           ▼
                ┌──────────────────────┐
                │   Fast Rule Filter    │ ── (Deterministic match in <0.1ms)
                └──────────┬───────────┘
                           │ Uncertain
                           ▼
                ┌──────────────────────┐
                │  MLP head on SHARED  │ ── (~1ms; vector already computed)
                │  MiniLM vector       │
                └──────────┬───────────┘
                           │ Complexity Score [0.0 - 1.0]
                           ▼
                 Score < τ ? Economy : Frontier
```

### Stage 0: Hard Feasibility Filters (run before any scoring)
Routing is a *constrained* optimisation. These are constraints, not preferences — they override the classifier unconditionally:
* **Context window fit**: if $\text{prompt\_tokens} + \text{max\_tokens} > 0.9 \times \text{ctx}(m_{\text{economy}})$, the economy tier is ineligible. Forcing a 150K-token prompt into a smaller-context model is a guaranteed 400, not a cheap answer.
* **Capability fit**: requests carrying `tools`/`tool_choice`, `response_format: json_schema`, or image content parts are routed by a **capability matrix** in the registry, not by complexity score. Economy models are materially worse at multi-tool selection; `tools` with $\ge 3$ functions routes Frontier by default (configurable).
* **Explicit client override**: a client sending a concrete `model` (not `auto`) is honoured verbatim. The router is opt-in; silently overriding an explicit model choice would be indefensible.

### Stage 1: Fast Rule Filter (<0.1ms)
Bypasses neural scoring for clear-cut extremes:
* **Definitely Simple (Score = 0.15)**: $< 15$ words, single factual interrogative (`what is`, `who is`, `when was`, `define`, `hours`, `status`), no code markers, no reasoning keywords.
* **Definitely Complex (Score = 0.85)**: markdown code fences, explicit multi-step reasoning triggers (`explain step by step`, `prove that`, `analyze the architectural tradeoffs`, `debug this concurrency lock`), or token count $> 250$.

### Stage 2: Neural Embedding Classifier (~1ms on the shared vector)
For the remaining ~65% of ambiguous traffic:
1. Reuse the `all-MiniLM-L6-v2` vector already computed at Step 3 of the pipeline. **No second forward pass.**
2. Feed the 384-d vector into a trained MLP with hidden layers $(128, 64)$ and ReLU activation.
3. Output a **calibrated** posterior $P(\text{requires\_frontier} \mid \text{embedding}) \in [0, 1]$. Calibration is not optional: raw MLP outputs are overconfident, so we fit **Platt scaling / isotonic regression** on a held-out split and report a reliability diagram plus Expected Calibration Error (ECE) in the benchmark report. An uncalibrated score makes the threshold $\tau$ meaningless.
4. If $P \ge \tau \rightarrow$ Frontier; else Economy. $\tau$ defaults to 0.50 but is **derived from the Pareto sweep** in [§2](#the-escalation-break-even-a-result-that-reframes-the-whole-design).

### Multi-Turn Conversation Handling (a gap v1 did not address)
Customer support is inherently multi-turn, but v1 implicitly treated every request as single-shot. Three rules:
1. **Classification input** is the last user message plus a 512-token rolling summary of prior turns — not the raw full transcript, which would push every conversation past the "definitely complex" token threshold by turn four.
2. **Sticky escalation**: once a conversation escalates to Frontier, subsequent turns in that `conversation_id` remain Frontier for a decay window of 3 turns. Quality oscillating mid-conversation (sharp answer, then a shallow one, then sharp again) is far more damaging to perceived quality than a uniformly cheaper tier.
3. **Semantic cache is disabled for turns $\ge 2$** unless the turn is self-contained (no anaphora: `it`, `that`, `the previous one`, `same as before`). A follow-up's meaning lives in the history, not the text.

---

## Layer 3: Confidence-Based Escalation

No classifier is infallible. If a complex query is misrouted to an economy model, returning a bad answer causes silent quality degradation. Layer 3 intercepts economy-tier outputs and evaluates **uncertainty** across 5 signals before returning them to the caller.

> **Naming correction.** v1 called the aggregate `C_composite` ("confidence") but defined every signal so that **high = bad**, then wrote the escalation rule in opposite directions in §3 and §10. We rename it $U_{\text{composite}}$ (**uncertainty**) throughout. High $U$ = low confidence = escalate. The word "confidence" never appears in the code.

### The 5 Uncertainty Signals

#### 1. Per-Token Log-Probabilities ($S_{\text{logprob}}$)
Where the provider supports it (OpenAI `logprobs=True`, `top_logprobs=0` — we need only the *chosen* token's logprob; requesting top-k inflates the response payload for no benefit):
$$S_{\text{logprob}} = \begin{cases} 1.0 & \mu_{\text{logprob}} < -1.8 \\ 0.5 & -1.8 \le \mu_{\text{logprob}} < -1.0 \\ 0.0 & \mu_{\text{logprob}} \ge -1.0 \end{cases}$$

#### 2. Hedging & Epistemic Uncertainty Markers ($S_{\text{hedge}}$)
```python
HEDGE_PATTERNS = [
    r"\bi('m| am) not (entirely|completely|totally)? sure\b",
    r"\bit (might|could|may) be\b",
    r"\bi (cannot|can't|am unable to) verify\b",
    r"\bas an ai language model\b",
    r"\bactually, (wait|let me reconsider)\b",
]
```
Normalized: $S_{\text{hedge}} = \min(\text{count} / 3.0, 1.0)$.

#### 3. Length & Depth Anomaly ($S_{\text{length}}$)
If the prompt demands structured output (`explain`, `compare`, `troubleshoot`) but the economy model emits $< 35$ tokens, $S_{\text{length}} = 0.90$.

#### 4. Repetition Loop Detection ($S_{\text{repeat}}$)
$$S_{\text{repeat}} = 1.0 - \frac{\text{Unique Sentences}}{\text{Total Sentences}}$$
Only evaluated when total sentences $\ge 4$; below that the statistic is too coarse to be meaningful and produces spurious 0.5s on two-sentence answers.

#### 5. Structural Completeness ($S_{\text{struct}}$)
Detects abrupt termination: missing terminal punctuation, unclosed quotes, open code fences, unbalanced JSON braces.

### Missing-Signal Renormalization (a bug in v1's arithmetic)
**Anthropic does not expose per-token logprobs.** On the Claude Haiku path $S_{\text{logprob}}$ is simply unavailable, so v1's maximum achievable score silently dropped from 1.00 to 0.70 — making the fixed 0.45 threshold roughly 40% stricter for Anthropic than for OpenAI, for no principled reason. Correct formulation over the available signal set $A$:

$$U_{\text{composite}} = \frac{\sum_{i \in A} w_i S_i}{\sum_{i \in A} w_i}$$

Default weights: $w_{\text{logprob}} = 0.30$, $w_{\text{hedge}} = 0.25$, $w_{\text{length}} = 0.20$, $w_{\text{repeat}} = 0.15$, $w_{\text{struct}} = 0.10$.

**A deliberate property worth stating explicitly**: with these weights, *no single signal can reach the 0.45 threshold alone* (the largest, hedging, maxes at 0.25). Escalation therefore requires **at least two independent signals to agree**. This is intentional — it is what keeps the false-escalation rate low, and it is why the weights are not uniform.

### Escalation Suppression Guards (edge cases that would otherwise burn money)
Escalation costs $C_e + C_f$ — *more* than never having tried. These four guards prevent escalations that cannot possibly help:

| Guard | Condition | Rationale |
|:---|:---|:---|
| **Truncation guard** | `finish_reason == "length"` | The answer is short because `max_tokens` cut it off, not because the model was uncertain. $S_{\text{struct}}$ and $S_{\text{length}}$ both fire spuriously. The frontier model would be truncated identically. **Suppress escalation; return as-is.** |
| **Refusal guard** | Response matches a safety-refusal pattern | A refusal trips the hedging regex (`as an AI language model`). The frontier model will refuse too. **Suppress; return the refusal.** |
| **Latency-budget guard** | $t_{\text{elapsed}} + \hat{L}_{f,P95} > \text{deadline}$ | Escalating would breach the client's SLA. Better a merely-acceptable answer on time than a great one after timeout. Log `escalation_skipped_budget`. |
| **Cost-ceiling guard** | Per-request or per-tenant spend cap reached | A hard financial circuit breaker. Log and return the economy answer with `X-Router-Degraded: cost-ceiling`. |

### The Composite Decision Function
**Action**:
* If $U_{\text{composite}} > 0.45$ **and** no suppression guard fires: the output is discarded and the query is re-executed on Frontier.
* The event is flagged `escalated: true` and logged with all signal values.
* The client receives the clean, authoritative frontier response without seeing the failed attempt.
* **Single escalation only.** There is no escalation chain; a frontier answer is terminal regardless of its own uncertainty score. Unbounded escalation is an unbounded bill.

---

# 4. Production Infrastructure & Gateway Resilience

```
                                 Client Request
                                       │
                                       ▼
                       ┌──────────────────────────────┐
                       │  Auth + Token-Bucket Limiter │
                       │    (Atomic Redis Script)     │
                       └──────────────┬───────────────┘
                                      │ Quota OK
                                      ▼
                       ┌──────────────────────────────┐
                       │   Circuit Breaker Manager    │
                       │   (OpenAI, Anthropic, etc.)  │
                       └──────────────┬───────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
     Provider Healthy                                 Provider Failing
  ┌──────────────────────┐                        ┌──────────────────────┐
  │ Execute Call with    │                        │ Fast Failover to     │
  │ Jittered Backoff     │                        │ Alternate Provider   │
  └──────────────────────┘                        └──────────────────────┘
```

---

## Authentication & Tenancy

v1 had no auth model at all, which makes the rate limiter's "client quota" meaningless and the cache's tenant namespacing unenforceable. Minimum viable scheme:
* `Authorization: Bearer sk-router-<random>`; keys stored as SHA-256 hashes in Redis, never in plaintext, mapping to `{client_id, tenant_id, rpm, tpm, monthly_budget_usd, allowed_models}`.
* `client_id` is the rate-limiter bucket key and the cache namespace. `tenant_id` is the semantic-cache partition.
* Provider API keys live only in environment variables, are never logged, and are redacted by a logging filter that scans for `sk-`, `sk-ant-` prefixes on every emitted record.
* **Idempotency**: an optional `Idempotency-Key` header is stored with the response for 24h. A retried request with the same key returns the stored response without re-billing. Without this, any client-side retry (which is standard in every HTTP SDK) silently doubles cost.

---

## Circuit Breaker Pattern

Prevents cascading gateway failures when an upstream LLM provider suffers latency degradation or 5xx outages.

### State Machine
* **CLOSED (Normal Operation)**: All calls routed directly to provider; outcomes recorded in a rolling window.
* **OPEN (Tripped)**: All calls to this provider fail over immediately to the secondary without waiting for network timeouts.
* **HALF-OPEN (Recovery Probe)**: After a 30-second cooldown, a limited number of probe requests are permitted.
  * $M = 3$ consecutive successes $\rightarrow$ **CLOSED**.
  * Any probe failure $\rightarrow$ immediately back to **OPEN** (with the cooldown doubled, capped at 5 minutes).

### Trip Condition (corrected from v1)
v1 specified "5 **consecutive** 5xx **within 60 seconds**", which conflates two incompatible policies — under low traffic, five consecutive failures can span ten minutes, and under high traffic a 5-failure counter trips on a 0.1% error rate. We adopt the standard Hystrix formulation:

$$\text{TRIP} \iff \big(\text{requests}_{60s} \ge V_{\min} = 20\big) \;\wedge\; \big(\text{error\_rate}_{60s} > 0.50\big)$$

with a **sliding window of ten 6-second buckets** so the window advances smoothly rather than resetting on a cliff. Timeouts and 5xx count as failures; 4xx (client error) and 429 do **not** — a client sending malformed JSON must never be able to trip the breaker for every other tenant.

### Half-Open Concurrency Guard
A naive HALF-OPEN lets *every* in-flight request become a "probe" simultaneously, hammering a recovering provider at full volume — the exact stampede the breaker exists to prevent. Admission is gated by a Redis token: `SET cb:probe:<provider> <req_id> NX PX 10000`. Exactly one request at a time probes; all others are treated as OPEN.

### Exponential Backoff with Decorrelated Jitter
$$t_{\text{sleep}} = \min\big(t_{\text{max}},\; \text{Uniform}(0.5 \cdot t_{\text{base}} \cdot 2^{\text{attempt}},\; 1.5 \cdot t_{\text{base}} \cdot 2^{\text{attempt}})\big)$$
Retries are attempted only for 429/503/504 and connection errors, capped at 3 attempts, and the total retry budget is bounded by the request deadline — a retry that will land after the client has given up is pure waste.

---

## Token-Bucket Rate Limiter

Enforces client and IP quotas atomically via Redis-evaluated Lua, eliminating race conditions under concurrency.

**Two bugs in the v1 script, both exploitable:**
1. **Hardcoded `expire(key, 120)`.** If a bucket takes longer than 120 s to refill (e.g. `capacity = 1000`, `refill = 1/s` → 1000 s), an idle client's key expires and the bucket silently resets to **full capacity**. A client that idles 121 seconds gets a fresh 1000-token burst instead of the ~120 tokens it earned. The TTL must be $\ge \lceil \text{capacity} / \text{refill\_rate} \rceil$.
2. **`now` supplied by the application via `ARGV`.** Across multiple gateway replicas with skewed clocks, a fast instance writes a future `last_refill`; every other replica then computes `elapsed = 0` and stops refilling that bucket entirely. The clock must come from Redis itself, which is by definition the single source of truth for this data.

```lua
-- KEYS[1] = bucket key
-- ARGV[1] = capacity (tokens)
-- ARGV[2] = refill_rate (tokens per second)
-- ARGV[3] = requested (tokens)
-- Returns: {allowed(0|1), tokens_remaining, retry_after_seconds}

local key         = KEYS[1]
local capacity    = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local requested   = tonumber(ARGV[3])

-- Clock from Redis, never from the caller: immune to replica clock skew.
local t   = redis.call('TIME')            -- {seconds, microseconds}
local now = tonumber(t[1]) + tonumber(t[2]) / 1000000

local bucket      = redis.call('hmget', key, 'tokens', 'last_refill')
local tokens      = tonumber(bucket[1]) or capacity
local last_refill = tonumber(bucket[2]) or now

local elapsed  = math.max(0, now - last_refill)
local refilled = math.min(capacity, tokens + (elapsed * refill_rate))

-- TTL must cover a full refill from empty, or an idle client gets a free reset.
local ttl = math.ceil(capacity / refill_rate) + 60

if refilled >= requested then
    redis.call('hmset', key, 'tokens', refilled - requested, 'last_refill', now)
    redis.call('expire', key, ttl)
    return {1, math.floor(refilled - requested), 0}
else
    redis.call('hmset', key, 'tokens', refilled, 'last_refill', now)
    redis.call('expire', key, ttl)
    local deficit = requested - refilled
    return {0, math.floor(refilled), math.ceil(deficit / refill_rate)}
end
```

> `redis.call('TIME')` is non-deterministic and therefore requires **effects replication**, the default since Redis 5. On Redis 4 or earlier, call `redis.replicate_commands()` as the script's first statement.

* **Two independent buckets per client**: requests-per-minute *and* **tokens**-per-minute. RPM alone is not a cost control — one 100K-token request costs more than a thousand small ones. The TPM bucket is debited with an estimate pre-flight and reconciled with actual usage post-flight.
* **Redis unavailable → fail open**, with a per-process in-memory limiter as degraded fallback, and `llm_ratelimit_degraded_total` incremented. A rate limiter that takes the whole gateway down when its datastore blips is a worse outage than the one it prevents. This is a deliberate, documented availability-over-enforcement trade-off.
* **Eviction safety**: rate-limiter and lock keys live in a separate Redis logical DB from the cache, because a cache-driven `allkeys-lru` eviction that evicts limiter buckets is a silent quota bypass.

---

## SLA-Aware Load Balancing

When multiple healthy providers exist in the same tier (e.g. OpenAI `gpt-6-luna` and Groq `llama-3.3-70b`), the gateway computes selection probabilities from real-time health and latency.

v1 used $W_m = (1/\text{Cost}_m) \cdot \Lambda_{P95}(m) \cdot (1 - \text{ErrorRate}_m)$, which has three defects: `Cost` was undefined (input? output? blended?), the reciprocal-cost term *dominates* everything else (a 1.7× cheaper provider wins ~63% of traffic even when markedly slower), and a provider driven to near-zero weight stops producing latency samples and can therefore **never recover**. Corrected:

$$\text{Cost}_m = \bar{n}_{in} \cdot P^{in}_m + \bar{n}_{out} \cdot P^{out}_m \quad \text{(blended at the tenant's trailing 1h token mix)}$$

$$u_m = \log\!\left(\frac{1}{\text{Cost}_m}\right) + \log \Lambda_{P95}(m) + \log(1 - \text{ErrorRate}_{5\min}(m) + \epsilon)$$

$$\Pr(m) = (1 - k\eta)\cdot\frac{e^{u_m / T}}{\sum_j e^{u_j / T}} \;+\; \eta$$

* $\Lambda_{P95}$ dampens traffic when a provider's P95 latency rises above **its tier's typical P95**: $1.0$ below 1.5× the tier median P95, $0.6$ from 1.5× to 3×, $0.2$ beyond. Thresholds are relative because absolute ones (the earlier 800 / 2,000 ms) would mark every frontier provider as degraded — GPT-6.1 Sol's measured median alone is 2.9 s.
* Softmax with temperature $T$ (default 0.5) keeps the trade-off **smooth and tunable** instead of letting one term dominate.
* $\eta = 0.05$ is a **floor probability** per healthy provider ($k$ = number of healthy providers) so every provider keeps producing fresh latency and error samples. Without this floor the balancer is not exploring, and its own measurements go stale.

---

## SSE Streaming Pass-Through Engine

For client requests with `stream: true`, the gateway preserves low **Time-To-First-Token (TTFT)**:
* Chunks are parsed as Server-Sent Events and yielded immediately downstream without buffering.
* Concurrently, an async accumulator reconstructs the full completion text and token counts.
* On `[DONE]`, the aggregate is asynchronously dispatched to the cost logger and (subject to admission policy) the two-tier cache.
* **Cache hits are re-chunked into synthetic SSE frames** so streaming clients see a uniform protocol ([§3](#tier-1a-exact-match-cache-redis)).
* **Streaming Escalation Policy**: emitted tokens cannot be recalled. If a streaming economy response shows high uncertainty, the gateway logs `would_have_escalated` and feeds it to the offline trainer to tighten upfront classification. It does **not** attempt destructive rollback.
* **Conservative streaming threshold**: because the safety net is unavailable in streaming mode, the classifier threshold is tightened to $\tau_{\text{stream}} = \tau - 0.10$. We buy back with upfront caution what we cannot fix after the fact. This asymmetry is measured and reported, not assumed.
* **Mid-stream provider failure**: if the upstream dies after $n > 0$ tokens have been emitted, we cannot silently restart on another provider — the client would receive a spliced, incoherent answer. We terminate the stream with an SSE `error` event and `X-Router-Stream-Aborted: upstream-failure`, and the request is **not** billed to the client's quota. Silent mid-stream splicing is the kind of bug that destroys trust in a gateway.

---

# 5. The Learning Loop: Offline Policy Retraining

A static router degrades as language models evolve. The router features a closed feedback loop:

```
┌────────────────────────┐        ┌────────────────────────┐
│   Live Traffic Logs    │ ─────► │ Filter Discrepancies   │
│  (DuckDB ledger)       │        │ (Escalations, Errors)  │
└───────────┬────────────┘        └───────────┬────────────┘
            │                                 │
            │  ε-greedy exploration           ▼
            │  supplies counterfactual  ┌────────────────────────┐
            │  labels for BOTH arms     │ Retrain MLP + Recalib. │
            │                           │ (IPW-weighted)         │
            ▼                           └───────────┬────────────┘
┌────────────────────────┐                          │
│ Shadow-Eval Sample (2%)│                          ▼
└────────────────────────┘        ┌────────────────────────┐
                                  │ Offline Policy Eval    │
                                  │ gate → symlink swap    │
                                  │ (auto-rollback armed)  │
                                  └────────────────────────┘
```

### ⚠ The Selection-Bias Problem (the deepest flaw in v1's design)

v1 stated: *"Every escalation is a verified misclassification ($Y=1$). Every non-escalated high-confidence economy response is a verified cheap label ($Y=0$)."*

Both labels come **only from prompts the router already sent to Economy**. Prompts routed to Frontier produce **no label at all** — we never observe that they would have been fine on the cheap model. This is textbook **bandit feedback**, and the consequence is monotone and unrecoverable:

> The policy can only ever learn *"this should have been Frontier."* It can never learn the reverse. Over successive retraining cycles $\beta$ shrinks, $\delta$ grows, and the measured savings decay week over week — while every offline metric looks fine, because the evaluation set is drawn from the same biased distribution.

**This is the single most intellectually serious issue in the specification, and fixing it is the project's strongest research contribution.** Three mechanisms:

1. **ε-greedy exploration**: route $\varepsilon = 5\%$ of *frontier-classified* traffic to Economy anyway, run the full uncertainty check, and log the outcome. This is the counterfactual label source. Bounded cost: at most $\varepsilon \cdot \delta$ of traffic pays $C_e + C_f$ — under the Expected scenario, $0.05 \times 0.30 \times 0.06 \approx 0.09\%$ of baseline spend. **Vanishingly cheap insurance against policy collapse.** Excluded for requests marked `critical: true` by the client.
2. **Shadow evaluation**: on a 2% sample, call *both* tiers, judge offline with an LLM judge, and emit an unbiased label pair. Slower and costlier than (1), but it yields graded quality labels rather than a binary escalate/no-escalate signal.
3. **Inverse-propensity weighting**: each logged example carries the probability $\pi(a \mid x)$ with which the logging policy chose its action. Training reweights by $1/\pi(a \mid x)$ so the biased logging distribution is corrected rather than baked in.

### Cold Start: Where the Bootstrap Labels Come From
v1 listed `training/data/labeled_prompts.jsonl` in the repo tree but never said where it comes from — the single largest schedule risk in the plan, since Week 7 stalls without it. Decided now:
* **Primary**: public preference data from **Chatbot Arena / RouteLLM** (~80K human preference pairs). A pair where the strong and weak models tie is a $Y=0$ (economy sufficient); a pair where the strong model wins decisively is $Y=1$. This is exactly the supervision signal RouteLLM itself uses, which also makes our numbers directly comparable to theirs.
* **Secondary**: 2,000 synthetic domain prompts generated and labelled by a frontier model with a rubric, manually spot-checked at 10%.
* **Tertiary**: our own 500-query benchmark corpus, held out entirely from training and used *only* for evaluation. **Training on the benchmark would invalidate every number in the report**; the corpus hash is recorded and a CI check asserts no overlap with training data.

### Retraining Pipeline
1. **Telemetry Collection**: every decision, uncertainty score, escalation event, exploration flag, propensity, and (if provided) user rating is written to the DuckDB ledger.
2. **Dataset Synthesis**: labels drawn from escalations, non-escalations, exploration arms, and shadow evaluations, each carrying its propensity.
3. **Model Fine-Tuning**: a weekly job re-fits the MLP head and **re-fits the calibrator**. An updated model with a stale calibrator silently shifts the meaning of $\tau$.
4. **Offline Policy Evaluation gate**: the candidate is scored on a frozen held-out set. It is promoted **only if** estimated cost falls *and* estimated quality stays within the TOST margin. A candidate that is cheaper but worse is rejected automatically.
5. **Versioned Artifacts**: `routing_policy_vYYYYMMDD_HHMM.pkl`, with the training-data hash, git SHA, and metrics embedded in a sidecar JSON.
6. **Zero-Downtime Hot Swap**: production reads `routing_policy_latest.pkl` via symlink; swaps are atomic (`os.replace`), no restart. **Auto-rollback**: after promotion, the gateway watches escalation rate and P95 latency for 30 minutes; a >50% regression on either reverts the symlink automatically and pages.

---

# 6. Observability, Metrics & Telemetry Stack

## Per-Request Accounting Ledger

Every interaction emits a structured record, written to **DuckDB** (not a bare JSONL file): the benchmark report needs SQL aggregation, and Prometheus counters reset on restart, so the durable financial record must live somewhere queryable.

```json
{
  "request_id": "req_8f3a2b1c",
  "idempotency_key": null,
  "timestamp": "2026-09-20T11:30:00Z",
  "client_id": "cust_support_webapp",
  "tenant_id": "techstore",
  "conversation_id": "conv_77b1",
  "turn_index": 1,
  "prompt_hash": "a3f8b2c1d4e5",
  "cache": {
    "hit": false,
    "type": null,
    "lookup_latency_ms": 1.4,
    "admission_rejected_reason": null
  },
  "classification": {
    "raw_score": 0.31,
    "calibrated_score": 0.38,
    "threshold": 0.50,
    "method": "embedding_mlp",
    "policy_version": "v20260918_0400",
    "assigned_tier": "economy",
    "exploration": { "is_exploration": false, "propensity": 0.93 }
  },
  "routing": {
    "initial_model": "gpt-6-luna",
    "initial_provider": "openai",
    "escalated": true,
    "escalation_suppressed_by": null,
    "uncertainty": {
      "composite": 0.62,
      "signals": { "logprob": 0.5, "hedge": 0.72, "length": 0.60, "repeat": 0.0, "struct": 0.0 },
      "available_signals": ["logprob", "hedge", "length", "repeat", "struct"]
    },
    "final_model": "gpt-6.1-sol",
    "final_provider": "openai"
  },
  "usage": {
    "prompt_tokens": 142,
    "cached_prompt_tokens": 0,
    "completion_tokens": 88,
    "total_tokens": 230
  },
  "economics": {
    "actual_cost_usd": 0.001254,
    "baseline_cost_usd_estimated": 0.002875,
    "baseline_estimator": "kappa_calibrated_v1",
    "verbosity_kappa": 1.34,
    "savings_usd_estimated": 0.001621,
    "savings_pct_estimated": 56.38,
    "estimate_ci95": [0.00131, 0.00193]
  },
  "performance": {
    "ttft_ms": 320,
    "total_latency_ms": 845,
    "router_overhead_ms": 13.6
  }
}
```

### ⚠ The Counterfactual Baseline Problem (the easiest claim to attack)

`baseline_cost_usd` is a number for a call **that never happened**. On a cache hit or an economy call, the frontier model's `completion_tokens` are unobserved. If we price the baseline using the *economy* model's actual completion count at frontier rates — which is the obvious implementation and what v1 implied — we **systematically understate the baseline**, because frontier models are reliably more verbose. The headline savings figure then becomes unfalsifiable, and a sharp reviewer will say so.

Three corrections:
1. **Rename the field** to `baseline_cost_usd_estimated` and record `baseline_estimator` in every row. Honesty in the schema, not just the prose.
2. **Calibrate with a verbosity factor** measured on the benchmark, where both arms genuinely execute:
   $$\kappa = \text{median}\left(\frac{n^{out}_{\text{frontier}}}{n^{out}_{\text{economy}}}\right), \qquad \widehat{C_f} = n^{in} P^{in}_f + \kappa \cdot n^{out} P^{out}_f$$
   $\kappa$ is reported with a bootstrap 95% CI and recomputed per benchmark run. Every live savings figure inherits that interval, hence `estimate_ci95`.
3. **State the boundary plainly**: live dashboard savings are *estimates*; the benchmark's savings are *measured*. The report uses only the measured number for claim C1. Papering over this distinction is the fastest way to lose an evaluator's trust; naming it is the fastest way to earn it.

**Provider-side prompt caching**: both OpenAI and Anthropic discount repeated prefix tokens. `usage.prompt_tokens_details.cached_tokens` must be read and priced at the discounted rate — otherwise we *overstate* our own cost and *understate* the baseline's, and, worse, we would be claiming credit for savings the provider produced. The ledger records cached tokens separately so provider-cache savings and router savings are never conflated.

---

## Prometheus Instrumentation & Grafana Dashboard

```
# Prometheus Metric Declarations
llm_requests_total{tier, model, cache_hit, escalated, exploration}
llm_cost_dollars_total{tier, model}
llm_baseline_cost_dollars_estimated_total
llm_cost_savings_dollars_estimated_total
llm_request_duration_seconds_bucket{tier, phase}          # histogram, not summary
llm_router_overhead_seconds_bucket
llm_cache_hits_total{cache_type}
llm_cache_admission_rejected_total{reason}
llm_escalations_total{reason}
llm_escalations_suppressed_total{guard}
llm_circuit_breaker_state{provider}                        # 0=Closed, 1=Open, 0.5=Half-Open
llm_ratelimit_degraded_total
llm_policy_version_info{version}
```

> **Counters reset on restart.** v1's headline panel was a "real-time cumulative dollar counter" over `llm_cost_savings_dollars_total` — which zeroes the moment the container bounces, mid-demo. All cumulative panels use `increase(...[$__range])`, and the authoritative lifetime total is read from the DuckDB ledger via the Grafana SQL datasource. Use **histograms**, not summaries, so quantiles are aggregatable across replicas.

### The 10 Essential Grafana Panels
1. **Gross Financial Savings (\$ vs. Calibrated Baseline)** — with the CI band drawn, not a bare number.
2. **Net Savings Percentage Gauge** — targeting the 40–60% corridor.
3. **Traffic Allocation by Tier** — Cache / Economy / Escalated / Frontier.
4. **Latency Heatmap (P50, P90, P99)** — end-to-end, plus a separate router-overhead series for claim C3.
5. **Cache Hit Efficiency** — Exact vs. Semantic, stacked, with **admission rejections overlaid** (the safety net made visible).
6. **Escalation Rate Tracker** — alarms above **15%** (single canonical threshold; see below).
7. **Escalation Reason Distribution** — plus suppressed-escalation reasons.
8. **Circuit Breaker Status Grid** — availability matrix per upstream provider.
9. **Token Throughput (Tokens/Sec)** — prompt vs. completion, with cached-prompt-tokens broken out.
10. **Error Rate & Fallback Frequency** — 429s, 5xxs, failover shifts, degraded-mode counters.

> **Single source of truth for thresholds.** v1 quoted the escalation alarm at 15% (§6), 25% (Week 8), while the cost model assumed 5% (§2). All three now derive from one constant block in `app/config.py`: `ESCALATION_TARGET = 0.07`, `ESCALATION_WARN = 0.15`, `ESCALATION_CRITICAL = 0.25`. The spec quotes the constant names, never the literals.

---

## OpenTelemetry Distributed Tracing

Exported to **Jaeger**:

```
[chat_completion] ────────────────────────────────────────────────────────── 845ms
  ├── [auth_and_idempotency] ──────────────────────────────────── 0.6ms
  ├── [rate_limit_check] ──────────────────────────────────────── 1.2ms
  ├── [exact_cache_lookup] ────────────────────────────────────── 0.4ms (miss)
  ├── [embed_shared] ─────────────────────────────────────────── 11.0ms   ◄── computed ONCE
  ├── [semantic_cache_lookup] ─────────────────────────────────── 1.8ms (miss)
  ├── [complexity_classification] ─────────────────────────────── 1.1ms (calibrated=0.38)
  ├── [provider_call: gpt-6-luna] ───────────────────────────── 320.0ms
  ├── [uncertainty_verification] ──────────────────────────────── 2.1ms (U=0.62: hedge+length)
  ├── [escalation_provider_call: gpt-6.1-sol] ──────────────── 490.0ms
  └── [cache_store_async] ─────────────────────────────────────── 4.8ms
                                          router overhead total ≈ 13.6ms  ◄── claim C3
```

Trace context (`traceparent`) is propagated from inbound headers so the router slots into a client's existing trace rather than starting an orphan.

---

# 7. The Proof Engine: Benchmark & Evaluation Suite

A central requirement of this project is **not just claiming, but proving** the cost reduction with defensible quality evidence.

---

## Dual-Track Evaluation Corpora

v1 evaluated exclusively on a self-authored 500-query support corpus scored by an LLM judge. That has three weaknesses a reviewer will press on: we wrote the questions *and* the reference answers *and* chose the judge (circularity); there is no external point of comparison; and "quality" is never grounded in anything objectively checkable. We therefore run **two tracks**.

### Track A — Domain Track (narrative, relatability, RAGAS)
A fixed, reproducible corpus of **500 stratified queries** simulating real support traffic, plus a companion `knowledge_base.jsonl` of ~120 TechStore policy, product, and order documents that supplies the *reference contexts* RAGAS faithfulness requires. (v1 specified RAGAS but never specified a knowledge base — RAGAS cannot run without one.)

| Category | Count | Proportion | Expected Optimal Tier | Cacheable? |
|:---|:---|:---|:---|:---|
| **Simple FAQ & Policy** | 60 | 12% | Economy / Cache | ✅ High |
| **Order Status & Account** | 60 | 12% | Economy | ❌ **Never** (user-scoped, volatile) |
| **Basic Product Information** | 40 | 8% | Economy | ✅ High |
| **Product Comparison** | 50 | 10% | Economy → Escalation | ⚠ Exact only |
| **Simple Troubleshooting** | 50 | 10% | Economy | ✅ Moderate |
| **Complex Billing Disputes** | 70 | 14% | Frontier | ❌ Never |
| **Technical API Support** | 70 | 14% | Frontier | ⚠ Exact only |
| **Multi-Step Policy Edge Cases** | 60 | 12% | Frontier | ⚠ Exact only |
| **Out of Scope / Unanswerable** | 40 | 8% | Economy | ⚠ Exact only |

Note the cacheability column: **26% of the corpus must never be semantically cached**. Reporting an overall $\alpha$ without that decomposition would overstate the achievable cache hit rate. A separate **multi-turn subset** of 60 conversations (3–6 turns each) exercises sticky escalation and anaphora handling.

### Track B — Public Track (objective ground truth, external comparability)
Quality measured by **verifiable correctness, not opinion**. This track is what makes the result hard to argue with:

| Benchmark | n | Metric | Why it matters here |
|:---|:--|:---|:---|
| **GSM8K** (subset) | 300 | Exact-match on final numeric answer | Multi-step arithmetic reasoning — the canonical place cheap models fail. **Objective.** |
| **HumanEval / MBPP** | 164 / 200 | `pass@1` via unit-test execution | Code correctness decided by a test runner, not a judge. **Fully objective.** |
| **MMLU** (4 subjects) | 400 | Multiple-choice accuracy | Breadth of knowledge, zero grading ambiguity. **Objective.** |
| **MT-Bench** | 80 | Judge score 1–10 | Open-ended quality; comparable to published routing literature. |

Track B lets us report the two metrics the routing literature actually uses — **APGR** (average performance gap recovered between economy and frontier) and **CPT(x%)** (the fraction of frontier calls needed to recover x% of the frontier–economy gap) — which makes our numbers **directly comparable to RouteLLM's published results**. Being able to say "on MT-Bench we reach CPT(50%) at *n*% frontier calls, versus RouteLLM's published figure" is worth more than any amount of self-scored prose.

---

## The Five-Arm Comparative Harness

v1 compared the router against a single strawman ("always frontier"). Beating a strawman proves little; the interesting question is *how close to optimal* the routing is. Five arms:

```
                    [ Track A (500)  +  Track B (1,144) ]
                                  │
    ┌───────────┬─────────────────┼─────────────────┬───────────┐
    ▼           ▼                 ▼                 ▼           ▼
[Always      [Always          [ROUTER]          [Random     [ORACLE
 Frontier]    Economy]                           @matched    router]
                                                  cost]
 Quality      Cost floor,      The claim        Does the    Upper bound:
 ceiling,     quality floor                     classifier  perfect
 cost ceiling                                   beat a      hindsight
                                                coin flip?  routing
    └───────────┴─────────────────┼─────────────────┴───────────┘
                                  ▼
                   [ Cost–Quality Pareto Frontier Plot ]
             x = normalised cost, y = quality; all five arms plotted
```

* **Always-Economy** establishes the quality *floor* — it quantifies how much quality the router is actually buying back, and without it a 60% saving is uninterpretable.
* **Random @ matched cost** routes randomly while spending exactly what the router spent. If the router does not beat it, the classifier has learned nothing — this arm is the honest null model, and running it is a strong signal of intellectual seriousness.
* **Oracle** routes with perfect hindsight (economy iff economy actually scored as well as frontier), giving the theoretical upper bound. Reporting "we capture 84% of the oracle's available savings" is a far more sophisticated claim than a raw percentage.

**The Pareto plot with all five arms is the single most important figure in the report.** It is the slide the presentation opens on.

### Reproducibility Controls
Without these, re-running the benchmark yields different numbers and "reproducible" becomes false advertising:
* Pinned model snapshot IDs (never floating aliases), recorded per run alongside the `pricing.yaml` `as_of` date.
* `temperature = 0` **where the model accepts it**. GPT-6.1 Sol and GPT-6 Luna both reject the parameter, so their answers vary between runs: the $k = 3$ repeats below are therefore **required**, not optional, and every result records the temperature actually used (`temperature_used`, null when rejected). Fixed `seed` where supported; fixed output cap.
* Corpus SHA-256 and git commit recorded in every result file.
* $k = 3$ repeat runs; report mean ± SD, because even at $T=0$ provider outputs are not perfectly deterministic.
* All raw responses committed to `benchmarks/results/<run_id>/` so a third party can re-grade with a judge of their own choosing.

### Judge Independence
v1 used **GPT-4o as the judge while GPT-4o was also the baseline arm** — textbook self-preference bias; models score their own outputs measurably higher. Corrections:
* The judge is from a **different family** than either arm under test (Claude judges the OpenAI arms, and vice versa on the cross-check).
* **Two independent judges** on a 150-item subsample, reporting Cohen's $\kappa$; $\kappa < 0.6$ invalidates the judged results and we fall back to Track B's objective metrics.
* **Position randomisation** per item, plus an order-swap replication on 100 items to measure position bias directly.
* The judge never sees which arm produced which response, and never sees routing metadata.
* **The AI judge is calibrated against humans before it is trusted.** It grades a human-graded set first, and is used for the benchmark only if its agreement with the humans reaches $\kappa \ge 0.6$. Phase 0 showed why: an AI grader and two humans, grading the same 50 answers, agreed 88% of the time but reached only $\kappa = 0.50$, with the humans consistently stricter.

### Grading Rubric

Every judge, human or AI, applies the same four verdicts and three rules. They were tightened after Phase 0, where each disagreement between graders traced back to a case the original one-line definitions did not settle.

| Verdict | Meaning |
|:---|:---|
| `correct` | Answers the question fully; every fact matches the evidence the model was given |
| `partial` | Right but incomplete; **or** says information is unavailable when the evidence contained it; **or** makes an inference the evidence does not state |
| `wrong` | Contradicts the evidence, or gets the arithmetic wrong |
| `hallucinated` | States a fact the evidence does not contain and that is not a correct calculation |

1. Extra detail that the evidence supports does not lower the verdict.
2. Style and formatting are recorded in notes and do not change the verdict.
3. If the evidence lacks something and the answer says so, that is the correct behaviour — the gap belongs to the knowledge base or the retriever, not the model.

---

## Statistical Protocol: Non-Inferiority by TOST

### ⚠ What was wrong in v1
v1 declared:
```
H₀: μ_router < μ_baseline      H₁: μ_router ≥ μ_baseline
… two-tailed paired t-test … if p > 0.05 we accept quality parity
```
Three separate errors, any one of which a statistically literate examiner will catch:
1. **$H_0$ must contain the equality.** As written the hypothesis pair is not a valid test specification.
2. **The hypotheses are one-sided but the test is two-tailed.** Internally contradictory.
3. **"$p > 0.05$ therefore parity" is affirming the null.** Failing to reject is *absence of evidence*, not *evidence of absence* — an underpowered study reliably "proves parity" precisely by being bad. This is the flaw that would have cost the most marks.

### The Correct Framework
Quality parity is an **equivalence / non-inferiority** question, which requires **TOST** (two one-sided tests) against a pre-declared margin.

* **Pre-registered margin**: $\delta = 0.25$ on the 5-point judge scale (and $\delta = 0.02$ absolute on Track B accuracy metrics). Justification, stated *before* seeing results: 0.25 is below the threshold at which two human raters reliably distinguish responses, and it is one-fifth of a single scale point. The margin is committed to `docs/evaluation_protocol.md` and git-timestamped **before the first benchmark run** — pre-registration is what makes it credible.
* **Primary endpoint** (exactly one, declared in advance): mean paired judge score on Track A. Everything else is secondary and explicitly labelled exploratory.
* **Non-inferiority test** (we care about not being *worse*; being *better* is a bonus):

$$H_0: \mu_{\text{router}} - \mu_{\text{baseline}} \le -\delta \qquad H_1: \mu_{\text{router}} - \mu_{\text{baseline}} > -\delta$$

  Rejecting $H_0$ at $\alpha = 0.05$ **demonstrates non-inferiority**. For full equivalence, run both one-sided tests and show the **90% CI for $\bar{d}$ lies entirely within $(-\delta, +\delta)$**.

* **Test statistic** (paired, per query):
$$t = \frac{\bar{d} + \delta}{s_d / \sqrt{n}}$$

* **Power analysis, computed in advance** (this is what makes the result meaningful rather than lucky): with $n = 500$, $s_d \approx 0.7$, $\alpha = 0.05$, the minimum detectable difference at 80% power is
$$\Delta_{\min} = 2.80 \cdot \frac{s_d}{\sqrt{n}} = 2.80 \cdot \frac{0.7}{22.36} \approx 0.088$$
  Comfortably finer than the 0.25 margin — so the study **is** powered to detect a difference that matters, and "no significant difference" is genuinely informative.

* **Robustness checks**, because 1–5 judge scores are ordinal, not interval:
  * **Wilcoxon signed-rank** as a non-parametric companion.
  * **Bootstrap** (10,000 resamples) CI on both $\bar{d}$ and total cost savings — the cost saving gets a confidence interval too, not a point estimate.
  * **Multiplicity control**: 4 judge criteria × 3 RAGAS metrics × 4 Track-B benchmarks = many tests. Only the primary endpoint is confirmatory; all secondaries are reported with **Holm–Bonferroni** adjustment and labelled exploratory.
  * **Per-category breakdown**: overall parity can hide a catastrophic failure in one stratum. We report the TOST per category and flag any category where the CI crosses $-\delta$, even if the aggregate passes. Hiding a stratum failure inside a good average is exactly the kind of thing an examiner looks for.

### RAGAS Quality Framework (Track A, secondary)
* **Faithfulness** — claims grounded in the retrieved `knowledge_base.jsonl` contexts.
* **Answer Relevancy** — directly answers the prompt without padding.
* **Semantic Similarity** — router output vs. baseline frontier output.

---

# 8. Competitive Landscape & Market Differentiation

## Open-Source GitHub Projects

| Project | Stars / Backing | Architecture / Approach | Critical Missing Gaps vs Our Project |
|:---|:---|:---|:---|
| **RouteLLM** | 3.5K+ ⭐ (UC Berkeley / LMSYS) | Matrix factorization & BERT preference classifiers trained on 80K Chatbot Arena pairs. | Pure research code. No API gateway, caching, rate limiting, circuit breakers, failover, or streaming. No post-hoc verification of the routing decision. |
| **LLMRouter** | 800+ ⭐ (UIUC) | Research framework, 16+ algorithms (KNN, SVM, MLP, graph) + xRouteBench. | Academic benchmark tool. No production gateway; no real-time uncertainty escalation. |
| **Maestro** | AY Automate | Orchestration implementing "cheap-first" execution and escalation. | No two-tier caching, rate limiting, or Prometheus/Grafana observability. |
| **LiteLLM** | 18K+ ⭐ (BerriAI) | Universal proxy translating across 100+ LLM backends. | **No intelligent routing.** Routes only where explicitly told. No complexity scoring or uncertainty checks. |
| **Portkey Gateway** | 7K+ ⭐ (Acquired by Palo Alto Networks) | Enterprise control plane with semantic caching, retries, guardrails. | Static manual routing rules. No ML-driven tier routing, and **no entity-aware semantic-cache admission control** — the failure mode we explicitly engineer against. |

## Commercial Startups & Industry Giants

* **Martian (\$9M Seed + Accenture, ~\$1.3B valuation)**: first commercial LLM router, proprietary "Model Mapping" via mechanistic interpretability. Closed-source SaaS.
* **Not Diamond**: dynamic cross-model routing. Decision layer only, not the gateway. Proprietary.
* **Unify AI**: routes on daily automated quality/speed/cost benchmarks. Usage-based SaaS.
* **OpenRouter**: unified API aggregator for 100+ models. **Does not route intelligently** — users pick models manually.

## Our Unique Architectural Value Proposition

```
                    ┌────────────────────────────┐
                    │    Research Intelligence   │
                    │   (RouteLLM, LLMRouter)    │
                    └─────────────┬──────────────┘
                                  ▼
┌──────────────────────────────────────────────────────────────┐
│                    OUR ROUTING GATEWAY                       │
│                                                              │
│  + Calibrated complexity classification (pre-hoc)            │
│  + Uncertainty-based escalation  (post-hoc)  ◄── unique      │
│  + Entity-aware semantic cache admission      ◄── unique      │
│  + Exploration-corrected learning loop        ◄── unique      │
│  + Multi-provider abstraction, circuit breakers, limiting    │
│  + Pre-registered TOST non-inferiority proof  ◄── unique      │
│  + Open-source, self-hosted, explainable                     │
└──────────────────────────────────────────────────────────────┘
                                  ▲
                    ┌─────────────┴──────────────┐
                    │  Production Infrastructure │
                    │    (LiteLLM, Portkey)      │
                    └────────────────────────────┘
```

**Core differentiator**: we bridge academic routing research and enterprise production infrastructure. Concretely, three things exist nowhere else in the open-source landscape:

1. **Two-sided routing** — every competitor decides *before* the call. We also verify *after* it, so a classifier mistake is caught rather than silently shipped to the user.
2. **Cache admission control that is safe by construction** — every semantic cache in this space (Portkey included) will happily serve one customer's order status to another. We treat that as a first-class safety property with a CI-enforced adversarial test suite.
3. **An evaluation that could fail** — a pre-registered non-inferiority margin, an oracle upper bound, and a random-at-matched-cost null model. Most projects in this space report a number that could not have come out badly.

---

# 9. Selected Use Case: AI Customer Support Agent

We ground the implementation in an **Enterprise AI Customer Support Agent** for an online electronics retailer ("TechStore").

### ⚠ What TechStore Is — and What It Is Not

**TechStore is not software. No part of it is built.** There is no TechStore website, application, database server, checkout flow, or user account system, and not one line of TechStore code will be written.

TechStore is **three text files**:

| Artifact | What it actually is | Size | Effort |
|:---|:---|:---|:---|
| System prompt | ~10 lines instructing the model to act as a support agent | 10 lines | 1 hour |
| `knowledge_base.jsonl` | ~120 fabricated policy / product / order documents | ~15 KB | 1–2 days |
| `customer_support_500.jsonl` | 500 test questions + 60 multi-turn conversations | ~80 KB | 2–3 days |

The deliverable of this project is the **router** — approximately 6,000 lines of Python across `app/`, `benchmarks/`, and `tests/`. TechStore is the test harness that router is measured on, in the same sense that a benchmark corpus is not the thing being benchmarked.

**The proof that this is true**: if the domain were changed from an electronics retailer to a legal firm, we would rewrite three text files and **zero lines of code**. That property is not incidental — it is the evidence that the router is genuinely domain-agnostic infrastructure.

A use case is nonetheless mandatory, for three reasons: (1) a cost-and-quality claim requires questions to ask and answers to grade; (2) "is this query hard?" is only meaningful inside a domain, so the classifier needs a realistic query distribution to learn and be measured against; (3) a terminal printing `{"tier":"economy","cost":0.00026}` persuades nobody, whereas a support conversation visibly escalating mid-demo persuades everyone.

**One correction to the above.** The domain is data, but there *is* a thin application layer — the support agent that retrieves documents and calls a model. It is ~660 lines, it is built first, and it is specified immediately below. What is *not* built is the retailer: no storefront, catalogue, cart, checkout, or user accounts. Those would cost weeks and contribute nothing to the thesis.

---

## Phase 0: The TechStore Support Agent (built first)

**Built before the router, in Weeks 1–2.** A question arrives, relevant knowledge-base documents are retrieved, one model is called, an answer is returned — with tokens, cost, and latency recorded for every call. No router, no cache, no classifier, no circuit breaker.

```
techstore/
├── config.py            model ids, as-of-dated pricing, paths
├── retriever.py         BM25-lite (stdlib) + MiniLM backends, auto-selected
├── agent.py             retrieve → assemble context → call model → Answer record
├── cli.py               single question, --dry-run, or --batch over JSONL
├── app.py               Streamlit chat + inspector panel
├── validate_data.py     corpus integrity + progress against the 500 target
├── system_prompt.txt
├── data/{knowledge_base,orders,questions_seed}.jsonl
└── tests/test_agent.py  no API calls; free to run in CI
```

### Why it is built first

1. **It is the baseline arm.** `benchmarks/run_baseline.py` is `SupportAgent` in a loop. The Week 10 deliverable is written in Week 2 and paid for immediately.
2. **It validates the corpus while correction is cheap.** Retrieval failures and knowledge-base gaps surface in Week 2, not during the benchmark week.
3. **It makes before/after concrete.** *"Same application, one line changed, 60% cheaper, quality statistically unchanged"* is a materially stronger demonstration than comparing two benchmark scripts.
4. **It gives the router a drop-in target.** In Week 4, `OPENAI_BASE_URL` is repointed at the gateway and nothing else changes — which is what makes the one-line-swap demo real rather than hypothetical.
5. **It surfaces design gaps that paper review does not.** The retrieval requirement in [§2](#-the-400-token-assumption-requires-a-retriever) was found by building this, not by reviewing the specification.

### Design decisions

| Decision | Rationale |
|:---|:---|
| **Retrieval, not full-context** | Top-3 documents at ~507 tokens, versus ~7,700 for concatenating the whole knowledge base — a 7× cost difference that grows with every document added |
| **Two retrieval backends** | `keyword` (BM25-lite, pure stdlib) makes the corpus loop runnable with zero installs and no API key; `embedding` uses the same MiniLM the router needs for Layers 1B and 2, validating that pipeline early. `auto` prefers embeddings and falls back silently |
| **OpenAI-compatible client** | The same client reaches OpenAI, Groq, Together — and, from Week 4, our own gateway |
| **`Answer` dataclass records tokens, cost, latency, retrieved ids** | This record is the seed of the [§6](#per-request-accounting-ledger) accounting ledger |
| **Inspector panel from day one** | It shows retrieval/tokens/cost/latency now and gains cache, tier, and escalation rows in Week 4. The response schema grows with it instead of being retrofitted during the recording week |
| **Orders 48213 and 48217 hold different products deliberately** | Near-identical queries, entirely different correct answers — the fixture for the Week 2 cache-safety suite and for the blocked-attack demo moment |

### Phase 0 Exit Criteria

* `validate_data.py` passes: no duplicate ids, no dangling `context_ids`/`order_ids`, order totals reconcile against line items
* Top-3 retrieval recall = 100% on the labelled recall set, on the **zero-dependency** backend
* Assembled prompt stays under 900 tokens for every seed question (guards the [§2](#-the-400-token-assumption-requires-a-retriever) economics)
* The agent returns sensible answers across all eight categories with cost and latency logged
* Demonstrable to a third party in a browser

### Phase 0 Results: First Run Against the Real Model (2026-10-03)

**Status: exit criteria met.** All 50 seed questions answered by GPT-6.1 Sol through the full agent; the remaining milestone is the demonstration to the mentor.

| Measure | Result |
|:---|:---|
| Cost | **\$0.1104** total, \$0.0022 per question (projected \$0.0023) |
| Tokens per question | prompt 639 · output 93 (median 75, p90 185) · hidden reasoning 7 |
| Latency | median 2.9 s · p90 5.0 s |
| Out-of-scope behaviour | **10/10** — declined off-topic, admitted unknowns, answered catalogue questions from About TechStore, split the half-answerable question |
| Answerable questions refused outright | **0 / 40** |
| Invented prices | **0** — all three flagged ₹ amounts were correct arithmetic |
| **Human grading** (Rahul 46 questions, Kanishk 4) | **42 correct · 8 partial · 0 wrong · 0 hallucinated** |
| Claude's grading (provisional; not independent — Claude wrote the knowledge base and questions) | 44 correct · 6 partial · 0 wrong · 0 hallucinated |
| Agreement, humans vs Claude | 44/50 = 88% · Cohen's $\kappa$ = **0.50**, below the 0.6 reliability threshold of [§7](#judge-independence) |

**What the run exposed, and what was done:**

| Finding | Fix | Verified by re-run |
|:---|:---|:---|
| Knowledge base contradicted itself on whether over-ear headphones are returnable once opened (the model noticed and hedged) | Hygiene policy now covers all headphone types; Y500 page states it | ✅ q037 |
| "Refunded in full" after failed delivery did not say whether the delivery charge is included | Stated explicitly | ✅ q039 |
| The model knows the real date, so against frozen order records deliveries looked overdue — results would drift with the calendar | Fixed simulated date (`SIMULATED_TODAY`, 30 Sep 2026) in every prompt, with an explicit rule to use it; fixtures validated against it | ✅ q006 correct 3/3, q008, q009 |
| Comparisons naming two products retrieved only one | Named-product rule: product pages carry aliases and are always included when named | ✅ q017, q018 · retrieval 82.8% → 84.5%, comparisons 70% → 80% |
| Complete answers ending with a needless hand-off | Prompt: offer a human only for actions (e.g. investigating an overdue refund); one fixed partial-answer phrasing | ✅ two of four resolved; two remaining were judged legitimate |
| Grader counted every partial answer as a refusal | Grader separates outright refusals, partial answers caused by retrieval misses, and possible hedges to check | — |

**Grading.** Two human graders independently found no wrong or hallucinated answer. Their 8 `partial` verdicts and Claude's 6 overlapped on 4 (q017, q019, q020, q036). The six disagreements split into two patterns: humans marked down unnecessary hand-offs (q008, q028) and answers they judged incomplete or awkward (q026, q031); Claude marked down claims the evidence did not support (q037, q039). Each pattern is now a written rule in the [grading rubric](#grading-rubric). Human grading also exposed one gap in the test data — order #48712's reversed hold had no date, so the model rightly said it could not give one — and one style rule (write "order #48712"). Both were fixed and verified on a real re-run. Grades are archived in `techstore/runs/2026-10-03_phase0/`.

Controls re-run alongside the fixes (q001, q026, q041, q044, q050) were unchanged — no regressions. **Category questions** — naming a category rather than a product ("which of your headphones is lighter", "a laptop for college") — missed the product pages they needed (q019, q020). Fixed with a one-line-per-product catalogue, added on top of the searched documents only when a question names a category and asks to compare, choose or buy; `validate_data.py` checks every price and spec number in it against the product pages. Verified on a real re-run: both now answer fully and correctly (q020's three totals checked), and a category question about an owned item (q021, pairing) is unaffected.

### The Three Datasets (these are routinely confused)

| # | Dataset | Size | Purpose | Origin | May it train the model? |
|:--|:---|:---|:---|:---|:---|
| 1 | **Knowledge base** | ~120 docs | The facts the agent knows; the reference contexts RAGAS scores against | **We author it** | n/a |
| 2 | **Benchmark corpus** | 500 Q + 60 conversations | The exam. Measurement only | **We author it** | ❌ **Never** — CI-enforced |
| 3 | **Training data** | ~80K preference pairs | Teaches the complexity classifier | **Downloaded** (Chatbot Arena / RouteLLM) | ✅ Yes |
| 4 | Cache calibration pairs | 400 | Tunes the cosine threshold; CI safety gate | We author it | n/a |
| 5 | Track B public benchmarks | 1,144 | Objective-ground-truth evaluation | Downloaded | ❌ Never |

Dataset 2 is the exam paper. If the classifier has seen it, every number in the report is void — which is why `training/` asserts zero hash overlap against it in CI.

### Category Structure, with Representative Queries

| Category | n | Representative query | Expected tier | Cacheable? |
|:---|--:|:---|:---|:---|
| **Simple FAQ & Policy** | 60 | *"What's your return window?"* | Economy | ✅ High |
| **Order Status & Account** | 60 | *"Where is my order #48213?"* | Economy | ❌ **Never** — user-scoped and volatile |
| **Basic Product Information** | 40 | *"Does the SoundWave X200 have noise cancellation?"* | Economy | ✅ High |
| **Product Comparison** | 50 | *"X200 vs Y500 for a noisy open-plan office — which?"* | Economy → escalation | ⚠ Exact only |
| **Simple Troubleshooting** | 50 | *"My headphones won't pair with my phone."* | Economy | ✅ Moderate |
| **Complex Billing Disputes** | 70 | *"I was charged ₹12,999 three times. Two were cancelled but I only received one refund. Where is my money?"* | Frontier | ❌ Never |
| **Technical API Support** | 70 | *"Your webhook returns 403 with a valid HMAC signature — here is my Python code."* | Frontier | ⚠ Exact only |
| **Multi-Step Policy Edge Cases** | 60 | *"I bought a laptop 35 days ago and it is faulty. Your return window is 30 days but the warranty is 2 years. What are my rights?"* | Frontier | ⚠ Exact only |
| **Out of Scope / Unanswerable** | 40 | *"Do you offer a student discount?"* · *"What is the capital of France?"* | Economy | ⚠ Exact only |

**Out-of-scope questions test refusal, not knowledge.** Each carries an `expected_behavior`: `decline_off_topic` (unrelated to TechStore — must decline even if the model knows the answer), `admit_unknown` (about TechStore but absent from the knowledge base — must say so, never invent), `answer_from_about` (answered by the About TechStore document, e.g. *"we don't sell washing machines"*), or `partial` (answer the covered half, admit the rest). The system prompt fixes the exact refusal wording (defined once in `config.py`), so `review_results.py` grades the behaviour automatically — and also flags the opposite failure, a model that refuses questions it *can* answer. The category is taken from the two largest easy categories, so the total stays at 500 and the economy/frontier split is unchanged.

The last three rows are where economy models demonstrably fail — arithmetic across multiple charges, reading code, and reconciling two policies that conflict. That failure is not incidental to the project; it is what Layer 3 exists to catch, and what makes the escalation demo compelling rather than theoretical.

**Corpus authoring method** (to avoid a week lost to writing JSON): author 10 genuine queries per category by hand (80 total) to fix tone and difficulty; generate ~55 variations per category from those exemplars plus the knowledge base; then **review every single one manually** against the knowledge base for answer correctness and category label. Budget 2–3 days for the review — it is not optional, and it is the step that determines whether the benchmark measures anything. Deliberately include: queries with no answer in the knowledge base (does the model hallucinate or admit ignorance?), two questions in one message, and hostile phrasing.

### Use-Case Validity Assessment (why we keep it — and what we add)

| Criterion | Verdict | Notes |
|:---|:---|:---|
| Natural complexity spectrum | ✅ Strong | Trivial FAQs → complex multi-order billing disputes. Exactly the spread the router needs to demonstrate value. |
| Cacheability | ✅ Strong, ⚠ with a catch | 15–30% of FAQ traffic repeats, but **26% of the corpus must never be semantically cached**. This is a feature: it forces us to build admission control, which is a differentiator. |
| Escalation visibility | ✅ Strong | Cheap models demonstrably waffle on billing disputes — the safety net is *watchable* in the demo. |
| Stakeholder relatability | ✅ Strongest available | Everyone understands a support bot and a dollar figure. |
| Objective ground truth | ❌ **Weak** | We write the questions, the knowledge base, and pick the judge. Circular on its own. |
| External comparability | ❌ **Weak** | No published numbers to compare against. |
| Novelty of domain | ⚠ Low | Customer support is the default demo in this space. |

**Decision: keep customer support as the narrative and demo domain, but never let it carry the quantitative claim alone.** The last three rows are precisely why [§7](#dual-track-evaluation-corpora) adds Track B. That split gives us all of: relatability (Track A demo), objectivity (GSM8K exact-match, HumanEval unit tests), and external comparability (MT-Bench, APGR/CPT vs. RouteLLM).

Alternatives considered and rejected as the *sole* domain:
* **Developer/code assistant** — objective grading via unit tests, but poor cacheability and low stakeholder relatability. **Retained as Track B**, which captures its benefit without its cost.
* **RAG over a public document corpus** — good RAGAS fit, but retrieval quality becomes a confound: it gets hard to say whether a quality delta came from the router or the retriever.
* **General chat assistant** — maximum external comparability, zero narrative and near-zero cacheability.

The dual-track design is strictly better than any single choice, and the reasoning above is itself worth presenting — it shows the evaluation design was chosen, not defaulted into.

### Why Customer Support Showcases the Router
1. **Natural complexity spectrum**: an ideal mix of trivial FAQs, standard tracking queries, and complex billing/technical disputes.
2. **High cacheability**: 15–30% of users ask identical or semantically equivalent questions.
3. **Clear escalation scenarios**: a cheap model summarises a return policy fine, but waffles on multi-order billing disputes — visible, satisfying escalation.
4. **Instant relatability**: mentors, engineers, and non-technical stakeholders immediately grasp the business impact.
5. **A genuine safety story**: user-scoped queries make cache admission control necessary rather than decorative.

### System Prompt
```
You are an expert customer support agent for TechStore, a premium consumer
electronics retailer. You assist customers with product inquiries, order tracking,
billing disputes, warranty claims, and technical troubleshooting.

Guidelines:
- Maintain an empathetic, professional, and concise tone.
- When answering policy questions, cite exact terms (e.g., 30-day return window).
- For billing disputes, detail all charges and explain the resolution clearly.
- Provide step-by-step diagnostic instructions for technical troubleshooting.
```

---

## Demonstration Strategy

The product's user is a **developer**, not a consumer, so a chat window alone proves nothing — the always-frontier baseline also produces a chat window, merely more expensively. The demonstration must make the *invisible* part visible. Five surfaces:

| # | Surface | What it proves | Effort |
|:--|:---|:---|:---|
| 1 | Streamlit chat + **routing inspector sidebar** | It works end to end | ~120 lines, Week 12 |
| 2 | Grafana dashboard | It saves real money, live | Week 11, mostly config |
| 3 | `X-Router-*` response headers | Developers can actually use it | Free — Week 1 |
| 4 | Benchmark report | It is proven, not claimed | Week 10 |
| 5 | **The one-line swap** | Zero-friction adoption | Free — already true |

Surface 5 is the strongest technical moment and costs nothing: any existing OpenAI-targeted application adopts the router by changing `base_url` and nothing else. It says "deployable today" more convincingly than any slide.

In the Streamlit demo the left pane is the customer's view and the right pane is the **routing inspector** — cache status, complexity score, tier, model, uncertainty score, latency, cost, cumulative savings, and any escalation or admission-rejection event. The inspector *is* the product; the chat is the costume. Design effort goes to the inspector, not the chat bubbles.

### The Six-Moment Demo Script (target: 6 minutes)

| Time | Moment | Point made |
|:---|:---|:---|
| 0:00 | **One-line swap** — change `base_url` on a plain OpenAI script, rerun, show `X-Router-Tier` / `X-Router-Cost-USD` in the headers | Adoption costs one line |
| 0:45 | **Easy question** — return policy → economy tier, ~300 ms, 94% saved | Cheap model, correct answer |
| 1:30 | **Cache hit** — same question, completely different wording → 2 ms, \$0.00 | Semantic cache, not string matching |
| 2:15 | ⭐ **Escalation** — triple-charge billing dispute → routed economy → uncertainty climbs to 0.62 → **ESCALATED** → frontier answers correctly | The router caught its own mistake before the customer saw it |
| 3:45 | ⭐ **Blocked attack** — ask about order #48213, then #48217 (cosine distance 0.01) → `ADMISSION REJECTED: entity_mismatch` | A naive semantic cache would have leaked one customer's data to another |
| 4:30 | **Kill a provider** — `docker stop` the primary mid-conversation; breaker trips on Grafana, traffic shifts, chat never breaks | Production resilience, not a prototype |
| 5:15 | **The numbers** — Grafana savings counter, then the report: measured reduction, TOST non-inferiority, five-arm Pareto plot | A measurement with a confidence interval, not a claim |

The 2:15 and 3:45 moments are the two that no competing open-source project can show. They should receive the most rehearsal.

> **Week 8 dependency**: sketch this sidebar on paper in Week 8, not Week 12. It consumes fields — individual uncertainty signals, admission-rejection reason, cache distance — that must be present in the API response schema. Discovering that in Week 12 means editing `app/gateway/` during the week reserved for recording.

---

## Licensing & Distribution Strategy

**Decision: MIT, public from Week 1. Do not attempt to sell it.**

**Blocking prerequisite**: confirm the institution's intellectual-property policy before publishing. Many institutions claim ownership or a licence over work produced for credit or under faculty supervision. This is the only genuinely blocking item in the project and is resolved by one email.

**Why not commercialise.** Enterprise infrastructure is bought on trust, not code quality: buyers require 24/7 support, security review (often SOC 2), a multi-year viability signal, and a financially-backed SLA. A twelve-week-old repository with no production deployments can offer none of these — a structural constraint, not a quality judgement. Portkey was acquired by Palo Alto Networks and Martian raised \$9M; neither competes on implementation. Additionally, LiteLLM is free, open source, and has ~18K stars, so the opening sentence of any sales conversation is "pay for something adjacent to a thing you already have for free."

**Why open source is the higher-value choice now.** The asset this project produces is *demonstrated capability*. A public repository containing a working distributed system, a CI-enforced safety suite, a pre-registered statistical evaluation, and a benchmark report with confidence intervals is a stronger professional credential than any plausible near-term licensing revenue.

**The asymmetry that settles it.** We may relicense our own code at any time while we remain the only contributors (see [§12 Q4](#12-critical-engineering-nuances--faqs)); we can never un-publish. For an unknown project, **obscurity is a far greater risk than appropriation**.

**MIT over Apache 2.0.** MIT is already the repository's licence, is the most common choice for student projects, and is the simplest to read. Apache 2.0 adds an explicit patent grant, which matters mainly if the project is ever commercialised; while the authors remain the only contributors, switching is a one-file change (see [§12 Q4](#12-critical-engineering-nuances--faqs)).

**Dataset licences are the real constraint, not the code licence.** Chatbot Arena, GSM8K, HumanEval, MBPP, MMLU, and MT-Bench each carry their own terms, and some restrict commercial use. `docs/DATA_LICENSES.md` enumerates every external data source with its licence and permitted use. If this project is ever commercialised, that file — not `LICENSE` — is what will constrain it.

**If traction appears**, the proven path is open-core: the router stays free and self-hostable; a hosted version with a dashboard, support, and an SLA is the commercial surface. That decision belongs to a future with users.

---

# 10. End-to-End 12-Week Phased Delivery Roadmap

```
W1-W2: Foundation & Safe Caching ──► W3-W4: Providers & MVP ──► W5-W6: Resilience & Streaming
                                                                           │
W11-W12: Packaging & Demo   ◄──── W9-W10: Learning & Proof ◄──── W7-W8: Routing & Escalation
```

> **Scope reality check.** Two people, twelve weeks, zero slack. If you fall behind, descope in this order: **(1) OpenTelemetry/Jaeger** — beautiful in a trace diagram, contributes nothing to the thesis; **(2) SLA-aware load balancing** — the valuable half of Week 9 is the learned policy; **(3) SSE streaming** — a gateway feature, not a routing contribution, and the safety net does not work there anyway. **Never descope Weeks 2, 7, 8, or 10.** Caching + classification + escalation + proof *is* the project; everything else is supporting infrastructure.

### Two-Person Work Split

The single largest schedule risk is not code — it is the corpus. The 500 questions and the knowledge base require no code, are therefore easy to postpone, and Week 10 then arrives with a working router and nothing to measure it on. **They are authored in Weeks 2–6, in parallel with the core build, by the person not writing the pipeline.**

**Phase 0 ([§9](#phase-0-the-techstore-support-agent-built-first)) occupies Weeks 1–2** and is not additional work: the knowledge base was already scheduled for Weeks 2–3, and the Streamlit UI was already scheduled for Week 12. Both simply move forward, where they are useful for eleven weeks instead of one. Net cost ≈ 3–4 days, absorbed by the Week 12 buffer.

| Wk | Stream A — core system | Stream B — data & infrastructure | Milestone |
|:--|:---|:---|:---|
| 1 | Docker Compose, CI, repo, Ollama dev provider | **Phase 0: knowledge base, orders, system prompt** | `validate_data.py` passes |
| 2 | **Phase 0: retriever, agent, CLI, Streamlit inspector** | **Seed questions; manual review pass** | 🎯 **Working support agent, demonstrable** |
| 3 | FastAPI gateway skeleton, auth, idempotency, health/ready | **KB expansion; 500 questions — start** | Gateway green; **logprobs confirmed per provider** |
| 4 | Exact + semantic cache, admission controller; provider adapters | **500 questions — continue** | Cache-safety suite passes |
| 4b | Rate limiter, DuckDB ledger; **agent repointed at the router** | | 🎯 **Working MVP — one-line swap proven** |
| 5 | Circuit breakers, failover | Chaos suite; 400 cache-calibration pairs | Provider outage survived |
| 6 | SSE streaming, degradation matrix | **500 questions + 60 conversations complete** | Streaming works; **corpora done** |
| 7 | Classifier, calibration, shared-embedding refactor | Arena bootstrap data; **`select_tier_pair.py`** | Tier pair chosen on evidence |
| 8 | Uncertainty checker, escalation guards | Threshold Pareto sweep; **sketch demo sidebar** | 🎯 **Core system complete** |
| 9 | Learning loop, exploration, IPW | SLA balancer, policy training pipeline | Self-improves; rollback proven |
| 10 | Router + oracle arms | **All five arms; protocol pre-registered first** | 🎯 **THE NUMBER** |
| 11 | Prometheus instrumentation | Grafana, Jaeger, Locust | Dashboards live |
| 12 | Streamlit demo, API docs | Demo video, report, presentation, ≥2 days buffer | 🎯 **Ship** |

---

### Week 1: Project Scaffold, CI & Phase 0 Data Layer
* Initialize repository, Docker Compose, Pydantic v2 schemas, `.github/workflows/ci.yml` (ruff + mypy + pytest + coverage) **on day one**, not in Week 12.
* Async FastAPI application with lifespan connection management.
* Async Redis pool and ChromaDB container; separate Redis logical DBs for cache vs. control keys.
* API-key auth (hashed keys → `client_id`/`tenant_id`), `Idempotency-Key` handling, secret-redaction log filter.
* Expose `POST /v1/chat/completions` (stub), `GET /health` (liveness), `GET /ready` (dependency health).
* **Phase 0 data layer**: knowledge base, order fixtures, system prompt, `validate_data.py`.
* **Exit Criteria**: `docker compose up` starts cleanly; CI green; `validate_data.py` passes with zero dangling references; unauthenticated requests rejected 401.

### Week 2: Phase 0 Support Agent (then caching, Weeks 3–4)
* `ExactCache` with the **full** semantic key (tools, response_format, max_tokens, stop, seed, routing_profile), temperature-tiered TTL, and singleflight stampede protection.
* `SemanticCache` on `all-MiniLM-L6-v2` + ChromaDB cosine, partitioned by `(tenant, system_prompt_hash, kb_version)`.
* **`CacheAdmissionController`**: entity-set gate, volatility blocklist, negation/antonym guard, length-ratio bound, 256-token truncation-tail fingerprint.
* `tests/test_cache_safety.py` with ≥40 adversarial pairs; **CI fails on any false positive**.
* `benchmarks/calibrate_cache.py` selecting $d$ by $F_{0.5}$ on 400 labelled pairs.
* **Phase 0**: retriever (keyword + MiniLM backends), `SupportAgent`, cost-accounting `Answer` record, CLI with `--dry-run` and `--batch`, Streamlit inspector panel. Meets the Phase 0 exit criteria in [§9](#phase-0-exit-criteria).
* **Exit Criteria (Week 2)**: 🎯 **a working support agent a third party can use in a browser**, with cost and latency logged per call; 100% top-3 retrieval recall on the labelled set; prompt under 900 tokens for every seed question.
* **Exit Criteria (caching, Weeks 3–4)**: identical request < 1 ms via Redis; equivalent query < 15 ms via ChromaDB; **all 40 adversarial pairs correctly rejected**; order-number swap across tenants provably cannot hit.

### Week 3: Provider Abstraction & Model Registry
* Abstract `LLMProvider` with `chat_completion()`, `health_check()`, `calculate_cost()`, and a declared **capability matrix** (tools, vision, json_schema, logprobs, context window).
* `OpenAIProvider` (`AsyncOpenAI`) and `AnthropicProvider` (`AsyncAnthropic`, with message-schema translation).
* `ModelRegistry` reading `pricing.yaml` with a mandatory `as_of` date; CI staleness check.
* Cost calculation reads `cached_tokens` and prices prefix-cached input at the discounted rate.
* Add a local **Ollama provider** for development so Weeks 1–9 consume near-zero API budget.
* ⚠ **Confirm per-token logprob availability on every candidate economy provider.** Uncertainty signal #1 carries 30% of the weight; Anthropic does not expose logprobs at all and hosted open-model providers vary. A provider without logprobs is usable via availability renormalization, but this must be known in Week 3, not discovered in Week 8.
* **Exit Criteria**: calls succeed across all providers; USD cost accurate to the cent against each provider's own billing dashboard for a 100-request sample; logprob support documented per provider in `pricing.yaml`.

### Week 4: Rate Limiting & Gateway MVP
* Distributed token-bucket via the corrected Lua script (Redis `TIME`, capacity-derived TTL), with **both** RPM and TPM buckets.
* Rate-limit headers (`X-RateLimit-Limit/Remaining/Reset`, `Retry-After`).
* DuckDB `RequestLogger` writing the full ledger schema.
* Redis-down fail-open path with in-process fallback limiter.
* **Exit Criteria (🎯 WORKING MVP)**: rate-limited, cached, multi-provider gateway processing requests end-to-end with durable cost logging; a 121-second idle **does not** reset a client's bucket.

### Week 5: Circuit Breakers & Failover Resilience
* 3-state `CircuitBreaker` with sliding-window trip condition ($V_{\min}=20$, error rate > 50%) and Redis-gated half-open probe admission.
* Decorrelated-jitter retry bounded by the request deadline.
* Failover controller: primary trips → transparent shift to secondary within the same tier.
* Chaos suite injecting 503s, timeouts, slow-loris responses, and malformed payloads.
* **Exit Criteria**: simulated OpenAI outage trips the breaker and subsequent requests succeed via Anthropic with zero client-visible errors; a single client sending 4xx traffic **cannot** trip the breaker for others.

### Week 6: SSE Streaming Pass-Through & Degradation Policy
* SSE engine yielding chunks with zero buffering; async token accumulator to `[DONE]`.
* Synthetic SSE re-chunking for cache hits.
* Mid-stream failure → `error` event + `X-Router-Stream-Aborted`, request not billed.
* Post-stream async cache population (subject to admission) and cost logging; `would_have_escalated` labels.
* Implement the full degradation matrix from [§13](#13-failure-semantics-edge-cases--degradation-policy).
* **Exit Criteria**: TTFT within 50 ms of a direct provider call; tokens and cost recorded accurately; killing Redis mid-run degrades cleanly instead of 500-ing.

### Week 7: Complexity Classifier, Calibration & Threshold Derivation
* Shared-embedding refactor: `app/embeddings.py` computes the MiniLM vector **once** per request.
* Stage 0 hard feasibility filters (context fit, capability matrix, explicit-model override).
* Stage 1 rule filter; Stage 2 MLP head on the shared vector.
* **Probability calibration** (Platt/isotonic) + reliability diagram + ECE.
* Bootstrap training from Chatbot Arena/RouteLLM preference data; assert zero overlap with the benchmark corpus.
* `benchmarks/tune_threshold.py` Pareto sweep to derive $\tau$ from the latency SLA.
* **`benchmarks/select_tier_pair.py`** — run the 50-query development subset against three economy candidates (GPT-6 Luna, Llama 3.3 70B via Groq, Llama 3.1 8B via Groq), measuring realised $\gamma$, saving, and quality for each. Cost ≈ \$1, one afternoon. Adopt the winner and republish the [§2](#-tier-pair-selection-why-the-cheapest-economy-model-is-not-the-best-one) table with measured columns.
* **Exit Criteria**: simple → Economy, complex → Frontier; **total router overhead < 20 ms at P95** (claim C3); ECE < 0.05; $\tau$ chosen by sweep, not by assumption; **tier pair selected on measured escalation rate, not on price ratio alone**.

### Week 8: Uncertainty-Based Escalation
* `UncertaintyChecker`: 5 signals with **availability-set renormalization**.
* `EscalationManager` with all four suppression guards (truncation, refusal, latency budget, cost ceiling) and single-escalation-only enforcement.
* Sticky conversation-level escalation with 3-turn decay.
* Escalation logging capturing every signal, the available set, and the suppressing guard.
* Guardrails from `app/config.py` constants (`ESCALATION_WARN`, `ESCALATION_CRITICAL`).
* **Sketch the Week 12 demo sidebar on paper (10 minutes).** It consumes fields — per-signal uncertainty values, admission-rejection reason, cache distance — that must exist in the response schema. Adding them now is free; adding them in Week 12 costs recording time.
* **Exit Criteria**: weak economy responses escalate; a `finish_reason == "length"` response does **not** escalate; a refusal does **not** escalate; escalation rate on the dev set within `ESCALATION_TARGET ± 0.03`.

### Week 9: Learned Policy, Exploration & SLA Balancing
* Offline training pipeline extracting IPW-weighted pairs from the DuckDB ledger.
* **ε-greedy exploration (5% of frontier-classified traffic)** and 2% shadow evaluation — the counterfactual label source.
* Offline policy-evaluation promotion gate; versioned artifacts with sidecar metrics; atomic symlink swap; 30-minute auto-rollback watchdog.
* `SLALoadBalancer` with log-softmax weighting and a 5% exploration floor.
* **Exit Criteria**: policy retrains and hot-swaps without restart; a deliberately-worse candidate is **rejected by the gate**; an injected regression triggers automatic rollback; exploration produces non-zero $Y=0$ labels for frontier-classified prompts.

### Week 10: Five-Arm Benchmark & Statistical Proof
* Curate Track A: 500 support queries + ~120-document `knowledge_base.jsonl` + 60 multi-turn conversations.
* Assemble Track B: GSM8K (300), HumanEval (164), MBPP (200), MMLU (400), MT-Bench (80).
* **Commit `docs/evaluation_protocol.md` with the pre-registered margin $\delta$ and primary endpoint BEFORE the first run.**
* Implement `run_baseline.py`, `run_economy.py`, `run_router.py`, `run_random.py`, `run_oracle.py`.
* `evaluate_quality.py`: RAGAS + cross-family LLM judge + dual-judge $\kappa$ + position randomisation; objective scorers for Track B (exact-match, sandboxed `pass@1` runner, MC accuracy).
* `stats.py`: TOST, bootstrap CIs, Wilcoxon, Holm–Bonferroni, per-category breakdown, power report.
* `generate_report.py`: automated Markdown report + the five-arm Pareto plot.
* **Exit Criteria (🎯 CORE DELIVERABLE)**: **40–60% measured cost reduction**, non-inferiority demonstrated at $\delta = 0.25$, router strictly dominates the random-at-matched-cost arm, and the fraction of oracle-available savings captured is reported.

### Week 11: Production Observability Stack
* Prometheus counters/histograms/gauges; Grafana provisioning with the 10 panels (`increase()` over range, DuckDB datasource for lifetime totals).
* OpenTelemetry tracing across all pipeline steps → Jaeger, with inbound `traceparent` propagation.
* Locust load test: 50 concurrent users; validate throughput, P99, and that router overhead holds under load.
* **Exit Criteria**: dashboard shows live savings with CI band and tier distribution; Jaeger shows end-to-end spans; P99 overhead stays < 25 ms at 50 concurrent users.

### Week 12: Packaging, Demo & Buffer
* Unified production `docker-compose.yml` (app, Redis, ChromaDB, Prometheus, Grafana, Jaeger, DuckDB volume).
* Streamlit demo (~120 lines) with a live routing sidebar: tier chosen, uncertainty signals, cache status, **admission rejections**, and running savings.
* `docs/`: architecture, API reference, deployment guide, threat model, evaluation protocol, benchmark report.
* 5–8 minute demo video: code walkthrough, live chat with a visible escalation, an attempted cache-collision attack that gets blocked, Grafana, benchmark results.
* **Reserve ≥2 days as explicit buffer.** A twelve-week plan with no slack is a ten-week plan that ships late.
* **Exit Criteria**: turnkey open-source repository; `git clone && docker compose up && make benchmark` reproduces the headline numbers on a clean machine.

---

# 11. Repository Structure & GitHub Setup

```
Tokenomics/
├── docker-compose.yml                  # app, redis, chromadb, prometheus, grafana, jaeger
├── docker-compose.dev.yml              # live-reload dev overrides
├── Dockerfile                          # multi-stage build
├── requirements.txt / requirements-dev.txt
├── .env.example
├── Makefile                            # run, test, benchmark, retrain, calibrate
├── README.md
├── LICENSE                             # MIT
├── CONTRIBUTING.md
├── SECURITY.md                         # vulnerability disclosure + secret-handling policy
├── .github/workflows/ci.yml            # ruff, mypy, pytest, coverage, cache-safety gate
│
├── techstore/                          # === PHASE 0: THE APPLICATION (built first) ===
│   ├── config.py                       # model ids, as-of-dated pricing, paths
│   ├── retriever.py                    # BM25-lite (stdlib) + MiniLM backends
│   ├── agent.py                        # retrieve -> context -> model -> Answer record
│   ├── cli.py                          # single question | --dry-run | --batch
│   ├── app.py                          # Streamlit chat + inspector panel
│   ├── validate_data.py                # corpus integrity + progress to 500
│   ├── system_prompt.txt
│   ├── data/
│   │   ├── knowledge_base.jsonl        # policy / product / billing / API documents
│   │   ├── orders.jsonl                # order fixtures incl. multi-charge dispute
│   │   └── questions_seed.jsonl        # category exemplars -> grows to the 500
│   └── tests/test_agent.py             # no API calls; free in CI
│
├── app/
│   ├── main.py  config.py  schemas.py  dependencies.py
│   ├── embeddings.py                   # ◄ SHARED MiniLM encoder, computed once per request
│   │
│   ├── security/
│   │   ├── auth.py                     # API key -> client_id / tenant_id
│   │   ├── idempotency.py              # Idempotency-Key store
│   │   └── redaction.py                # secret + PII log scrubbing
│   │
│   ├── gateway/
│   │   ├── router.py                   # POST /v1/chat/completions
│   │   ├── pipeline.py                 # request lifecycle orchestrator
│   │   ├── degradation.py              # ◄ dependency-failure policy matrix (§13)
│   │   └── middleware.py               # request ID, CORS, latency timer, traceparent
│   │
│   ├── cache/
│   │   ├── exact_cache.py              # SHA-256 Redis cache + singleflight
│   │   ├── semantic_cache.py           # MiniLM + ChromaDB
│   │   ├── admission.py                # ◄ entity gate, volatility, negation, truncation-tail
│   │   ├── vector_store.py             # VectorStore interface (Chroma | Qdrant | pgvector)
│   │   └── cache_manager.py            # unified cascade
│   │
│   ├── providers/
│   │   ├── base.py  openai_provider.py  anthropic_provider.py
│   │   ├── registry.py                 # provider + capability matrix
│   │   ├── ollama_provider.py          # ◄ local open-weight models for development ($0)
│   │   ├── openai_compatible.py        # ◄ Groq / Together / Fireworks (hosted open weights)
│   │   ├── pricing.yaml                # ◄ dated price table (CI staleness check)
│   │   └── capabilities.py             # tools / vision / json_schema / logprobs / ctx
│   │
│   ├── classifier/
│   │   ├── complexity.py               # rule + MLP on the shared vector
│   │   ├── calibration.py              # ◄ Platt / isotonic + ECE
│   │   ├── uncertainty.py              # 5-signal evaluator with renormalization
│   │   └── escalation.py               # escalation + 4 suppression guards
│   │
│   ├── routing/
│   │   ├── tier_router.py              # score -> tier, plus hard feasibility filters
│   │   ├── load_balancer.py            # log-softmax SLA balancer with exploration floor
│   │   ├── exploration.py              # ◄ epsilon-greedy + shadow sampling + propensities
│   │   └── learned_policy.py           # policy inference + hot swap + rollback watchdog
│   │
│   ├── resilience/
│   │   ├── circuit_breaker.py          # sliding-window, probe-gated
│   │   ├── retry.py  rate_limiter.py  fallback.py
│   │   └── budget.py                   # ◄ per-request deadline + cost ceiling
│   │
│   ├── observability/
│   │   ├── ledger.py                   # ◄ DuckDB accounting ledger
│   │   ├── baseline_estimator.py       # ◄ kappa-calibrated counterfactual cost
│   │   ├── request_logger.py  metrics.py  tracing.py
│   │
│   └── streaming/
│       └── sse_handler.py              # pass-through + synthetic re-chunk + abort semantics
│
├── benchmarks/
│   ├── datasets/
│   │   ├── customer_support_500.jsonl  # Track A corpus
│   │   ├── knowledge_base.jsonl        # ◄ RAGAS reference contexts (~120 docs)
│   │   ├── multiturn_60.jsonl          # ◄ multi-turn conversations
│   │   ├── cache_adversarial_400.jsonl # ◄ threshold calibration pairs
│   │   └── public/                     # ◄ Track B: gsm8k, humaneval, mbpp, mmlu, mt_bench
│   ├── run_baseline.py  run_economy.py  run_router.py
│   ├── run_random.py                   # ◄ null model at matched cost
│   ├── run_oracle.py                   # ◄ hindsight upper bound
│   ├── tune_threshold.py               # ◄ cost-latency-quality Pareto sweep
│   ├── select_tier_pair.py             # ◄ measures gamma per economy candidate (Week 7)
│   ├── calibrate_cache.py              # ◄ F_0.5 threshold selection
│   ├── evaluate_quality.py             # RAGAS + cross-family judge + kappa
│   ├── stats.py                        # ◄ TOST, bootstrap, Wilcoxon, Holm-Bonferroni, power
│   ├── generate_report.py              # Markdown report + Pareto plot
│   └── results/<run_id>/               # raw responses, committed for third-party re-grading
│
├── demo/streamlit_app.py
├── monitoring/{prometheus,grafana,jaeger}/
├── training/
│   ├── bootstrap_from_arena.py         # ◄ Chatbot Arena -> labelled pairs
│   ├── train_classifier.py  train_routing_policy.py
│   ├── offline_policy_eval.py          # ◄ promotion gate
│   └── models/
│
├── tests/
│   ├── conftest.py
│   ├── test_cache.py
│   ├── test_cache_safety.py            # ◄ 40+ adversarial pairs; CI-blocking
│   ├── test_classifier.py  test_uncertainty.py
│   ├── test_escalation_guards.py       # ◄ truncation / refusal / budget / ceiling
│   ├── test_resilience.py  test_degradation.py
│   ├── test_pipeline.py
│   └── load_tests/locustfile.py
│
└── docs/
    ├── architecture.md  api_reference.md  deployment_guide.md
    ├── threat_model.md                 # ◄ data flow, PII, secret handling
    ├── evaluation_protocol.md          # ◄ PRE-REGISTERED margin + primary endpoint
    ├── DATA_LICENSES.md                # ◄ every external dataset + its licence + permitted use
    └── benchmark_report.md
```

---

# 12. Critical Engineering Nuances & FAQs

### Q1: Do we need to build a complex frontend application?
**No.** The product is an API Gateway; its users are applications and developers. Visibility comes from HTTP response headers (`X-Router-Tier`, `X-Router-Cache`, `X-Router-Escalated`, `X-Router-Cost-USD`), the Grafana dashboard, automated benchmark reports, and a ~120-line Streamlit interface built solely for the demo video.

### Q2: How do we handle escalation during streaming?
Emitted tokens cannot be recalled, so we do not attempt destructive rollback. We tighten the upfront threshold ($\tau_{\text{stream}} = \tau - 0.10$), pass tokens through, and log `would_have_escalated` as training signal. Non-streaming requests run the full check-and-escalate loop. The asymmetry is measured and reported.

### Q3: How do we prevent false-positive hits in semantic caching?
Five independent controls, all of which must pass: tenant/system-prompt namespacing, **entity-set equality**, volatility blocklisting, a negation/antonym guard, and a length-ratio bound — plus a truncation-tail fingerprint for prompts beyond MiniLM's 256-token limit. The threshold itself is calibrated by $F_{0.5}$ (precision weighted double recall) rather than assumed. `tests/test_cache_safety.py` blocks CI on a single false positive. See [§3](#-semantic-cache-admission-control-the-most-important-safety-control-in-the-system).

### Q4: Can we change the open-source license later?
**Yes.** With two contributors and no external PRs merged, re-licensing from MIT to Apache 2.0 or proprietary requires only editing `LICENSE`. Once outside contributions land, you need their consent — so either decide before accepting PRs, or add a CLA.

### Q5: How do we prove the router is actually saving money?
We run the same corpora through **five arms** — always-frontier, always-economy, router, random-at-matched-cost, and an oracle — with both arms genuinely executed, so nothing is counterfactual. We report measured cost with a bootstrap CI, demonstrate non-inferiority by pre-registered TOST, show the router beats the random null model, and state what fraction of the oracle's available savings we captured. Live dashboard savings are separately labelled *estimated* and carry the $\kappa$ calibration interval. See [§7](#the-five-arm-comparative-harness).

### Q6: Isn't escalation just paying twice?
Yes — an escalated request costs $C_e + C_f$. But the break-even escalation rate on cost is $p < 1 - \rho = 0.94$, so cost is almost never the binding constraint; **latency is** ($p < 0.81$ on the mean, tighter at P99). This is why $\tau$ is derived from a Pareto sweep against a latency SLA rather than set to 0.50 by convention, and why four suppression guards prevent escalations that cannot help. See [§2](#the-escalation-break-even-a-result-that-reframes-the-whole-design).

### Q7: Won't the retraining loop make the router progressively more expensive?
It would have, in the v1 design — that is the selection-bias failure described in [§5](#-the-selection-bias-problem-the-deepest-flaw-in-v1s-design). Because labels only arrive for prompts sent to Economy, the policy can only ever learn "escalate more." ε-greedy exploration (5% of frontier-classified traffic), shadow evaluation (2%), and inverse-propensity weighting supply the missing counterfactual labels. Cost of the insurance: ~0.09% of baseline spend.

### Q8: What if the classifier is just learning prompt length?
A real risk, and we test for it. Ablations reported in the benchmark: (a) length-only logistic baseline, (b) rule-filter-only, (c) full model. If the full model does not beat the length-only baseline by a meaningful margin on Track B, the embedding contributes nothing and we say so. Feature-importance and a confusion matrix over the 8 Track-A categories are included.

### Q9: What happens if Redis or ChromaDB goes down?
Nothing user-visible. Every dependency has a declared degradation mode — cache failures fail *open* (skip the cache, serve from the provider), the rate limiter falls back to an in-process limiter, and only provider-tier failure is client-visible. The full matrix is in [§13](#13-failure-semantics-edge-cases--degradation-policy), and `tests/test_degradation.py` kills each dependency in turn.

### Q10: Do we need a React frontend to demo an API gateway?
**No — and a polished consumer UI would work against us.** A chat window proves nothing the baseline cannot also show. The ~120-line Streamlit demo exists so the *routing inspector* has somewhere to live: cache status, complexity score, tier, uncertainty signals, cost, cumulative savings. That sidebar is the product; the chat is the costume. The strongest technical moment costs nothing at all — an existing OpenAI application adopts the router by changing `base_url` and nothing else. Full demonstration strategy and the six-moment script are in [§9](#demonstration-strategy).

### Q11: Should we use open-weight models instead of paid APIs?
**In three different places, with three different answers.** *Locally, for development* — yes; Weeks 1–9 need no frontier model, and an Ollama backend reduces development spend to near zero. *Hosted, as the economy tier* — a strong candidate, decided empirically by `select_tier_pair.py` in Week 7. *For the benchmark, both tiers local* — no: the project's claim is denominated in dollars, and a locally-hosted model has no marginal per-token price, so the headline result degenerates to "60% of \$0". See [§2](#open-weight-models-where-they-fit).

### Q12: Isn't the cheapest economy model automatically the best choice?
**No, and this is the most counter-intuitive result in the specification.** A weaker economy model escalates more often, and every escalation pays *both* tiers. Llama 3.1 8B at a 20% escalation rate returns 49.1% savings — *worse* than GPT-6 Luna at 5% (61.9%) — despite being 3.6× cheaper per token. **Escalation rate dominates price ratio**, and escalation rate can only be measured, not looked up. Hence the Week 7 tier-pair experiment.

### Q13: Is the 500-query corpus used for training?
**No, and this is enforced.** The benchmark corpus is held out entirely; training draws from Chatbot Arena preference data and synthetic prompts. A CI check asserts zero hash overlap between training data and benchmark data. Training on the benchmark would invalidate every number in the report.

---

# 13. Failure Semantics, Edge Cases & Degradation Policy

A gateway's quality is judged by how it behaves when things go wrong. Every dependency has a declared failure mode; none of them is "500".

## Dependency Degradation Matrix

| Dependency | Failure Mode | Policy | Client Impact | Metric |
|:---|:---|:---|:---|:---|
| Redis (cache) | Down / timeout | **Fail open** — skip exact cache | Slower, correct | `llm_cache_degraded_total` |
| Redis (limiter) | Down / timeout | **Fail open** + in-process fallback limiter | None; enforcement weakened | `llm_ratelimit_degraded_total` |
| ChromaDB | Down / timeout | **Fail open** — skip semantic cache | Slower, correct | `llm_cache_degraded_total` |
| Embedding model | Load failure | **Fail open** — rule filter only, default Frontier | Costlier, correct | `llm_classifier_degraded_total` |
| Policy artifact | Corrupt / missing | Fall back to last-known-good, then to rule filter | Costlier, correct | `llm_policy_fallback_total` |
| Economy provider | 5xx / timeout | Circuit breaker → sibling economy → Frontier | None | `llm_failover_total` |
| Frontier provider | 5xx / timeout | Circuit breaker → sibling frontier | None | `llm_failover_total` |
| **All providers** | Down | **Fail closed** — 503 + `Retry-After` | Error (unavoidable) | `llm_all_providers_down_total` |
| DuckDB ledger | Write failure | Buffer in memory, spill to disk, never block the request | None | `llm_ledger_degraded_total` |

**Guiding principle**: *an optimisation component must never be able to take down the thing it optimises.* Cache, classifier, limiter, and ledger are all optional at request time. Only the provider call is mandatory.

## Edge-Case Catalogue

Each of these is a concrete test case, not a note.

| # | Edge Case | Failure If Unhandled | Handling |
|:--|:---|:---|:---|
| E1 | Order-number swap across users | **Data leak** via semantic cache | Entity-set equality gate + tenant partition |
| E2 | Negation flip (`enable`/`disable` 2FA) | Semantically inverted answer served | Antonym/negation lexicon guard |
| E3 | Prompt > 256 word-pieces | MiniLM truncates; distinct prompts collide | Truncation-tail SHA fingerprint; no semantic admission |
| E4 | `finish_reason == "length"` | Spurious escalation; frontier truncates identically | Truncation suppression guard |
| E5 | Safety refusal from economy model | Hedging regex fires; frontier also refuses; 2× cost | Refusal suppression guard |
| E6 | Client retries (standard SDK behaviour) | Double billing | `Idempotency-Key` store |
| E7 | $k$ concurrent identical cold requests | $k\times$ provider cost for one answer | Singleflight lock |
| E8 | Prompt exceeds economy context window | Guaranteed 400 from provider | Stage 0 context-fit hard filter |
| E9 | Request carries `tools` / `json_schema` | Economy model fumbles tool selection | Capability-matrix routing |
| E10 | Same messages, different `tools` array | Wrong cached response served | `tools` included in cache key |
| E11 | Multi-turn follow-up (`"and the other one?"`) | Meaningless classification and cache hit | Anaphora detection; cache off for turns ≥ 2 |
| E12 | Quality oscillation within a conversation | Worse perceived quality than uniform economy | Sticky escalation, 3-turn decay |
| E13 | Escalated response also low-confidence | Unbounded escalation chain, unbounded bill | Single-escalation-only rule |
| E14 | Escalation would breach client deadline | SLA violation | Latency-budget guard |
| E15 | Runaway spend (loop, abuse, bug) | Unbounded bill | Per-request + per-tenant cost ceiling |
| E16 | Mid-stream provider failure | Spliced, incoherent output | Abort stream with `error` event; do not bill |
| E17 | Cache hit on a `stream: true` request | Protocol violation for the client parser | Synthetic SSE re-chunking |
| E18 | Idle client's limiter key expires | Free full-capacity burst | TTL $\ge$ capacity/refill_rate |
| E19 | Replica clock skew | Bucket stops refilling entirely | Redis `TIME` as clock source |
| E20 | Cache eviction removes limiter keys | Silent quota bypass | Separate Redis logical DBs |
| E21 | Client sends 4xx-inducing traffic | Breaker trips for all tenants | 4xx/429 excluded from failure count |
| E22 | Provider recovering from outage | HALF-OPEN stampede re-kills it | Redis-gated single-probe admission |
| E23 | Provider-side prompt caching | Cost over-reported; savings misattributed | Read `cached_tokens`; price separately |
| E24 | Knowledge base updated | Stale-but-confident cached answers | `kb_version` in the collection partition key |
| E25 | Policy update degrades quality | Silent regression in production | Promotion gate + 30-min auto-rollback watchdog |
| E26 | Model deprecated by provider | Hard outage on a fixed model ID | Registry aliasing + `/ready` capability probe |
| E27 | Provider returns malformed / empty content | Downstream crash | Schema validation; treat as a provider failure |
| E28 | `n > 1` or high temperature | Wrong cached sample returned | Cache bypass |
| E29 | Non-English prompt | Rule filter misfires; MiniLM weaker | Language detection; default Frontier below a confidence floor |
| E30 | Prompt-injection text in a cached answer | Poisoned reuse across users | Cache admission requires a clean completion (`finish_reason == "stop"`, no refusal) |

## Privacy & Security Posture

* **The semantic cache is a prompt store.** ChromaDB holds raw prompt text, which for this domain includes customer PII. `docs/threat_model.md` documents: retention (30-day TTL on all cached documents), tenant isolation, encryption at rest on the volume, and a `DELETE /v1/cache/{tenant_id}` erasure endpoint for right-to-be-forgotten requests.
* **The ledger stores `prompt_hash`, never prompt text.** Raw prompts appear only in the semantic cache, only under tenant partition, only under a TTL.
* Provider keys are env-only and never logged; a regex log filter redacts `sk-` / `sk-ant-` prefixed strings at the handler level as defence in depth.
* Rate limits are per `client_id`, and cost ceilings are per tenant, so one compromised key cannot exhaust another tenant's budget.

---

# 14. Total Cost of Ownership & Project Budget

A cost-optimisation system that costs more to run than it saves is a net negative. We state the break-even explicitly — no comparable open-source project does, and it takes one table.

### Router Infrastructure Cost

| Component | Spec | Monthly (cloud) |
|:---|:---|:---|
| Gateway (2 vCPU, 4 GB) | CPU-only MiniLM inference | ~\$60 |
| Redis (1 GB managed) | cache + control keys | ~\$35 |
| ChromaDB (2 GB volume) | vector store | ~\$25 |
| Prometheus + Grafana | self-hosted alongside | ~\$10 |
| **Total** | | **≈ \$130/mo** |

### Break-Even Analysis

Savings per request under the Expected scenario with the GPT-6.1 Sol / GPT-6 Luna pair: $C_f(1 - R) = \$0.002300 \times 0.599 \approx \$0.001378$.

$$\text{Break-even volume} = \frac{\$130}{\$0.001378} \approx \mathbf{94{,}400 \text{ requests/month}} \approx 0.036 \text{ RPS}$$

**The router pays for itself at roughly two requests per minute** — effectively immediately for any real deployment. At 50 RPS (the Locust target, ~130M requests/month) it saves on the order of \$178K/month against baseline. Cheaper frontier pricing halves the absolute saving per request relative to earlier model generations, but the *percentage* saving — the project's claim — is unchanged.

### Project API Budget

**Available: \$50 of prepaid OpenAI credit**, with the project spend limit set to \$20/month (Settings → Project → Limits) and alerts at 50% and 100%. The judge runs on a separate Anthropic account.

Cost of **one full five-arm benchmark run** (Track A 500 + Track B 1,144), OpenAI side, at official prices:

| Frontier model | Track A | Track B | Standard | **Batch API (−50%)** |
|:---|---:|---:|---:|---:|
| GPT-6 Astra | \$11.86 | \$61.37 | \$73.24 | \$36.62 |
| **GPT-6.1 Sol (selected)** | **\$2.50** | **\$12.93** | **\$15.42** | **\$7.71** |

Plus the judge (Claude Sonnet 5, cross-family): \$9.86 per run, **\$4.93** batched.

**Why Sol, not Astra:** Astra costs 4.75× more to benchmark and buys 2.5 percentage points of headline saving (62.4% vs 59.9%). One batched Astra run would consume most of the \$50 credit.

**Cost controls, applied in order:**

| # | Lever | Effect |
|:--|:---|:---|
| 1 | **Mock mode** for UI work and development; Ollama local models once the gateway exists | Development spend → near \$0 |
| 2 | **No real API calls in tests** — CI uses fakes | CI spend → \$0 |
| 3 | **Batch API for every benchmark run** — nothing in a benchmark is latency-sensitive | \$15.42 → \$7.71 per run |
| 4 | **50-question development subset** for iteration; full corpus only for final numbers | ~\$0.15 per iteration |
| 5 | **`check_setup.py --ping` before any large run** — catches wrong model ids, keys and request parameters for under \$0.001 | Avoids paying for failed batches |
| 6 | **Mid-tier judge** (Claude Sonnet 5), which also gives cross-family independence | ~⅓ of an Opus-class judge |

Prompt caching is **not** counted as a saving: the only prefix shared across questions is the 170-token system prompt, likely below OpenAI's caching threshold, and cache *writes* bill at 1.25× input.

### Budget Allocation

| Item | When | OpenAI credit | Anthropic credit |
|:---|:---|---:|---:|
| Phase 0: 50 seed questions, plus ~3 reruns after fixes | Week 2 | ~\$1 | — |
| Development checks (mostly mock mode) | Weeks 3–9 | ~\$5 | — |
| Tier-pair selection (`select_tier_pair.py`) | Week 7 | ~\$1 | — |
| **Final benchmark: 3 full runs, batched** | Week 10 | **~\$23** | **~\$15** (judge) |
| Reserve: failed runs, re-grades, ablations | — | ~\$20 | — |
| **Total** | | **≈ \$50 (prepaid)** | **≈ \$15** |

**Whole project: ≈ \$65 in API spend**, against ~\$130 estimated in v2.1 at the previous generation's prices. A reduced-scope variant — Track B trimmed to 300 items, two final runs — costs ~\$6 on OpenAI and ~\$5 for the judge.

**Batch queue limit.** At usage tier 2, OpenAI allows 1,350,000 tokens queued per model in Batch. Several arms call GPT-6.1 Sol, so submitting all five at once would exceed it. The benchmark runner submits **one arm at a time**.

### 🚨 Spending Caps (configured)

* \$50 prepaid credit; auto-recharge off
* Project spend limit \$20/month, with email alerts at 50% (\$10) and 100% (\$20). OpenAI notes actual costs can slightly exceed the limit, which is why the early alert matters.
* The API key is created **inside the capped project** — a key from another project would not be covered by the limit

This project builds a system that calls LLMs in loops, with retries, escalation, and automated benchmark runners. **A defect in a retry loop or an off-by-one in a benchmark script can issue thousands of calls in minutes.** Note the symmetry with edge case **E15** in [§13](#edge-case-catalogue) — a per-request and per-tenant cost ceiling is a control this router implements for its users, applied first to our own accounts. The agent likewise never retries rate-limit or server errors automatically; it retries only a rejected request parameter, which OpenAI does not bill.

### Free and Discounted Access Worth Checking

* **GitHub Student Developer Pack** — bundled provider credits, via student email
* **Groq free tier** — rate-limited but potentially covers development traffic for the Llama economy candidates
* **Institutional research credits** — some departments hold cloud or API budgets for final-year projects; one email to the supervisor

---

## Appendix A: Revision History

### Changes in v2.7 (catalogue, knowledge-base wording)

| Area | v2.6 | v2.7 | Severity |
|:---|:---|:---|:---|
| Category questions | Missed product pages (q019, q020) | Product catalogue included for category comparisons; cross-checked against product pages; verified on a real re-run | Medium |
| Claims about real-world rules | Privacy, GST-invoice and power-bank documents asserted what law or airlines require | Restated as TechStore's own policy, or as advice to check the airline's rules | Medium |

### Changes in v2.6 (Phase 0 graded)

| Area | v2.5 | v2.6 | Severity |
|:---|:---|:---|:---|
| Phase 0 quality | Provisional, author-graded (44/6/0/0) | **Human-graded: 42 correct · 8 partial · 0 wrong · 0 hallucinated** | — |
| Grading rubric | One-line definitions per verdict | Precise definitions plus three rules; each traces to a real Phase 0 disagreement | High |
| AI judge | Trusted once two judges agree at κ ≥ 0.6 | Must first match **human** grades at κ ≥ 0.6; Phase 0 human-vs-AI agreement was κ = 0.50 | High |
| Test data | Order #48712's reversed hold undated | Dated; `validate_data.py` now requires a date on every reversed charge | Low |
| Answer style | — | Orders written as "order #48712" | Low |

### Changes in v2.5 (Phase 0 measured)

| Area | v2.4 | v2.5 | Severity |
|:---|:---|:---|:---|
| Frontier latency | 1.2–2 s assumed | **2.9 s median, 5.0 s p90, measured**; latency break-even 0.812 → 0.897 (provisional) | High |
| Latency target | Absolute P95 ≤ 2,000 ms | Relative: no worse than the always-frontier baseline (which itself misses 2 s) | High |
| Load-balancer latency penalty | Absolute 800 / 2,000 ms thresholds | Relative to the tier's typical P95 | Medium |
| Reproducibility | `temperature = 0` | Both models reject temperature; k = 3 repeats required; temperature recorded per result | High |
| Date handling | Unaddressed | Fixed simulated date in every prompt; fixtures validated against it | High |
| Phase 0 | Built, unmeasured | Measured: \$0.11 for 50 questions, 0 hallucinations, 10/10 out-of-scope, 44/6/0/0 provisional grading; fixes verified by targeted re-run | — |

### Changes in v2.4 (GPT-6 generation, official pricing)

| Area | v2.3 | v2.4 | Severity |
|:---|:---|:---|:---|
| Model pair | GPT-5.6 Sol / GPT-5.6 Luna (previous generation, prices from third-party research) | **GPT-6.1 Sol / GPT-6 Luna**, ids confirmed on the account, prices confirmed on OpenAI's official pricing page | **Critical** |
| Price ratio | $\rho$ = 0.0565 (18×) | $\rho$ = 0.050 (20×); expected saving 59.9%; claim unaffected | Medium |
| Economy candidates | Luna, Llama 3.3 70B, DeepSeek V3.1 | Luna, Llama 3.3 70B, Llama 3.1 8B — cheaper Sol shrank the others' advantage below 5× | Medium |
| Failover | Implied per-tier fallback | Both tiers must fail over together; Sol + Haiku is a 2× pair and fails the claim | High |
| Full-context cost | 21× / 24,000 tokens (v2.2, word-count estimate) | **7× / ~7,700 tokens, measured with the real tokenizer**. Retrieval still required; the earlier figure was overstated | High |
| Budget | ~\$130, generic | ≈ \$65 total, fitted to the \$50 prepaid OpenAI credit; Batch API for every benchmark run; queue limit handled by submitting arms sequentially | High |
| Prompt caching | Counted as a ~25% budget saving | Not counted: shared prefix too short; cache writes cost 1.25× input | Medium |
| Request parameters | `temperature`, `max_tokens` assumed accepted | Agent adapts if a reasoning model rejects them; output cap raised to 2,000 so hidden reasoning cannot produce empty answers | High |

### Changes in v2.3 (out-of-scope handling, licence)

| Area | v2.2 | v2.3 | Severity |
|:---|:---|:---|:---|
| Unanswerable questions | Every seed question was answerable; refusal behaviour untested | New `out_of_scope` category (40 of the 500) with `expected_behavior` labels; refusals graded automatically, including over-refusal of answerable questions | High |
| Refusal wording | Single generic instruction | Two fixed sentences (off-topic vs. not in documents), defined once in `config.py` and test-enforced against the system prompt | High |
| Catalogue boundaries | Model could not truthfully say what TechStore does *not* sell | About TechStore document: online-only, six product families, explicit exclusions, support hours | Medium |
| Empty retrieval | Empty `REFERENCE DOCUMENTS` heading | Explicit "No reference documents matched this question." | Medium |
| Category targets | Simple FAQ 80, Product info 60 | 60 and 40; total and economy/frontier split unchanged | Low |
| Licence | Apache 2.0 recommended | MIT, matching the repository's `LICENSE` | Low |
| Repository | `llm-cost-router` | `kanishksingh23/Tokenomics` | Low |

### Changes in v2.2 (Phase 0 application layer)

| Area | v2.1 | v2.2 | Severity |
|:---|:---|:---|:---|
| Retrieval | **Absent.** §2's 400-token assumption had no mechanism behind it | Specified and required; full-context concatenation shown to cost 21× (\\$49.50 vs \\$2.43 per benchmark arm) and is CI-guarded | **Critical** |
| Application layer | "TechStore is not software" — overstated | A ~660-line agent **is** built, in Weeks 1–2; the *retailer* still is not | **Critical** |
| Build order | Router first, baseline as a Week 10 script | Phase 0 first; the baseline arm exists from Week 2 and validates the corpus while correction is cheap | High |
| Prompt size | 400 tokens assumed | ~470 measured on the seed set; ρ 0.0565 → 0.0561 (immaterial), absolute cost +6% | Medium |
| Weeks 1–2 | Scaffold + caching | Scaffold + Phase 0; caching shifts to Weeks 3–4 | Medium |
| Demo UI | Week 12, 120 lines | Built Week 2 as the inspector panel; gains routing rows in Week 4 | Medium |
| Repository | `app/`, `benchmarks/`, `tests/` | `techstore/` added as the application layer | Low |


### Changes in v2.1 (current models, measured tier selection, corrected budget)

| Area | v2.0 | v2.1 | Severity |
|:---|:---|:---|:---|
| Model lineup | GPT-4o / GPT-4o-mini (2024 generation) | GPT-5.6 Sol / GPT-5.6 Luna, verified Sept 2026; full current-market table | **Critical** |
| Tier-pair selection | Implicit, unexamined | Shown to determine claim feasibility (Sonnet 5 / Haiku 4.5 yields 32%, failing the claim); **measured** by `select_tier_pair.py` in Week 7 | **Critical** |
| Cheapest-is-best assumption | Unstated | Refuted: escalation rate dominates price ratio; Llama 3.1 8B @ γ=20% (49.6%) loses to Luna @ γ=5% (61.5%) | **Critical** |
| Project budget | ~\$450 (computed on 2024 pricing) | ~\$130, with six itemised cost controls and mandatory hard spend caps | High |
| Open-weight models | Not addressed | Three distinct roles resolved: local for dev ✅, hosted as economy candidate ✅, fully-local benchmark ❌ (dollar claim collapses) | High |
| Logprob availability | Assumed | Week 3 per-provider verification task; affects 30% of uncertainty weight | High |
| Licence | MIT | Apache 2.0 (patent grant); full distribution strategy; `DATA_LICENSES.md`; institutional IP check flagged blocking | High |
| Use-case ambiguity | "TechStore" read as software to build | Stated explicitly as three text files; five datasets disambiguated | High |
| Corpus scheduling | Implied Week 10 | Authored Weeks 2–6 in parallel; two-person work-split table added | High |
| Demonstration | One line in Week 12 | Five surfaces + six-moment demo script + Week 8 schema dependency | Medium |
| Category examples | Abstract descriptions | Representative query per category, for corpus authoring | Medium |
| Economy-model capability | Not considered | Flagged: stronger 2026 economy models make the always-economy arm the serious objection | Medium |
| Break-even volume | 88,000 req/mo | 47,500 req/mo (~0.018 RPS) under the new pairing | Low |

### Changes from Spec v1.0 to v2.0

| Area | v1.0 | v2.0 | Severity |
|:---|:---|:---|:---|
| Hypothesis test | $H_0$ without equality; two-tailed for one-sided hypotheses; "$p>0.05$ ⇒ parity" | Pre-registered TOST non-inferiority, $\delta=0.25$, power analysis, Holm–Bonferroni | **Critical** |
| Semantic cache | 2 guardrails; cross-user reuse possible | 5-control admission gate; tenant partition; CI-blocking adversarial suite | **Critical** |
| Learning loop | Labels only from economy-routed traffic | ε-greedy exploration + shadow eval + IPW + promotion gate + auto-rollback | **Critical** |
| Baseline cost | `baseline_cost_usd` asserted as fact | $\kappa$-calibrated estimator, CI, estimated/measured distinction | **Critical** |
| Escalation direction | `C_composite > 0.45` vs `confidence < 0.45` (contradictory) | Renamed $U_{\text{composite}}$; one direction; one threshold constant | High |
| Missing logprobs (Anthropic) | Threshold silently 40% stricter | Availability-set renormalization | High |
| Rate limiter | Fixed 120 s TTL; app-supplied clock | Capacity-derived TTL; Redis `TIME`; RPM+TPM buckets | High |
| Circuit breaker | "5 consecutive within 60 s" | Sliding window, $V_{\min}$ + error rate; probe admission gate | High |
| Cache key | Omitted `tools`, `response_format`, `max_tokens`, `seed`; included chosen model | Full semantic key; routing profile replaces model | High |
| Embedding | Computed twice (~23 ms) | Computed once (~11 ms) | Medium |
| MiniLM 256-token truncation | Unaddressed | Truncation-tail fingerprint; no semantic admission | Medium |
| Evaluation corpus | Self-authored only; GPT-4o judged its own arm | Dual-track (+ objective ground truth); cross-family judge; $\kappa$ | High |
| Comparison arms | 1 (always-frontier) | 5 (+ economy, random@cost, oracle) + Pareto plot | High |
| Escalation guards | None | Truncation, refusal, latency-budget, cost-ceiling; single-escalation | High |
| Multi-turn | Unaddressed | Rolling-summary classification, sticky escalation, anaphora gate | High |
| Cost model | $\rho$ smuggled in; 55–67% vs 40–60% contradiction | $\rho$ derived; 4-scenario sensitivity table; reconciled | Medium |
| Threshold sourcing | $\tau = 0.50$ assumed | Derived from cost–latency–quality Pareto sweep | Medium |
| Calibration | Unaddressed | Platt/isotonic + reliability diagram + ECE | Medium |
| Bootstrap labels | File listed, source unstated | Chatbot Arena / RouteLLM + synthetic + holdout enforcement | High |
| Auth & tenancy | Absent | API keys, tenants, idempotency, redaction | High |
| Failure semantics | Absent | Full degradation matrix + 30-case edge catalogue | High |
| Prometheus counters | Reset on restart | `increase()` + DuckDB lifetime ledger | Medium |
| Threshold constants | 5% / 15% / 25% in three places | Single constant block | Low |
| TCO / budget | Absent | Infra break-even + \$450 project API budget | Medium |
