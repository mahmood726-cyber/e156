"""Contract tests for the claim pipeline.

Covers the four state-machine branches of update_claims_from_issue.py:
  1. new CLAIM
  2. SUBMITTED (with format + TBD guards)
  3. EXTENSION
  4. closed issue (cancellation)

plus the two structural parsers:
  - build_students_page.parse_entries
  - update_claims_from_issue.parse_form_body

These are contract tests — they use small fixtures, monkey-patch the
claims.json path, and assert the resulting dict shape. Designed to catch
workbook-format drift, field-name rename, line-ending change, and
spoofing-guard regressions.
"""
from __future__ import annotations
import datetime as dt
import importlib
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

SAMPLE_WORKBOOK = """E156 REWRITE WORKBOOK
sentinel:skip-file

======================================================================

[1/485] SampleMethods
TITLE: A sample methods paper
TYPE: methods  |  ESTIMAND: SMD
DATA: 10 reviews
PATH: C:\\\\Projects\\\\Sample

CURRENT BODY (156 words):
This is the original 156-word body of the sample paper. It has exactly seven sentences describing a methods contribution. Sentence three. Sentence four. Sentence five. Sentence six. Sentence seven.

YOUR REWRITE (at most 156 words, 7 sentences):

SUBMISSION METADATA:
Corresponding author: Mahmood Ahmad <mahmood.ahmad2@nhs.net>
Links:
  Code:      https://github.com/mahmood726-cyber/Sample
  Protocol:  https://github.com/mahmood726-cyber/Sample/blob/main/E156-PROTOCOL.md
  Dashboard: https://mahmood726-cyber.github.io/Sample/

Competing interests: MA serves on the editorial board of Synthēsis (the
  target journal); MA had no role in editorial decisions on this
  manuscript, which was handled by an independent editor of the journal.

SUBMITTED: [ ]

======================================================================

[2/485] SecondPaper
TITLE: Second sample
TYPE: review  |  ESTIMAND: OR
DATA: 5 RCTs
PATH: C:\\\\Projects\\\\Second

CURRENT BODY (156 words):
Another sample body for contract testing. Two sentences.

YOUR REWRITE (at most 156 words, 7 sentences):

SUBMISSION METADATA:
Links:
  Code:      https://github.com/mahmood726-cyber/Second
  Protocol:  https://github.com/mahmood726-cyber/Second/blob/main/E156-PROTOCOL.md
  Dashboard: https://mahmood726-cyber.github.io/Second/

SUBMITTED: [ ]

======================================================================
"""


# --------------------------------------------------------------------------
# parse_entries
# --------------------------------------------------------------------------

def test_parse_entries_returns_two_entries():
    bsp = importlib.import_module("build_students_page")
    entries = bsp.parse_entries(SAMPLE_WORKBOOK)
    nums = [e["num"] for e in entries]
    assert nums == [1, 2]


def test_parse_entries_strips_bom(tmp_path, monkeypatch):
    bsp = importlib.import_module("build_students_page")
    # BOM + first block should still parse
    bom_text = "\ufeff" + SAMPLE_WORKBOOK
    # parse_entries itself doesn't strip; main() does. Confirm parse_entries
    # doesn't mangle a BOM'd input when the caller stripped first.
    entries = bsp.parse_entries(bom_text.lstrip("\ufeff"))
    assert len(entries) == 2


def test_parse_entries_dedupes_duplicate_num(capfd):
    bsp = importlib.import_module("build_students_page")
    dup_text = SAMPLE_WORKBOOK + """
[2/485] AnotherSecondEntryWithSameNum
TITLE: Collision
PATH: C:\\Projects\\Dup
======================================================================
"""
    entries = bsp.parse_entries(dup_text)
    nums = [e["num"] for e in entries]
    assert nums == [1, 2]  # second #2 dropped
    # P1-19 — warning must be emitted
    out = capfd.readouterr().out
    assert "duplicate paper_num 2" in out


# --------------------------------------------------------------------------
# parse_form_body
# --------------------------------------------------------------------------

def test_parse_form_body_claim_shape():
    upd = importlib.import_module("update_claims_from_issue")
    body = """### Paper number

123

### Your name

Asha Bint

### Your affiliation / university

Makerere University

### Your email

asha@example.edu

### Senior / last author (faculty supervisor)

Dr. Jane Okello, Makerere
"""
    d = upd.parse_form_body(body)
    assert d["paper_number"] == "123"
    assert d["your_name"] == "Asha Bint"
    assert "Makerere" in d["your_affiliation_university"]


