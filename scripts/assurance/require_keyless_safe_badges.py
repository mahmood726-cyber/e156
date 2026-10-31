"""Prepare HMAC-free E156 badges for mandatory Sigstore keyless signing.

This check never signs, verifies, or removes a legacy HMAC. When the authentic
CI HMAC secret is unavailable, any pre-existing HMAC mark must be refused
rather than silently reclassified as valid. Keyless signing AND identity-bound
bundle verification remain mandatory later in the assurance workflow.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def check(root: Path) -> int:
    root = root.resolve()
    if not root.is_dir():
        print("REFUSED: assurance root is missing", file=sys.stderr)
        return 2
    badges = sorted(p for p in root.rglob("assurance.json")
                    if ".git" not in p.relative_to(root).parts)
    if not badges:
        print("REFUSED: no assurance.json files for keyless signing", file=sys.stderr)
        return 2
    for path in badges:
        try:
            rel = path.relative_to(root)
            if any(root.joinpath(*rel.parts[:i]).is_symlink()
                   for i in range(1, len(rel.parts) + 1)):
                raise ValueError("symlink in badge path")
            if not path.is_file() or path.stat().st_size == 0:
                raise ValueError("missing or empty badge")
            badge = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(badge, dict):
                raise ValueError("badge must be a JSON object")
            if "signature" in badge or "signed_at" in badge:
                raise ValueError("unverified legacy HMAC fields present")
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
            print(f"REFUSED: unsafe badge {path}: {exc}", file=sys.stderr)
            return 2
    print(f"Keyless preflight PASS: {len(badges)} unsigned badge(s); "
          "Sigstore signing and verification still required.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    return check(args.repo)


if __name__ == "__main__":
    raise SystemExit(main())
