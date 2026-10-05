"""Data integrity checks. Run after every corpus edit; wire into CI in Week 1.

    python validate_data.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter

import config

# 300 questions in two sets that never mix (see config.py). The test set is
# sized for the claims the project makes: about 200 paired questions prove the
# spec's 0.25-point quality margin even if the router is slightly worse, and
# "at most 7 points fewer correct answers". Per-category results are descriptive.
DEV_TARGETS = {
    "simple_faq": 12, "order_status": 12, "product_info": 8, "product_comparison": 10,
    "troubleshooting": 10, "billing_dispute": 12, "technical_api": 12,
    "policy_edge_case": 12,
    # Questions the documents cannot or should not answer: tests that the model
    # refuses correctly instead of inventing.
    "out_of_scope": 12,
}
TEST_TARGETS = {
    "simple_faq": 24, "order_status": 24, "product_info": 16, "product_comparison": 20,
    "troubleshooting": 20, "billing_dispute": 28, "technical_api": 28,
    "policy_edge_case": 24, "out_of_scope": 16,
}
CATEGORIES = DEV_TARGETS
# What a correct reply does, for out_of_scope questions (see review_results.py).
BEHAVIORS = {"decline_off_topic", "admit_unknown", "answer_from_about", "partial"}


def rows(path):
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def freeze() -> int:
    """Record the test set's fingerprint. After this, any edit to it fails validation."""
    import hashlib
    if not config.TEST_QUESTIONS_PATH.exists():
        print("no test set to freeze")
        return 1
    if main() != 0:
        print("\nfix the errors above before freezing")
        return 1
    digest = hashlib.sha256(config.TEST_QUESTIONS_PATH.read_bytes()).hexdigest()
    config.TEST_LOCK_PATH.write_text(digest + "  questions_test.jsonl\n")
    print(f"\nfrozen: {config.TEST_LOCK_PATH.name} written. Commit both files.")
    return 0


