"""Publication-gate regressions: no unkeyed or vacuous green badge signings."""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for folder in (ROOT / "scripts", ROOT / "scripts" / "assurance"):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))

publisher = importlib.import_module("assurance.publish_hmac_badges")
signer = importlib.import_module("assurance.sign_badge")
verifier = importlib.import_module("assurance.verify_badges")


def _badge(path: Path, *, data=None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"tier": "bronze", "checks": {"readiness": "not-tested"}}
                               if data is None else data), encoding="utf-8")
    return path


def test_missing_ci_secret_refuses_even_with_keyfile(tmp_path, monkeypatch):
    _badge(tmp_path / "assurance.json")
    keyfile = tmp_path / "fallback-secret.key"
    keyfile.write_text("do-not-use", encoding="utf-8")
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEYFILE", str(keyfile))
    monkeypatch.delenv("E156_ASSURANCE_HMAC_KEY", raising=False)
    assert publisher.publish(tmp_path) == 2
    assert "signature" not in json.loads((tmp_path / "assurance.json").read_text())


def test_blank_ci_secret_refuses(tmp_path, monkeypatch):
    _badge(tmp_path / "assurance.json")
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEY", "   ")
    assert publisher.publish(tmp_path) == 2


def test_no_badges_refuses(tmp_path, monkeypatch):
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEY", "test-ci-secret")
    assert publisher.publish(tmp_path) == 2


def test_badges_only_inside_git_are_not_signed(tmp_path, monkeypatch):
    _badge(tmp_path / ".git" / "assurance.json")
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEY", "test-ci-secret")
    assert publisher.publish(tmp_path) == 2


def test_malformed_second_badge_refuses_before_mutating_first(tmp_path, monkeypatch):
    first = _badge(tmp_path / "a" / "assurance.json")
    second = tmp_path / "b" / "assurance.json"
    second.parent.mkdir(parents=True)
    second.write_text("{invalid", encoding="utf-8")
    before = first.read_bytes()
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEY", "test-ci-secret")
    assert publisher.publish(tmp_path) == 2
    assert first.read_bytes() == before


def test_non_object_json_refuses(tmp_path, monkeypatch):
    _badge(tmp_path / "assurance.json", data=["not a badge"])
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEY", "test-ci-secret")
    assert publisher.publish(tmp_path) == 2


def test_signs_and_verifies_multiple_real_hmac_badges(tmp_path, monkeypatch):
    first = _badge(tmp_path / "a" / "assurance.json")
    second = _badge(tmp_path / "b" / "assurance.json")
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEY", "test-ci-secret")
    assert publisher.main(["--repo", str(tmp_path)]) == 0
    for path in (first, second):
        signed = json.loads(path.read_text(encoding="utf-8"))
        assert signed["signature"].startswith("HMAC-SHA256:")
        assert signer.verify(signed, b"test-ci-secret")
        assert not signer.verify(signed, b"wrong-key")
    assert verifier.verify_repo(tmp_path, True, b"test-ci-secret") == ([], [])


def test_missing_repo_root_refuses(tmp_path, monkeypatch):
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEY", "test-ci-secret")
    assert publisher.publish(tmp_path / "does-not-exist") == 2
