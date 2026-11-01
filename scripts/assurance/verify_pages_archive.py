"""Fail closed if a GitHub Pages staging tree differs from an exact Git commit.

The git-archive command alone is insufficient: .gitattributes export-subst
changes blob bytes and export-ignore silently removes tracked files. Verify
EVERY staged regular file against Git blob IDs and reject missing/extra files,
symlinks, submodules and path collisions before privileged Pages upload.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath


def _refuse(message: str) -> int:
    print(f"REFUSED: Pages stage is not exact committed source: {message}", file=sys.stderr)
    return 2


def _git(repo: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout


def verify(repo: Path, sha: str, stage: Path) -> int:
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", sha):
        return _refuse("missing or malformed immutable commit SHA")
    if stage.is_symlink() or not stage.is_dir() or not repo.is_dir():
        return _refuse("missing repository or non-directory/symlinked stage")
    repo, stage = repo.resolve(), stage.resolve()
    if stage == repo or repo in stage.parents:
        return _refuse("stage resides inside source repository")
    try:
        fmt = _git(repo, "rev-parse", "--show-object-format").decode().strip()
        if fmt not in ("sha1", "sha256"):
            return _refuse("unknown Git object format")
        if (fmt == "sha1" and len(sha) != 40) or (fmt == "sha256" and len(sha) != 64):
            return _refuse("commit SHA format mismatches repository")
        tree = _git(repo, "ls-tree", "-rz", "--full-tree", sha)
    except (OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        return _refuse(f"cannot read immutable source tree: {type(exc).__name__}")

    expected: dict[str, str] = {}
    folded: set[str] = set()
    try:
        for record in tree.split(b"\0"):
            if not record:
                continue
            header, name = record.split(b"\t", 1)
            mode, kind, oid = header.decode("ascii").split(" ")
            path = name.decode("utf-8", "strict")
            parts = PurePosixPath(path).parts
            # Always use the same safe path semantics on Windows and Linux.
            if (not parts or path.startswith("/") or "\\" in path or ":" in path
                    or any(part in ("", ".", "..") or part.endswith((" ", ".")) for part in parts)):
                return _refuse("unsafe Git-tree path")
            if mode not in ("100644", "100755") or kind != "blob":
                return _refuse("symlink, submodule or non-regular Git-tree entry")
            if not re.fullmatch(r"[0-9a-f]+", oid) or len(oid) != len(sha):
                return _refuse("invalid Git-tree blob digest")
            key = path.casefold()
            if key in folded:
                return _refuse("case-colliding Git paths")
            folded.add(key)
            expected[path] = oid
    except (UnicodeError, ValueError, TypeError):
        return _refuse("malformed Git tree entry")
    if "assurance.html" not in expected or not expected:
        return _refuse("missing committed dashboard or empty tree")

    actual: set[str] = set()
    for parent, dirs, files in os.walk(stage, followlinks=False):
        base = Path(parent)
        for name in dirs:
            if (base / name).is_symlink():
                return _refuse("symlinked stage directory")
        for name in files:
            source = base / name
            try:
                st = source.lstat()
                if not stat.S_ISREG(st.st_mode):
                    return _refuse("non-regular stage file")
                rel = source.relative_to(stage).as_posix()
                if rel not in expected:
                    return _refuse("extra or unexpected stage file")
                digest = hashlib.new(fmt)
                digest.update(f"blob {st.st_size}\0".encode("ascii"))
                with source.open("rb") as fileobj:
                    while True:
                        block = fileobj.read(1024 * 1024)
                        if not block:
                            break
                        digest.update(block)
                if digest.hexdigest() != expected[rel]:
                    return _refuse("modified stage blob")
                actual.add(rel)
            except (OSError, ValueError) as exc:
                return _refuse(f"stage file unreadable: {type(exc).__name__}")
    if actual != set(expected):
        return _refuse("missing tracked file (possibly export-ignore)")
    print(f"Exact committed Pages tree PASS: {len(actual)} authenticated Git blobs at {sha}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--stage", type=Path, required=True)
    args = parser.parse_args(argv)
    return verify(args.repo, args.sha, args.stage)


if __name__ == "__main__":
    raise SystemExit(main())
