"""Guard E156 production assurance for *every* protected master push.

Read-only mutation tests. Passing these checks does not prove that the independent
Pages deployment waits for assurance or that production signing succeeded.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "assurance.yml"


def public_source_trigger_problems(text: str) -> list[str]:
    try:
        document = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return [f"invalid YAML: {exc}"]
    if not isinstance(document, dict):
        return ["missing workflow"]
    # PyYAML YAML-1.1 parses the unquoted GitHub key 'on' as Boolean True.
    events = document.get("on", document.get(True))
    if not isinstance(events, dict):
        return ["missing event inventory"]
    if any(event in events for event in ("pull_request", "pull_request_target")):
        return ["privileged publishing assurance cannot run on untrusted PR events"]
    push = events.get("push")
    if not isinstance(push, dict) or "master" not in push.get("branches", []):
        return ["missing protected master push trigger"]
    if "paths" in push or "paths-ignore" in push:
        return ["partial path filtering can bypass assurance for a Pages-published master change"]
    return []


def test_actual_workflow_assures_every_master_push():
    assert public_source_trigger_problems(WORKFLOW.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize("filter_line", [
    "paths:\n      - 'paper/**'",
    "paths-ignore:\n      - 'docs/**'",
])
def test_partial_master_push_path_filters_are_refused(filter_line):
    original = WORKFLOW.read_text(encoding="utf-8")
    needle = "    branches: [master]\n"
    assert original.count(needle) == 1
    modified = original.replace(needle, needle + "    " + filter_line + "\n", 1)
    assert modified != original
    assert any("partial path filtering" in p for p in public_source_trigger_problems(modified))


def test_untrusted_pr_event_cannot_acquire_privileged_assurance():
    original = WORKFLOW.read_text(encoding="utf-8")
    assert original.count("  push:\n") == 1
    modified = original.replace(
        "  push:\n", "  pull_request:\n    branches: [master]\n  push:\n", 1
    )
    assert any("untrusted PR" in p for p in public_source_trigger_problems(modified))


def test_removed_master_branch_refuses_assurance_gap():
    original = WORKFLOW.read_text(encoding="utf-8")
    assert original.count("    branches: [master]\n") == 1
    modified = original.replace("    branches: [master]\n", "    branches: [other]\n", 1)
    assert any("protected master" in p for p in public_source_trigger_problems(modified))


def test_invalid_workflow_yaml_refused():
    assert any("invalid YAML" in p for p in public_source_trigger_problems("on: [\n"))
