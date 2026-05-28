"""Tests for the badge-signature enforcement gate (verify_badges.py)."""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT, ROOT / "scripts", ROOT / "scripts" / "assurance"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

vb = importlib.import_module("assurance.verify_badges")
sb = importlib.import_module("assurance.sign_badge")

KEY = b"test-key-not-for-production"


def _badge():
    return {"tier": "bronze", "checks": {"citation_cascade": "pass"}, "version": 1}


def _write(path: Path, badge: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(badge), encoding="utf-8")


def test_valid_signature_passes(tmp_path):
    _write(tmp_path / "e156-submission" / "assurance.json", sb.sign(_badge(), KEY))
    invalid, unsigned = vb.verify_repo(tmp_path, require_signed=True, key=KEY)
    assert invalid == [] and unsigned == []


def test_forged_badge_is_invalid(tmp_path):
    signed = sb.sign(_badge(), KEY)
    signed["tier"] = "gold"  # tamper after signing
    _write(tmp_path / "assurance.json", signed)
    invalid, _ = vb.verify_repo(tmp_path, require_signed=False, key=KEY)
    assert len(invalid) == 1


def test_unsigned_only_fails_with_require_signed(tmp_path):
    _write(tmp_path / "assurance.json", _badge())  # no signature
    invalid, unsigned = vb.verify_repo(tmp_path, require_signed=True, key=KEY)
    assert invalid == [] and len(unsigned) == 1


def test_main_returns_nonzero_on_forgery(tmp_path, monkeypatch):
    signed = sb.sign(_badge(), KEY)
    signed["checks"]["citation_cascade"] = "fail"  # tamper
    _write(tmp_path / "assurance.json", signed)
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEY", KEY.decode())
    assert vb.main(["--repo", str(tmp_path)]) == 1


def test_main_passes_clean(tmp_path, monkeypatch):
    _write(tmp_path / "assurance.json", sb.sign(_badge(), KEY))
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEY", KEY.decode())
    assert vb.main(["--repo", str(tmp_path), "--require-signed"]) == 0
