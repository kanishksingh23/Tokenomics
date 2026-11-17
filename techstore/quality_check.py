"""Automatic quality check: did an experiment change answers compared with a graded baseline?

Step 1, compare (free, no API):
    python quality_check.py runs/2026-10-15_baseline/luna_baseline.jsonl \\
        runs/2026-10-15_shortprompt/luna_short.jsonl \\
        --grades runs/2026-10-15_baseline/luna_grades_claude_draft.csv
  writes, next to the experiment file:
    luna_short.check.csv   one row per question: same / changed, why, inherited grade
    luna_short.judge.md    the changed answers only, with the documents each was given

Step 2, grade the changed answers (an AI grader or a person) into luna_short.judge.csv
with columns  id,verdict,confident,notes  then fold them in:
    python quality_check.py <baseline> <experiment> --grades <csv> --merge luna_short.judge.csv

An answer keeps its baseline grade only if ALL of these hold:
  1. the same kind of reply (an answer stays an answer; each refusal type stays that type)
  2. exactly the same numbers (prices, days, order numbers, step numbers)
  3. very close meaning: MiniLM cosine similarity >= --threshold (default 0.90)
Anything else counts as changed. Being strict costs a little grading; being loose could
hide a wrong answer.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

import config
from review_results import load_jsonl, refusal_kind

VERDICTS = ("correct", "partial", "wrong", "hallucinated")
NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")


def numbers(text: str) -> set[str]:
    """Every number in an answer, normalised: '₹1,34,999.00' and '134999' match."""
    out = set()
    for m in NUMBER.findall(text or ""):
        n = m.replace(",", "").rstrip(".")
        if "." in n:
            n = n.rstrip("0").rstrip(".")
        out.add(n)
    return out


def reply_kind(answer: str) -> str:
    return refusal_kind(answer) or "answer"


_REFUSAL_LINES = (config.REFUSAL_OFF_TOPIC, config.REFUSAL_UNKNOWN)


def refusal_opening_cap(answer: str, expected_behavior: str | None, verdict: str) -> str:
    """Rubric rule 4 (decided 2026-11-17): if an answerable question gets a reply that OPENS
    with a refusal line and then answers anyway, the verdict is at best `partial`. The facts
    may be right, but the customer first reads "I can't help with that"."""
    if verdict != "correct" or expected_behavior in ("decline_off_topic", "admit_unknown"):
        return verdict
    if refusal_kind(answer) not in ("off_topic", "unknown"):
        return verdict
    rest = answer
    for line in _REFUSAL_LINES:
        rest = rest.replace(line, "")
    return "partial" if len(rest.split()) > 3 else verdict


def _embedder():
    try:
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415
    except ImportError:
        return None
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")

    def similarity(a: str, b: str) -> float:
        va, vb = model.encode([a or "", b or ""], normalize_embeddings=True)
        return float(va @ vb)
    return similarity


def compare(base: dict, cand: dict, similarity, threshold: float) -> tuple[bool, float | None, list[str]]:
    """(same?, similarity, reasons it changed)."""
    if cand.get("error"):
        return False, None, [f"error: {cand['error'][:80]}"]
    a, b = base.get("answer", ""), cand.get("answer", "")
    reasons = []
    ka, kb = reply_kind(a), reply_kind(b)
    if ka != kb:
        reasons.append(f"reply kind {ka} -> {kb}")
    na, nb = numbers(a), numbers(b)
    if na != nb:
        diff = sorted(na ^ nb, key=len)[:6]
        reasons.append(f"numbers differ: {', '.join(diff)}")
    sim = None
    if similarity is None:
        reasons.append("no embedding model to compare meaning")
    else:
        sim = similarity(a, b)
        if sim < threshold:
            reasons.append(f"meaning similarity {sim:.2f} < {threshold:.2f}")
    return not reasons, sim, reasons


def load_grades(path: str | None) -> dict[str, str]:
    if not path:
        return {}
    with open(path, encoding="utf-8") as fh:
        # A merged check file (*.check.csv) can serve as the grades for the next comparison.
        return {r["id"]: (r.get("verdict") or r.get("final_verdict") or "").strip().lower()
                for r in csv.DictReader(fh)}


def _evidence(docs: dict, orders: dict, row: dict) -> str:
    parts = []
    for doc_id in row.get("retrieved", []):
        d = docs.get(doc_id)
        if d:
            parts.append(f"--- [{doc_id}] {d['title']}\n{d['text']}")
    for oid in row.get("orders_used", []):
        if oid in orders:
            parts.append(f"--- ORDER {oid}\n{json.dumps(orders[oid], ensure_ascii=False)}")
    return "\n".join(parts) or "(no documents were given)"


def judge_pack(rows: list[dict], questions: dict) -> str:
    """Markdown evidence pack for the changed answers: question, answer, and exactly the
    documents and order records that answer was given."""
    docs = {d["id"]: d for d in load_jsonl(config.KB_PATH)}
    orders = {o["order_id"]: o for o in load_jsonl(config.ORDERS_PATH)}
    out = ["# Answers to grade", "",
           "Grade each answer ONLY against the evidence shown with it. Store date: 30 September 2026.",
           "Verdicts: correct / partial / wrong / hallucinated (rubric: Tokenomics.md §7, Grading Rubric).",
           ""]
    for r in rows:
        q = questions.get(r["id"], {})
        out.append(f"\n========== {r['id']} [{r.get('category', q.get('category', '?'))}] ==========")
        out.append(f"QUESTION: {r['question']}")
        if q.get("expected_behavior"):
            out.append(f"EXPECTED BEHAVIOUR (out of scope): {q['expected_behavior']}")
        missing = [g for g in q.get("context_ids", []) if g not in r.get("retrieved", [])]
        out.append(f"NEEDED DOCS: {q.get('context_ids', [])}   MISSING FROM WHAT THE MODEL SAW: {missing}")
        out.append(f"\nANSWER:\n{r.get('answer', '')}\n")
        out.append("EVIDENCE THE MODEL WAS GIVEN:")
        out.append(_evidence(docs, orders, r))
    return "\n".join(out) + "\n"


def cost_per_correct(rows: list[dict], verdicts: dict[str, str]) -> float | None:
    """Total cost / number of answers graded correct. None if anything is ungraded."""
    if any(verdicts.get(r["id"]) not in VERDICTS for r in rows):
        return None
    n = sum(1 for r in rows if verdicts[r["id"]] == "correct")
    return sum(r.get("cost_usd", 0) for r in rows) / n if n else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("baseline")
    ap.add_argument("experiment")
    ap.add_argument("--grades", help="CSV with id,verdict for the baseline answers")
    ap.add_argument("--questions", default=str(config.DEV_QUESTIONS_PATH))
    ap.add_argument("--threshold", type=float, default=0.90)
    ap.add_argument("--merge", help="grader CSV (id,verdict,confident,notes) for the changed answers")
    args = ap.parse_args()

    base = {r["id"]: r for r in load_jsonl(args.baseline)}
    cand = load_jsonl(args.experiment)
    questions = {q["id"]: q for q in load_jsonl(args.questions)}
    expected = {i: q.get("expected_behavior") for i, q in questions.items()}
    grades = {i: refusal_opening_cap(base[i]["answer"], expected.get(i), v) if i in base else v
              for i, v in load_grades(args.grades).items()}
    stem = Path(args.experiment).with_suffix("")
    similarity = _embedder()

    rows, changed = [], []
    for r in cand:
        b = base.get(r["id"])
        if b is None:
            same, sim, reasons = False, None, ["not in baseline"]
        else:
            same, sim, reasons = compare(b, r, similarity, args.threshold)
        inherited = grades.get(r["id"], "") if same else ""
        rows.append({"id": r["id"], "category": r.get("category", ""),
                     "status": "same" if same else "changed",
                     "similarity": "" if sim is None else f"{sim:.3f}",
                     "reasons": "; ".join(reasons),
                     "baseline_verdict": grades.get(r["id"], ""), "inherited_verdict": inherited})
        if not same:
            changed.append(r)

    judged = {}
    if args.merge:
        with open(args.merge, encoding="utf-8") as fh:
            judged = {j["id"]: j for j in csv.DictReader(fh)}
    final = {}
    for row in rows:
        j = judged.get(row["id"], {})
        row["judge_verdict"] = (j.get("verdict") or "").strip().lower()
        row["judge_confident"] = (j.get("confident") or "").strip().lower()
        row["judge_notes"] = j.get("notes", "")
        answer = next(r["answer"] for r in cand if r["id"] == row["id"])
        row["final_verdict"] = refusal_opening_cap(
            answer, expected.get(row["id"]), row["inherited_verdict"] or row["judge_verdict"])
        worse = (row["baseline_verdict"] in VERDICTS and row["final_verdict"] in VERDICTS
                 and VERDICTS.index(row["final_verdict"]) > VERDICTS.index(row["baseline_verdict"]))
        row["needs_human"] = "yes" if (row["status"] == "changed" and
                                       (row["judge_confident"] != "yes" or worse)) else ""
        final[row["id"]] = row["final_verdict"]

    with open(f"{stem}.check.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    Path(f"{stem}.judge.md").write_text(judge_pack(changed, questions), encoding="utf-8")

    n_same = sum(1 for r in rows if r["status"] == "same")
    print(f"{Path(args.experiment).name} vs {Path(args.baseline).name}  (threshold {args.threshold})")
    print(f"  same as baseline : {n_same}/{len(rows)}"
          f"  ({sum(1 for r in rows if r['inherited_verdict'])} inherit a graded verdict)")
    print(f"  changed          : {len(changed)}  -> {stem.name}.judge.md")
    why = Counter("meaning drifted" if reason.startswith("meaning") else reason.split(":")[0]
                  for r in rows for reason in (r["reasons"].split("; ") if r["reasons"] else []))
    if why:
        print("  why changed      : " + ", ".join(f"{k} ({v})" for k, v in why.most_common()))
    if args.merge:
        print(f"  final verdicts   : {dict(Counter(v or 'ungraded' for v in final.values()))}")
        base_counts = Counter(grades.get(i, "") or "ungraded" for i in final)
        print(f"  baseline verdicts: {dict(base_counts)}")
        for label, rws, v in (("baseline", list(base.values()), grades), ("experiment", cand, final)):
            cpc = cost_per_correct(rws, v)
            print(f"  cost per correct ({label}): " + (f"${cpc:.6f}" if cpc else "n/a (ungraded answers)"))
        need = [r["id"] for r in rows if r["needs_human"]]
        print(f"  needs a human    : {len(need)} {need}")
    print(f"  details          : {stem.name}.check.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
