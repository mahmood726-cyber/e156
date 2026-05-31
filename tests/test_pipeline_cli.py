"""Smoke tests for the capsule-pipeline CLIs.

Network-free and fast: they confirm each tool parses and exposes --help, that the
injectors round-trip and fail closed, that the capsule carries every live-data
marker, and that the committed provenance + pipeline config are well-formed. The
fetch tools (which need the network) are exercised only via --help here.
"""
import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
DATA = ROOT / "data"
CAPSULE = ROOT / "flagship" / "sglt2-hf-capsule.html"

CLIS = [
    "register_protocol.py", "fetch_ctgov.py", "fetch_pubmed.py", "fetch_openalex.py",
    "inject_screening.py", "inject_extraction.py", "run_pipeline.py",
]


def run(*args, **kw):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, timeout=60, **kw)


@pytest.mark.parametrize("cli", CLIS)
def test_cli_parses(cli):
    ast.parse((SCRIPTS / cli).read_text(encoding="utf-8"))


@pytest.mark.parametrize("cli", CLIS)
def test_cli_help(cli):
    r = run(SCRIPTS / cli, "--help")
    assert r.returncode == 0, r.stderr
    assert "usage" in (r.stdout + r.stderr).lower()


def _mini_capsule(tmp_path, start, end):
    cap = tmp_path / "cap.html"
    cap.write_text("<html><script>const X=%s{}%s;</script></html>" % (start, end), encoding="utf-8")
    return cap


def test_inject_screening_roundtrip(tmp_path):
    cap = _mini_capsule(tmp_path, "/*SCREEN_START*/", "/*SCREEN_END*/")
    dec = tmp_path / "d.json"
    dec.write_text(json.dumps({"decisions": {"NCT00000000": {"decision": "include", "reason": "ok", "confidence": 0.9}}}), encoding="utf-8")
    r = run(SCRIPTS / "inject_screening.py", "--decisions", dec, "--capsule", cap)
    assert r.returncode == 0, r.stderr
    out = cap.read_text(encoding="utf-8")
    assert '"NCT00000000"' in out and "/*SCREEN_START*/{}" not in out


def test_inject_extraction_roundtrip(tmp_path):
    cap = _mini_capsule(tmp_path, "/*EXTRACT_START*/", "/*EXTRACT_END*/")
    ex = tmp_path / "e.json"
    ex.write_text(json.dumps({"extractions": {"NCT00000000": {"fields": [{"k": "N", "v": "100", "snip": "n=100", "c": 0.9}]}}}), encoding="utf-8")
    r = run(SCRIPTS / "inject_extraction.py", "--extraction", ex, "--capsule", cap)
    assert r.returncode == 0, r.stderr
    assert '"N"' in cap.read_text(encoding="utf-8")


def test_inject_fail_closed_missing_markers(tmp_path):
    cap = tmp_path / "c.html"
    cap.write_text("<html>no markers</html>", encoding="utf-8")
    dec = tmp_path / "d.json"
    dec.write_text(json.dumps({"decisions": {"NCT00000000": {"decision": "include", "reason": "x", "confidence": 0.5}}}), encoding="utf-8")
    r = run(SCRIPTS / "inject_screening.py", "--decisions", dec, "--capsule", cap)
    assert r.returncode != 0


def test_inject_fail_closed_missing_file(tmp_path):
    cap = _mini_capsule(tmp_path, "/*SCREEN_START*/", "/*SCREEN_END*/")
    r = run(SCRIPTS / "inject_screening.py", "--decisions", tmp_path / "nope.json", "--capsule", cap)
    assert r.returncode != 0


def test_inject_fail_closed_bad_decision(tmp_path):
    cap = _mini_capsule(tmp_path, "/*SCREEN_START*/", "/*SCREEN_END*/")
    dec = tmp_path / "d.json"
    dec.write_text(json.dumps({"decisions": {"X": {"decision": "maybe", "reason": "x", "confidence": 0.5}}}), encoding="utf-8")
    r = run(SCRIPTS / "inject_screening.py", "--decisions", dec, "--capsule", cap)
    assert r.returncode != 0


def test_capsule_has_all_live_markers():
    html = CAPSULE.read_text(encoding="utf-8")
    for m in ["CTGOV_START", "PUBMED_START", "OPENALEX_START", "SCREEN_START", "EXTRACT_START", "PROTOREG_START"]:
        assert m in html, "capsule missing marker " + m


@pytest.mark.parametrize("fn", [
    "ctgov-records.json", "pubmed-records.json", "openalex-records.json",
    "screening-decisions.json", "extraction-live.json",
])
def test_provenance_json_valid(fn):
    json.loads((DATA / fn).read_text(encoding="utf-8"))


def test_pipeline_config_valid():
    cfg = json.loads((ROOT / "pipelines" / "sglt2-hf.json").read_text(encoding="utf-8"))
    assert cfg.get("capsule") and cfg.get("ncts") and cfg.get("pmid_map")


def test_run_pipeline_dryrun_local_steps():
    # screening + extraction only -> no network, just injector dry-runs
    r = run(SCRIPTS / "run_pipeline.py", "--config", ROOT / "pipelines" / "sglt2-hf.json",
            "--only", "screening,extraction", "--dry-run", cwd=ROOT)
    assert r.returncode == 0, r.stderr
    assert "complete" in (r.stdout + r.stderr).lower()
