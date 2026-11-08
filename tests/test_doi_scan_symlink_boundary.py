# sentinel:skip-file — fabricated DOI strings for synthetic scanner tests.
"""Guard DOI scanner filesystem containment before any file content is read.

These use only temporary synthetic material and do not authorize processing
scientific publications or bypass the separate source-rights gate.
"""
from __future__ import annotations

import importlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
for parent in (ROOT, ROOT / "scripts"):
    if str(parent) not in sys.path:
        sys.path.insert(0, str(parent))
dr = importlib.import_module("assurance.doi_resolver")


def test_synthetic_outside_file_symlink_is_never_scanned(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    outside = tmp_path / "external-synthetic.md"
    outside.write_text("doi: 10.9999/external-synthetic\n", encoding="utf-8")
    alias = repo / "linked.md"
    try:
        alias.symlink_to(outside)
    except (OSError, NotImplementedError):
        # Windows workers may lack symlink privileges. The same classifier
        # branch is exercised with an explicitly marked synthetic path.
        alias.write_text(outside.read_text(encoding="utf-8"), encoding="utf-8")
        real = Path.is_symlink
        monkeypatch.setattr(Path, "is_symlink",
                            lambda self: self == alias or real(self))
    normal = repo / "normal.md"
    normal.write_text("doi: 10.9999/normal-synthetic\n", encoding="utf-8")
    assert dr.scan_repo_dois(repo) == {"10.9999/normal-synthetic"}


def test_synthetic_symlinked_parent_directory_is_excluded(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    nested = repo / "linked-dir"
    nested.mkdir(parents=True)
    (nested / "synthetic.json").write_text(
        '{"metadata":"see doi: 10.9999/nested-synthetic"}', encoding="utf-8"
    )
    (repo / "normal.json").write_text(
        '{"metadata":"see doi: 10.9999/normal-synthetic"}', encoding="utf-8"
    )
    # Simulate traversal on a platform/version that yields a symlinked directory
    # without requiring SeCreateSymbolicLinkPrivilege on Windows.
    real = Path.is_symlink
    monkeypatch.setattr(Path, "is_symlink",
                        lambda self: self == nested or real(self))
    assert dr.scan_repo_dois(repo) == {"10.9999/normal-synthetic"}


def test_normal_files_and_skip_marker_keep_existing_contract(tmp_path):
    (tmp_path / "ordinary.txt").write_text(
        "doi: 10.9999/normal-synthetic\n", encoding="utf-8"
    )
    (tmp_path / "negative-fixture.md").write_text(
        "sentinel:skip-file\ndoi: 10.9999/skip-synthetic\n", encoding="utf-8"
    )
    assert dr.scan_repo_dois(tmp_path) == {"10.9999/normal-synthetic"}
