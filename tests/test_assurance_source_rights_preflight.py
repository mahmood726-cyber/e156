"""Fail-closed source-rights hold for E156's privileged production workflow.

No Synthesis permission manifest or private decision log is available. The
production job must stop before checkout, cache reads, DOI network traffic,
Sentinel article scanning, or publication artifacts. These mutation tests use
only the workflow YAML and do not authorize any article processing.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml


WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / ".github" / "workflows" / "assurance.yml"
)


def require_precheckout_hold(workflow: str) -> None:
    jobs = yaml.safe_load(workflow)["jobs"]
    assert set(jobs) == {"assurance", "deploy-pages"}
    assurance = jobs["assurance"]
    assert "if" not in assurance and "continue-on-error" not in assurance
    steps = assurance["steps"]
    assert len(steps) >= 2
    hold = steps[0]
    assert "uses" not in hold and "if" not in hold
    assert "continue-on-error" not in hold
    assert hold.get("shell") == "bash"
    assert "SOURCE_RIGHTS_HOLD" in hold["run"]
    assert "exit 1" in hold["run"]
    assert steps[1]["uses"].startswith("actions/checkout@")
    assert jobs["deploy-pages"].get("needs") == "assurance"


def test_production_refuses_source_processing_before_checkout():
    require_precheckout_hold(WORKFLOW.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "mutation",
    [
        lambda src: src.replace("          exit 1", "          echo proceed", 1),
        lambda src: src.replace(
            "      - name: SOURCE_RIGHTS_HOLD", "      - name: renamed", 1
        ).replace("SOURCE_RIGHTS_HOLD: no reviewed", "unreviewed", 1),
        lambda src: src.replace(
            "      - name: SOURCE_RIGHTS_HOLD",
            "      - name: SOURCE_RIGHTS_HOLD\n        if: false",
            1,
        ),
        lambda src: src.replace(
            "      - name: SOURCE_RIGHTS_HOLD",
            "      - name: SOURCE_RIGHTS_HOLD\n        continue-on-error: true",
            1,
        ),
        lambda src: src.replace(
            "      - uses: actions/checkout@",
            "      - uses: actions/checkout@",
            1,
        ).replace(
            "    steps:\n      # Run before checkout",
            "    steps:\n      - uses: actions/checkout@v4\n      # Run before checkout",
            1,
        ),
    ],
)
def test_source_rights_hold_bypass_mutations_are_refused(mutation):
    source = WORKFLOW.read_text(encoding="utf-8")
    planted = mutation(source)
    assert planted != source
    with pytest.raises(AssertionError):
        require_precheckout_hold(planted)
