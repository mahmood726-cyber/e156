"""Tests for the public assurance dashboard generator (GitHub Pages)."""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT, ROOT / "scripts"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

bpd = importlib.import_module("assurance.build_pages_dashboard")


def _badge(tier="silver", signed=True, name="demo", checks=None):
    b = {"tier": tier, "project_name": name,
         "checks": checks or {"citation_cascade": "pass", "claim_language": "pass"}}
    if signed:
        b["_signed"] = True  # verified runtime result, NOT an HMAC mark
    return b


def test_renders_tiers_and_names():
    out = bpd.build_dashboard_html([_badge(tier="gold", name="alpha"), _badge(tier="none", name="beta")])
    assert "Gold" in out and "Unrated" in out
    assert "alpha" in out and "beta" in out
    assert out.startswith("<!doctype html>")


def test_signed_indicator():
    # the footer legend always shows the lock glyph, so compare row counts:
    # a signed badge adds one more lock (its row) than an unsigned one.
    signed = bpd.build_dashboard_html([_badge(signed=True)])
    unsigned = bpd.build_dashboard_html([_badge(signed=False)])
    assert signed.count("&#128274;") == unsigned.count("&#128274;") + 1


def test_escapes_xss_in_name():
    out = bpd.build_dashboard_html([_badge(name="<script>alert(1)</script>")])
    assert "<script>alert(1)</script>" not in out
    assert "&lt;script&gt;" in out


def test_collect_badges(tmp_path):
    sub = tmp_path / "e156-submission"
    sub.mkdir()
    (sub / "assurance.json").write_text(json.dumps({"tier": "bronze", "checks": {}}), encoding="utf-8")
    (tmp_path / "assurance.json").write_text(json.dumps({"tier": "none", "checks": {}}), encoding="utf-8")
    badges = bpd.collect_badges(tmp_path)
    assert len(badges) == 2
    assert {b["tier"] for b in badges} == {"bronze", "none"}


def test_cli_writes_html(tmp_path):
    (tmp_path / "assurance.json").write_text(json.dumps({"tier": "silver", "checks": {}, "signature": "HMAC-SHA256:x"}), encoding="utf-8")
    bpd.main(["--repo", str(tmp_path)])
    out = tmp_path / "assurance.html"
    assert out.is_file()
    assert "Silver" in out.read_text(encoding="utf-8")

def test_unverified_hmac_is_not_an_authenticated_lock():
    legacy = {"tier": "silver", "project_name": "old", "signature": "HMAC-SHA256:forged"}
    original = bpd.build_dashboard_html([legacy])
    unsigned = bpd.build_dashboard_html([{"tier": "silver", "project_name": "old"}])
    assert original.count("&#128274;") == unsigned.count("&#128274;")


def test_dashboard_refuses_claiming_authenticated_without_bundle(tmp_path):
    (tmp_path / "assurance.json").write_text('{"tier":"bronze"}', encoding="utf-8")
    assert bpd.main(["--repo", str(tmp_path), "--require-keyless-verified"]) == 2
    assert not (tmp_path / "assurance.html").exists()


def test_authenticated_dashboard_requires_positive_verifier(tmp_path, monkeypatch):
    from assurance import verify_sigstore_badges
    (tmp_path / "assurance.json").write_text('{"tier":"bronze"}', encoding="utf-8")
    monkeypatch.setattr(verify_sigstore_badges, "verify", lambda root: 0)
    assert bpd.main(["--repo", str(tmp_path), "--require-keyless-verified"]) == 0
    assert (tmp_path / "assurance.html").read_text(encoding="utf-8").count("&#128274;") == 2


def test_direct_cli_keyless_gate_imports_verifier_before_refusal(tmp_path):
    """The production workflow executes this file as a script, not a package.

    Import-based tests alone missed a ModuleNotFoundError in the mandatory
    --require-keyless-verified path. A missing real bundle must refuse safely.
    """
    (tmp_path / "assurance.json").write_text('{"tier":"bronze"}', encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/assurance/build_pages_dashboard.py"),
         "--repo", str(tmp_path), "--require-keyless-verified"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "REFUSED: dashboard cannot claim authenticated badges" in result.stderr
    assert "ModuleNotFoundError" not in result.stderr
    assert not (tmp_path / "assurance.html").exists()
