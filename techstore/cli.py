"""Command-line harness. Single question, or batch over a JSONL file.

    python cli.py "Can I return opened headphones?"
    python cli.py --dry-run "Where is my order #48213?"     # shows context, no API call
    python cli.py --batch questions.jsonl --out results.jsonl
    python cli.py --conversations data/conversations_dev.jsonl --memory facts --out chats.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import config
from agent import SupportAgent
from tokenomics import tracing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="?")
    ap.add_argument("--model", default=None)
    ap.add_argument("--retriever", default=None, choices=["embedding", "keyword", "auto"])
    ap.add_argument("--top-k", type=int, default=None)
    ap.add_argument("--reasoning-effort", default=None,
                    help="none/low/medium/high (which values a model accepts varies)")
    ap.add_argument("--answer-length", default=None, choices=["default", "concise"],
                    help="concise: add the short-answer rule (techniques.py)")
    ap.add_argument("--verbosity", default=None,
                    help="provider length setting: low/medium/high, or off (default: low)")
    ap.add_argument("--no-faq", action="store_true", help="turn the FAQ shortcut off")
    ap.add_argument("--cache", action="store_true",
                    help="use the safe response cache (off by default so experiments always call the model)")
    ap.add_argument("--faq-drafts", action="store_true",
                    help="also serve FAQ answers not yet approved (measuring only, never customers)")
    ap.add_argument("--system-prompt", default=None,
                    help="prompt file in this folder (default: system_prompt.txt, the short version; "
                         "system_prompt_original.txt is the 436-token original)")
    ap.add_argument("--dry-run", action="store_true",
                    help="assemble and print the prompt context without calling the API")
    ap.add_argument("--mock", action="store_true",
                    help="run the full pipeline against a stub model: no API key, no spend")
    ap.add_argument("--batch", help="JSONL file with a 'question' field per line")
    ap.add_argument("--conversations", help="JSONL file, one chat per line: {'id', 'turns': [questions]}")
    ap.add_argument("--memory", default=None, choices=["off", "window", "facts", "summary"],
                    help="conversation memory: how earlier turns are kept (techniques.py)")
    ap.add_argument("--keep-turns", type=int, default=None,
                    help="earlier exchanges kept word for word (default 2)")
    ap.add_argument("--context-margin", type=lambda v: -1.0 if v.lower() == "off" else float(v),
                    default=None,
                    help="adaptive context: keep documents within this score of the best "
                         "(default 0.25 with the embedding retriever; off = always top-k)")
    ap.add_argument("--passage-margin", type=float, default=None,
                    help="smaller context: keep sentences within this score of the best (off by default)")
    ap.add_argument("--client", default=None,
                    help="client id for per-client spending limits (default: app-wide cap only)")
    ap.add_argument("--layout", default=None, choices=["classic", "cache"],
                    help="cache: fixed instructions first, documents last (provider prompt caching). "
                         "Default: classic for single questions; cache for --conversations "
                         "when memory is off")
    ap.add_argument("--out", help="write results as JSONL")
    ap.add_argument("--session", help="Langfuse session that groups this run's traces "
                                      "(default for --batch: the --out file name)")
    args = ap.parse_args()
    if args.layout is None and args.conversations and (args.memory or config.MEMORY_MODE) == "off":
        args.layout = config.CHAT_LAYOUT     # chats: cache layout by default (config.py)

    agent = SupportAgent(model=args.model, retriever_mode=args.retriever,
                         top_k=args.top_k, mock=args.mock,
                         reasoning_effort=args.reasoning_effort, system_prompt=args.system_prompt,
                         answer_length=args.answer_length, verbosity=args.verbosity,
                         faq=False if args.no_faq else None, faq_drafts=args.faq_drafts,
                         cache=True if args.cache else None,
                         memory=args.memory, keep_turns=args.keep_turns, layout=args.layout,
                         context_margin=args.context_margin, passage_margin=args.passage_margin)
    print(f"model={agent.model}{' (MOCK)' if agent.mock else ''}  "
          f"retriever={agent.retriever.name}  docs={len(agent.docs)}  "
          f"top_k={agent.top_k}  effort={agent.reasoning_effort or 'default'}  "
          f"prompt={agent.system_prompt_name}  length={agent.answer_length}"
          f"{'  verbosity=' + agent.verbosity if agent.verbosity else ''}"
          f"  cache={'on' if agent.cache else 'off'}  memory={agent.memory_mode}"
          f"  layout={agent.prompt_layout}"
          f"  faq={len(agent.faq.entries) if agent.faq else 0} answers"
          f"{' (incl. drafts)' if args.faq_drafts else ''}", file=sys.stderr)

    if args.conversations:
        chats = [json.loads(line) for line in open(args.conversations, encoding="utf-8") if line.strip()]
        out = open(args.out, "w", encoding="utf-8") if args.out else None
        session = args.session or (Path(args.out).stem if args.out else None)
        total, n = 0.0, 0
        for chat in chats:
            history: list[dict] = []
            for turn, question in enumerate(chat["turns"], 1):
                res = agent.ask(question, session_id=f"{session}-{chat['id']}" if session else chat["id"],
                                history=history, client_id=args.client)
                total += res.cost_usd
                n += 1
                print(f"[{chat['id']} turn {turn}] {res.prompt_tokens:5d} in  ${res.cost_usd:.6f}  "
                      f"{question[:55]}", file=sys.stderr)
                # With layout "cache" the history keeps each message exactly as sent, so the
                # next prompt starts with this one and the provider can reuse its cache.
                sent = res.sent_user_message if agent.prompt_layout == "cache" else question
                history += [{"role": "user", "content": sent},
                            {"role": "assistant", "content": res.answer}]
                if out:
                    rec = json.loads(res.to_json())
                    rec.update({"conversation_id": chat["id"], "id": f"{chat['id']}-{turn}"})
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if out:
            out.close()
        tracing.flush()
        tag = " ESTIMATED (mock)" if agent.mock else ""
        print(f"\ntotal ${total:.4f} over {n} turns in {len(chats)} conversations{tag}", file=sys.stderr)
        return 0

    if args.batch:
        rows = [json.loads(line) for line in open(args.batch, encoding="utf-8") if line.strip()]
        out = open(args.out, "w", encoding="utf-8") if args.out else None
        session = args.session or (Path(args.out).stem if args.out else None)
        total = 0.0
        for i, row in enumerate(rows, 1):
            res = agent.ask(row["question"], session_id=session, client_id=args.client)
            total += res.cost_usd
            tag = {"faq": " FAQ", "cache": f" CACHE-{(res.cache_kind or '').upper()}"}.get(res.served_by, "")
            print(f"[{i}/{len(rows)}]{tag} ${res.cost_usd:.6f}  {res.latency_ms:7.1f}ms  "
                  f"{row['question'][:60]}", file=sys.stderr)
            if out:
                rec = json.loads(res.to_json())
                rec.update({k: row[k] for k in ("id", "category") if k in row})
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if out:
            out.close()
        tracing.flush()
        tag = " ESTIMATED (mock)" if agent.mock else ""
        print(f"\ntotal ${total:.4f} over {len(rows)} questions "
              f"(mean ${total/max(len(rows),1):.6f}){tag}", file=sys.stderr)
        if tracing.enabled() and session:
            print(f"Langfuse: traces grouped under session '{session}'", file=sys.stderr)
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

    res = agent.ask(args.question, session_id=args.session, client_id=args.client)
    tracing.flush()
    if res.error:
        print(f"ERROR: {res.error}", file=sys.stderr)
        return 1
    print(res.answer)
    est = " (ESTIMATE: output length assumed)" if res.cost_is_estimate else ""
    print(f"\n-- {res.model} | {res.prompt_tokens}+{res.completion_tokens} tok "
          f"| ${res.cost_usd:.6f}{est} | {res.latency_ms:.0f}ms "
          f"| docs={','.join(res.retrieved)}", file=sys.stderr)
    url = tracing.trace_url(res.trace_id)
    if url:
        print(f"-- trace: {url}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
