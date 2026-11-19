# Tokenomics

[![CI](https://github.com/kanishksingh23/Tokenomics/actions/workflows/ci.yml/badge.svg)](https://github.com/kanishksingh23/Tokenomics/actions/workflows/ci.yml)

Tokenomics cuts what an app pays for LLM calls without making answers worse: a set of
measured techniques (FAQ shortcut, safe response cache, spending limits, conversation memory,
prompt-caching layout, adaptive context, reasoning and answer-length control) behind one
OpenAI-compatible gateway, with model routing last. Every saving is checked for quality.

## Repository layout

| Folder | What it is |
|---|---|
| [`tokenomics/`](tokenomics/) | **The product**: the techniques (each works on any OpenAI-style request) and the gateway |
| [`techstore/`](techstore/) | **The test app**: a pretend electronics shop's support chatbot, its data, experiments and results |
| [`Tokenomics.md`](Tokenomics.md) | The full specification and roadmap (§10) |

Install the package once from the repo root: `pip install -e ".[gateway,embeddings]"`.
**Already have a copy from before 18 Nov 2026?** Run that once after `git pull`: the shared code
moved from `techstore/` into the `tokenomics/` package, and the TechStore scripts need it installed.

- **Run the gateway** (any OpenAI-compatible app switches with two settings):
  [tokenomics/README.md](tokenomics/README.md)
- **Run the TechStore chatbot**, directly or through the gateway: [techstore/README.md](techstore/README.md)

New to the terms used here? See the [learning guide](LEARNING.md): every concept in the project, explained in plain language. 
