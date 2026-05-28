"""Verify HMAC signatures on every assurance.json badge — the enforcement
point that makes signing load-bearing.

The 2026-05-28 security review found that sign_badge.py was decorative: nothing
ever called verify(), so a forged badge published anywhere was never checked.
This script is the gate. It loads the key (E156_ASSURANCE_HMAC_KEY or a
gitignored keyfile) and exits non-zero if any badge's signature is INVALID, and
— with --require-signed — also if any badge is UNSIGNED. Run it in CI with the
key as a secret (the commit-time Sentinel rules cannot, by design, hold the
key); the public, keyless counterpart is cosign verify-blob in the workflow.

Rollout: default mode fails only on INVALID signatures (so the gate can land
before every legacy badge is signed); flip --require-signed once the portfolio
is fully signed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sign_badge  # noqa: E402  (sibling module in scripts/assurance/)


def verify_repo(root: Path, require_signed: bool, key: bytes) -> tuple[list, list]:
    invalid: list[tuple[Path, str]] = []
    unsigned: list[Path] = []
    for p in sorted(root.rglob("assurance.json")):
        if ".git" in p.parts:
            continue
        try:
            badge = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            invalid.append((p, "unreadable / invalid JSON"))
            continue
        if not isinstance(badge, dict) or not badge.get("signature"):
            unsigned.append(p)
            continue
        if not sign_badge.verify(badge, key):
            invalid.append((p, "signature does not match content (forged or stale)"))
    return invalid, unsigned


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Verify assurance.json badge signatures.")
    ap.add_argument("--repo", default=".", help="Repo root to scan (default: cwd)")
    ap.add_argument("--require-signed", action="store_true",
                    help="also fail if any badge is unsigned (default: only fail on invalid)")
    args = ap.parse_args(argv)

    root = Path(args.repo).resolve()
    try:
        key = sign_badge.get_key()
    except sign_badge.MissingKeyError as e:
        sys.stderr.write(f"{e}\n")
        return 2

    invalid, unsigned = verify_repo(root, args.require_signed, key)
    for p, why in invalid:
        print(f"FAIL {p}: {why}")
    if args.require_signed:
        for p in unsigned:
            print(f"FAIL {p}: unsigned")
    elif unsigned:
        print(f"note: {len(unsigned)} unsigned badge(s) (not failing; pass --require-signed to enforce)")

    ok = not invalid and (not args.require_signed or not unsigned)
    print("OK: all badge signatures valid" if ok else "FAILED: badge signature verification")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
