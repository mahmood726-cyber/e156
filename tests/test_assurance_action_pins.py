"""Lock third-party Actions independently within each approved assurance job.

Reviewed action pins are exact Git commits, not external attestations.
The PR-only OIDC canary is a separate, explicitly allowlisted job; adding it
must not relax the action count or unexpected-job refusals.
"""
from __future__ import annotations

from copy import deepcopy
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
# Explicit approved job inventories and exact per-job action multiplicity.
# In particular, the OIDC canary cannot silently authorize an extra publisher.
WORKFLOWS = {
    "assurance-pr.yml": {
        "assurance-tests": ("actions/checkout", "actions/setup-python", "actions/upload-artifact"),
        "keyless-oidc-canary": ("actions/checkout", "sigstore/cosign-installer"),
    },
    "assurance.yml": {
        "assurance": ("actions/checkout", "actions/setup-python", "sigstore/cosign-installer"),
    },
}


def action_pin_problems(filename: str, content: str) -> list[str]:
    required_jobs = WORKFLOWS[filename]
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        return [f"invalid assurance workflow YAML: {exc}"]
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), dict):
        return ["missing assurance CI job inventory"]
    jobs = data["jobs"]
    if set(jobs) != set(required_jobs):
        return [f"unexpected assurance job inventory: {sorted(jobs)}"]

    problems = []
    for job_name, required in required_jobs.items():
        job = jobs[job_name]
        if not isinstance(job, dict) or not isinstance(job.get("steps"), list):
            problems.append(f"{job_name}: missing assurance CI step inventory")
            continue
        actions = []
        for step in job["steps"]:
            if not isinstance(step, dict):
                problems.append(f"{job_name}: malformed step")
                continue
            if "uses" not in step:
                continue
            ref = step["uses"]
            if not isinstance(ref, str) or "@" not in ref:
                problems.append(f"{job_name}: unparseable action reference: {ref!r}")
                continue
            action, commit = ref.rsplit("@", 1)
            actions.append(action)
            if action not in required:
                problems.append(f"{job_name}: unreviewed action step: {ref}")
            elif commit != ACTION_PINS[action]:
                problems.append(f"{job_name}: mutable, substituted or unreviewed action commit: {ref}")
        for action in required:
            if actions.count(action) != 1:
                problems.append(
                    f"{job_name}: {action}: expected exactly one action, found {actions.count(action)}"
                )
    return problems


def _workflow(filename: str) -> dict:
    source = (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
    return yaml.safe_load(source)


def _action_index(steps: list, action: str) -> int:
    hits = [
        i for i, step in enumerate(steps)
        if isinstance(step, dict) and isinstance(step.get("uses"), str)
        and step["uses"].startswith(action + "@")
    ]
    assert len(hits) == 1, f"expected one reviewed {action} per job, got {hits}"
    return hits[0]


@pytest.mark.parametrize("filename", list(WORKFLOWS))
def test_real_assurance_workflows_use_reviewed_commit_pins(filename):
    source = (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
    assert action_pin_problems(filename, source) == []


@pytest.mark.parametrize("filename", list(WORKFLOWS))
def test_mutable_and_wrong_action_refs_are_refused(filename):
    original = _workflow(filename)
    for job_name, required in WORKFLOWS[filename].items():
        for action in required:
            steps = original["jobs"][job_name]["steps"]
            index = _action_index(steps, action)
            exact = f"{action}@{ACTION_PINS[action]}"
            assert steps[index]["uses"] == exact
            for bad in (
                f"{action}@v3", f"{action}@v4", f"{action}@main",
                f"{action}@{'0' * 40}",
                f"untrusted/{action.split('/')[-1]}@{ACTION_PINS[action]}",
            ):
                planted = deepcopy(original)
                planted["jobs"][job_name]["steps"][index]["uses"] = bad
                assert action_pin_problems(filename, yaml.safe_dump(planted)), (job_name, bad)


@pytest.mark.parametrize("filename", list(WORKFLOWS))
def test_missing_duplicate_and_unreviewed_action_steps_are_refused(filename):
    original = _workflow(filename)
    for job_name, required in WORKFLOWS[filename].items():
        action = required[0]
        idx = _action_index(original["jobs"][job_name]["steps"], action)
        for kind in ("missing", "duplicate", "unreviewed"):
            planted = deepcopy(original)
            steps = planted["jobs"][job_name]["steps"]
            if kind == "missing":
                steps.pop(idx)
            elif kind == "duplicate":
                steps.insert(idx, deepcopy(steps[idx]))
            else:
                steps.insert(idx, {"uses": "random/other@v1"})
            assert action_pin_problems(filename, yaml.safe_dump(planted)), (job_name, kind)


@pytest.mark.parametrize("filename", list(WORKFLOWS))
def test_missing_or_extra_job_inventory_is_refused(filename):
    original = _workflow(filename)
    for job_name in WORKFLOWS[filename]:
        planted = deepcopy(original)
        del planted["jobs"][job_name]
        assert action_pin_problems(filename, yaml.safe_dump(planted)), job_name
    planted = deepcopy(original)
    planted["jobs"]["unreviewed-job"] = {"runs-on": "ubuntu-latest", "steps": []}
    assert action_pin_problems(filename, yaml.safe_dump(planted))
