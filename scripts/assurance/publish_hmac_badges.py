"""Fail-closed publication HMAC gate for E156 assurance badges.

The elevated publication workflow must not silently omit authentication when
its secret is absent or when no badge exists. This runner preflights every
candidate before changing any badge, signs them with the *CI secret only*,
and verifies the result using the existing repository verifier.

This does not verify Sigstore/OIDC provenance or other ecosystems.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import sign_badge
import verify_badges


def publish(root: Path) -> int:
    secret = os.environ.get("E156_ASSURANCE_HMAC_KEY", "")
    if not secret.strip():
        print("REFUSED: E156_ASSURANCE_HMAC_KEY is missing or blank; "
              "publication requires the CI secret.", file=sys.stderr)
        return 2

    root = root.resolve()
    if not root.is_dir():
        print(f"REFUSED: publication root is not a directory: {root}", file=sys.stderr)
        return 2

    badges = sorted(p for p in root.rglob("assurance.json")
                    if ".git" not in p.relative_to(root).parts)
    if not badges:
        print("REFUSED: no assurance.json badges exist; refusing vacuous signing.",
              file=sys.stderr)
        return 2

    # Preflight *all* files before writing any signed badges. This prevents a
    # corrupt second badge from leaving a partially republished badge set.
    loaded: list[tuple[Path, dict]] = []
    for path in badges:
        if path.is_symlink() or not path.is_file():
            print(f"REFUSED: unsafe assurance badge path: {path}", file=sys.stderr)
            return 2
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            print(f"REFUSED: unreadable or invalid assurance badge {path}: {exc}",
                  file=sys.stderr)
            return 2
        if not isinstance(data, dict):
            print(f"REFUSED: assurance badge must be a JSON object: {path}",
                  file=sys.stderr)
            return 2
        loaded.append((path, data))

    key = secret.encode("utf-8")
    for path, badge in loaded:
        signed = sign_badge.sign(badge, key)
        path.write_text(json.dumps(signed, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")

    invalid, unsigned = verify_badges.verify_repo(root, require_signed=True, key=key)
    if invalid or unsigned:
        for path, reason in invalid:
            print(f"REFUSED: invalid signature for {path}: {reason}", file=sys.stderr)
        for path in unsigned:
            print(f"REFUSED: unsigned assurance badge: {path}", file=sys.stderr)
        return 1

    print(f"HMAC publication gate PASS: signed and verified {len(loaded)} badge(s).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."),
                        help="repository root containing assurance.json files")
    args = parser.parse_args(argv)
    return publish(args.repo)


if __name__ == "__main__":
    raise SystemExit(main())
