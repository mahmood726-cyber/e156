"""Synthetic contract tests for the production publication-processing hold.

The PR-only assurance corpus may run on synthetic fixtures. Production E156
must not access DOI networks, read publication caches or replay article data
before a reviewed operation-specific Synthesis source-rights gate exists.
This test DOES NOT approve any publication access or replace that gate.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml


WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / ".github" / "workflows" / "assurance.yml"
)


def require_hold_before_production_processing(workflow: str) -> None:
    jobs = yaml.safe_load(workflow)["jobs"]
    preflight = jobs["source-rights-preflight"]
    assert "if" not in preflight, "source-rights hold cannot be conditional"
    assert preflight["permissions"] == {"contents": "read"}
    assert "continue-on-error" not in preflight
    steps = preflight["steps"]
    assert len(steps) == 1, "no checkout, cache read or acquisition before hold"
    refusal = steps[0]
    assert refusal.get("shell") == "bash"
    assert "uses" not in refusal and "if" not in refusal
    assert "continue-on-error" not in refusal
    run = refusal["run"]
    assert "SOURCE_RIGHTS_HOLD" in run
    assert "exit 1" in run, "hold must stop before processing"
    assurance = jobs["assurance"]
    assert assurance.get("needs") == "source-rights-preflight"
    assert "if" not in assurance, "no alternate assurance bypass"
    assert jobs["deploy-pages"].get("needs") == "assurance"


def test_production_assurance_requires_failing_rights_preflight():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    require_hold_before_production_processing(workflow)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda text: text.replace("needs: source-rights-preflight", ""),
        lambda text: text.replace("exit 1", "echo 'continue without review'"),
        lambda text: text.replace("      contents: read\n    steps:", "      contents: write\n    steps:", 1),
        lambda text: text.replace(
            "  source-rights-preflight:\n",
            "  source-rights-preflight:\n    if: false\n",
            1,
        ),
        lambda text: text.replace(
            "  assurance:\n    needs: source-rights-preflight",
            "  assurance:\n    needs: source-rights-preflight\n    if: always()",
            1,
        ),
    ],
)
def test_mutated_unsafe_gate_cannot_pass_contract(mutation):
    workflow = WORKFLOW.read_text(encoding="utf-8")
    weakened = mutation(workflow)
    assert weakened != workflow
    with pytest.raises((AssertionError, KeyError)):
        require_hold_before_production_processing(weakened)
