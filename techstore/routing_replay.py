"""Technique 14: evaluate routing for free by replaying real, already-graded answers.

Every dev question was already answered by BOTH models in real runs, and every answer is
graded. So any routing policy can be scored without a single new call: if it sends a question
to Luna, take Luna's real answer, cost and grade; if it escalates, add Sol's real cost and use
Sol's grade. The five arms of the plan (Tokenomics.md section 7):

    always-frontier   every question to Sol
    always-economy    every question to Luna
    router            cheap-first + checks (tokenomics/routing.py)
    careful variant   the router with "I don't have information about" as a strong signal
    random            same number of escalations as the router, chosen at random (the null model:
                      the router must beat it, or its checks are no better than luck)
    oracle            knows the grades in advance: Luna when Luna is correct, else Sol (the ceiling)

Latency: an escalated question waits for Luna, then Sol (both real latencies, added).

    python routing_replay.py                 # all run pairs, summary table
    python routing_replay.py --detail combo  # per-question decisions for one pair
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import statistics as st
from pathlib import Path

from agent import make_router

RUNS = Path(__file__).parent / "runs"
# (name, luna run, sol run): same settings within each pair.
PAIRS = [
    ("combo",    "2026-11-25_credit_checks/luna_combo",    "2026-11-25_credit_checks/sol_combo"),
    ("rerun",    "2026-11-25_credit_checks/luna_rerun",    "2026-11-25_credit_checks/sol_rerun"),
    ("verblow",  "2026-11-25_credit_checks/luna_verblow",  "2026-11-25_credit_checks/sol_verblow"),
    ("adaptive", "2026-11-25_credit_checks/luna_adaptive", "2026-11-25_credit_checks/sol_adaptive"),
    ("concise",  "2026-11-25_credit_checks/luna_concise",  "2026-11-25_credit_checks/sol_concise"),
    ("oct",      "2026-10-15_shortprompt/luna_short",      "2026-10-15_shortprompt/sol_short"),
]
SCORE = {"correct": 1.0, "partial": 0.5}


def load(run: str) -> dict:
    answers = {}
    for line in open(RUNS / f"{run}.jsonl", encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            answers[r["id"]] = r
    for g in csv.DictReader(open(RUNS / f"{run}.check.csv", encoding="utf-8")):
        answers[g["id"]]["verdict"] = g["final_verdict"] or g["baseline_verdict"]
    return answers


def arm(name, ids, luna, sol, escalated: set, direct: set = frozenset()):
    cost = lat = 0.0
    verdicts, lats = [], []
    for q in ids:
        if q in direct:                                   # routed straight to Sol
            c, v, t = sol[q]["cost_usd"], sol[q]["verdict"], sol[q]["latency_ms"]
        elif q in escalated:                              # Luna first, then Sol
            c = luna[q]["cost_usd"] + sol[q]["cost_usd"]
            v, t = sol[q]["verdict"], luna[q]["latency_ms"] + sol[q]["latency_ms"]
        else:
            c, v, t = luna[q]["cost_usd"], luna[q]["verdict"], luna[q]["latency_ms"]
        cost += c
        lat += t
        verdicts.append(v)
        lats.append(t)
    correct = verdicts.count("correct")
    lats.sort()
    return {"arm": name, "cost": cost, "correct": correct, "partial": verdicts.count("partial"),
            "wrong": len(verdicts) - correct - verdicts.count("partial"),
            "score": sum(SCORE.get(v, 0) for v in verdicts) / len(verdicts),
            "per_correct": cost / correct if correct else float("inf"),
            "p50": st.median(lats), "p90": lats[int(0.9 * (len(lats) - 1))],
            "to_sol": len(escalated) + len(direct)}


def evaluate(luna_run: str, sol_run: str, seeds: int = 200, **router_overrides):
    luna, sol = load(luna_run), load(sol_run)
    ids = [q for q in luna if q in sol]
    router = make_router(**router_overrides)
    direct, escalated, checks = set(), set(), {}
    for q in ids:
        d = router.choose(luna[q]["question"])
        if d.tier == "frontier":
            direct.add(q)
            continue
        c = router.check(luna[q]["question"], luna[q]["answer"], luna[q].get("finish_reason"))
        checks[q] = c
        if c.escalate:
            escalated.add(q)
    arms = [arm("always Sol", ids, luna, sol, set(), set(ids)),
            arm("always Luna", ids, luna, sol, set()),
            arm("router", ids, luna, sol, escalated, direct)]
    # Random null model: the same number of escalations, chosen at random; averaged.
    rnd = random.Random(0)
    k = len(escalated) + len(direct)
    runs = [arm("random", ids, luna, sol, set(rnd.sample(ids, k))) for _ in range(seeds)]
    avg = {key: (st.mean(r[key] for r in runs) if isinstance(runs[0][key], (int, float)) else runs[0][key])
           for key in runs[0]}
    avg["arm"] = "random (same # to Sol)"
    arms.append(avg)
    oracle = {q for q in ids if luna[q]["verdict"] != "correct"}
    arms.append(arm("oracle", ids, luna, sol, set(), oracle))
    return arms, luna, sol, checks, escalated, direct


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--detail", help="pair name: print every question's routing decision")
    args = ap.parse_args()
    if args.detail:
        _, luna_run, sol_run = next(p for p in PAIRS if p[0] == args.detail)
        arms, luna, sol, checks, esc, direct = evaluate(luna_run, sol_run)
        for q, c in checks.items():
            if c.signals or q in esc:
                print(f"{q} {'ESCALATE' if c.escalate else 'keep    '} U={c.uncertainty:.2f} "
                      f"luna={luna[q]['verdict']:8} sol={sol[q]['verdict']:8} {c.signals} "
                      f"{c.suppressed_by or ''}\n     {luna[q]['answer'][:150]!r}")
        for q in direct:
            print(f"{q} DIRECT to Sol")
        return 0
    print(f"{'pair':9} {'arm':24} {'cost $':>8} {'vs Sol':>7} {'correct':>7} {'partial':>7} {'wrong':>5} "
          f"{'$/correct':>10} {'to Sol':>6} {'p50 s':>6} {'p90 s':>6}")
    for name, luna_run, sol_run in PAIRS:
        arms = evaluate(luna_run, sol_run)[0]
        careful = evaluate(luna_run, sol_run, missing_info_weight=0.6)[0][2]
        careful["arm"] = "router, careful variant"
        arms.insert(3, careful)
        base = arms[0]["cost"]
        for a in arms:
            print(f"{name:9} {a['arm']:24} {a['cost']:8.4f} {a['cost'] / base - 1:+7.0%} {a['correct']:7.1f} "
                  f"{a['partial']:7.1f} {a['wrong']:5.1f} {a['per_correct']:10.6f} {a['to_sol']:6.1f} "
                  f"{a['p50'] / 1000:6.2f} {a['p90'] / 1000:6.2f}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
