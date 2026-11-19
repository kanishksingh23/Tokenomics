"""Safety suite for the response cache, using TechStore's questions and product names.

Each pair: cache side A, ask side B. Pairs marked must-not-hit must miss; CI runs this
with the real embedding model and fails on any false hit.

    python cache_safety.py               # run the 75 pairs in data/cache_pairs.jsonl
    python cache_safety.py --stats       # what the TechStore agent's cache holds
    python cache_safety.py --clear
"""
from __future__ import annotations

import argparse
import json

import numpy as np

import config
from agent import SupportAgent
from tokenomics.response_cache import DEFAULT_THRESHOLD, ResponseCache, _minilm

CACHE_PATH = config.BASE_DIR / ".cache" / "responses.sqlite"
PAIRS_PATH = config.DATA_DIR / "cache_pairs.jsonl"


def run_safety(threshold: float) -> int:
    """Each pair: cache side A, ask side B. Pairs marked must_not_hit must miss.
    Returns the number of false hits (the suite fails on any)."""
    agent = SupportAgent(retriever_mode="keyword", mock=True, faq=False)
    extra = lambda q: frozenset(d.id for d in agent.named_products(q))  # noqa: E731
    with open(PAIRS_PATH, encoding="utf-8") as fh:
        pairs = [json.loads(line) for line in fh if line.strip()]
    encode = _minilm()
    false_hits, good_hits, paraphrases = [], 0, 0
    for i, p in enumerate(pairs):
        cache = ResponseCache(":memory:", encode=encode, threshold=threshold)
        cache.store(p["a"], "ANSWER-A", f"ns{i}", "m", extra(p["a"]))
        res = cache.lookup(p["b"], f"ns{i}", extra(p["b"]))
        if p["should_hit"]:
            paraphrases += 1
            good_hits += bool(res.hit)
            mark = "hit " if res.hit else "miss"
        else:
            if res.hit:
                false_hits.append(p)
            mark = "FALSE HIT" if res.hit else "blocked"
        print(f"{mark:9} [{p['kind']:16}] {p['a']!r} / {p['b']!r}  ->  {res.reason}")
    n_adv = len(pairs) - paraphrases
    print(f"\nthreshold {threshold}: adversarial pairs blocked {n_adv - len(false_hits)}/{n_adv}"
          f" · paraphrases reused {good_hits}/{paraphrases}")
    if false_hits:
        print(f"FAIL: {len(false_hits)} false hit(s)")
    return len(false_hits)


def main() -> int:
    ap = argparse.ArgumentParser(description="safe response cache")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--clear", action="store_true")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    args = ap.parse_args()
    if not (args.stats or args.clear):
        return 1 if run_safety(args.threshold) else 0
    cache = ResponseCache(CACHE_PATH, encode=lambda texts: np.zeros((len(texts), 384)))
    if args.clear:
        cache.clear()
        print("cache cleared")
    if args.stats:
        print(cache.stats())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
