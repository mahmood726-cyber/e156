"""Tests for the public assurance dashboard generator (GitHub Pages)."""
from __future__ import annotations

import importlib
import json
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
        b["signature"] = "HMAC-SHA256:abc"
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
