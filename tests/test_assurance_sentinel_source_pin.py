"""Fail-closed regression for the accepted Sentinel source in both E156 workflows.

These source/mutation tests do not establish a signed upstream release or run
the privileged publishing workflow. Hosted assurance separately checks out
and tests this exact source on Ubuntu and Windows.
"""
from __future__ import annotations

from pathlib import Path
import re

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SENTINEL_SHA = "d87211a0c0a43e805b3aba36ec920693928e86b5"
SUPERSEDED_SENTINEL_SHA = "97273997db160aee99d89af94fcc18bf621b3cb9"
WORKFLOWS = (
    (".github/workflows/assurance-pr.yml", "Fetch exact Sentinel source outside the E156 scan root"),
    (".github/workflows/assurance.yml", "Check out Sentinel (mandatory, exact tested commit)"),
)
PIN_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")


def source_pin_problems(workflow: str, step_name: str) -> list[str]:
    """Check exact checkout, independently matched source identity, and no pin drift."""
    try:
        document = yaml.safe_load(workflow)
        steps = document["jobs"][next(iter(document["jobs"]))]["steps"]
    except (yaml.YAMLError, KeyError, TypeError, StopIteration) as exc:
        return [f"Unparseable or missing required workflow: {exc}"]
    matches = [s for s in steps if s.get("name") == step_name]
    if len(matches) != 1:
        return ["Missing or duplicated required Sentinel checkout step"]
    run = matches[0].get("run", "")
    problems = []
    # The exact detached checkout and separate HEAD assertion must use the
    # same accepted SHA. A tag, branch, or stale sha must not silently pass.
    checkout = re.findall(
        r"git -C [^\n]+ checkout --quiet --detach ([0-9a-f]{40})", run
    )
    if checkout != [EXPECTED_SENTINEL_SHA]:
        problems.append("Sentinel detached checkout is not the accepted exact commit")
    all_shas = PIN_RE.findall(run)
    if all_shas != [EXPECTED_SENTINEL_SHA, EXPECTED_SENTINEL_SHA]:
        problems.append("Sentinel source and HEAD identity assertion disagree or drift")
    if "git clone --quiet https://github.com/" not in run:
        problems.append("Sentinel source is not cloned")
    if "rev-parse HEAD" not in run:
        problems.append("Sentinel HEAD is not checked")
    return problems


@pytest.mark.parametrize("path,step_name", WORKFLOWS)
def test_assurance_workflows_pin_merged_and_tested_sentinel(path, step_name):
    text = (ROOT / path).read_text(encoding="utf-8")
    assert not source_pin_problems(text, step_name), (path, source_pin_problems(text, step_name))


@pytest.mark.parametrize("path,step_name", WORKFLOWS)
def test_sentinel_pin_mutations_are_refused(path, step_name):
    text = (ROOT / path).read_text(encoding="utf-8")
    assert text.count(EXPECTED_SENTINEL_SHA) == 2
    mutations = (
        text.replace(EXPECTED_SENTINEL_SHA, SUPERSEDED_SENTINEL_SHA, 1),
        text.replace(EXPECTED_SENTINEL_SHA, SUPERSEDED_SENTINEL_SHA),
        text.replace("checkout --quiet --detach " + EXPECTED_SENTINEL_SHA,
                     "checkout --quiet --detach main"),
        text.replace("rev-parse HEAD", "echo " + EXPECTED_SENTINEL_SHA),
    )
    for mutated in mutations:
        assert mutated != text, "Mutation did not reach the checked source"
        assert source_pin_problems(mutated, step_name), (path, mutated)
