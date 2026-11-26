"""Tokens, cost and latency per run file. Usage: python summarize.py a.jsonl b.jsonl ..."""
import json
import statistics as st
import sys


def mean(rows, key):
    return st.mean(x.get(key) or 0 for x in rows)


print(f"{'run':34} {'n':>3} {'input':>6} {'cached':>6} {'output':>6} {'think':>5} "
      f"{'total$':>8} {'p50 ms':>7} err cut")
for p in sys.argv[1:]:
    r = [json.loads(line) for line in open(p, encoding="utf-8") if line.strip()]
    cost = sum(x.get("cost_usd") or 0 for x in r)
    p50 = st.median(x.get("latency_ms") or 0 for x in r)
    errors = sum(bool(x.get("error")) for x in r)
    cut = sum(x.get("finish_reason") == "length" for x in r)
    print(f"{p.split('/')[-1][:34]:34} {len(r):3d} {mean(r, 'prompt_tokens'):6.0f} "
          f"{mean(r, 'cached_prompt_tokens'):6.0f} {mean(r, 'completion_tokens'):6.1f} "
          f"{mean(r, 'reasoning_tokens'):5.1f} {cost:8.4f} {p50:7.0f} {errors:3d} {cut:3d}")
