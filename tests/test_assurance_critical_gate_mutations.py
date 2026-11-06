"""Mutation canaries for E156's non-optional, same-source publication prerequisites.

These are structural policy regressions on the existing PR, not production
DOI/Sentinel/OIDC evidence or a substitute for authenticated publication.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/assurance.yml"

# The test suite, DOI resolver, and both Sentinel scans must not silently turn
# into skipped/successful no-ops while the dependent Pages job stays green.
GATES = (
    ("Run the assurance test suite (hard gate)",
     "python -m pytest tests/ -q --junitxml"),
    ("Refuse omitted or skipped tests (hard gate)",
     "python scripts/assurance/require_corpus_results.py"),
    ("Resolve DOIs against doi.org (live)",
     "python scripts/assurance/doi_resolver.py --repo ."),
    ("Sentinel scan for findings (hard gate)",
     'PYTHONPATH="$SENTINEL_ROOT" python -m sentinel scan --repo .'),
    ("Reject unverified legacy HMAC marks before mandatory keyless signing",
     "python scripts/assurance/require_keyless_safe_badges.py --repo ."),
    ("Verify Sigstore badge bundles and workflow identity (hard gate)",
     "python scripts/assurance/verify_sigstore_badges.py --repo ."),
    ("Build the public assurance dashboard (served by existing Pages)",
     "--require-keyless-verified"),
    ("Sentinel rescan generated publication artifacts (hard gate)",
     'PYTHONPATH="$SENTINEL_ROOT" python -m sentinel scan --repo .'),
)


def problems(workflow: dict) -> list[str]:
    errors: list[str] = []
    # PyYAML's YAML-1.1 resolver interprets the unquoted "on" key as True.
    events = workflow.get("on", workflow.get(True, {}))
    if not isinstance(events, dict):
        return ["workflow triggers unavailable"]
    push = events.get("push")
    if (not isinstance(push, dict) or push.get("branches") != ["master"]
            or any(k in push for k in ("paths", "paths-ignore", "branches-ignore"))):
        errors.append("master source edits no longer unconditionally trigger assurance")
    if "workflow_dispatch" not in events or "schedule" not in events:
        errors.append("manual or periodic DOI revalidation trigger missing")

    jobs = workflow.get("jobs", {})
    assurance = jobs.get("assurance", {})
    steps = assurance.get("steps", [])
    names = [s.get("name") for s in steps]
    indices: list[int] = []
    for name, command in GATES:
        if names.count(name) != 1:
            errors.append(f"missing or duplicated gate: {name}")
            continue
        idx = names.index(name)
        indices.append(idx)
        step = steps[idx]
        if command not in str(step.get("run", "")):
            errors.append(f"required executable absent: {name}")
        if step.get("continue-on-error") not in (None, False):
            errors.append(f"gate could report success despite failure: {name}")
        expected_if = "always()" if name.startswith("Refuse omitted") else None
        if step.get("if") != expected_if:
            errors.append(f"gate can be conditionally bypassed: {name}")
    if len(indices) == len(GATES) and indices != sorted(indices):
        errors.append("critical gates are out of order")

    # Preserve dependent Pages (no independent green deploy on failed assurance).
    deploy = jobs.get("deploy-pages", {})
    if deploy.get("needs") != "assurance":
        errors.append("Pages no longer depends on successful assurance")
    return errors


def current() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def test_current_workflow_has_unconditional_critical_gates():
    assert problems(current()) == []


def test_mutations_fail_closed_if_doi_sentinel_tests_or_triggers_are_bypassed():
    baseline = current()
    kinds = (
        "drop-push", "filter-public-edits", "remove-schedule",
        "skip-doi", "do-nothing-doi", "optional-doi",
        "skip-first-sentinel", "skip-final-sentinel", "optional-sentinel",
        "skip-test-suite", "optional-coverage", "bypass-keyless",
        "bypass-dashboard", "independent-pages",
    )
    for kind in kinds:
        wf = deepcopy(baseline)
        events = wf.get("on", wf.get(True))
        steps = wf["jobs"]["assurance"]["steps"]
        def step_named(name):
            return next(step for step in steps if step.get("name") == name)

        if kind == "drop-push":
            del events["push"]
        elif kind == "filter-public-edits":
            events["push"]["paths"] = ["scripts/**"]
        elif kind == "remove-schedule":
            del events["schedule"]
        elif kind == "skip-doi":
            step_named(GATES[2][0])["if"] = "false"
        elif kind == "do-nothing-doi":
            step_named(GATES[2][0])["run"] = "echo green"
        elif kind == "optional-doi":
            step_named(GATES[2][0])["continue-on-error"] = True
        elif kind == "skip-first-sentinel":
            step_named(GATES[3][0])["if"] = "false"
        elif kind == "skip-final-sentinel":
            step_named(GATES[7][0])["run"] = "true"
        elif kind == "optional-sentinel":
            step_named(GATES[7][0])["continue-on-error"] = True
        elif kind == "skip-test-suite":
            step_named(GATES[0][0])["if"] = "false"
        elif kind == "optional-coverage":
            step_named(GATES[1][0])["continue-on-error"] = True
        elif kind == "bypass-keyless":
            step_named(GATES[5][0])["run"] = "echo keyless"
        elif kind == "bypass-dashboard":
            step_named(GATES[6][0])["run"] = "python scripts/assurance/build_pages_dashboard.py --repo ."
        else:
            wf["jobs"]["deploy-pages"]["needs"] = "other-job"
        assert problems(wf), kind
