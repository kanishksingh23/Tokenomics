"""Data integrity checks. Run after every corpus edit; wire into CI in Week 1.

    python validate_data.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter

import config

TARGET_QUESTIONS = 500
CATEGORIES = {
    "simple_faq": 60, "order_status": 60, "product_info": 40,
    "product_comparison": 50, "troubleshooting": 50, "billing_dispute": 70,
    "technical_api": 70, "policy_edge_case": 60,
    # Questions the documents cannot or should not answer. Tests that the model
    # refuses correctly instead of inventing. Taken from the two largest easy
    # categories so the total and the economy/frontier split are unchanged.
    "out_of_scope": 40,
}
# What a correct reply does, for out_of_scope questions (see review_results.py).
BEHAVIORS = {"decline_off_topic", "admit_unknown", "answer_from_about", "partial"}


def rows(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def main() -> int:
    errors, warnings = [], []

    kb = rows(config.KB_PATH)
    kb_ids = {d["id"] for d in kb}
    if len(kb_ids) != len(kb):
        errors.append("duplicate knowledge-base ids")
    for d in kb:
        if len(d["text"].split()) < 25:
            warnings.append(f"thin document: {d['id']}")

    orders = rows(config.ORDERS_PATH)
    order_ids = {o["order_id"] for o in orders}
    for o in orders:
        got = sum(i["qty"] * i["unit_price"] for i in o["items"])
        if got != o["total"]:
            errors.append(f"order {o['order_id']}: total {o['total']} != items {got}")

    qpath = config.DATA_DIR / "questions_seed.jsonl"
    full = config.DATA_DIR / "customer_support_500.jsonl"
    if full.exists():
        qpath = full
    qs = rows(qpath)
    qids = {q["id"] for q in qs}
    if len(qids) != len(qs):
        errors.append("duplicate question ids")
    for q in qs:
        for c in q.get("context_ids", []):
            if c not in kb_ids:
                errors.append(f"{q['id']}: unknown context_id {c}")
        for o in q.get("order_ids", []):
            if o not in order_ids:
                errors.append(f"{q['id']}: unknown order_id {o}")
        b = q.get("expected_behavior")
        if q["category"] == "out_of_scope" and b not in BEHAVIORS:
            errors.append(f"{q['id']}: out_of_scope needs expected_behavior in {sorted(BEHAVIORS)}")
        if b is not None and b not in BEHAVIORS:
            errors.append(f"{q['id']}: unknown expected_behavior {b!r}")

    counts = Counter(q["category"] for q in qs)
    unknown = set(counts) - set(CATEGORIES)
    if unknown:
        errors.append(f"unknown categories: {sorted(unknown)}")

    print(f"knowledge base : {len(kb)} documents")
    print(f"orders         : {len(orders)}")
    print(f"questions      : {len(qs)} / {TARGET_QUESTIONS}  ({qpath.name})")
    print()
    print(f"{'category':22s} {'have':>5s} {'target':>7s}  progress")
    for cat, target in CATEGORIES.items():
        have = counts.get(cat, 0)
        bar = "#" * int(20 * min(have / target, 1.0))
        print(f"{cat:22s} {have:5d} {target:7d}  {bar:<20s} {100*have/target:5.1f}%")
    print(f"\n{'TOTAL':22s} {len(qs):5d} {TARGET_QUESTIONS:7d}"
          f"{'':>23s}{100*len(qs)/TARGET_QUESTIONS:5.1f}%")

    if warnings:
        print("\nwarnings:")
        for w in warnings:
            print("  ! " + w)
    if errors:
        print("\nERRORS:")
        for e in errors:
            print("  x " + e)
        return 1
    print("\nall integrity checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
