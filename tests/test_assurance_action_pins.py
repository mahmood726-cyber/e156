"""Lock all third-party Actions in E156's read-only and privileged assurance jobs.

The expected commits were resolved from the upstream GitHub major-version refs
and their commits' GitHub verification records on 26 October 2026. A fixed
commit prevents mutable-tag drift; it is NOT an independent release attestation,
a binary/archive signature, or a full-system canary.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
ACTION_PINS = {
    "actions/checkout": "11d5960a326750d5838078e36cf38b85af677262",
    "actions/setup-python": "a26af69be951a213d495a4c3e4e4022e16d87065",
    "sigstore/cosign-installer": "398d4b0eeef1380460a10c8013a76f728fb906ac",
    "actions/upload-artifact": "ea165f8d65b6e75b540449e92b4886f43607fa02",
}
WORKFLOWS = {
    "assurance-pr.yml": ("assurance-tests", ("actions/checkout", "actions/setup-python", "actions/upload-artifact")),
    "assurance.yml": (
        "assurance",
        ("actions/checkout", "actions/setup-python", "sigstore/cosign-installer"),
    ),
}


def action_pin_problems(filename: str, content: str) -> list[str]:
    job_name, required = WORKFLOWS[filename]
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        return [f"invalid assurance workflow YAML: {exc}"]
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), dict):
        return ["missing assurance CI job inventory"]
    jobs = data["jobs"]
    if set(jobs) != {job_name}:
        return [f"unexpected assurance job inventory: {sorted(jobs)}"]
    job = jobs[job_name]
    if not isinstance(job, dict) or not isinstance(job.get("steps"), list):
        return ["missing assurance CI step inventory"]
    actions = []
    problems = []
    for step in job["steps"]:
        if not isinstance(step, dict):
            problems.append("malformed step")
            continue
        if "uses" not in step:
            continue
        ref = step["uses"]
        if not isinstance(ref, str) or "@" not in ref:
            problems.append(f"unparseable action reference: {ref!r}")
            continue
        action, commit = ref.rsplit("@", 1)
        actions.append(action)
        if action not in required:
            problems.append(f"unreviewed action step: {ref}")
        elif commit != ACTION_PINS[action]:
            problems.append(f"mutable, substituted or unreviewed action commit: {ref}")
    for action in required:
        if actions.count(action) != 1:
            problems.append(f"{action}: expected exactly one action, found {actions.count(action)}")
    return problems


@pytest.mark.parametrize("filename", list(WORKFLOWS))
def test_real_assurance_workflows_use_reviewed_commit_pins(filename):
    text = (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
    assert action_pin_problems(filename, text) == []


@pytest.mark.parametrize("filename", list(WORKFLOWS))
def test_mutable_and_wrong_action_refs_are_refused(filename):
    text = (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
    for action in WORKFLOWS[filename][1]:
        exact = f"{action}@{ACTION_PINS[action]}"
        assert text.count(exact) == 1
        for bad in (f"{action}@v3", f"{action}@v4", f"{action}@main", f"{action}@{'0' * 40}",
                    f"untrusted/{action.split('/')[-1]}@{ACTION_PINS[action]}"):
            planted = text.replace(exact, bad)
            assert action_pin_problems(filename, planted), bad


@pytest.mark.parametrize("filename", list(WORKFLOWS))
def test_missing_duplicate_and_unreviewed_action_steps_are_refused(filename):
    text = (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
    action = WORKFLOWS[filename][1][0]
    line = f"- uses: {action}@{ACTION_PINS[action]}"
    assert text.count(line) == 1
    assert action_pin_problems(filename, text.replace(line, "", 1))
    assert action_pin_problems(filename, text.replace(line, line + "\n      " + line, 1))
    assert action_pin_problems(filename, text.replace(line, line + "\n      - uses: random/other@v1", 1))


@pytest.mark.parametrize("filename", list(WORKFLOWS))
def test_missing_job_inventory_is_refused(filename):
    text = (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
    required_job = WORKFLOWS[filename][0]
    assert action_pin_problems(filename, text.replace(f"  {required_job}:", f"  unreviewed-job:", 1))
    assert action_pin_problems(filename, "name: empty\njobs: {}\n")
