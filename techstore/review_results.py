"""Review a batch run: cost, output length, retrieval, and a per-answer read-through.

    python review_results.py results_real.jsonl                # summary + every answer
    python review_results.py results_real.jsonl --flagged      # only answers worth a look
    python review_results.py results_real.jsonl --sheet review.csv   # grading sheet

The sheet has blank `verdict` and `notes` columns. Fill verdict with one of
correct / partial / wrong / hallucinated, and it becomes the first hand-graded
quality data for the project.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import defaultdict

import config

RUPEES = re.compile(r"₹\s?([\d,]+)")
LONG_ANSWER_TOKENS = 400


def load_jsonl(path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def known_amounts() -> set[int]:
    """Every rupee figure the agent could legitimately cite: KB text and order records."""
    amounts: set[int] = set()
    for d in load_jsonl(config.KB_PATH):
        amounts.update(int(m.replace(",", "")) for m in RUPEES.findall(d["text"]))
        if d.get("price"):
            amounts.add(int(d["price"]))
    for o in load_jsonl(config.ORDERS_PATH):
        amounts.add(int(o["total"]))
        amounts.update(int(i["unit_price"]) for i in o["items"])
        amounts.update(int(c["amount"]) for c in o["charges"])
    return amounts


def _norm(text: str) -> str:
    return " ".join(text.replace("\u2019", "'").replace("\u2018", "'").lower().split())


# Match on the opening clause of each fixed refusal, so a trailing sentence or
# small punctuation change in the model's reply still counts.
_UNKNOWN = _norm(config.REFUSAL_UNKNOWN.split(".")[0])      # "i don't have that information"
_OFF_TOPIC = _norm(config.REFUSAL_OFF_TOPIC.split(",")[0])  # "i can only help with techstore orders"


def refusal_kind(answer: str) -> str | None:
    """'unknown', 'off_topic', or None if the reply contains neither refusal."""
    a = _norm(answer or "")
    if _OFF_TOPIC in a:
        return "off_topic"
    if _UNKNOWN in a:
        return "unknown"
    return None


def behavior_problem(expected: str | None, answer: str) -> str | None:
    """None if the reply behaved as expected, else a description of what went wrong."""
    kind = refusal_kind(answer)
    if expected is None:                                   # an ordinary, answerable question
        return ("refused an answerable question (over-refusal: check retrieval and prompt)"
                if kind else None)
    if expected == "decline_off_topic":
        if kind == "off_topic":
            return None
        return ("declined, but with the 'unknown' wording (offered a human for an off-topic question)"
                if kind == "unknown" else "ANSWERED an off-topic question instead of declining")
    if expected == "admit_unknown":
        if kind == "unknown":
            return None
        return ("treated a TechStore question as off-topic" if kind == "off_topic"
                else "did NOT admit it lacks the information: check for invented facts")
    if expected == "answer_from_about":
        return ("refused, but the About TechStore document answers this" if kind else None)
    if expected == "partial":
        return (None if kind == "unknown"
                else "did not flag the unanswerable half of the question")
    return f"unknown expected_behavior {expected!r}"


def pct(xs: list[float], p: float) -> float:
    s = sorted(xs)
    return s[min(len(s) - 1, int(round(p * (len(s) - 1))))]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("--questions", default=str(config.DATA_DIR / "questions_seed.jsonl"))
    ap.add_argument("--flagged", action="store_true", help="print only rows with flags")
    ap.add_argument("--sheet", help="write a CSV grading sheet")
    ap.add_argument("--no-answers", action="store_true", help="summary only")
    args = ap.parse_args()

    rows = load_jsonl(args.results)
    if not rows:
        print("no rows in", args.results)
        return 1
    qs = load_jsonl(args.questions)
    by_id = {q["id"]: q for q in qs}
    by_text = {q["question"]: q for q in qs}
    titles = {d["id"]: d["title"] for d in load_jsonl(config.KB_PATH)}
    amounts = known_amounts()

    estimated = sum(bool(r.get("cost_is_estimate")) for r in rows)
    real = [r for r in rows if not r.get("cost_is_estimate") and not r.get("error")]

    # -------------------------------------------------------------- per-row flags
    graded = []
    for r in rows:
        q = by_id.get(r.get("id")) or by_text.get(r["question"]) or {}
        gold = q.get("context_ids", [])
        missing = [g for g in gold if g not in r.get("retrieved", [])]
        cited = [int(m.replace(",", "")) for m in RUPEES.findall(r.get("answer") or "")]
        unknown = sorted({a for a in cited if a not in amounts})
        flags = []
        if r.get("error"):
            flags.append("ERROR")
        if r.get("finish_reason") == "length":
            flags.append("TRUNCATED at max_tokens")
        if missing:
            flags.append("missing gold doc: " + ", ".join(titles.get(m, m) for m in missing))
        if unknown and not r.get("cost_is_estimate"):
            flags.append("rupee amount not in KB/orders (invented, or computed -- check): "
                         + ", ".join(f"₹{a:,}" for a in unknown))
        if (r.get("completion_tokens") or 0) > LONG_ANSWER_TOKENS and not r.get("cost_is_estimate"):
            flags.append(f"long answer ({r['completion_tokens']} tokens)")
        behavior = None
        if not r.get("cost_is_estimate") and not r.get("error"):
            behavior = behavior_problem(q.get("expected_behavior"), r.get("answer") or "")
            if behavior:
                flags.append("BEHAVIOUR: " + behavior)
        r["_behavior_ok"] = behavior is None
        graded.append((r, q, gold, missing, flags))

    # -------------------------------------------------------------- summary
    print(f"{len(rows)} rows from {args.results}")
    if estimated:
        print(f"WARNING: {estimated} row(s) are MOCK estimates. Their output length is assumed,"
              " so they say nothing about real answers. Calibration uses real rows only.")
    errors = [r for r in rows if r.get("error")]
    if errors:
        print(f"{len(errors)} row(s) errored. First: {errors[0]['error'][:160]}")

    total = sum(r.get("cost_usd", 0) for r in rows)
    print(f"\ncost      total ${total:.4f}   mean ${total/len(rows):.6f}/question"
          + ("   (includes estimates)" if estimated else ""))

    if real:
        out = [r["completion_tokens"] for r in real]
        vis = [r["completion_tokens"] - r.get("reasoning_tokens", 0) for r in real]
        rea = [r.get("reasoning_tokens", 0) for r in real]
        inp = [r["prompt_tokens"] for r in real]
        lat = [r["latency_ms"] for r in real if r.get("latency_ms")]
        print(f"prompt    mean {statistics.mean(inp):6.0f} tokens")
        print(f"output    mean {statistics.mean(out):6.0f}   median {statistics.median(out):5.0f}"
              f"   p90 {pct(out, .9):5.0f}   max {max(out)} tokens (billed)")
        if any(rea):
            print(f"          of which hidden reasoning: mean {statistics.mean(rea):.0f};"
                  f" visible answer mean {statistics.mean(vis):.0f}")
        if lat:
            print(f"latency   median {statistics.median(lat):6.0f} ms   p90 {pct(lat, .9):6.0f} ms")
        truncated = sum(r.get("finish_reason") == "length" for r in real)
        if truncated:
            print(f"          {truncated} answer(s) hit MAX_TOKENS={config.MAX_TOKENS} and were cut off")
        suggested = round(statistics.mean(out))
        print(f"\ncalibration: set MOCK_OUTPUT_TOKENS = {suggested} in config.py"
              f"  (currently {config.MOCK_OUTPUT_TOKENS}; mean, because cost is linear in tokens)")
    else:
        print("\ncalibration: no real rows -- run without --mock first")

    # per-category
    cat = defaultdict(lambda: {"n": 0, "cost": 0.0, "out": [], "gold": 0, "hit": 0})
    for r, q, gold, missing, _ in graded:
        c = cat[r.get("category") or q.get("category", "?")]
        c["n"] += 1
        c["cost"] += r.get("cost_usd", 0)
        if not r.get("cost_is_estimate") and not r.get("error"):
            c["out"].append(r["completion_tokens"])
        c["gold"] += len(gold)
        c["hit"] += len(gold) - len(missing)
    print(f"\n{'category':22s} {'n':>3s} {'mean $':>10s} {'mean out':>9s} {'retrieval':>10s}")
    for name in sorted(cat):
        c = cat[name]
        out_s = f"{statistics.mean(c['out']):9.0f}" if c["out"] else f"{'-':>9s}"
        ret = f"{100*c['hit']/c['gold']:9.0f}%" if c["gold"] else f"{'-':>10s}"
        print(f"{name:22s} {c['n']:3d} {c['cost']/c['n']:10.6f} {out_s} {ret}")

    checked = [(r, q) for r, q, *_ in graded
               if not r.get("cost_is_estimate") and not r.get("error")]
    if checked:
        oos = [(r, q) for r, q in checked if q.get("expected_behavior")]
        normal = [(r, q) for r, q in checked if not q.get("expected_behavior")]
        print(f"\nbehaviour  out-of-scope handled correctly: "
              f"{sum(r['_behavior_ok'] for r, _ in oos)}/{len(oos)}"
              f"    answerable questions refused: "
              f"{sum(not r['_behavior_ok'] for r, _ in normal)}/{len(normal)}")

    n_flagged = sum(bool(f) for *_, f in graded)
    print(f"\n{n_flagged}/{len(rows)} answers flagged for a closer look")

    # -------------------------------------------------------------- read-through
    if not args.no_answers:
        for r, q, gold, missing, flags in graded:
            if args.flagged and not flags:
                continue
            print("\n" + "=" * 78)
            print(f"{r.get('id') or q.get('id', '?')}  [{r.get('category') or q.get('category', '?')}]"
                  f"  ${r.get('cost_usd', 0):.6f}  {r.get('prompt_tokens', 0)}+{r.get('completion_tokens', 0)} tok")
            print("Q:", r["question"])
            marks = [("✓ " if d in gold else "  ") + titles.get(d, d) for d in r.get("retrieved", [])]
            print("retrieved:", " | ".join(marks) or "(none)")
            for f in flags:
                print("  ⚑", f)
            print("-" * 78)
            print(r.get("error") or r.get("answer") or "(empty answer)")

    # -------------------------------------------------------------- grading sheet
    if args.sheet:
        with open(args.sheet, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["id", "category", "expected_behavior", "question", "answer", "retrieved",
                        "missing_gold", "flags", "cost_usd", "completion_tokens", "verdict", "notes"])
            for r, q, gold, missing, flags in graded:
                w.writerow([r.get("id") or q.get("id", ""), r.get("category") or q.get("category", ""),
                            q.get("expected_behavior", ""),
                            r["question"], r.get("error") or r.get("answer", ""),
                            "; ".join(r.get("retrieved", [])), "; ".join(missing),
                            " | ".join(flags), r.get("cost_usd", 0), r.get("completion_tokens", 0),
                            "", ""])
        print(f"\ngrading sheet written to {args.sheet}  (fill 'verdict': correct / partial / wrong / hallucinated)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
