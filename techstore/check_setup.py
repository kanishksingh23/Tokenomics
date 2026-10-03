"""Pre-flight check before spending anything on real API calls.

    python check_setup.py           # free: config, key, model ids, pricing, data
    python check_setup.py --ping    # also makes ONE tiny real call (< $0.001)

Exit code 0 only if every required check passes.
"""
from __future__ import annotations

import argparse
import difflib
import importlib
import subprocess
import sys
from datetime import date

import config

OK, WARN, FAIL = "  ok  ", " warn ", " FAIL "
_failures = 0


def report(status: str, msg: str, hint: str | None = None) -> None:
    global _failures
    if status == FAIL:
        _failures += 1
    print(f"[{status}] {msg}")
    if hint:
        print(f"         -> {hint}")


def match_models(available: list[str], wanted: list[str]) -> dict[str, list[str]]:
    """For each wanted model id missing from `available`, return close matches.
    An empty list for a missing id means nothing similar exists.

    Versioned ids of the SAME model (``gpt-5.6-sol-2026-08-01`` for ``gpt-5.6-sol``)
    rank first. Plain string similarity alone ranks ``gpt-5.6-luna`` above them,
    which would suggest the economy model as a replacement for the frontier one
    and silently make every benchmark arm run the same model.
    """
    have = set(available)
    out = {}
    for w in wanted:
        if w in have:
            continue
        same_model = sorted((a for a in available if a.startswith(w + "-")), key=len)
        fuzzy = [a for a in difflib.get_close_matches(w, available, n=3, cutoff=0.5)
                 if a not in same_model]
        out[w] = (same_model + fuzzy)[:3]
    return out


def check_python() -> None:
    v = sys.version_info
    report(OK if v >= (3, 10) else FAIL, f"python {v.major}.{v.minor} at {sys.executable}",
           None if v >= (3, 10) else "3.10+ required (the code uses X | None annotations)")


def check_packages() -> bool:
    required = {"openai": "real model calls", "dotenv": "loading .env"}
    optional = {"streamlit": "the UI", "tiktoken": "exact token counts in mock mode",
                "sentence_transformers": "the embedding retriever"}
    have_openai = True
    for mod, why in required.items():
        try:
            importlib.import_module(mod)
            report(OK, f"{mod} installed")
        except ImportError:
            have_openai = have_openai and mod != "openai"
            pip = "python-dotenv" if mod == "dotenv" else mod
            report(FAIL, f"{mod} missing (needed for {why})",
                   f"{sys.executable} -m pip install {pip}")
    for mod, why in optional.items():
        try:
            importlib.import_module(mod)
            report(OK, f"{mod} installed")
        except ImportError:
            report(WARN, f"{mod} not installed (optional: {why})")
    return have_openai


def check_env() -> bool:
    env = config.BASE_DIR / ".env"
    if not env.exists():
        report(FAIL, ".env not found", "cp .env.example .env, then add your key")
    else:
        report(OK, ".env present")
    key = config.API_KEY
    if not key:
        report(FAIL, "OPENAI_API_KEY is empty")
        return False
    if key.strip() != key or " " in key:
        report(FAIL, "OPENAI_API_KEY contains whitespace", "check for a trailing space or newline")
        return False
    if not key.startswith("sk-") or key == "sk-...":
        report(FAIL, "OPENAI_API_KEY does not look like a real key", "it should start with sk-")
        return False
    report(OK, f"OPENAI_API_KEY set (…{key[-4:]})")
    report(OK, f"base URL {config.BASE_URL}")
    return True


def check_gitignore() -> None:
    try:
        out = subprocess.run(["git", "check-ignore", "-q", str(config.BASE_DIR / ".env")],
                             cwd=config.BASE_DIR, capture_output=True, timeout=10)
    except Exception:                                   # noqa: BLE001
        report(WARN, "could not ask git whether .env is ignored")
        return
    if out.returncode == 0:
        report(OK, ".env is git-ignored")
    elif out.returncode == 1:
        report(FAIL, ".env is NOT git-ignored -- your key could be committed",
               "add .env to .gitignore before committing")
    else:
        report(WARN, "not inside a git repository yet; confirm .env is ignored once it is")


