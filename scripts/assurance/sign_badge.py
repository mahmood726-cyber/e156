"""e156 Assurance — badge signing (Track C).

The assurance badge asserts a tier; assurance_badge_integrity proves the tier
matches the checks; but neither stops someone from rewriting BOTH consistently.
A signature binds the badge to a holder of a secret key, so a published badge
can be verified as issued by the operator and untampered.

Crypto rules (lessons.md "Cryptography / Signing"):
  - The HMAC key MUST NOT come from the bundle. It comes from
    $E156_ASSURANCE_HMAC_KEY, or a gitignored key file
    ($E156_ASSURANCE_HMAC_KEYFILE, default ~/.e156/assurance-hmac.key).
  - Fail closed if no key is available — never silent-default to a constant.
  - A placeholder signature is a P0 security bug; this module emits real
    HMAC-SHA256 only.
  - Verification uses hmac.compare_digest (constant-time).

The signature covers the canonical JSON of the badge with the `signature` and
`signed_at` fields removed, so signing is idempotent and the signature commits
to the substantive content (tier + checks + evidence + provenance).
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SIG_FIELDS = ("signature", "signed_at")
SIG_ALG = "HMAC-SHA256"
DEFAULT_KEYFILE = Path.home() / ".e156" / "assurance-hmac.key"


class MissingKeyError(RuntimeError):
    """No HMAC key available — fail closed rather than sign with a default."""


def get_key() -> bytes:
    env = os.environ.get("E156_ASSURANCE_HMAC_KEY")
    if env:
        return env.encode("utf-8")
    keyfile = os.environ.get("E156_ASSURANCE_HMAC_KEYFILE")
    candidates = [Path(keyfile)] if keyfile else []
    candidates.append(DEFAULT_KEYFILE)
    for p in candidates:
        try:
            if p.is_file():
                data = p.read_bytes().strip()
                if data:
                    return data
        except OSError:
            continue
    raise MissingKeyError(
        "no HMAC key: set $E156_ASSURANCE_HMAC_KEY or create a gitignored "
        f"key file ($E156_ASSURANCE_HMAC_KEYFILE or {DEFAULT_KEYFILE}). "
        "Signing fails closed rather than using a forgeable default."
    )


def canonical_payload(badge: dict) -> bytes:
    """Canonical bytes the signature commits to: the badge minus signature
    fields, JSON with sorted keys and tight separators."""
    body = {k: v for k, v in badge.items() if k not in SIG_FIELDS}
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_signature(badge: dict, key: bytes) -> str:
    return hmac.new(key, canonical_payload(badge), hashlib.sha256).hexdigest()


def sign(badge: dict, key: bytes) -> dict:
    """Return a copy of `badge` with a fresh signature + signed_at."""
    signed = dict(badge)
    signed["signature"] = f"{SIG_ALG}:{compute_signature(badge, key)}"
    signed["signed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return signed


def verify(badge: dict, key: bytes) -> bool:
    """Constant-time check that the badge's signature matches its content."""
    sig = badge.get("signature")
    if not isinstance(sig, str) or ":" not in sig:
        return False
    alg, _, hexdigest = sig.partition(":")
    if alg != SIG_ALG:
        return False
    expected = compute_signature(badge, key)
    return hmac.compare_digest(expected, hexdigest)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, badge: dict) -> None:
    path.write_text(json.dumps(badge, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Sign or verify an e156 assurance.json badge.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sign", help="add/refresh the HMAC signature on a badge")
    s.add_argument("path")
    v = sub.add_parser("verify", help="verify a badge's signature (exit 0 = valid)")
    v.add_argument("path")
    args = ap.parse_args(argv)

    path = Path(args.path)
    try:
        key = get_key()
    except MissingKeyError as e:
        sys.stderr.write(f"{e}\n")
        return 2

    if args.cmd == "sign":
        badge = _load(path)
        _save(path, sign(badge, key))
        print(f"signed {path}")
        return 0

    if args.cmd == "verify":
        badge = _load(path)
        if verify(badge, key):
            print(f"OK: signature valid for {path}")
            return 0
        sys.stderr.write(f"INVALID signature for {path}\n")
        return 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
