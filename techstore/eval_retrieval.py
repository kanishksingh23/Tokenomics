"""Compare retrieval backends on questions with labelled context_ids.

    python eval_retrieval.py                  # seed set
    python eval_retrieval.py --k 5 --misses   # list every missed gold document

Metric: context recall@k -- the fraction of labelled gold documents that appear
in the top k. A question needing three documents that gets two scores 2/3.

Caveat on the numbers: some knowledge-base tags were tuned while diagnosing
seed-set questions, which favours the keyword backend on this set. Report
absolute retrieval figures only from questions not used for tuning. The
router-vs-baseline comparison is unaffected, because every arm shares the
same retriever.
"""
from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict

import config
from retriever import KeywordRetriever, load_docs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=config.TOP_K)
    ap.add_argument("--questions", default=str(config.DATA_DIR / "questions_seed.jsonl"))
    ap.add_argument("--misses", action="store_true")
    args = ap.parse_args()

    docs = load_docs(config.KB_PATH)
    ids = [d.id for d in docs]
    titles = {d.id: d.title for d in docs}
    qs = [json.loads(l) for l in open(args.questions, encoding="utf-8") if l.strip()]
    qs = [q for q in qs if q.get("context_ids")]

    kw = KeywordRetriever(docs)
    methods = {"keyword": lambda q, n: [d.id for d, _ in kw.search(q, n)]}

    # What the agent actually sends: named product pages first, then keyword search.
    from agent import SupportAgent                      # noqa: PLC0415
    agent = SupportAgent(retriever_mode="keyword", top_k=args.k)
    methods["keyword+names"] = lambda q, n: agent.build_context(q)[1]

    try:
        from retriever import EmbeddingRetriever  # noqa: PLC0415
        emb = EmbeddingRetriever(docs)

        def emb_rank(q, n):
            return [d.id for d, _ in emb.search(q, n)]

        def hybrid(q, n, c=60):
            score = defaultdict(float)
            for ranking in (methods["keyword"](q, 20), emb_rank(q, 20)):
                for i, d in enumerate(ranking):
                    score[d] += 1 / (c + i + 1)          # reciprocal rank fusion
            return sorted(score, key=lambda d: -score[d])[:n]

        methods["embedding"] = emb_rank
        methods["hybrid"] = hybrid
    except Exception as exc:                              # noqa: BLE001
        print(f"(embedding backend unavailable: {exc}; keyword only)\n")

    cats = sorted({q["category"] for q in qs})
    gold = sum(len(q["context_ids"]) for q in qs)
    print(f"context recall@{args.k} on {len(qs)} labelled questions ({gold} gold docs)\n")
    print(f"{'method':10s} {'overall':>8s} {'ms/query':>9s}   " + "  ".join(f"{c[:11]:>11s}" for c in cats))

    missed = {}
    for name, fn in methods.items():
        per = defaultdict(lambda: [0, 0])
        hit, t0, miss = 0, time.perf_counter(), []
        for q in qs:
            got = set(fn(q["question"], args.k))
            for c in q["context_ids"]:
                ok = c in got
                hit += ok
                per[q["category"]][0] += ok
                per[q["category"]][1] += 1
                if not ok:
                    miss.append((q["id"], q["question"], c))
        ms = (time.perf_counter() - t0) * 1000 / len(qs)
        missed[name] = miss
        print(f"{name:10s} {100*hit/gold:7.1f}% {ms:9.2f}   "
              + "  ".join(f"{100*per[c][0]/per[c][1]:10.0f}%" for c in cats))

    if args.misses:
        for name, miss in missed.items():
            print(f"\n{name}: {len(miss)} missed gold documents")
            for qid, text, c in miss:
                print(f"  {qid}  {text[:58]:58s}  missing {titles.get(c, c)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