def check_pricing() -> None:
    for role, model in (("frontier", config.FRONTIER_MODEL), ("economy", config.ECONOMY_MODEL)):
        if model in config.PRICING:
            p = config.PRICING[model]
            report(OK, f"{role} {model} priced at ${p['input']}/${p['output']} per 1M")
        else:
            report(FAIL, f"{role} {model} has no entry in config.PRICING",
                   "every cost for this model would be recorded as $0")
    age = (date.today() - date.fromisoformat(config.PRICING_AS_OF)).days
    report(OK if age <= 90 else WARN, f"pricing table is {age} days old (as of {config.PRICING_AS_OF})",
           None if age <= 90 else "re-check prices against the provider's pricing page")
    print("         note: prices come from research, not your account. Confirm them on the")
    print("         provider's pricing page; a wrong price makes every measured cost wrong.")


def check_models() -> list[str]:
    """Returns the model ids that are usable."""
    import openai                                       # noqa: PLC0415
    client = openai.OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)
    try:
        available = sorted(m.id for m in client.models.list())
    except openai.AuthenticationError:
        report(FAIL, "API key rejected (401)", "regenerate the key, or check it belongs to this org")
        return []
    except openai.PermissionDeniedError as e:
        report(FAIL, f"permission denied listing models: {e}")
        return []
    except openai.APIConnectionError:
        report(FAIL, f"cannot reach {config.BASE_URL}", "check your network or OPENAI_BASE_URL")
        return []
    except openai.APIStatusError as e:
        report(FAIL, f"provider returned {e.status_code} listing models")
        return []

    report(OK, f"key accepted; {len(available)} models visible to your account")
    wanted = [config.FRONTIER_MODEL, config.ECONOMY_MODEL]
    missing = match_models(available, wanted)
    for w in wanted:
        if w not in missing:
            report(OK, f"model {w} exists")
        elif missing[w]:
            top = missing[w][0]
            same = top.startswith(w + "-")
            report(FAIL, f"model {w} not found",
                   ("likely the same model, versioned: " if same
                    else "no versioned match. Similar names (may be DIFFERENT models -- "
                         "do not substitute blindly): ")
                   + ", ".join(missing[w])
                   + "  (set FRONTIER_MODEL / ECONOMY_MODEL in .env, and add its price)")
        else:
            report(FAIL, f"model {w} not found, and nothing similar is listed")
    return [w for w in wanted if w not in missing]


def ping(model: str) -> None:
    import openai                                       # noqa: PLC0415
    client = openai.OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)
    try:
        r = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": "Reply with the word ok."}],
            max_tokens=5, temperature=0)
    except openai.RateLimitError as e:
        msg = str(e)
        report(FAIL, f"{model}: rate limited or out of credit (429)",
               "add prepaid credit" if "quota" in msg.lower() else "wait and retry")
        return
    except openai.BadRequestError as e:
        report(FAIL, f"{model}: request rejected (400): {e}",
               "some newer models reject max_tokens or temperature; paste this error to fix agent.py")
        return
    except openai.APIStatusError as e:
        report(FAIL, f"{model}: provider returned {e.status_code}: {e}")
        return
    u = r.usage
    cost = config.price(model, u.prompt_tokens, u.completion_tokens)
    report(OK, f"{model} answered ({u.prompt_tokens}+{u.completion_tokens} tokens, ${cost:.6f})")


def check_data() -> None:
    import validate_data                                # noqa: PLC0415
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = validate_data.main()
    report(OK if rc == 0 else FAIL, "corpus integrity (validate_data.py)",
           None if rc == 0 else "run python validate_data.py for details")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ping", action="store_true",
                    help="make one tiny real call per configured model (< $0.001 total)")
    args = ap.parse_args()

    print("== environment"); check_python(); have_openai = check_packages()
    print("\n== credentials"); key_ok = check_env(); check_gitignore()
    print("\n== pricing"); check_pricing()
    print("\n== data"); check_data()

    usable: list[str] = []
    print("\n== provider")
    if have_openai and key_ok:
        usable = check_models()
    else:
        report(WARN, "skipped: needs the openai package and a valid key")

    if args.ping:
        print("\n== live call")
        for m in usable:
            ping(m)
        if not usable:
            report(WARN, "skipped: no usable models")

    print()
    if _failures:
        print(f"{_failures} check(s) failed. Fix these before spending anything.")
        return 1
    print("All required checks passed." + ("" if args.ping else
          " Run with --ping to confirm a real call works."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
