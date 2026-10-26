"""Fail-closed, source-level checks for Sentinel coverage of published artifacts.

These tests check the production workflow declaration and injected negative
mutations. They do NOT execute a privileged workflow, invoke live Sentinel,
authenticate releases, or certify a complete ecosystem canary.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/assurance.yml"
BUILD = "Build the public assurance dashboard (served by existing Pages)"
RESCAN = "Sentinel rescan generated publication artifacts (hard gate)"
PUBLISH = "Commit refreshed cache, badges, signatures, dashboard"
COMMAND = 'PYTHONPATH="$SENTINEL_ROOT" python -m sentinel scan --repo .'


def publication_gate_problems(steps: list[dict]) -> list[str]:
    if not isinstance(steps, list):
        return ["missing workflow steps"]
    names = [step.get("name") if isinstance(step, dict) else None for step in steps]
    for required in (BUILD, RESCAN, PUBLISH):
        if names.count(required) != 1:
            return [f"missing or duplicated publication stage: {required}"]
    builder = names.index(BUILD)
    final_scan = names.index(RESCAN)
    publisher = names.index(PUBLISH)
    problems = []
    if builder >= final_scan or final_scan != publisher - 1:
        problems.append("Sentinel must run after dashboard generation and immediately before publication")
    step = steps[final_scan]
    # No conditions, continue-on-error, bypass env, or substitute commands.
    if step != {"name": RESCAN, "run": COMMAND}:
        problems.append("Sentinel publication scan must be mandatory and unmodified")
    return problems


def _production_steps() -> list[dict]:
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    return data["jobs"]["assurance"]["steps"]


def test_real_workflow_has_final_mandatory_sentinel_gate():
    assert publication_gate_problems(_production_steps()) == []


def test_missing_skipped_bypassed_or_reordered_final_scan_is_refused():
    baseline = _production_steps()
    assert publication_gate_problems(baseline) == []

    for defect in (
        "missing", "duplicate", "early", "conditional", "silent-failure",
        "bypass-env", "no-scan", "post-scan-mutation"
    ):
        steps = deepcopy(baseline)
        at = next(i for i, step in enumerate(steps) if step.get("name") == RESCAN)
        if defect == "missing":
            steps.pop(at)
        elif defect == "duplicate":
            steps.insert(at, deepcopy(steps[at]))
        elif defect == "early":
            steps.insert(0, steps.pop(at))
        elif defect == "conditional":
            steps[at]["if"] = "false"
        elif defect == "silent-failure":
            steps[at]["continue-on-error"] = True
        elif defect == "bypass-env":
            steps[at]["env"] = {"SENTINEL_BYPASS": "1"}
        elif defect == "no-scan":
            steps[at]["run"] = 'echo "Sentinel skipped"'
        elif defect == "post-scan-mutation":
            steps.insert(at + 1, {"name": "Unscanned artifact mutation", "run": "touch assurance.json"})
        assert publication_gate_problems(steps), f"Accepted unsafe workflow: {defect}"
