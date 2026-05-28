# sentinel:skip-file — assurance golden corpus; deliberately contains
# example bad-DOI / overclaim strings that the rules are meant to catch.
"""Golden corpus for the e156 Assurance Standard.

Each fixture is a known-defect (or known-good) capsule snippet written to a
tmp repo and run through the REAL Sentinel rule that owns the matching risk
class. This is the integration layer — Sentinel already unit-tests each rule
in isolation; here we lock in that the assurance vocabulary (4 risk classes)
keeps catching the defects it claims to catch, capsule-shaped.

"Every error becomes a future validator." When a Track B/D check closes one of
the xfail holes below, the xfail flips to XPASS and (strict=True) FAILS the
suite — forcing the marker to be removed. That is the intended ratchet.

Fixtures are written to tmp_path at runtime (never committed to disk) so they
can never pollute a real Sentinel scan of the E156 repo.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_TESTS_DIR = Path(__file__).resolve().parent
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

import _sentinel_discovery as disc  # noqa: E402

_SENT_ROOT = disc.find_sentinel_root()
if _SENT_ROOT and str(_SENT_ROOT) not in sys.path:
    sys.path.insert(0, str(_SENT_ROOT))

try:
    from sentinel.core import RepoContext, ScanMode, Severity  # noqa: E402
    from sentinel.registry.plugin_loader import load_plugin_rule  # noqa: E402
    _SENT_OK = _SENT_ROOT is not None
except Exception:  # pragma: no cover - only on machines without Sentinel
    _SENT_OK = False

_PLUGINS = (_SENT_ROOT / "sentinel" / "rules" / "plugins") if _SENT_ROOT else None

requires_sentinel = pytest.mark.skipif(
    not _SENT_OK,
    reason="Sentinel not importable (set SENTINEL_ROOT or place at C:\\Sentinel / F:\\Sentinel)",
)


def _run(rule_file: str, repo: Path):
    rule = load_plugin_rule(_PLUGINS / rule_file)
    return list(rule.check(RepoContext(repo_root=repo, mode=ScanMode.REPO)))


def _write(repo: Path, name: str, content: str) -> None:
    (repo / name).write_text(content, encoding="utf-8")


def _blocks(verdicts):
    return [v for v in verdicts if v.severity == Severity.BLOCK]


# ===========================================================================
# Risk class 1 — Made-up citations  (citation_cascade)
# ===========================================================================

@requires_sentinel
def test_malformed_doi_blocks(tmp_path):
    _write(tmp_path, "refs.md", "See doi: 10.999/some-suffix for details.\n")
    vs = _run("citation_cascade.py", tmp_path)
    assert any("DOI" in v.detail for v in _blocks(vs))


@requires_sentinel
def test_locatorless_reference_warns(tmp_path):
    _write(
        tmp_path, "paper.md",
        "# Notes\n\n## References\n\n"
        "1. Smith J, Jones K, et al. A study of things (2020).\n",
    )
    vs = _run("citation_cascade.py", tmp_path)
    assert any(v.severity == Severity.WARN for v in vs)


@requires_sentinel
def test_valid_doi_clean(tmp_path):
    _write(tmp_path, "refs.md", "Reference: https://doi.org/10.1136/bmj.n2387\n")
    assert _blocks(_run("citation_cascade.py", tmp_path)) == []


@requires_sentinel
def test_fabricated_doi_blocked_via_resolution_cache(tmp_path):
    # Track B (closed): citation_cascade (shape-only) clears a well-formed but
    # fabricated DOI, but the out-of-band resolver records it unresolved in
    # doi-cache.json and citation_resolution BLOCKs it offline.
    _write(tmp_path, "refs.md", "Key evidence: doi: 10.9999/invented.study.2099.\n")
    (tmp_path / "doi-cache.json").write_text(
        json.dumps({
            "10.9999/invented.study.2099": {
                "status": "unresolved", "http_status": 404,
                "checked_at": "2026-05-28T00:00:00Z",
            }
        }),
        encoding="utf-8",
    )
    # citation_cascade still passes it (the shape is valid) ...
    assert _blocks(_run("citation_cascade.py", tmp_path)) == []
    # ... but citation_resolution catches the unresolved DOI.
    assert any("did not resolve" in v.detail for v in _blocks(_run("citation_resolution.py", tmp_path)))


@requires_sentinel
def test_citation_resolution_inert_without_cache(tmp_path):
    # FP discipline: with no doi-cache.json the rule must do nothing, so it
    # cannot regress pushes on the ~hundreds of repos that never ran the resolver.
    _write(tmp_path, "refs.md", "doi: 10.9999/invented.study.2099\n")
    assert _run("citation_resolution.py", tmp_path) == []


@requires_sentinel
def test_citation_resolution_skips_skip_marker_files(tmp_path):
    # FP discipline: negative-test fixtures carrying sentinel:skip-file are not
    # blocked even when the cache marks their example DOI unresolved.
    _write(tmp_path, "fixture.md", "sentinel:skip-file\ndoi: 10.9999/invented.study.2099\n")
    (tmp_path / "doi-cache.json").write_text(
        json.dumps({
            "10.9999/invented.study.2099": {"status": "unresolved", "http_status": 404}
        }),
        encoding="utf-8",
    )
    assert _run("citation_resolution.py", tmp_path) == []


# ===========================================================================
# Risk class 2 — Data-extraction errors  (denominator_logic)
# ===========================================================================

_DASH = "demo_REVIEW.html"  # denominator_logic scans *_REVIEW.html


@requires_sentinel
def test_events_exceed_total_blocks(tmp_path):
    _write(
        tmp_path, _DASH,
        "<html><script>\nrealData = { 'NCT01234567': "
        "{ tE: 50, tN: 40, cE: 5, cN: 100, publishedHR: 0.80, "
        "hrLCI: 0.65, hrUCI: 0.95 } };\n</script></html>\n",
    )
    vs = _run("denominator_logic.py", tmp_path)
    assert any("exceeds sample size" in v.detail for v in _blocks(vs))


@requires_sentinel
def test_ci_not_bracketing_hr_blocks(tmp_path):
    _write(
        tmp_path, _DASH,
        "<html><script>\nrealData = { 'NCT02223334': "
        "{ tE: 10, tN: 100, cE: 20, cN: 100, publishedHR: 0.40, "
        "hrLCI: 0.65, hrUCI: 0.95 } };\n</script></html>\n",
    )
    vs = _run("denominator_logic.py", tmp_path)
    assert any("not bracketed" in v.detail for v in _blocks(vs))


@requires_sentinel
def test_consistent_data_clean(tmp_path):
    _write(
        tmp_path, _DASH,
        "<html><script>\nrealData = { 'NCT09998887': "
        "{ tE: 10, tN: 100, cE: 20, cN: 100, publishedHR: 0.80, "
        "hrLCI: 0.65, hrUCI: 0.95 } };\n</script></html>\n",
    )
    assert _blocks(_run("denominator_logic.py", tmp_path)) == []


# ===========================================================================
# Risk class 3 — Analysis errors  (dashboard_match — the only live numeric
# consistency rule; it range-checks but never recomputes the pool)
# ===========================================================================

@requires_sentinel
def test_consistent_but_wrong_pooled_estimate_is_caught(tmp_path):
    # Track B (closed): per-trial HRs 0.80 & 0.90 re-pool to ~0.846, but the
    # body claims 0.65. That is inside dashboard_match's loose per-trial range
    # (+/-0.2 -> [0.60, 1.10]) so the range heuristic clears it; pooled_recompute
    # re-pools and flags it.
    _write(
        tmp_path, "wrongpool_REVIEW.html",
        "<html><body>\n"
        "<p>Pooled HR 0.65 (95% CI 0.55-0.77) across two trials.</p>\n"
        "<script>\nrealData = {\n"
        " 'NCT01111111': { tE:10, tN:100, cE:12, cN:100, publishedHR:0.80, hrLCI:0.70, hrUCI:0.92 },\n"
        " 'NCT02222222': { tE:11, tN:100, cE:13, cN:100, publishedHR:0.90, hrLCI:0.78, hrUCI:1.04 }\n"
        "};\n</script></body></html>\n",
    )
    # The loose range check clears it (0.65 is within [0.60, 1.10]) ...
    assert _run("dashboard_match.py", tmp_path) == []
    # ... but re-pooling the review's own data flags the mismatch.
    assert len(_run("pooled_recompute.py", tmp_path)) >= 1


# ===========================================================================
# Risk class 4 — Overclaiming  (claim_language)
# ===========================================================================

@requires_sentinel
def test_causal_overclaim_word_fires(tmp_path):
    _write(
        tmp_path, "students.html",
        "<html><body><p>This analysis proves the treatment works.</p></body></html>\n",
    )
    assert len(_run("claim_language.py", tmp_path)) >= 1


@requires_sentinel
def test_certainty_plus_heterogeneity_fires(tmp_path):
    _write(
        tmp_path, "students.html",
        "<html><body><p>The drug is effective. Heterogeneity was high (I2 = 80%).</p></body></html>\n",
    )
    assert len(_run("claim_language.py", tmp_path)) >= 1


@requires_sentinel
def test_hedged_claim_clean(tmp_path):
    _write(
        tmp_path, "students.html",
        "<html><body><p>The intervention was associated with lower mortality, "
        "consistent with prior trials; evidence certainty was graded low.</p></body></html>\n",
    )
    assert _run("claim_language.py", tmp_path) == []


@requires_sentinel
def test_overclaim_without_trigger_word_is_caught(tmp_path):
    # Track D (closed): no banned trigger word, but the comparative-confidence
    # detector catches the intensifier+verb pattern ("clearly reduces").
    _write(
        tmp_path, "students.html",
        "<html><body><p>The treatment clearly reduces mortality; the protective "
        "effect is robust and strong across all subgroups.</p></body></html>\n",
    )
    assert any("comparative-confidence" in v.detail for v in _run("claim_language.py", tmp_path))
