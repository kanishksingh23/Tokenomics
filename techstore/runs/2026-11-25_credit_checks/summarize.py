"""Tokens, cost and latency per run file. Usage: python summarize.py a.jsonl b.jsonl ..."""
import json
import statistics as st
import sys

print(f"{'run':34} {'n':>3} {'input':>6} {'cached':>6} {'output':>6} {'think':>5} {'total$':>8} {'p50 ms':>7} err cut")
for p in sys.argv[1:]:
    r = [json.loads(line) for line in open(p, encoding="utf-8") if line.strip()]
    m = lambda k: st.mean(x.get(k) or 0 for x in r)  # noqa: E731
    print(f"{p.split('/')[-1][:34]:34} {len(r):3d} {m('prompt_tokens'):6.0f} {m('cached_prompt_tokens'):6.0f} "
          f"{m('completion_tokens'):6.1f} {m('reasoning_tokens'):5.1f} {sum(x.get('cost_usd') or 0 for x in r):8.4f} "
          f"{st.median(x.get('latency_ms') or 0 for x in r):7.0f} {sum(bool(x.get('error')) for x in r):3d} "
          f"{sum(x.get('finish_reason') == 'length' for x in r):3d}")
