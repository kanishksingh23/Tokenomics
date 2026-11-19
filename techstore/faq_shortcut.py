"""TechStore's FAQ answers: evaluate, review and approve them.

The matcher itself is the product's (tokenomics/faq.py); the answers in data/faq.jsonl are
TechStore's. Only answers a person has approved are ever served.

    python faq_shortcut.py --eval                         # what it would do with each dev question
    python faq_shortcut.py --review                       # writes FAQ_REVIEW.md: answers beside sources
    python faq_shortcut.py --approve faq_cancel,faq_emi --by Kanishk   # (or --approve all)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json

import config
from tokenomics.faq import DEFAULT_MARGIN, DEFAULT_THRESHOLD, FaqShortcut
from tokenomics.faq import load_faq as _load

FAQ_PATH = config.DATA_DIR / "faq.jsonl"


def load_faq(path=FAQ_PATH) -> list[dict]:
    return _load(path)


def evaluate(threshold: float, margin: float) -> None:
    """Treat every dev question as a customer question and show what the shortcut would do.
    A hit is right when the FAQ's source documents overlap the documents the question needs,
    and the question is not one that must be declined or admitted as unknown."""
    from agent import SupportAgent  # noqa: PLC0415
    from review_results import load_jsonl  # noqa: PLC0415

    agent = SupportAgent(retriever_mode="keyword", mock=True)
    block = lambda q: "names a product" if agent.named_products(q) else None  # noqa: E731
    sc = FaqShortcut(load_faq(), include_drafts=True, threshold=threshold, margin=margin, block=block)
    rows = load_jsonl(config.DEV_QUESTIONS_PATH)
    served = right = wrong = 0
    for q in rows:
        m = sc.lookup(q["question"])
        if not m.entry:
            continue
        served += 1
        ok = (q.get("expected_behavior") not in ("decline_off_topic", "admit_unknown")
              and bool(set(m.entry["sources"]) & set(q.get("context_ids", []))))
        right += ok
        wrong += not ok
        print(f"{'OK ' if ok else 'BAD'} {q['id']} {m.score:.2f} {m.entry['id']:22} {q['question']}")
    print(f"\nthreshold {threshold} margin {margin}: served {served}/{len(rows)} "
          f"({right} right, {wrong} WRONG)")


def write_review(path=config.BASE_DIR / "FAQ_REVIEW.md") -> None:
    """A page for approving answers: each answer beside the full text of its sources."""
    docs = {}
    with open(config.KB_PATH, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                d = json.loads(line)
                docs[d["id"]] = d
    out = ["# FAQ answers to approve", "",
           "These answers reach customers **with no model checking them**. For each one, check:",
           "every fact is in the source text below it; nothing important from the source is missing",
           "for this question; the tone is right. Then approve, e.g.:",
           "", "```", "python faq_shortcut.py --approve faq_cancel,faq_emi --by Kanishk", "```", "",
           "(Run it from `techstore/`. One-time setup after pulling: "
           "`pip install -e \".[gateway,embeddings]\"` from the repo root.)", "",
           "To change an answer, edit it in `data/faq.jsonl` first (keep `sources` accurate).", ""]
    for e in load_faq():
        out += [f"## {e['id']}: {e['question']}  ({e['status']})", "",
                f"**Answer:** {e['answer']}", "",
                f"*Also matches:* {'; '.join(e.get('examples', []))}", ""]
        for sid in e["sources"]:
            out += [f"> **Source `{sid}`: {docs[sid]['title']}**  ", f"> {docs[sid]['text']}", ""]
    path.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {path.name}: {len(load_faq())} answers")


def approve(ids: str, by: str) -> None:
    entries = load_faq()
    wanted = {e["id"] for e in entries} if ids == "all" else set(ids.split(","))
    unknown = wanted - {e["id"] for e in entries}
    if unknown:
        raise SystemExit(f"unknown FAQ ids: {sorted(unknown)}")
    today = dt.date.today().isoformat()
    for e in entries:
        if e["id"] in wanted:
            e.update(status="approved", approved_by=by, approved_on=today)
    with open(FAQ_PATH, "w", encoding="utf-8") as fh:
        for e in entries:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"approved {len(wanted)} by {by}; "
          f"{sum(e['status'] == 'approved' for e in entries)}/{len(entries)} now approved")


def main() -> int:
    ap = argparse.ArgumentParser(description="FAQ shortcut")
    ap.add_argument("--eval", action="store_true")
    ap.add_argument("--review", action="store_true", help="write FAQ_REVIEW.md")
    ap.add_argument("--approve", help="comma-separated FAQ ids, or 'all'")
    ap.add_argument("--by", help="who approved (required with --approve)")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    ap.add_argument("--margin", type=float, default=DEFAULT_MARGIN)
    args = ap.parse_args()
    if args.approve:
        if not args.by:
            ap.error("--approve needs --by NAME")
        approve(args.approve, args.by)
    if args.review:
        write_review()
    if args.eval:
        evaluate(args.threshold, args.margin)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
