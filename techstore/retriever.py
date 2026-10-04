"""Retrieval over the TechStore knowledge base.

Two backends. `embedding` (MiniLM) is better; `keyword` (BM25-lite, pure stdlib)
needs no dependencies so the agent is testable before anything is installed.
`auto` uses embeddings when sentence-transformers is importable, else keyword.

Why retrieval at all: sending all 85 documents in every prompt costs ~7,700
prompt tokens per request instead of ~500 -- 7x the cost, measured with the real
tokenizer, and growing with every document added. Retrieval is what makes the
section 2 cost assumption true.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

_WORD = re.compile(r"[a-z0-9]+")


# Light suffix stripping. Without it "coupons" does not match "coupon" and
# "paginate" does not match "pagination", which costs real recall. Deliberately
# crude: a full stemmer is not worth the dependency for a corpus this size.
_SUFFIXES = ("ions", "ion", "ing", "ers", "er", "ed", "es", "s", "e")


def _stem(w: str) -> str:
    if len(w) <= 4:
        return w
    for suf in _SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


# Without this, a short document can rank on "or", "for" and "a" alone. That is
# how "Monitor Flickering" surfaced for "X200 or Y500 for a noisy office?".
# Interrogatives are deliberately NOT stopwords here: "where is my order" and
# "how do I return this" differ almost entirely in their question word, and the
# knowledge base is tagged with those phrasings.
_STOP = frozenset("""
a about an and are as at be been but by can could do does did for from had has have he
her him his i if in into is it its me my no nor not of on or our out she so that
the their them then there these they this to too under up was we were while will
with would you your
""".split())


def _tokens(text: str, drop_stopwords: bool = True) -> list[str]:
    words = _WORD.findall(text.lower())
    if drop_stopwords:
        kept = [w for w in words if w not in _STOP]
        # Short queries can be entirely stopwords ("where is my order?" -> "order").
        # Stripping them destroys the only signal there is, so keep everything.
        if len(kept) >= 2:
            words = kept
    return [_stem(w) for w in words]


@dataclass
class Doc:
    id: str
    category: str
    title: str
    text: str
    tags: list[str]
    price: int | None = None          # products only
    meta: dict = field(default_factory=dict)   # forward-compatible spillover

    @property
    def searchable(self) -> str:
        return f"{self.title} {self.text} {' '.join(self.tags)}"


_DOC_FIELDS = {"id", "category", "title", "text", "tags", "price"}


def load_docs(path: Path) -> list[Doc]:
    """Unknown keys go to `meta` rather than raising, so the corpus schema can
    grow without breaking every consumer."""
    docs = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            missing = {"id", "category", "title", "text", "tags"} - set(raw)
            if missing:
                raise ValueError(f"{path.name}:{n} missing required field(s): {sorted(missing)}")
            known = {k: v for k, v in raw.items() if k in _DOC_FIELDS}
            extra = {k: v for k, v in raw.items() if k not in _DOC_FIELDS}
            docs.append(Doc(**known, meta=extra))
    return docs


class KeywordRetriever:
    """BM25-lite. No dependencies, adequate for a corpus this size."""

    name = "keyword"
    K1, B = 1.5, 0.75

    def __init__(self, docs: list[Doc]):
        self.docs = docs
        self.tokenised = [_tokens(d.searchable) for d in docs]
        self.lengths = [len(t) for t in self.tokenised]
        self.avg_len = sum(self.lengths) / max(len(self.lengths), 1)
        self.tf = [Counter(t) for t in self.tokenised]
        df = Counter()
        for t in self.tokenised:
            df.update(set(t))
        n = len(docs)
        self.idf = {
            w: math.log(1 + (n - c + 0.5) / (c + 0.5)) for w, c in df.items()
        }

    def search(self, query: str, k: int) -> list[tuple[Doc, float]]:
        q = _tokens(query)
        scored = []
        for i, doc in enumerate(self.docs):
            score, dl = 0.0, self.lengths[i]
            for w in q:
                f = self.tf[i].get(w, 0)
                if not f:
                    continue
                denom = f + self.K1 * (1 - self.B + self.B * dl / self.avg_len)
                score += self.idf.get(w, 0.0) * f * (self.K1 + 1) / denom
            if score > 0:
                scored.append((doc, score))
        scored.sort(key=lambda x: -x[1])
        return scored[:k]


class EmbeddingRetriever:
    """MiniLM cosine similarity. Same model the router uses in Layer 1B/2,
    so this validates the embedding pipeline early.

    Pinned to CPU. On Apple Silicon the library defaults to the MPS GPU, which
    recompiles for every new input length: measured p95 144 ms on unseen
    queries versus 9.8 ms on CPU. For a model this small the GPU is a loss.
    """

    name = "embedding"

    def __init__(self, docs: list[Doc], device: str = "cpu"):
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415

        self.docs = docs
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2",
                                         device=device)
        self.matrix = self.model.encode(
            [d.searchable for d in docs], normalize_embeddings=True
        )
        self.model.encode(["warm up"], normalize_embeddings=True)  # first call is ~400 ms

    def search(self, query: str, k: int) -> list[tuple[Doc, float]]:
        vec = self.model.encode([query], normalize_embeddings=True)[0]
        sims = self.matrix @ vec
        order = sims.argsort()[::-1][:k]
        return [(self.docs[i], float(sims[i])) for i in order]


def searchable(docs: list[Doc]) -> list[Doc]:
    """Documents the search may return. `inject_only` documents (the catalogue)
    are added by rule, never by search, so they cannot crowd out others."""
    return [d for d in docs if not d.meta.get("inject_only")]


def build_retriever(docs: list[Doc], mode: str = "auto"):
    docs = searchable(docs)
    if mode == "keyword":
        return KeywordRetriever(docs)
    if mode == "embedding":
        return EmbeddingRetriever(docs)
    try:
        return EmbeddingRetriever(docs)
    except Exception:
        return KeywordRetriever(docs)
