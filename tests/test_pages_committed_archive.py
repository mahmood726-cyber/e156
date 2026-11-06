"""Real Git archive canary: Pages staging cannot include ignored or symlinked data.

Synthetic-only. This test verifies git archive semantics on each hosted OS; the
workflow structure tests separately bind upload-pages-artifact to this archive.
"""
from __future__ import annotations

import io
import subprocess
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory


def git(root: Path, *args: str, input_data: bytes | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=root, input=input_data, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )


def test_pages_archive_excludes_ignored_data_and_binds_committed_bytes():
    with TemporaryDirectory() as temp:
        repo = Path(temp)
        git(repo, "init", "-q")
        git(repo, "config", "user.name", "Synthetic Test")
        git(repo, "config", "user.email", "synthetic@example.invalid")
        (repo / ".gitignore").write_text("private-session.log\n", encoding="utf-8")
        (repo / "assurance.html").write_text("assured v1\n", encoding="utf-8")
        git(repo, "add", ".gitignore", "assurance.html")
        git(repo, "commit", "-qm", "synthetic assured source")
        sha = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
        (repo / "private-session.log").write_text("NEVER SHIP PRIVATE DATA", encoding="utf-8")
        assert git(repo, "status", "--porcelain").stdout == b"", (
            "ignored data must reproduce why clean status alone is insufficient"
        )
        archive = git(repo, "-c", "core.autocrlf=false", "archive", "--format=tar", sha).stdout
        # Compare to committed blob bytes, not a literal LF assumption:
        # Windows Git may commit a CRLF test fixture, but it must not alter
        # the committed data when constructing the publication archive.
        original_bytes = git(repo, "show", f"{sha}:assurance.html").stdout
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tf:
            names = tf.getnames()
            assert "assurance.html" in names
            assert "private-session.log" not in names
            assured = tf.extractfile("assurance.html")
            assert assured is not None and assured.read() == original_bytes
        committed_blob = git(repo, "rev-parse", f"{sha}:assurance.html").stdout.strip()
        archived_blob = git(repo, "hash-object", "--stdin", input_data=original_bytes).stdout.strip()
        assert committed_blob == archived_blob
        # New unsigned working-tree bytes must not be included in archived SHA.
        (repo / "assurance.html").write_text("tampered v2\n", encoding="utf-8")
        assert git(repo, "status", "--porcelain").stdout != b""
        assert b"tampered" not in archive


def test_tracked_symlink_mode_is_detectable_without_filesystem_symlinks():
    # git update-index can plant a symlink *index entry* even when Windows
    # runners cannot create a filesystem symlink without extra privileges.
    with TemporaryDirectory() as temp:
        repo = Path(temp)
        git(repo, "init", "-q")
        git(repo, "config", "user.name", "Synthetic Test")
        git(repo, "config", "user.email", "synthetic@example.invalid")
        blob = git(repo, "hash-object", "-w", "--stdin", input_data=b"../outside").stdout.decode().strip()
        git(repo, "update-index", "--add", "--cacheinfo", f"120000,{blob},outbound-link")
        git(repo, "commit", "-qm", "synthetic symlink tree")
        sha = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
        tree = git(repo, "ls-tree", "-r", sha).stdout.decode()
        assert any(line.startswith("120000 blob ") for line in tree.splitlines()), (
            "symlink metadata must be detectable before any archive extraction"
        )
