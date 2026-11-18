"""Technique 8, the FAQ shortcut: answer common questions from human-approved answers,
with no model call at all (zero tokens, zero cost, instant).

The answers live in data/faq.jsonl. Each entry has a canonical question, a few example
phrasings (used only for matching), the answer, the documents it comes from, and a status.
**Only entries with status "approved" are ever served.** A saved answer reaches the customer
without any model checking it, so a person must approve every one.

A question gets a saved answer only if ALL of these hold:
  1. its meaning is close to one FAQ (MiniLM similarity >= threshold)
  2. it is clearly closer to that FAQ than to any other (no near-tie)
  3. it contains no digits: order numbers and amounts need a personal answer
  4. it is a single question
  5. the caller does not block it (TechStore blocks questions that name a product,
     which may need that product's page)
Everything else goes to the model as usual.

    python faq_shortcut.py --eval                         # what it would do with each dev question
    python faq_shortcut.py --review                       # writes FAQ_REVIEW.md: answers beside sources
    python faq_shortcut.py --approve faq_cancel,faq_emi --by Kanishk   # (or --approve all)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from dataclasses import dataclass

import numpy as np

import config

FAQ_PATH = config.DATA_DIR / "faq.jsonl"
DEFAULT_THRESHOLD = 0.75
DEFAULT_MARGIN = 0.05


@dataclass
class FaqMatch:
    entry: dict | None         # the FAQ served, or None
    best_id: str | None        # closest FAQ even when not served (for analysis)
    score: float
    reason: str                # why it was or wasn't served


def load_faq(path=FAQ_PATH) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def _minilm():
    from sentence_transformers import SentenceTransformer  # noqa: PLC0415
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    return lambda texts: model.encode(texts, normalize_embeddings=True)


class FaqShortcut:
    def __init__(self, entries: list[dict], encode=None, threshold: float = DEFAULT_THRESHOLD,
                 margin: float = DEFAULT_MARGIN, include_drafts: bool = False, block=None):
        """encode: list[str] -> array of unit vectors (default MiniLM).
        include_drafts: match draft entries too; for measuring only, never for customers.
        block: optional question -> reason|None, for app-specific exclusions."""
        self.entries = [e for e in entries if include_drafts or e.get("status") == "approved"]
        self.threshold, self.margin, self.block = threshold, margin, block
        # The embedding model loads only if there is something to match against.
        self.encode = encode or (_minilm() if self.entries else None)
        # Every phrasing of every entry is a matching target; a question scores against
        # the closest phrasing of each entry.
        self._owner, texts = [], []
        for i, e in enumerate(self.entries):
            for t in [e["question"], *e.get("examples", [])]:
                self._owner.append(i)
                texts.append(t)
        self._vecs = np.asarray(self.encode(texts)) if texts else np.zeros((0, 1))

    def scores(self, question: str) -> list[tuple[float, int]]:
        """(best similarity, entry index) per entry, best first."""
        if not self.entries:
            return []
        sims = self._vecs @ np.asarray(self.encode([question]))[0]
        best: dict[int, float] = {}
        for owner, s in zip(self._owner, sims, strict=True):
            best[owner] = max(best.get(owner, -1.0), float(s))
        return sorted(((s, i) for i, s in best.items()), reverse=True)

    def lookup(self, question: str) -> FaqMatch:
        ranked = self.scores(question)
        if not ranked:
            return FaqMatch(None, None, 0.0, "no approved FAQ entries")
        score, idx = ranked[0]
        best_id = self.entries[idx]["id"]

        def miss(reason):
            return FaqMatch(None, best_id, score, reason)

        if score < self.threshold:
            return miss(f"not close enough ({score:.2f} < {self.threshold:.2f})")
        if len(ranked) > 1 and score - ranked[1][0] < self.margin:
            return miss(f"near-tie with {self.entries[ranked[1][1]]['id']}")
        if re.search(r"\d", question):
            return miss("contains a number (order id or amount needs a personal answer)")
        if question.count("?") > 1:
            return miss("more than one question")
        if self.block:
            reason = self.block(question)
            if reason:
                return miss(reason)
        return FaqMatch(self.entries[idx], best_id, score, "served")


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