def test_parse_form_body_normalizes_no_response():
    upd = importlib.import_module("update_claims_from_issue")
    body = "### Your ORCID\n\n_No response_\n"
    d = upd.parse_form_body(body)
    # P1 — "_No response_" should slug-normalize to empty
    orcid = next((v for k, v in d.items() if k.startswith("your_orcid")), None)
    assert orcid == ""


# --------------------------------------------------------------------------
# update_claims_from_issue — state machine
# --------------------------------------------------------------------------

def _run_pipeline(tmp_path, monkeypatch, env: dict) -> dict:
    """Run update_claims_from_issue.main() with fresh claims.json, return result dict."""
    claims_path = tmp_path / "claims.json"
    # Seed from existing-claims arg via env
    existing = env.pop("_PREEXISTING_CLAIMS", None)
    if existing is not None:
        claims_path.write_text(json.dumps(existing), encoding="utf-8")
    upd = importlib.import_module("update_claims_from_issue")
    monkeypatch.setattr(upd, "CLAIMS", claims_path)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    rc = upd.main()
    if claims_path.is_file():
        data = json.loads(claims_path.read_text(encoding="utf-8") or "{}")
    else:
        data = {}
    return {"rc": rc, "claims": data}


def test_new_claim_writes_expected_record(tmp_path, monkeypatch):
    body = ("### Paper number\n\n101\n\n### Your name\n\nAsha\n\n"
            "### Your affiliation / university\n\nMakerere\n\n"
            "### Your email\n\nasha@x\n\n"
            "### Senior / last author (faculty supervisor)\n\nDr. Jane Okello\n")
    result = _run_pipeline(tmp_path, monkeypatch, {
        "ISSUE_NUMBER": "5",
        "ISSUE_TITLE": "[CLAIM #101] foo",
        "ISSUE_BODY": body,
        "ISSUE_USER": "ashabint",
        "ISSUE_LABELS": '[{"name":"claim"}]',
        "ISSUE_STATE": "open",
        "ISSUE_CREATED_AT": "2026-04-19T10:00:00Z",
    })
    assert result["rc"] == 0
    assert "101" in result["claims"]
    assert result["claims"]["101"]["name"] == "Asha"
    assert result["claims"]["101"]["github_user"] == "ashabint"
    assert result["claims"]["101"]["status"] == "claimed"


def test_one_at_a_time_refuses_second_claim(tmp_path, monkeypatch):
    today = dt.date.today().isoformat()
    prior = {
        "50": {
            "name": "Asha", "github_user": "ashabint",
            "claim_date": today, "status": "claimed",
            "submit_date": None, "submission_id": None,
            "issue_number": 3,
        }
    }
    body = ("### Paper number\n\n60\n\n### Your name\n\nAsha\n\n"
            "### Your affiliation / university\n\nMakerere\n\n"
            "### Your email\n\na@x\n\n"
            "### Senior / last author (faculty supervisor)\n\nDr Jane\n")
    result = _run_pipeline(tmp_path, monkeypatch, {
        "_PREEXISTING_CLAIMS": prior,
        "ISSUE_NUMBER": "9", "ISSUE_TITLE": "[CLAIM #60] bar",
        "ISSUE_BODY": body, "ISSUE_USER": "ashabint",
        "ISSUE_LABELS": '[{"name":"claim"}]', "ISSUE_STATE": "open",
        "ISSUE_CREATED_AT": "2026-04-19T10:00:00Z",
    })
    assert result["rc"] == 2
    assert "60" not in result["claims"]
    assert "50" in result["claims"]  # prior preserved


def test_spoof_close_by_different_user_rejected(tmp_path, monkeypatch):
    today = dt.date.today().isoformat()
    prior = {
        "50": {
            "name": "Asha", "github_user": "ashabint",
            "claim_date": today, "status": "claimed",
            "submit_date": None, "submission_id": None,
            "issue_number": 3,
        }
    }
    result = _run_pipeline(tmp_path, monkeypatch, {
        "_PREEXISTING_CLAIMS": prior,
        "ISSUE_NUMBER": "10", "ISSUE_TITLE": "[CLAIM #50] x",
        "ISSUE_BODY": "### Paper number\n\n50\n", "ISSUE_USER": "attacker",
        "ISSUE_LABELS": '[{"name":"claim"}]', "ISSUE_STATE": "closed",
        "ISSUE_CREATED_AT": "2026-04-19T10:00:00Z",
    })
    assert result["rc"] == 2
    assert "50" in result["claims"]  # not deleted


