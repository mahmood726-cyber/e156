"""Real Git-index negative canaries for privileged E156 generated-only commits.

Fixture tests, not a production master push, publication or signed ecosystem run.
"""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "scripts/assurance/refuse_unexpected_staged_changes.py"
spec = importlib.util.spec_from_file_location("e156_staged_guard", GUARD)
assert spec and spec.loader
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def _run(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _put(repo: Path, path: str, content: str) -> None:
    dest = repo / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")


def _fixture(tmp_path: Path) -> Path:
    repo = tmp_path / "isolated"
    repo.mkdir()
    _run(repo, "init", "-q")
    _run(repo, "config", "user.name", "CI Fixture")
    _run(repo, "config", "user.email", "fixture@example.invalid")
    for path in (
        "AGENTS.md", "rewrite-workbook.txt", "paper/protocol.md",
        "e156-submission/assurance.json", "doi-cache.json", "assurance.html",
    ):
        _put(repo, path, "original\n")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-qm", "fixture")
    return repo


def test_generated_only_stage_is_accepted(tmp_path):
    repo = _fixture(tmp_path)
    _put(repo, "doi-cache.json", "new evidence\n")
    _put(repo, "e156-submission/assurance.json", "new badge\n")
    _put(repo, "e156-submission/assurance.json.cosign.bundle", "new synthetic bundle\n")
    _put(repo, "assurance.html", "new dashboard\n")
    _run(repo, "add", "-A")
    assert guard.check(repo) == 0


def test_protected_human_records_and_unsafe_additions_refuse(tmp_path):
    for bad in ("AGENTS.md", "rewrite-workbook.txt", "paper/protocol.md", "paper/extra.html"):
        repo = _fixture(tmp_path / bad.replace("/", "_"))
        _put(repo, "doi-cache.json", "allowed\n")
        _put(repo, bad, "tampered\n")
        _run(repo, "add", "-A")
        assert guard.check(repo) == 2, bad


def test_deletions_refuse_even_of_generated_files(tmp_path):
    repo = _fixture(tmp_path)
    (repo / "assurance.html").unlink()
    _run(repo, "add", "-A")
    assert guard.check(repo) == 2


def test_missing_repository_refuses(tmp_path):
    assert guard.check(tmp_path / "absent") == 2


def test_production_workflow_runs_stage_guard_before_commit():
    text = (ROOT / ".github/workflows/assurance.yml").read_text(encoding="utf-8")
    snippet = "python scripts/assurance/refuse_unexpected_staged_changes.py --repo ."
    assert text.count(snippet) == 1
    assert text.index("git add -A") < text.index(snippet) < text.index("git commit -m")
