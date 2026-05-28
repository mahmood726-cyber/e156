"""Tests for the hardened multi-persona review gate (Track D)."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT, ROOT / "scripts"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

rv = importlib.import_module("review_e156")


def _complete(verdict="pass", note="A substantive review note about the analysis and its limitations.",
              reviewer_prefix="desk"):
    personas = {
        name: {
            "verdict": verdict, "notes": note,
            "reviewer_id": f"{reviewer_prefix}-{name}", "signed_at": "2026-05-28",
        }
        for name in rv.REQUIRED_PERSONAS
    }
    return {"reviewed_at": "2026-05-28", "personas": personas}


def test_complete_review_passes():
    s = rv.summarize_review(_complete())
    assert s["ok"] is True
    assert s["gate"] == "pass"


def test_seeded_template_does_not_pass():
    # A freshly seeded template (desk ids prefilled) must NOT read as approval.
    personas = {
        name: rv.build_persona_stub(name, starter_mode=False, seed_reviewers=True)
        for name in rv.REQUIRED_PERSONAS
    }
    review = {"reviewed_at": "", "personas": personas}
    s = rv.summarize_review(review)
    assert s["gate"] == "block"
    assert s["ok"] is False
    assert all(p["verdict"] == "revise" for p in personas.values())   # never default pass
    assert all(p["signed_at"] == "" for p in personas.values())       # no auto-signoff


def test_weak_notes_block():
    s = rv.summarize_review(_complete(note="ok"))
    assert len(s["weak_notes"]) == len(rv.REQUIRED_PERSONAS)
    assert s["gate"] == "block"


def test_self_review_is_blocked():
    review = _complete()
    review["personas"]["clinician"]["reviewer_id"] = "mahmood@example.com"
    s = rv.summarize_review(review, author="Mahmood@Example.com")  # case-insensitive
    assert "clinician" in s["conflicted_reviewers"]
    assert s["gate"] == "block"


def test_one_revise_is_revise_gate():
    review = _complete()
    review["personas"]["skeptic"]["verdict"] = "revise"
    s = rv.summarize_review(review)
    assert s["gate"] == "revise"
    assert s["ok"] is True


def test_one_block_is_block_gate():
    review = _complete()
    review["personas"]["statistician"]["verdict"] = "block"
    s = rv.summarize_review(review)
    assert s["gate"] == "block"


def test_placeholder_desk_labels_block():
    # using the seed desk labels as the reviewer ids is not a real review
    review = _complete()
    for name in rv.REQUIRED_PERSONAS:
        review["personas"][name]["reviewer_id"] = rv.DEFAULT_REVIEWER_IDS[name]
    s = rv.summarize_review(review)
    assert len(s["placeholder_reviewers"]) == len(rv.REQUIRED_PERSONAS)
    assert s["gate"] == "block"


def test_duplicate_reviewer_ids_block():
    # one person filling all five desks with the same id
    review = _complete()
    for name in rv.REQUIRED_PERSONAS:
        review["personas"][name]["reviewer_id"] = "one-person"
    s = rv.summarize_review(review)
    assert s["duplicate_reviewers"]
    assert s["gate"] == "block"