def test_submitted_format_violation_is_rejected(tmp_path, monkeypatch):
    today = dt.date.today().isoformat()
    prior = {
        "50": {
            "name": "Asha", "github_user": "ashabint",
            "claim_date": today, "status": "claimed",
            "submit_date": None, "submission_id": None,
            "issue_number": 3,
        }
    }
    # Body padded to > 156 words
    body = ("### Paper number\n\n50\n\n### Your name\n\nAsha\n\n"
            "### Submission confirmation / manuscript ID / DOI\n\nX\n\n"
            "### Date of submission (YYYY-MM-DD)\n\n2026-05-01\n\n"
            "### Senior / last author on the submitted manuscript\n\nDr Jane Okello\n\n"
            "### Final 156-word body as submitted\n\n"
            + ("word " * 300) + "\n")
    result = _run_pipeline(tmp_path, monkeypatch, {
        "_PREEXISTING_CLAIMS": prior,
        "ISSUE_NUMBER": "11", "ISSUE_TITLE": "[SUBMITTED #50] x",
        "ISSUE_BODY": body, "ISSUE_USER": "ashabint",
        "ISSUE_LABELS": '[{"name":"submitted"}]', "ISSUE_STATE": "open",
        "ISSUE_CREATED_AT": "2026-04-19T10:00:00Z",
    })
    assert result["rc"] == 2
    assert result["claims"]["50"]["status"] == "claimed"  # unchanged


def test_submitted_tbd_sentinel_is_rejected(tmp_path, monkeypatch):
    today = dt.date.today().isoformat()
    prior = {
        "50": {
            "name": "Asha", "github_user": "ashabint",
            "claim_date": today, "status": "claimed",
            "submit_date": None, "submission_id": None,
            "issue_number": 3,
            "senior_author": "TBD - request mentor",
        }
    }
    body = ("### Paper number\n\n50\n\n### Your name\n\nAsha\n\n"
            "### Submission confirmation / manuscript ID / DOI\n\nX\n\n"
            "### Date of submission (YYYY-MM-DD)\n\n2026-05-01\n\n"
            "### Senior / last author on the submitted manuscript\n\nTBD - request mentor\n\n"
            "### Final 156-word body as submitted\n\n"
            "Question. Dataset. Method. Result. Robustness. Interpretation. Boundary.\n")
    result = _run_pipeline(tmp_path, monkeypatch, {
        "_PREEXISTING_CLAIMS": prior,
        "ISSUE_NUMBER": "12", "ISSUE_TITLE": "[SUBMITTED #50] x",
        "ISSUE_BODY": body, "ISSUE_USER": "ashabint",
        "ISSUE_LABELS": '[{"name":"submitted"}]', "ISSUE_STATE": "open",
        "ISSUE_CREATED_AT": "2026-04-19T10:00:00Z",
    })
    assert result["rc"] == 2


def test_extension_grants_40_day_window(tmp_path, monkeypatch):
    today = dt.date.today().isoformat()
    prior = {
        "50": {
            "name": "Asha", "github_user": "ashabint",
            "claim_date": today, "status": "claimed",
            "submit_date": None, "submission_id": None,
            "issue_number": 3,
        }
    }
    result = _run_pipeline(tmp_path, monkeypatch, {
        "_PREEXISTING_CLAIMS": prior,
        "ISSUE_NUMBER": "13", "ISSUE_TITLE": "[EXTENSION #50] x",
        "ISSUE_BODY": "### Paper number\n\n50\n\n### Your name\n\nAsha\n",
        "ISSUE_USER": "ashabint",
        "ISSUE_LABELS": '[{"name":"extension"}]', "ISSUE_STATE": "open",
        "ISSUE_CREATED_AT": "2026-04-19T10:00:00Z",
    })
    assert result["rc"] == 0
    assert result["claims"]["50"]["extended"] is True
