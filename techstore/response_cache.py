"""Technique 7, the safe response cache: reuse a model's earlier answer when the same
question comes again, so the repeat costs zero tokens.

Two tiers, looked up in order:
  exact     the same question (after trimming case, spaces and end punctuation)
  semantic  a question with the same meaning (MiniLM similarity >= threshold), allowed
            only if EVERY safety check passes (Tokenomics.md §3, admission control):
    1. same namespace: same app instructions, knowledge-base version, model and settings
       (built into the key, so a change to any of them can never reuse an old answer)
    2. same entities: identical numbers, amounts, dates, emails and product names
    3. no negation/antonym flip: "enable" vs "disable", "with" vs "without", ...
    4. similar length: neither question more than 3.5x longer than the other
    5. short enough to embed whole (MiniLM reads only the first 256 word-pieces)
Some questions are never cached at all, in either tier:
    personal or time-varying ones (an order number, "my order", "today", "in stock", ...),
    and any answer built from a customer's private records (the caller says so).

Storage is one SQLite file (stdlib). The gateway step can swap in Redis/ChromaDB behind
the same methods.

    python response_cache.py --safety    # run the adversarial pairs; exit 1 on any false hit
    python response_cache.py --stats     # what is stored
    python response_cache.py --clear
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import threading
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

import config

CACHE_PATH = config.BASE_DIR / ".cache" / "responses.sqlite"
PAIRS_PATH = config.DATA_DIR / "cache_pairs.jsonl"
DEFAULT_THRESHOLD = 0.88          # most similar dangerous pair 0.79; least similar paraphrase 0.86
DEFAULT_TTL_HOURS = 24
MAX_LENGTH_RATIO = 3.5
MAX_WORDS = 150                   # well inside MiniLM's 256 word-piece window

_NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
_DATE_WORDS = {"january", "february", "march", "april", "may", "june", "july", "august",
               "september", "october", "november", "december", "jan", "feb", "mar", "apr",
               "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec", "monday", "tuesday",
               "wednesday", "thursday", "friday", "saturday", "sunday"}
# Words that flip the meaning when only one side has them...
NEGATIONS = {"not", "no", "never", "without", "except", "cannot", "can't", "don't", "doesn't",
             "isn't", "won't", "didn't", "aren't", "unopened", "unsealed", "non"}
# ...and pairs where one side has a word and the other side its opposite.
OPPOSITES = [("enable", "disable"), ("on", "off"), ("add", "remove"), ("activate", "deactivate"),
             ("before", "after"), ("increase", "decrease"), ("more", "less"),
             ("include", "exclude"), ("allow", "block"), ("accept", "reject"),
             ("open", "close"), ("refund", "exchange"), ("repair", "replace"), ("buy", "sell"),
             ("maximum", "minimum"), ("max", "min"), ("inside", "outside"),
             ("domestic", "international"), ("credit", "debit"), ("first", "last"),
             ("with", "without"), ("can", "cannot"), ("upgrade", "downgrade"),
             ("import", "export"), ("start", "stop"), ("pause", "resume")]


def _stem(word: str) -> str:
    """Crude: treat refunds/refund, accepted/accept, enabling/enable as one word."""
    for suffix in ("ing", "ed", "es", "s"):
        if len(word) > len(suffix) + 3 and word.endswith(suffix):
            return word[: -len(suffix)]
    return word


def meaning_flip(a: str, b: str) -> set[str]:
    wa, wb = {_stem(w) for w in _words(a)}, {_stem(w) for w in _words(b)}
    flips = (wa ^ wb) & {_stem(n) for n in NEGATIONS}
    only_one_side = wa ^ wb
    for x, y in OPPOSITES:
        x, y = _stem(x), _stem(y)
        # Both words appear across the two questions and at least one appears on one side
        # only: one question says x where the other says y. Symmetric by construction.
        if {x, y} <= (wa | wb) and {x, y} & only_one_side:
            flips.add(f"{x}/{y}")
    return flips


# Personal or time-varying questions: the right answer depends on who asks or when.
_VOLATILE = re.compile(
    r"\b(today|tonight|tomorrow|yesterday|right now|currently|latest|this week|"
    r"in stock|out of stock|stock|"
    r"(where|status) (is|of) my|my (order|orders|refund|payment|parcel|package|account|"
    r"delivery|invoice|emi|card|return|replacement|charge|charges))\b")


def normalise(question: str) -> str:
    q = re.sub(r"\s+", " ", question.strip().lower().replace("’", "'"))
    return q.rstrip("?!. ")


def _words(question: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", normalise(question))


def entities(question: str, extra: set[str] | frozenset = frozenset()) -> frozenset[str]:
    """Everything that makes two similar questions need different answers."""
    q = normalise(question)
    found = {f"num:{n.replace(',', '')}" for n in _NUMBER.findall(q)}
    found |= {f"email:{e}" for e in _EMAIL.findall(q)}
    found |= {f"date:{w}" for w in _words(q) if w in _DATE_WORDS}
    found |= {f"app:{e}" for e in extra}
    return frozenset(found)


def uncacheable(question: str) -> str | None:
    """Why a question must never be cached (None if it may be)."""
    q = normalise(question)
    if _NUMBER.search(q) and re.search(r"\b\d{5,}\b", q):
        return "contains an order or reference number"
    if _VOLATILE.search(q):
        return "personal or time-varying"
    return None


def admission_problem(new_q: str, new_ents: frozenset, old_q: str, old_ents: frozenset) -> str | None:
    """Safety checks 2-5 for a semantic hit (check 1, the namespace, is in the key)."""
    if new_ents != old_ents:
        return "different entities"
    flipped = meaning_flip(new_q, old_q)
    if flipped:
        return f"meaning flip ({', '.join(sorted(flipped))})"
    a, b = len(_words(new_q)) or 1, len(_words(old_q)) or 1
    if max(a, b) / min(a, b) > MAX_LENGTH_RATIO:
        return "very different lengths"
    if max(a, b) > MAX_WORDS:
        return "too long to compare safely"
    return None


@dataclass
class CacheHit:
    answer: str
    kind: str                 # "exact" or "semantic"
    score: float              # similarity (1.0 for exact)
    cached_question: str
    model: str


@dataclass
class Lookup:
    hit: CacheHit | None
    reason: str               # why it hit, missed or was skipped


def _minilm():
    from sentence_transformers import SentenceTransformer  # noqa: PLC0415
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    return lambda texts: model.encode(texts, normalize_embeddings=True)


class ResponseCache:
    def __init__(self, path: Path | str = CACHE_PATH, encode=None,
                 threshold: float = DEFAULT_THRESHOLD, ttl_hours: float = DEFAULT_TTL_HOURS):
        self.path = Path(path)
        if str(path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        # Shared across threads (Streamlit answers each message on a new thread); the lock
        # makes each read-and-update a single step.
        self.db = sqlite3.connect(str(path), check_same_thread=False)
        self._lock = threading.RLock()
        self.db.execute("""CREATE TABLE IF NOT EXISTS entries (
            namespace TEXT, question TEXT, norm TEXT, entities TEXT, answer TEXT, model TEXT,
            vector BLOB, created REAL, expires REAL, hits INTEGER DEFAULT 0,
            PRIMARY KEY (namespace, norm))""")
        self.threshold, self.ttl = threshold, ttl_hours * 3600
        self._encode = encode

    @property
    def encode(self):
        if self._encode is None:
            self._encode = _minilm()
        return self._encode

    def _vec(self, text: str) -> np.ndarray:
        return np.asarray(self.encode([normalise(text)]), dtype=np.float32)[0]

    def lookup(self, question: str, namespace: str, extra_entities=frozenset(),
               private: bool = False) -> Lookup:
        with self._lock:
            if private:
                return Lookup(None, "skipped: private request")
            why = uncacheable(question)
            if why:
                return Lookup(None, f"skipped: {why}")
            now = time.time()
            norm = normalise(question)
            new_ents = entities(question, extra_entities)
            row = self.db.execute(
                "SELECT answer, question, model, entities FROM entries "
                "WHERE namespace=? AND norm=? AND expires>?", (namespace, norm, now)).fetchone()
            # Same words are not enough: entities known from outside the text (e.g. the product
            # being discussed) must match too.
            if row and frozenset(json.loads(row[3])) == new_ents:
                self.db.execute("UPDATE entries SET hits=hits+1 WHERE namespace=? AND norm=?",
                                (namespace, norm))
                self.db.commit()
                return Lookup(CacheHit(row[0], "exact", 1.0, row[1], row[2]), "exact hit")
            rows = self.db.execute(
                "SELECT question, norm, entities, answer, model, vector FROM entries "
                "WHERE namespace=? AND expires>?", (namespace, now)).fetchall()
            if not rows:
                return Lookup(None, "miss: nothing cached here yet")
            vecs = np.stack([np.frombuffer(r[5], dtype=np.float32) for r in rows])
            sims = vecs @ self._vec(question)
            order = np.argsort(-sims)
            best_reason = f"miss: closest {float(sims[order[0]]):.2f} < {self.threshold:.2f}"
            for i in order:
                sim = float(sims[i])
                if sim < self.threshold:
                    break
                q_old, norm_old, ents_old, answer, model, _ = rows[i]
                problem = admission_problem(question, new_ents, q_old, frozenset(json.loads(ents_old)))
                if problem:
                    best_reason = f"rejected: {problem} (similarity {sim:.2f})"
                    continue
                self.db.execute("UPDATE entries SET hits=hits+1 WHERE namespace=? AND norm=?",
                                (namespace, norm_old))
                self.db.commit()
                return Lookup(CacheHit(answer, "semantic", sim, q_old, model), "semantic hit")
            return Lookup(None, best_reason)

    def store(self, question: str, answer: str, namespace: str, model: str,
              extra_entities=frozenset(), private: bool = False) -> str:
        """Save an answer for reuse. Returns what happened."""
        with self._lock:
            if private:
                return "not stored: private request"
            why = uncacheable(question)
            if why:
                return f"not stored: {why}"
            if not answer.strip():
                return "not stored: empty answer"
            now = time.time()
            self.db.execute(
                "INSERT OR REPLACE INTO entries (namespace, question, norm, entities, answer, model, "
                "vector, created, expires, hits) VALUES (?,?,?,?,?,?,?,?,?,0)",
                (namespace, question, normalise(question),
                 json.dumps(sorted(entities(question, extra_entities))), answer, model,
                 self._vec(question).tobytes(), now, now + self.ttl))
            self.db.commit()
            return "stored"

    def stats(self) -> dict:
        with self._lock:
            n, hits = self.db.execute("SELECT COUNT(*), COALESCE(SUM(hits),0) FROM entries").fetchone()
            live = self.db.execute("SELECT COUNT(*) FROM entries WHERE expires>?",
                                   (time.time(),)).fetchone()[0]
            return {"entries": n, "live": live, "hits_served": hits}

    def clear(self) -> None:
        with self._lock:
            self.db.execute("DELETE FROM entries")
            self.db.commit()


def namespace_key(**parts) -> str:
    """Everything that changes the right answer apart from the question itself."""
    return hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest()[:16]


def run_safety(threshold: float) -> int:
    """Each pair: cache side A, ask side B. Pairs marked must_not_hit must miss.
    Returns the number of false hits (the suite fails on any)."""
    from agent import SupportAgent  # noqa: PLC0415

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
    ap.add_argument("--safety", action="store_true", help="run the adversarial pair suite")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--clear", action="store_true")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    args = ap.parse_args()
    if args.safety:
        return 1 if run_safety(args.threshold) else 0
    cache = ResponseCache(encode=lambda texts: np.zeros((len(texts), 384)))
    if args.clear:
        cache.clear()
        print("cache cleared")
    if args.stats:
        print(cache.stats())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
