"""API keys for apps using the gateway.

The gateway issues its own keys ("tk-..."); an app sends one instead of an OpenAI key, and
never sees the provider key. Only a SHA-256 fingerprint of each key is stored, so the keys
file is useless to anyone who copies it. A key is shown once, when created.

    python -m tokenomics.keys create --client techstore --daily-budget 1.00
    python -m tokenomics.keys list
    python -m tokenomics.keys revoke --client techstore
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
from dataclasses import asdict, dataclass, field
from pathlib import Path

DEFAULT_KEYS_PATH = Path(os.getenv("TOKENOMICS_KEYS", "gateway_keys.json"))


@dataclass
class Client:
    client_id: str
    daily_budget_usd: float | None = None      # None: the gateway's default per-client budget
    allowed_models: list[str] = field(default_factory=list)   # empty: any priced model
    active: bool = True


def fingerprint(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


class KeyStore:
    def __init__(self, path: Path | str = DEFAULT_KEYS_PATH):
        self.path = Path(path)
        self._clients: dict[str, Client] = {}
        if self.path.exists():
            for fp, c in json.loads(self.path.read_text(encoding="utf-8")).items():
                self._clients[fp] = Client(**c)

    def lookup(self, key: str | None) -> Client | None:
        if not key:
            return None
        c = self._clients.get(fingerprint(key))
        return c if c and c.active else None

    def create(self, client_id: str, daily_budget_usd: float | None = None,
               allowed_models: list[str] | None = None) -> str:
        key = "tk-" + secrets.token_urlsafe(24)
        self._clients[fingerprint(key)] = Client(client_id, daily_budget_usd, allowed_models or [])
        self._save()
        return key

    def revoke(self, client_id: str) -> int:
        n = 0
        for c in self._clients.values():
            if c.client_id == client_id and c.active:
                c.active, n = False, n + 1
        self._save()
        return n

    def clients(self) -> list[Client]:
        return list(self._clients.values())

    def _save(self) -> None:
        self.path.write_text(json.dumps({fp: asdict(c) for fp, c in self._clients.items()}, indent=2),
                             encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="manage Tokenomics gateway keys")
    ap.add_argument("action", choices=["create", "list", "revoke"])
    ap.add_argument("--client", help="client id (the app or team the key is for)")
    ap.add_argument("--daily-budget", type=float, default=None, help="USD per day for this client")
    ap.add_argument("--models", default="", help="comma-separated allowed models (default: any)")
    ap.add_argument("--keys", default=str(DEFAULT_KEYS_PATH), help="keys file")
    args = ap.parse_args()
    store = KeyStore(args.keys)
    if args.action == "create":
        if not args.client:
            ap.error("create needs --client")
        key = store.create(args.client, args.daily_budget, [m for m in args.models.split(",") if m])
        print(f"key for {args.client} (shown once, store it safely):\n{key}")
    elif args.action == "revoke":
        print(f"revoked {store.revoke(args.client)} key(s) for {args.client}")
    else:
        for c in store.clients():
            print(f"{c.client_id:20} budget={c.daily_budget_usd} models={c.allowed_models or 'any'} "
                  f"{'active' if c.active else 'revoked'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
