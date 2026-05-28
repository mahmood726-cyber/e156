"""Tests for the assurance badge signer/verifier (Track C)."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT, ROOT / "scripts"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

sb = importlib.import_module("assurance.sign_badge")

KEY = b"test-key-not-for-production"


def _fresh() -> dict:
    return {
        "tier": "silver",
        "checks": {
            "citation_cascade": "pass", "claim_language": "pass",
            "data_file_present": "pass", "code_runs": "pass",
            "dashboard_match": "pass", "analysis_rerun": "not-run",
            "external_review": "not-run",
        },
        "version": 1,
    }


def test_sign_then_verify():
    signed = sb.sign(_fresh(), KEY)
    assert signed["signature"].startswith("HMAC-SHA256:")
    assert "signed_at" in signed
    assert sb.verify(signed, KEY) is True


def test_tampering_with_tier_breaks_signature():
    signed = sb.sign(_fresh(), KEY)
    signed["tier"] = "gold"  # forge the tier after signing
    assert sb.verify(signed, KEY) is False


def test_tampering_with_a_check_breaks_signature():
    signed = sb.sign(_fresh(), KEY)
    signed["checks"]["external_review"] = "pass"
    assert sb.verify(signed, KEY) is False


def test_wrong_key_does_not_verify():
    signed = sb.sign(_fresh(), KEY)
    assert sb.verify(signed, b"a-different-key") is False


def test_unsigned_badge_does_not_verify():
    assert sb.verify(_fresh(), KEY) is False


def test_signature_is_deterministic_over_content():
    assert sb.compute_signature(_fresh(), KEY) == sb.compute_signature(_fresh(), KEY)


def test_signing_is_idempotent_over_content():
    once = sb.sign(_fresh(), KEY)
    twice = sb.sign(once, KEY)  # re-sign an already-signed badge
    assert once["signature"] == twice["signature"]  # sig fields excluded from payload
    assert sb.verify(twice, KEY) is True


def test_get_key_from_env(monkeypatch):
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEY", "env-secret")
    assert sb.get_key() == b"env-secret"


def test_get_key_from_keyfile(monkeypatch, tmp_path):
    monkeypatch.delenv("E156_ASSURANCE_HMAC_KEY", raising=False)
    kf = tmp_path / "k.key"
    kf.write_bytes(b"file-secret\n")
    monkeypatch.setenv("E156_ASSURANCE_HMAC_KEYFILE", str(kf))
    assert sb.get_key() == b"file-secret"  # whitespace stripped


def test_get_key_fails_closed(monkeypatch, tmp_path):
    monkeypatch.delenv("E156_ASSURANCE_HMAC_KEY", raising=False)
    monkeypatch.delenv("E156_ASSURANCE_HMAC_KEYFILE", raising=False)
    monkeypatch.setattr(sb, "DEFAULT_KEYFILE", tmp_path / "does-not-exist.key")
    with pytest.raises(sb.MissingKeyError):
        sb.get_key()
