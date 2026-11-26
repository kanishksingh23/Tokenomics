"""FAQ shortcut matcher: answer common questions from human-approved answers with no
model call at all (zero tokens, zero cost, instant).

Entries (one JSON object per line): id, question, examples (other phrasings, used only for
matching), answer, sources, status. **Only entries with status "approved" are ever
served**: a saved answer reaches the customer without any model checking it.

A question gets a saved answer only if ALL of these hold:
  1. its meaning is close to one FAQ (MiniLM similarity >= threshold)
  2. it is clearly closer to that FAQ than to any other (no near-tie), counting entries not
     yet approved too: a question that best matches an unapproved answer gets no saved
     answer, rather than the nearest approved one (which may be about something else)
  3. it contains no digits: order numbers and amounts need a personal answer
  4. it is a single question
  5. the caller does not block it (e.g. TechStore blocks questions naming a product)
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass

import numpy as np

DEFAULT_THRESHOLD = 0.75
DEFAULT_MARGIN = 0.05


def load_faq(path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


@dataclass
class FaqMatch:
    entry: dict | None         # the FAQ served, or None
    best_id: str | None        # closest FAQ even when not served (for analysis)
    score: float
    reason: str                # why it was or wasn't served


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
        # Unapproved entries are still matched against, never served: they stop a question
        # about their topic from receiving a neighbouring approved answer.
        self._candidates = self.entries + [e for e in entries if e not in self.entries]
        self.threshold, self.margin, self.block = threshold, margin, block
        # The embedding model loads only if there is something to serve.
        self.encode = encode or (_minilm() if self.entries else None)
        # Every phrasing of every entry is a matching target; a question scores against
        # the closest phrasing of each entry.
        self._owner, texts = [], []
        for i, e in enumerate(self._candidates if self.entries else []):
            for t in [e["question"], *e.get("examples", [])]:
                self._owner.append(i)
                texts.append(t)
        self._vecs = np.asarray(self.encode(texts)) if texts else np.zeros((0, 1))

    def scores(self, question: str) -> list[tuple[float, int]]:
        """(best similarity, candidate index) per entry, best first; unapproved included."""
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
        best_id = self._candidates[idx]["id"]

        def miss(reason):
            return FaqMatch(None, best_id, score, reason)

        if score < self.threshold:
            return miss(f"not close enough ({score:.2f} < {self.threshold:.2f})")
        if idx >= len(self.entries):
            return miss(f"closest FAQ ({best_id}) is not approved yet")
        if len(ranked) > 1 and score - ranked[1][0] < self.margin:
            return miss(f"near-tie with {self._candidates[ranked[1][1]]['id']}")
        if re.search(r"\d", question):
            return miss("contains a number (order id or amount needs a personal answer)")
        if question.count("?") > 1:
            return miss("more than one question")
        if self.block:
            reason = self.block(question)
            if reason:
                return miss(reason)
        return FaqMatch(self._candidates[idx], best_id, score, "served")
