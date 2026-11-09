"""Per-run release bundles must not reach the privileged assurance commit.

The master workflow signs every assurance.json (the verifier requires a bundle
beside each), but its commit gate allows only the root badge files. On
2026-11-09 the first unblocked master run created
releases/*/e156-submission/assurance.json.cosign.bundle, `git add -A` staged
them, and the gate refused the commit, so no master run could finish.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts" / "assurance"))

import refuse_unexpected_staged_changes as gate  # noqa: E402


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True)


def test_release_bundles_are_ignored_but_root_bundle_is_committable(tmp_path: Path) -> None:
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@example.invalid")
    _git(tmp_path, "config", "user.name", "t")
    shutil.copy(REPO / ".gitignore", tmp_path / ".gitignore")
    sub = tmp_path / "e156-submission"
    sub.mkdir()
    (sub / "assurance.json").write_text("{}\n", encoding="utf-8")
    release = tmp_path / "releases" / "demo" / "e156-submission"
    release.mkdir(parents=True)
    (release / "assurance.json").write_text("{}\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "base")

    # What a signing run leaves behind.
    (sub / "assurance.json.cosign.bundle").write_text("root-bundle\n", encoding="utf-8")
    (release / "assurance.json.cosign.bundle").write_text("release-bundle\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")

    assert gate.check(tmp_path) == 0
    staged = subprocess.run(["git", "-C", str(tmp_path), "diff", "--cached", "--name-only"],
                            capture_output=True, text=True, check=True).stdout.split()
    assert staged == ["e156-submission/assurance.json.cosign.bundle"]
