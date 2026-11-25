"""Gateway tests: in-process (FastAPI's test client), stand-in provider, no network, no cost."""
from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from tokenomics import response_cache  # noqa: E402
from tokenomics.gateway import Settings, _completion, create_app, mock_upstream  # noqa: E402
from tokenomics.keys import KeyStore  # noqa: E402


def _bow(texts):
    """Bag-of-words unit vectors: a tiny stand-in for the embedding model."""
    vocab: dict[str, int] = {}
    out = np.zeros((len(texts), 256))
    for i, t in enumerate(texts):
        for w in t.lower().replace("?", " ").split():
            out[i, vocab.setdefault(w, len(vocab)) % 256] += 1
    return out / np.maximum(np.linalg.norm(out, axis=1, keepdims=True), 1e-9)


@pytest.fixture
def gw(tmp_path, monkeypatch):
    monkeypatch.setattr(response_cache, "_minilm", lambda: _bow)
    keys = KeyStore(tmp_path / "keys.json")
    key = keys.create("techstore")
    poor = keys.create("poor-app", daily_budget_usd=0.004)
    seen = []
    s = Settings(upstream="mock", state_dir=":memory:", memory="window", keep_turns=1)
    base = mock_upstream(s)

    def upstream(req):
        seen.append(req)
        if "explode" in str(req["messages"]):
            raise RuntimeError("provider down")
        return base(req)
    app = create_app(s, upstream=upstream, keys=keys)
    return TestClient(app), key, poor, seen


def _ask(c, key, content, headers=None, messages=None, **extra):
    body = {"model": "gpt-6.1-sol", "messages": messages or [{"role": "user", "content": content}], **extra}
    return c.post("/v1/chat/completions", json=body,
                  headers={"Authorization": f"Bearer {key}", **(headers or {})})


def test_health_auth_and_models(gw):
    c, key, _, _ = gw
    assert c.get("/health").json() == {"status": "ok"}
    assert _ask(c, "tk-wrong", "hi").status_code == 401
    assert c.post("/v1/chat/completions", json={}).status_code == 401
    ids = [m["id"] for m in c.get("/v1/models", headers={"Authorization": f"Bearer {key}"}).json()["data"]]
    assert "gpt-6.1-sol" in ids and "gpt-6-luna" in ids
    assert _ask(c, key, "hi", stream=True).status_code == 400


def test_model_call_then_cache_hit(gw):
    c, key, _, seen = gw
    first = _ask(c, key, "Is delivery free?")
    assert first.status_code == 200 and first.headers["X-Tokenomics-Served-By"] == "model"
    data = first.json()
    assert data["choices"][0]["message"]["content"] and data["tokenomics"]["cost_usd"] > 0
    assert data["tokenomics"]["cache_store"] == "stored"
    again = _ask(c, key, "is delivery free")
    assert again.json()["tokenomics"]["served_by"] == "cache" and len(seen) == 1   # no provider call
    assert again.json()["usage"]["total_tokens"] == 0


def test_cache_respects_privacy_namespace_and_follow_ups(gw):
    c, key, _, seen = gw
    _ask(c, key, "Why was I charged twice?", headers={"X-Tokenomics-Private": "true"})
    _ask(c, key, "Why was I charged twice?", headers={"X-Tokenomics-Private": "true"})
    assert len(seen) == 2                                  # private: never stored or served
    _ask(c, key, "How long is the warranty?", headers={"X-Tokenomics-Namespace": "kb-v1"})
    _ask(c, key, "How long is the warranty?", headers={"X-Tokenomics-Namespace": "kb-v2"})
    assert len(seen) == 4                                  # knowledge changed: no reuse
    chat = [{"role": "user", "content": "Is delivery free?"}, {"role": "assistant", "content": "Yes"},
            {"role": "user", "content": "Is delivery free?"}]
    _ask(c, key, "", messages=chat)
    _ask(c, key, "", messages=chat)
    assert len(seen) == 6                                  # follow-ups are never cached


def test_memory_trims_what_the_provider_receives(gw):
    c, key, _, seen = gw
    chat = []
    for i in range(3):
        chat += [{"role": "user", "content": f"question {i}"},
                 {"role": "assistant", "content": f"answer {i}"}]
    r = _ask(c, key, "", messages=chat + [{"role": "user", "content": "question 3"}])
    assert r.json()["tokenomics"]["memory"]["dropped_turns"] == 2
    assert [m["content"] for m in seen[-1]["messages"]] == ["question 2", "answer 2", "question 3"]


def test_spending_limits_downgrade_then_refuse(gw):
    c, _, poor, _ = gw
    results = [_ask(c, poor, f"question number {i} about returns") for i in range(60)]
    models = [r.json().get("tokenomics", {}).get("model") for r in results if r.status_code == 200]
    assert models[0] == "gpt-6.1-sol" and "gpt-6-luna" in models          # downgraded past 80%
    assert results[-1].status_code == 429 and results[-1].headers["X-Tokenomics-Served-By"] == "limit"


def test_provider_error_is_reported(gw):
    c, key, _, _ = gw
    r = _ask(c, key, "please explode")
    assert r.status_code == 502 and "provider error" in r.json()["error"]["message"]


def test_keys_are_stored_as_fingerprints(tmp_path):
    store = KeyStore(tmp_path / "keys.json")
    key = store.create("app", 0.5, ["gpt-6-luna"])
    assert key.startswith("tk-") and key not in (tmp_path / "keys.json").read_text()
    assert store.lookup(key).client_id == "app" and store.lookup("tk-nope") is None
    store.revoke("app")
    assert KeyStore(tmp_path / "keys.json").lookup(key) is None


def test_completion_shape():
    out = _completion("m", "hello", {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2})
    assert out["object"] == "chat.completion" and out["choices"][0]["message"]["content"] == "hello"


def test_default_verbosity_low_unless_the_app_sets_it(gw):
    c, key, _, seen = gw
    r = _ask(c, key, "What colours does the Y500 come in?")
    assert seen[-1]["verbosity"] == "low" and r.json()["tokenomics"]["verbosity"].startswith("low")
    _ask(c, key, "How heavy is the Y500 exactly?", verbosity="high")
    assert seen[-1]["verbosity"] == "high"                  # the app's own choice wins
