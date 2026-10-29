"""Guard E156 assurance workflow coverage of public data and rendered pages.

This is a static PR test, not an executed OIDC signing/deployment gate.
The independently configured Pages source still needs protection (issue #85).
"""
from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "assurance.yml"
PUBLIC_SOURCES = frozenset({
    "paper/**",
    "rewrite-workbook.txt",
    "students.html",
    "e156-library.html",
    "index.html",
    "assurance.html",
    "templates/**",
    "scripts/build_paper_pages.py",
    "scripts/build_students_page.py",
    "scripts/build_library.py",
    "scripts/paper_charts.py",
})


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
    if "paths" not in push:
        return []  # All master pushes are a stronger coverage guarantee.
    patterns = push["paths"]
    if not isinstance(patterns, list) or not all(isinstance(p, str) for p in patterns):
        return ["invalid publication path filters"]
    return [f"public source excluded from assurance: {source}"
            for source in sorted(PUBLIC_SOURCES - set(patterns))]


def test_actual_workflow_covers_public_source_and_rendered_pages():
    assert public_source_trigger_problems(WORKFLOW.read_text(encoding="utf-8")) == []


def test_dropping_each_public_path_refuses_silent_assurance_omission():
    original = WORKFLOW.read_text(encoding="utf-8")
    for source in sorted(PUBLIC_SOURCES):
        modified = original.replace(f'      - "{source}"\\n', "", 1)
        assert modified != original, f"fixture did not remove {source}"
        assert f"public source excluded from assurance: {source}" in public_source_trigger_problems(modified)


def test_untrusted_pr_event_cannot_acquire_privileged_publishing_job():
    original = WORKFLOW.read_text(encoding="utf-8")
    modified = original.replace("  push:\\n", "  pull_request:\\n    branches: [master]\\n  push:\\n", 1)
    assert modified != original
    assert any("untrusted PR" in p for p in public_source_trigger_problems(modified))
