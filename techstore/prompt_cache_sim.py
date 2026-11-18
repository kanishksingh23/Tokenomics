"""Technique 10: what would provider prompt caching do to our bill?

Replays conversations through the agent (mock mode, no API calls), captures the exact
prompts it would send, and prices them under OpenAI's published caching rules
(developers.openai.com/api/docs/guides/prompt-caching, read 2026-11-18):
  - only prompts of 1,024+ tokens are cached, by EXACT prefix from the first token
  - the cache point is the end of the latest user message (implicit mode)
  - writing new tokens into the cache costs 1.25x the input price (30-minute cache)
  - reading cached tokens costs 0.05x for GPT-6.1 Sol, 0.1x for other models
Two billing cases, because the docs don't say whether a write is charged when the prefix
is never reused (to be confirmed with a real call):
  "writes billed"   every cacheable prompt pays 1.25x on its new part
  "writes free"     only the discount on reads counts

    python prompt_cache_sim.py                  # classic vs cache layout vs classic + facts
"""
from __future__ import annotations

import argparse
import hashlib
import json

import config
from agent import _MSG_OVERHEAD, _REPLY_PRIMING, SupportAgent, count_tokens

MIN_CACHE_TOKENS = 1024


def _msg_tokens(messages: list[dict]) -> list[int]:
    return [count_tokens(m["content"]) + _MSG_OVERHEAD for m in messages]


def _prefix_keys(messages: list[dict]) -> list[str]:
    """keys[i] identifies the exact prefix messages[: i + 1]."""
    keys, h = [], hashlib.sha256()
    for m in messages:
        h.update(json.dumps(m, sort_keys=True, ensure_ascii=False).encode())
        keys.append(h.copy().hexdigest())
    return keys


def price_requests(requests: list[list[dict]], model: str, writes_billed: bool) -> dict:
    """Input cost of a sequence of prompts sent within the cache lifetime, under the rules
    above. Returns token and dollar totals with and without caching."""
    p = config.PRICING[model]
    cache: dict[str, int] = {}          # prefix key -> its length in tokens
    tot = {"input_tokens": 0, "cached_tokens": 0, "written_tokens": 0,
           "cost_no_cache": 0.0, "cost_with_cache": 0.0}
    for messages in requests:
        sizes = _msg_tokens(messages)
        total = sum(sizes) + _REPLY_PRIMING
        keys = _prefix_keys(messages)
        cum = [sum(sizes[: i + 1]) for i in range(len(sizes))]
        read = max((cum[i] for i, k in enumerate(keys) if k in cache), default=0)
        last_user = max(i for i, m in enumerate(messages) if m["role"] == "user")
        breakpoint_len = cum[last_user]
        written = 0
        if breakpoint_len >= MIN_CACHE_TOKENS:
            written = breakpoint_len - read
            for i in range(last_user + 1):
                if cum[i] >= MIN_CACHE_TOKENS:
                    cache[keys[i]] = cum[i]
        plain = total - read - written
        write_rate = p["cache_write"] if writes_billed else p["input"]
        tot["input_tokens"] += total
        tot["cached_tokens"] += read
        tot["written_tokens"] += written
        tot["cost_no_cache"] += total * p["input"] / 1e6
        tot["cost_with_cache"] += (plain * p["input"] + read * p["cached_input"]
                                   + written * write_rate) / 1e6
    return tot


def collect(path, **agent_kwargs) -> list[list[list[dict]]]:
    """The exact prompts per turn, per conversation, as the agent would send them."""
    agent = SupportAgent(mock=True, faq=False, **agent_kwargs)
    chats = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    out = []
    for chat in chats:
        history, prompts = [], []
        for question in chat["turns"]:
            res = agent.ask(question, history=history)
            prompts.append(agent.last_request["messages"])
            sent = res.sent_user_message if agent.prompt_layout == "cache" else question
            history += [{"role": "user", "content": sent}, {"role": "assistant", "content": res.answer}]
        out.append(prompts)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="simulate provider prompt caching")
    ap.add_argument("--conversations", default=str(config.DATA_DIR / "conversations_dev.jsonl"))
    ap.add_argument("--model", default=config.FRONTIER_MODEL)
    args = ap.parse_args()
    setups = {"classic": {}, "classic + facts memory": {"memory": "facts"},
              "cache layout": {"layout": "cache"}}
    rows = {}
    for name, kw in setups.items():
        chats = collect(args.conversations, model=args.model, **kw)
        rows[name] = {wb: [price_requests(c, args.model, wb) for c in chats] for wb in (True, False)}
    base = sum(r["cost_no_cache"] for r in rows["classic"][True])
    print(f"model {args.model}, {len(rows['classic'][True])} conversations; input side only "
          f"(output is the same in every setup)\n")
    print(f"{'setup':24} {'input tok':>9} {'cached':>7} {'written':>8} {'no cache':>9} "
          f"{'writes billed':>14} {'writes free':>12}")
    for name, by in rows.items():
        t = {k: sum(r[k] for r in by[True]) for k in by[True][0]}
        free = sum(r["cost_with_cache"] for r in by[False])
        print(f"{name:24} {t['input_tokens']:9d} {t['cached_tokens']:7d} {t['written_tokens']:8d} "
              f"${t['cost_no_cache']:.4f}  ${t['cost_with_cache']:.4f} ({t['cost_with_cache']/base-1:+.0%})"
              f"  ${free:.4f} ({free/base-1:+.0%})")
    print("\npercentages are against 'classic, no cache' input cost")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
