"""Refuse commits containing anything beyond generated E156 assurance artifacts.

The privileged master assurance workflow creates cached DOI evidence, a badge,
its Sigstore bundle and a dashboard. It must not silently commit edits to
AGENTS.md, workbook human fields, protocols, research files or workflow code.
Run *after* git add -A, *before* git commit; a refusal prevents any push.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

GENERATED = frozenset({
    "doi-cache.json",
    "assurance.html",
    "e156-submission/assurance.json",
    "e156-submission/assurance.json.cosign.bundle",
})


def _git(repo: Path, *args: str) -> list[str]:
    data = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--no-renames", "-z", *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    ).stdout
    return [entry.decode("utf-8", "strict") for entry in data.split(b"\0") if entry]


def _refuse_nonregular_index_entries(repo: Path, paths: list[str]) -> None:
    """Reject staged symlinks, submodules and executable/generated path mode changes.

    Git's --name-only diff is not a content-type guarantee: a path allowed by
    name could have become a symlink or gitlink in the index. All new assurance
    outputs are generated regular non-executable files.
    """
    if not paths:
        return
    data = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "--stage", "-z", "--", *paths],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    ).stdout
    seen: set[str] = set()
    for record in data.split(b"\0"):
        if not record:
            continue
        metadata, filename = record.split(b"\t", 1)
        mode, _oid, stage = metadata.split()
        path = filename.decode("utf-8", "strict")
        if mode != b"100644" or stage != b"0":
            raise ValueError(f"non-regular or unmerged generated path: {path}")
        if path in seen:
            raise ValueError(f"duplicate generated path in index: {path}")
        seen.add(path)
    if seen != set(paths):
        raise ValueError("generated-path index differs from the staged diff")


def check(repo: Path) -> int:
    try:
        if not repo.is_dir():
            raise ValueError("missing source repository")
        paths = _git(repo, "--name-only")
        removed = _git(repo, "--diff-filter=D", "--name-only")
        if removed:
            raise ValueError("staged deletion forbidden: " + ", ".join(removed[:5]))
        unexpected = sorted(
            path for path in paths
            if path not in GENERATED
        )
        if unexpected:
            raise ValueError("non-generated staged path: " + ", ".join(unexpected[:5]))
        _refuse_nonregular_index_entries(repo, paths)
    except (ValueError, OSError, UnicodeError, subprocess.CalledProcessError) as exc:
        print(f"REFUSED: privileged assurance commit includes unsafe changes: {exc}", file=sys.stderr)
        return 2
    print(f"Generated-only commit gate PASS: {len(paths)} permitted staged artifact(s)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    return check(parser.parse_args(argv).repo)


if __name__ == "__main__":
    raise SystemExit(main())
