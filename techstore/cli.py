"""Command-line harness. Single question, or batch over a JSONL file.

    python cli.py "Can I return opened headphones?"
    python cli.py --dry-run "Where is my order #48213?"     # shows context, no API call
    python cli.py --batch questions.jsonl --out results.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys

from agent import SupportAgent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="?")
    ap.add_argument("--model", default=None)
    ap.add_argument("--retriever", default=None, choices=["embedding", "keyword", "auto"])
    ap.add_argument("--top-k", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true",
                    help="assemble and print the prompt context without calling the API")
    ap.add_argument("--mock", action="store_true",
                    help="run the full pipeline against a stub model: no API key, no spend")
    ap.add_argument("--batch", help="JSONL file with a 'question' field per line")
    ap.add_argument("--out", help="write results as JSONL")
    args = ap.parse_args()

    agent = SupportAgent(model=args.model, retriever_mode=args.retriever,
                         top_k=args.top_k, mock=args.mock)
    print(f"model={agent.model}{' (MOCK)' if agent.mock else ''}  "
          f"retriever={agent.retriever.name}  docs={len(agent.docs)}  "
          f"top_k={agent.top_k}", file=sys.stderr)

    if args.batch:
        rows = [json.loads(line) for line in open(args.batch, encoding="utf-8") if line.strip()]
        out = open(args.out, "w", encoding="utf-8") if args.out else None
        total = 0.0
        for i, row in enumerate(rows, 1):
            res = agent.ask(row["question"])
            total += res.cost_usd
            print(f"[{i}/{len(rows)}] ${res.cost_usd:.6f}  {res.latency_ms:7.1f}ms  "
                  f"{row['question'][:60]}", file=sys.stderr)
            if out:
                rec = json.loads(res.to_json())
                rec.update({k: row[k] for k in ("id", "category") if k in row})
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if out:
            out.close()
        tag = " ESTIMATED (mock)" if agent.mock else ""
        print(f"\ntotal ${total:.4f} over {len(rows)} questions "
              f"(mean ${total/max(len(rows),1):.6f}){tag}", file=sys.stderr)
        return 0

    if not args.question:
        ap.error("provide a question, or use --batch")

    if args.dry_run:
        ctx, retrieved, orders, ms = agent.build_context(args.question)
        approx = len(ctx.split()) * 4 // 3
        print(f"retrieved={retrieved}  orders={orders}  retrieval={ms:.2f}ms  "
              f"~{approx} prompt tokens\n", file=sys.stderr)
        print(ctx)
        return 0

    res = agent.ask(args.question)
    if res.error:
        print(f"ERROR: {res.error}", file=sys.stderr)
        return 1
    print(res.answer)
    est = " (ESTIMATE: output length assumed)" if res.cost_is_estimate else ""
    print(f"\n-- {res.model} | {res.prompt_tokens}+{res.completion_tokens} tok "
          f"| ${res.cost_usd:.6f}{est} | {res.latency_ms:.0f}ms "
          f"| docs={','.join(res.retrieved)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
