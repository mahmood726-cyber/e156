"""Published locations are portable; build destinations remain local."""
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import build_assurance_jsons as baj
from scripts.assurance import build_pages_dashboard as dashboard


def assert_portable(value, temporary_root):
    if isinstance(value, dict):
        for child in value.values():
            assert_portable(child, temporary_root)
    elif isinstance(value, list):
        for child in value:
            assert_portable(child, temporary_root)
    elif isinstance(value, str):
        assert not PurePosixPath(value).is_absolute(), value
        assert not PureWindowsPath(value).is_absolute(), value
        assert str(temporary_root) not in value
        assert temporary_root.as_posix() not in value


def test_build_assurance_tracked_publication_paths():
    root = Path(__file__).resolve().parents[1]
    paths = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=root
    ).decode("utf-8").split("\0")
    artifacts = [root / p for p in paths if p and (
        Path(p).name in ("assurance.json", "doi-cache.json")
        or p.endswith(".cosign.bundle")
    )]
    assert artifacts
    for artifact in artifacts:
        assert_portable(json.loads(artifact.read_text(encoding="utf-8")), root)


@pytest.mark.parametrize("mode", ["here", "workbook"])
@pytest.mark.parametrize("bundle_location", ["inside", "outside"])
def test_build_assurance_published_paths(tmp_path, monkeypatch, mode, bundle_location):
    repo = tmp_path / "capsule"
    sub = repo / "e156-submission"
    sub.mkdir(parents=True)
    assert repo.is_absolute()
    for filename in ("sentinel-findings.jsonl", "STUCK_FAILURES.jsonl"):
        (repo / filename).write_text("", encoding="utf-8")
    bundle = (repo if bundle_location == "inside" else tmp_path) / "bundle.json"
    bundle.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(baj, "_BUNDLE_INDEX", {"demo": bundle})
    entry = {"num": 1, "name": "demo", "path": str(repo),
             "body": "", "pages_url": ""}
    monkeypatch.setattr(baj, "iter_workbook_entries", lambda: iter([entry]))
    # Workbook output must still target the capsule, not the process cwd.
    monkeypatch.chdir(repo if mode == "here" else tmp_path)
    assert baj.main(["--here", "demo"] if mode == "here" else []) == 0
    output = sub / "assurance.json"
    blob = json.loads(output.read_text(encoding="utf-8"))
    assert_portable(blob, tmp_path)
    assert blob["local_path"] == "."
    assert blob["evidence"]["sentinel_findings"] == "sentinel-findings.jsonl"
    assert blob["evidence"]["stuck_failures"] == "STUCK_FAILURES.jsonl"
    if mode == "workbook" and bundle_location == "inside":
        assert blob["evidence"]["overmind_bundle"] == "bundle.json"
    else:
        assert "overmind_bundle" not in blob["evidence"]
    badges = dashboard.collect_badges(repo)
    assert badges[0]["_rel"] == "e156-submission/assurance.json"
    html = dashboard.build_dashboard_html(badges)
    assert "demo" in html
    assert str(tmp_path) not in html
    assert tmp_path.as_posix() not in html
