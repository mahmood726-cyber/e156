"""Require authentic Sigstore badge-bundle verification before E156 publication.

This production gate checks the signed badge bytes, bundle, GitHub Actions
workflow identity and Fulcio issuer. It does not authenticate upstream
Sentinel/Overmind/Meta-Harness releases or certify the full ecosystem.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

REPOSITORY = "mahmood726-cyber/e156"
REF = "refs/heads/master"
ISSUER = "https://token.actions.githubusercontent.com"
IDENTITY = f"https://github.com/{REPOSITORY}/.github/workflows/assurance.yml@{REF}"


def _refuse(message: str) -> int:
    print(f"REFUSED: {message}", file=sys.stderr)
    return 2


def verify(root: Path) -> int:
    if os.environ.get("GITHUB_REPOSITORY") != REPOSITORY:
        return _refuse("unexpected signing repository; refusing Sigstore publication")
    if os.environ.get("GITHUB_REF") != REF:
        return _refuse("unexpected signing ref; refusing Sigstore publication")
    # Prevent replay of an otherwise valid older master-workflow bundle. The
    # OIDC certificate must name the exact commit that triggered THIS run,
    # not merely a reusable repository/branch/workflow identity.
    workflow_sha = os.environ.get("GITHUB_SHA", "")
    if not re.fullmatch(r"[0-9a-f]{40}", workflow_sha):
        return _refuse("missing or malformed GitHub workflow source SHA")
    root = root.resolve()
    if not root.is_dir():
        return _refuse("assurance root missing")
    badges = sorted(p for p in root.rglob("assurance.json")
                    if ".git" not in p.relative_to(root).parts)
    if not badges:
        return _refuse("no badges exist; zero Sigstore checks is not success")

    # Fail closed *before* invoking cosign if even one required bundle is
    # absent, empty, symlinked or outside the expected repository tree.
    for badge in badges:
        bundle = Path(str(badge) + ".cosign.bundle")
        for path in (badge, bundle):
            try:
                relative = path.relative_to(root)
                parts = relative.parts
                if any((root.joinpath(*parts[:i])).is_symlink()
                       for i in range(1, len(parts) + 1)):
                    return _refuse(f"symlink in badge or bundle path: {path}")
                if not path.is_file() or not path.stat().st_size:
                    return _refuse(f"missing or empty badge/bundle: {path}")
            except (OSError, ValueError) as exc:
                return _refuse(f"unreadable badge/bundle {path}: {exc}")

    for badge in badges:
        bundle = Path(str(badge) + ".cosign.bundle")
        command = [
            "cosign", "verify-blob", "--bundle", str(bundle),
            "--certificate-identity", IDENTITY,
            "--certificate-oidc-issuer", ISSUER,
            "--certificate-github-workflow-repository", REPOSITORY,
            "--certificate-github-workflow-ref", REF,
            "--certificate-github-workflow-sha", workflow_sha,
            str(badge),
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=False)
        except OSError as exc:
            return _refuse(f"cosign unavailable or failed to execute: {exc}")
        if result.returncode != 0:
            return _refuse(f"Sigstore verification failed for {badge}: {result.stderr.strip()}")
    print(f"Sigstore hard gate PASS: {len(badges)} badge bundle(s) verified.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    return verify(parser.parse_args(argv).repo)


if __name__ == "__main__":
    raise SystemExit(main())
