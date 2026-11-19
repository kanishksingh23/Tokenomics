"""Technique 12, spending limits: check each client's budget BEFORE a request is sent.

Langfuse records what was spent after the fact; this decides beforehand (a prepaid balance,
not a bill). For every request that would call a model:

    estimated cost = input tokens (counted) x input price + expected output x output price
    whole app over its daily cap ............................ refuse  (runaway-loop guard)
    client over its daily budget ............................ refuse
    client past the soft limit (default 80% of budget) ....... downgrade to the cheap model
    client sending too many requests per minute .............. refuse that request
    otherwise ................................................ allow

After the call the ACTUAL cost is recorded, so estimates never drift from the bill.
Answers from the FAQ shortcut or the cache cost nothing and are never counted.

Spend is kept in a small SQLite file chosen by the caller (in memory by default).
Days are UTC calendar days.
"""
from __future__ import annotations

import datetime as dt
import sqlite3
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from tokenomics.pricing import PRICING
from tokenomics.tokens import prompt_tokens

# Defaults; callers (the TechStore agent, the gateway) pass their own settings.
DEFAULTS = {"client_daily_usd": 0.05, "global_daily_usd": 5.00, "soft_ratio": 0.8, "rpm": 20,
            "expected_output_tokens": 200}
GLOBAL = "__all__"                  # the row holding the whole app's spend


@dataclass
class Decision:
    action: str                     # "allow" | "downgrade" | "refuse"
    reason: str
    client_spent: float = 0.0       # today, before this request
    client_budget: float | None = None
    model: str | None = None        # model to use when downgrading


class TokenBucket:
    """Requests-per-minute limit: a bucket of `rate` tokens refilled continuously.
    Each request takes one; an empty bucket means wait. Bursts up to `rate` are fine."""

    def __init__(self, rate_per_minute: float, clock=time.monotonic):
        self.rate, self.clock = rate_per_minute, clock
        self.tokens, self.last = float(rate_per_minute), clock()

    def take(self) -> bool:
        now = self.clock()
        self.tokens = min(self.rate, self.tokens + (now - self.last) * self.rate / 60)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


class SpendingLimits:
    def __init__(self, path: Path | str = ":memory:", client_daily_usd: float | None = None,
                 global_daily_usd: float | None = None, soft_ratio: float | None = None,
                 rpm: float | None = None, downgrade_model: str | None = None,
                 clock=time.time, bucket_clock=time.monotonic):
        if str(path) != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        # Shared across threads (Streamlit answers each message on a new thread); the lock
        # makes each read-and-update a single step.
        self.db = sqlite3.connect(str(path), check_same_thread=False)
        self._lock = threading.RLock()
        self.db.execute("CREATE TABLE IF NOT EXISTS spend (client TEXT, day TEXT, usd REAL, "
                        "requests INTEGER, PRIMARY KEY (client, day))")
        pick = lambda v, k: DEFAULTS[k] if v is None else v  # noqa: E731
        self.client_daily = pick(client_daily_usd, "client_daily_usd")
        self.global_daily = pick(global_daily_usd, "global_daily_usd")
        self.soft_ratio = pick(soft_ratio, "soft_ratio")
        self.rpm = pick(rpm, "rpm")
        self.downgrade_model = downgrade_model    # None: never downgrade, refuse instead
        self.clock, self.bucket_clock = clock, bucket_clock
        self._buckets: dict[str, TokenBucket] = {}

    def _day(self) -> str:
        return dt.datetime.fromtimestamp(self.clock(), dt.timezone.utc).date().isoformat()

    def spent(self, client: str) -> float:
        with self._lock:
            row = self.db.execute("SELECT usd FROM spend WHERE client=? AND day=?",
                                  (client, self._day())).fetchone()
            return row[0] if row else 0.0

    def check(self, client: str | None, model: str, estimate, budget: float | None = None) -> Decision:
        """Decide before the call. `estimate(model) -> usd` prices this request on any model.
        `client` None means no per-client limits (e.g. a script); the app cap still applies.
        `budget` overrides the default per-client budget for this check (e.g. a key's own)."""
        with self._lock:
            est = estimate(model)
            total = self.spent(GLOBAL)
            if self.global_daily and total + est > self.global_daily:
                return Decision("refuse", f"app daily cap ${self.global_daily:.2f} reached "
                                          f"(${total:.4f} spent today)")
            if client is None:
                return Decision("allow", "no client limits")
            if self.rpm:
                bucket = self._buckets.setdefault(client, TokenBucket(self.rpm, self.bucket_clock))
                if not bucket.take():
                    return Decision("refuse", f"more than {self.rpm:g} requests per minute")
            mine = self.spent(client)
            budget = self.client_daily if budget is None else budget
            if not budget or mine + est <= budget * self.soft_ratio:
                return Decision("allow", "within budget", mine, budget)
            if self.downgrade_model and model != self.downgrade_model:
                # Past the soft limit: the cheap model, if that still fits the budget.
                if mine + estimate(self.downgrade_model) <= budget:
                    return Decision("downgrade", f"past {self.soft_ratio:.0%} of the daily budget",
                                    mine, budget, self.downgrade_model)
            elif mine + est <= budget:
                # No cheap model configured, or already using it: allow up to the budget.
                return Decision("allow", "past the soft limit, within budget", mine, budget)
            return Decision("refuse", f"daily budget ${budget:.2f} reached", mine, budget)

    def record(self, client: str | None, usd: float) -> None:
        """Add the ACTUAL cost of a call (to the client and to the app total)."""
        with self._lock:
            day = self._day()
            for who in ([client] if client else []) + [GLOBAL]:
                self.db.execute("INSERT INTO spend VALUES (?,?,?,1) ON CONFLICT(client, day) DO UPDATE "
                                "SET usd = usd + excluded.usd, requests = requests + 1", (who, day, usd))
            self.db.commit()


def estimate_cost(model: str, messages: list[dict], expected_output_tokens: int | None = None) -> float:
    """Cost before the call: real input tokens plus an expected answer length."""
    p = PRICING.get(model)
    if not p:
        return 0.0
    out = DEFAULTS["expected_output_tokens"] if expected_output_tokens is None else expected_output_tokens
    return (prompt_tokens(messages) * p["input"] + out * p["output"]) / 1e6