def main() -> int:
    errors, warnings = [], []

    kb = rows(config.KB_PATH)
    kb_ids = {d["id"] for d in kb}
    if len(kb_ids) != len(kb):
        errors.append("duplicate knowledge-base ids")
    for d in kb:
        if len(d["text"].split()) < 25:
            warnings.append(f"thin document: {d['id']}")

    # The catalogue repeats facts from the product pages, so it must never drift
    # from them: the agent quotes it to customers. Each line's name and price must
    # match its product page, and every number in its specs must appear there.
    import re
    cat = next((d for d in kb if d["id"] == "catalogue_summary"), None)
    products = {d["id"]: d for d in kb if d["category"] == "product"}
    if cat is None:
        errors.append("catalogue_summary is missing")
    else:
        lines = [line for line in cat["text"].split("\n")[1:] if line.strip()]
        if sorted(cat.get("sources", [])) != sorted(products) or len(lines) != len(products):
            errors.append("catalogue must list every product exactly once")
        for pid, line in zip(cat.get("sources", []), lines, strict=False):
            p = products.get(pid)
            name, _, price, specs = [x.strip() for x in line.split("|")]
            if not p or name != p["title"]:
                errors.append(f"catalogue line for {pid}: name {name!r} != product title")
                continue
            if int(price.replace("₹", "").replace(",", "")) != p["price"]:
                errors.append(f"catalogue line for {pid}: price {price} != {p['price']}")
            page = p["text"].replace(",", "")
            for num in re.findall(r"\d+(?:\.\d+)?", specs.replace(",", "")):
                if not re.search(r"(?<![\d.])" + re.escape(num) + r"(?![\d])", page):
                    errors.append(f"catalogue line for {pid}: '{num}' not found on the product page")

    orders = rows(config.ORDERS_PATH)
    order_ids = {o["order_id"] for o in orders}
    today = config.SIMULATED_TODAY
    for o in orders:
        happened = [o.get(k) for k in ("placed_at", "delivered_at", "cancelled_at")]
        due = [o.get("eta")]
        for c in o["charges"]:
            happened += [c["date"], c.get("refunded_at"), c.get("reversed_at")]
            if c.get("status") == "reversed" and not c.get("reversed_at"):
                errors.append(f"order {o['order_id']}: reversed charge has no reversed_at date")
            due.append(c.get("refund_eta"))
            if "reverses by " in c.get("note", ""):
                due.append(c["note"].split("reverses by ")[1])
        for dt in filter(None, happened):
            if dt > today:
                errors.append(f"order {o['order_id']}: event dated {dt}, after SIMULATED_TODAY {today}")
        for dt in filter(None, due):
            if dt < today:
                errors.append(f"order {o['order_id']}: due date {dt} already past on {today}")
    for o in orders:
        got = sum(i["qty"] * i["unit_price"] for i in o["items"])
        if got != o["total"]:
            errors.append(f"order {o['order_id']}: total {o['total']} != items {got}")

    def check_questions(qs, label, id_prefix):
        ids = [q["id"] for q in qs]
        if len(set(ids)) != len(ids):
            errors.append(f"{label}: duplicate question ids")
        for q in qs:
            if not q["id"].startswith(id_prefix):
                errors.append(f"{label} {q['id']}: ids in this set start with '{id_prefix}'")
            if q.get("category") not in DEV_TARGETS:
                errors.append(f"{label} {q['id']}: unknown category {q.get('category')!r}")
            for c in q.get("context_ids", []):
                if c not in kb_ids:
                    errors.append(f"{label} {q['id']}: unknown context_id {c}")
            for o in q.get("order_ids", []):
                if o not in order_ids:
                    errors.append(f"{label} {q['id']}: unknown order_id {o}")
            b = q.get("expected_behavior")
            if q.get("category") == "out_of_scope" and b not in BEHAVIORS:
                errors.append(f"{label} {q['id']}: out_of_scope needs expected_behavior "
                              f"in {sorted(BEHAVIORS)}")
            if b is not None and b not in BEHAVIORS:
                errors.append(f"{label} {q['id']}: unknown expected_behavior {b!r}")

    dev = rows(config.DEV_QUESTIONS_PATH)
    check_questions(dev, "dev", "q")
    test = rows(config.TEST_QUESTIONS_PATH) if config.TEST_QUESTIONS_PATH.exists() else []
    check_questions(test, "test", "t")
    # Test questions also carry what a correct answer must contain, and who wrote them
    # (see WRITING_TEST_QUESTIONS.md). Graders and the AI judge check against key_points.
    for q in test:
        kp = q.get("key_points")
        if not (isinstance(kp, list) and kp and all(isinstance(k, str) and k.strip() for k in kp)):
            errors.append(f"test {q['id']}: key_points must be a list of 1-3 non-empty strings")
        elif len(kp) > 3:
            warnings.append(f"test {q['id']}: {len(kp)} key points; keep to the 1-3 that matter")
        if q.get("source") not in ("human", "ai_assisted"):
            errors.append(f"test {q['id']}: source must be 'human' or 'ai_assisted'")
        if q.get("expected_tier") not in ("economy", "economy_escalation", "frontier"):
            errors.append(f"test {q['id']}: expected_tier must be economy, economy_escalation or frontier")
        if q.get("category") != "out_of_scope" and not q.get("context_ids"):
            errors.append(f"test {q['id']}: list the document(s) that answer it in context_ids")

    # The test set must contain nothing the system was tuned on.
    norm = lambda t: " ".join(t.lower().split())
    overlap = {norm(q["question"]) for q in dev} & {norm(q["question"]) for q in test}
    for t in sorted(overlap):
        errors.append(f"question appears in both dev and test sets: {t[:70]!r}")

    # Frozen means frozen: once the lock exists, any edit to the test set fails.
    import hashlib
    if test:
        digest = hashlib.sha256(config.TEST_QUESTIONS_PATH.read_bytes()).hexdigest()
        if config.TEST_LOCK_PATH.exists():
            if config.TEST_LOCK_PATH.read_text().split()[0] != digest:
                errors.append("questions_test.jsonl changed after it was frozen "
                              "(questions_test.sha256 no longer matches)")
        else:
            warnings.append("test set is not frozen yet: when it is complete, run "
                            "`python validate_data.py --freeze`")

    print(f"knowledge base : {len(kb)} documents")
    print(f"orders         : {len(orders)}")
    for label, qs, targets, fname in (("dev set", dev, DEV_TARGETS, config.DEV_QUESTIONS_PATH.name),
                                      ("test set", test, TEST_TARGETS, config.TEST_QUESTIONS_PATH.name)):
        total = sum(targets.values())
        counts = Counter(q["category"] for q in qs)
        frozen = " · FROZEN" if label == "test set" and config.TEST_LOCK_PATH.exists() else ""
        print(f"\n{label:9s}: {len(qs)} / {total}  ({fname}{frozen})")
        print(f"  {'category':22s} {'have':>5s} {'target':>7s}  progress")
        for cat, target in targets.items():
            have = counts.get(cat, 0)
            bar = "#" * int(20 * min(have / target, 1.0))
            print(f"  {cat:22s} {have:5d} {target:7d}  {bar:<20s} {100*have/target:5.1f}%")

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
    raise SystemExit(freeze() if "--freeze" in sys.argv else main())
