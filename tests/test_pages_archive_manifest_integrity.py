"""Synthetic Windows/Linux refusal canaries for the exact Pages Git-tree manifest."""
from __future__ import annotations

import io
import os
import shutil
import stat
import subprocess
import sys
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "assurance"))
from verify_pages_archive import _mode_matches_git_index, verify  # noqa: E402


def git(repo: Path, *args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], input=data,
                          check=True, capture_output=True).stdout


def repo_and_stage(parent: Path, *, attrs="") -> tuple[Path, Path, str]:
    repo = parent / "source"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Synthetic Test")
    git(repo, "config", "user.email", "synthetic@example.invalid")
    (repo / ".gitattributes").write_text(attrs, encoding="utf-8")
    (repo / "assurance.html").write_bytes(b"authenticated dashboard\n")
    (repo / "report.txt").write_bytes(b"digest=$Format:%H$\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "synthetic release")
    sha = git(repo, "rev-parse", "HEAD").decode().strip()
    stage = parent / "stage"
    stage.mkdir()
    archive = git(repo, "-c", "core.autocrlf=false", "archive", "--format=tar", sha)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as stream:
        for item in stream:
            if item.isfile():
                destination = stage / item.name
                destination.parent.mkdir(parents=True, exist_ok=True)
                with stream.extractfile(item) as input_file, destination.open("wb") as output_file:
                    shutil.copyfileobj(input_file, output_file)
    return repo, stage, sha


def test_exact_tree_accepts_original_commit_bytes():
    with TemporaryDirectory() as temp:
        repo, stage, sha = repo_and_stage(Path(temp))
        assert verify(repo, sha, stage) == 0


def test_tree_and_annotated_tag_cannot_masquerade_as_assured_commit():
    # git ls-tree accepts a tree object and peels a tag, so a manifest-only
    # verifier incorrectly accepted either SHA before the provenance guard.
    # Everything is constructed in a disposable synthetic Git repository.
    with TemporaryDirectory() as temp:
        repo, stage, sha = repo_and_stage(Path(temp))
        tree_sha = git(repo, "rev-parse", f"{sha}^{{tree}}").decode().strip()
        git(repo, "tag", "-a", "synthetic-release", "-m", "synthetic only", sha)
        tag_sha = git(repo, "rev-parse", "refs/tags/synthetic-release").decode().strip()
        assert git(repo, "cat-file", "-t", tree_sha).strip() == b"tree"
        assert git(repo, "cat-file", "-t", tag_sha).strip() == b"tag"
        assert verify(repo, tree_sha, stage) != 0
        assert verify(repo, tag_sha, stage) != 0
        assert verify(repo, sha, stage) == 0


def test_git_archive_export_subst_changes_unsigned_bytes_and_is_refused():
    with TemporaryDirectory() as temp:
        repo, stage, sha = repo_and_stage(Path(temp), attrs="report.txt export-subst\n")
        assert (stage / "report.txt").read_bytes() != git(repo, "show", f"{sha}:report.txt")
        assert verify(repo, sha, stage) != 0


def test_git_archive_export_ignore_omission_is_refused():
    with TemporaryDirectory() as temp:
        repo, stage, sha = repo_and_stage(Path(temp), attrs="report.txt export-ignore\n")
        assert not (stage / "report.txt").exists()
        assert verify(repo, sha, stage) != 0


def test_extra_or_changed_stage_files_are_refused():
    with TemporaryDirectory() as temp:
        repo, stage, sha = repo_and_stage(Path(temp))
        (stage / "untracked-private-session.log").write_text("secret", encoding="utf-8")
        assert verify(repo, sha, stage) != 0
        (stage / "untracked-private-session.log").unlink()
        (stage / "assurance.html").write_text("fake badge", encoding="utf-8")
        assert verify(repo, sha, stage) != 0


def test_symlink_tree_metadata_and_wrong_commit_sha_refused():
    with TemporaryDirectory() as temp:
        repo, stage, sha = repo_and_stage(Path(temp))
        assert verify(repo, "not-a-commit", stage) != 0
        blob = git(repo, "hash-object", "-w", "--stdin", data=b"../outside").decode().strip()
        git(repo, "update-index", "--add", "--cacheinfo", f"120000,{blob},sneaky-link")
        git(repo, "commit", "-qm", "synthetic unsafe link")
        updated_sha = git(repo, "rev-parse", "HEAD").decode().strip()
        assert verify(repo, updated_sha, stage) != 0
        assert verify(repo, sha, stage) == 0


def test_workflow_requires_full_manifest_verification_and_mutation_refusal():
    workflow = yaml.safe_load((ROOT / ".github/workflows/assurance.yml").read_text(encoding="utf-8"))
    steps = workflow["jobs"]["assurance"]["steps"]
    stage = next(s for s in steps if s.get("name", "").startswith("Stage only committed"))
    run = stage["run"]
    guard = 'python scripts/assurance/verify_pages_archive.py --repo . --sha "$ASSURED_SHA" --stage "$dest"'
    assert run.count(guard) == 1
    assert run.index("git -c core.autocrlf=false archive") < run.index(guard)
    assert stage.get("if") == "vars.E156_PAGES_ACTIONS_READY == 'true'"
    upload = next(s for s in steps if s.get("name", "").startswith("Package exact"))
    assert steps.index(stage) < steps.index(upload)
    assert upload.get("with", {}).get("path") == "${{ runner.temp }}/e156-assured-pages"
    for mutation in (run.replace(guard, "echo bypass"), run.replace(guard, "true"),
                     run.replace(guard, "")):
        assert mutation.count(guard) != 1


def test_git_executable_mode_policy_with_deterministic_modes():
    # Portable negative controls do not rely on Windows chmod semantics.
    assert _mode_matches_git_index("100644", stat.S_IFREG | 0o644)
    assert not _mode_matches_git_index("100644", stat.S_IFREG | 0o755)
    assert _mode_matches_git_index("100755", stat.S_IFREG | 0o755)
    assert not _mode_matches_git_index("100755", stat.S_IFREG | 0o644)


def test_stage_execute_bit_mutation_is_not_exact_committed_source():
    with TemporaryDirectory() as temp:
        repo, stage, sha = repo_and_stage(Path(temp))
        assert verify(repo, sha, stage) == 0
        filename = stage / "report.txt"
        # The original verifier compared only this unchanged blob digest.
        blob_before = git(repo, "hash-object", str(filename))
        filename.chmod(filename.stat().st_mode | stat.S_IXUSR)
        assert git(repo, "hash-object", str(filename)) == blob_before
        if os.name == "posix":
            assert verify(repo, sha, stage) != 0
        else:
            # Production Pages staging is Linux; Windows still exercises the
            # portable matching policy without pretending chmod is POSIX.
            assert not _mode_matches_git_index("100644", stat.S_IFREG | 0o744)


def test_tracked_executable_passes_and_lost_exec_bit_refuses():
    with TemporaryDirectory() as temp:
        repo, stage, _ = repo_and_stage(Path(temp))
        git(repo, "update-index", "--chmod=+x", "report.txt")
        git(repo, "commit", "-qm", "synthetic tracked executable")
        sha = git(repo, "rev-parse", "HEAD").decode().strip()
        filename = stage / "report.txt"
        if os.name == "posix":
            filename.chmod(filename.stat().st_mode | stat.S_IXUSR)
            assert verify(repo, sha, stage) == 0
            filename.chmod(filename.stat().st_mode & ~0o111)
            assert verify(repo, sha, stage) != 0
        else:
            assert _mode_matches_git_index("100755", stat.S_IFREG | 0o755)
            assert not _mode_matches_git_index("100755", stat.S_IFREG | 0o644)

def test_unreadable_stage_subdirectory_cannot_be_silently_skipped(monkeypatch):
    # os.walk's default onerror=None silently omits an unreadable subtree.
    # A complete-looking file manifest must not pass if the stage cannot
    # be fully enumerated. Simulate EACCES identically on Windows and Linux.
    with TemporaryDirectory() as temp:
        repo, stage, sha = repo_and_stage(Path(temp))
        unreadable = stage / "extra-unreadable-directory"
        unreadable.mkdir()
        assert verify(repo, sha, stage) == 0  # control: ordinary enumeration
        original_scandir = os.scandir
        failed_calls = []

        def refuse_scandir(path):
            if Path(path) == unreadable:
                failed_calls.append(str(path))
                raise PermissionError("synthetic unreadable stage directory")
            return original_scandir(path)

        with monkeypatch.context() as patch:
            patch.setattr(os, "scandir", refuse_scandir)
            assert verify(repo, sha, stage) != 0
        assert failed_calls
        assert verify(repo, sha, stage) == 0  # restored positive control
