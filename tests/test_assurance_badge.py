"""Regression tests for the e156 Assurance badge logic.

Two layers, both protecting the standard's founding principle ("the capsule
must agree with itself before asking the world to agree with it"):

  1. META-TEST: every rule ID in build_assurance_jsons.RULE_TO_CHECK must be a
     real, live Sentinel rule ID. A typo here makes the badge SILENTLY drop
     that check's findings (they default to "pass"), so the badge asserts a
     verdict the capsule never earned. This test would have caught the
     P1-claim-language vs P0-claim-language-workbook drift. It reads rule IDs
     by AST (no Sentinel import) so it runs even on a bare E156 checkout.

  2. TIER LOGIC: compute_tier() boundary tests + an on-disk self-consistency
     check (every assurance.json's stored tier must equal compute_tier of its
     own checks — catches forged or stale badges in present work).

These lock CURRENT behavior. Any deliberate change to tier semantics must
update the assertion in the same commit.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]  # C:\E156
for _p in (ROOT, ROOT / "scripts", Path(__file__).resolve().parent):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import _sentinel_discovery as disc  # noqa: E402
import build_assurance_jsons as baj  # noqa: E402


# ---------------------------------------------------------------------------
# Meta-test: RULE_TO_CHECK keys must be live Sentinel rule IDs
# ---------------------------------------------------------------------------

def _declared_rule_ids(plugins: Path) -> set[str]:
    """Module-level `ID = "..."` from every plugin, via AST (no execution)."""
    ids: set[str] = set()
    for py in plugins.glob("*.py"):
        if py.name == "__init__.py":
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "ID" for t in node.targets
            ):
                v = node.value
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    ids.add(v.value)
    return ids


def test_rule_to_check_keys_are_live_rule_ids():
    plugins = disc.plugins_dir()
    if plugins is None:
        pytest.skip(
            "Sentinel plugins dir not found (set SENTINEL_ROOT or place at "
            "C:\\Sentinel / F:\\Sentinel)"
        )
    declared = _declared_rule_ids(plugins)
    assert declared, "no rule IDs parsed from plugins dir — discovery/AST broke"
    missing = sorted(set(baj.RULE_TO_CHECK) - declared)
    assert not missing, (
        f"RULE_TO_CHECK references rule IDs that do not exist in Sentinel: "
        f"{missing}. The badge silently drops findings for these checks (they "
        f"default to 'pass'), so a capsule can claim a tier it never earned. "
        f"Fix the ID(s) in build_assurance_jsons.RULE_TO_CHECK."
    )


# ---------------------------------------------------------------------------
# compute_tier() boundary tests
# ---------------------------------------------------------------------------

def _checks(**override) -> dict:
    base = {
        "citation_cascade": "pass",
        "denominator_logic": "pass",
        "claim_language": "pass",
        "data_file_present": "pass",
        "code_runs": "pass",
        "dashboard_match": "pass",
        "analysis_rerun": "pass",
        "external_review": "pass",
    }
    base.update(override)
    return base


def test_full_pass_is_gold():
    assert baj.compute_tier(_checks()) == "gold"


def test_citation_fail_forces_none():
    assert baj.compute_tier(_checks(citation_cascade="fail")) == "none"


def test_missing_data_file_forces_none():
    # The current state of every live badge: data_file_present is "not-run",
    # so Bronze (which requires it == "pass") is unreachable -> tier "none".
    assert baj.compute_tier(_checks(data_file_present="not-run")) == "none"


def test_no_external_review_caps_at_silver():
    # Gold demands an independent external review; without it Silver is the
    # ceiling no matter how clean everything else is.
    assert baj.compute_tier(_checks(external_review="not-run")) == "silver"


def test_no_analysis_rerun_caps_at_silver():
    assert baj.compute_tier(_checks(analysis_rerun="not-run")) == "silver"


def test_claim_language_warn_caps_at_bronze():
    # A 'warn' (not a fail) in claim_language must NOT reach Silver, but the
    # capsule can still hold Bronze.
    assert baj.compute_tier(_checks(claim_language="warn")) == "bronze"


def test_any_contributing_fail_forces_none():
    # Doc-consistent (assurance-standard.md): a single 'fail' anywhere forces
    # tier none — honest under-claiming is the safer error.
    assert baj.compute_tier(_checks(claim_language="fail")) == "none"
    assert baj.compute_tier(_checks(denominator_logic="fail")) == "none"
    assert baj.compute_tier(_checks(analysis_rerun="fail")) == "none"
    assert baj.compute_tier(_checks(dashboard_match="fail")) == "none"


def test_dashboard_match_not_pass_caps_at_bronze():
    assert baj.compute_tier(_checks(dashboard_match="not-run")) == "bronze"


def test_badge_integrity_rule_matches_compute_tier():
    # The Sentinel assurance_badge_integrity rule duplicates the tier logic so
    # it can run self-contained. Assert it never drifts from the canonical
    # compute_tier, across the full 4^7 grid of check states.
    import itertools

    plugins = disc.plugins_dir()
    if plugins is None:
        pytest.skip("Sentinel not found; cannot check tier-logic contract")
    root = disc.find_sentinel_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from sentinel.rules.plugins import assurance_badge_integrity as abi

    keys = [
        "citation_cascade", "data_file_present", "code_runs", "dashboard_match",
        "claim_language", "analysis_rerun", "external_review", "pdf_match",
    ]
    states = ("pass", "warn", "fail", "not-run")
    for combo in itertools.product(states, repeat=len(keys)):
        checks = dict(zip(keys, combo))
        assert abi.compute_tier(checks) == baj.compute_tier(checks), checks


# ---------------------------------------------------------------------------
# On-disk badge self-consistency (present-work regression guard)
# ---------------------------------------------------------------------------

def test_build_assurance_here(tmp_path):
    # GitHub Actions per-repo mode: a repo with a data file but no Overmind/
    # workbook should earn Bronze (citation pass, data present, no fail).
    (tmp_path / "data.csv").write_text("a,b\n" + "x,y\n" * 500, encoding="utf-8")
    blob = baj.build_assurance_here(tmp_path, "demo")
    assert blob["project_name"] == "demo"
    assert blob["local_path"] == str(tmp_path)
    assert blob["checks"]["data_file_present"] == "pass"
    assert "fail" not in blob["checks"].values()
    assert blob["tier"] == "bronze"


def test_existing_badges_are_self_consistent():
    badges = [p for p in ROOT.rglob("assurance.json") if ".git" not in p.parts]
    if not badges:
        pytest.skip("no assurance.json badges on disk")
    mismatches = []
    for b in badges:
        try:
            data = json.loads(b.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        checks = data.get("checks")
        stored = data.get("tier")
        if not isinstance(checks, dict) or stored is None:
            continue
        recomputed = baj.compute_tier(checks)
        if recomputed != stored:
            mismatches.append(
                f"{b}: stored tier={stored!r} but compute_tier(checks)={recomputed!r}"
            )
    assert not mismatches, (
        "assurance.json tier disagrees with its own checks (forged or stale "
        "badge):\n" + "\n".join(mismatches)
    )
