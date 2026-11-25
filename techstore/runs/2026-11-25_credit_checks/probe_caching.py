"""PENDING_CREDITS #7: how provider prompt caching behaves in Chat Completions.

Sends one ~1,500-token prompt three times (Sol) and prints the full `usage` of each reply:
is caching on by default, which fields report cached / written tokens, is a write billed.
Run from techstore/:  python runs/2026-11-25_credit_checks/probe_caching.py
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from openai import OpenAI  # noqa: E402

import config  # noqa: E402
from tokenomics.pricing import price  # noqa: E402

docs = [json.loads(line) for line in open(config.KB_PATH, encoding="utf-8") if line.strip()]
system = (config.BASE_DIR / "system_prompt.txt").read_text() + "\n\nREFERENCE DOCUMENTS\n"
system += "\n\n".join(f"[{d['id']}] {d['title']}\n{d['text']}" for d in docs[:14])
client = OpenAI()
model = config.FRONTIER_MODEL
out = []
for i, q in enumerate(["Is delivery free?", "Is delivery free?", "What is the return window?"]):
    if i:
        time.sleep(3)
    r = client.chat.completions.create(model=model, messages=[
        {"role": "system", "content": system}, {"role": "user", "content": q}])
    u = r.usage.model_dump()
    d = u.get("prompt_tokens_details") or {}
    cost = price(model, u["prompt_tokens"], u["completion_tokens"],
                 d.get("cached_tokens") or 0, d.get("cache_write_tokens") or 0)
    print(f"call {i + 1} ({q!r}): cost ${cost:.6f}\n{json.dumps(u, indent=1)}\n")
    out.append({"call": i + 1, "question": q, "usage": u, "cost_usd": cost})
Path(__file__).with_name("caching_probe.json").write_text(json.dumps(out, indent=1))
