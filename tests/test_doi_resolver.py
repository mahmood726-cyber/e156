# sentinel:skip-file — contains example fabricated DOI strings for testing.
"""Unit tests for the out-of-band DOI resolver (Track B, risk class 1).

Network is never touched: the fetcher is injectable and these tests pass a fake.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT, ROOT / "scripts", Path(__file__).resolve().parent):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

dr = importlib.import_module("assurance.doi_resolver")


# ---- DOI extraction --------------------------------------------------------

def test_extract_dois_wellformed():
    text = "see doi: 10.1136/bmj.n2387 and https://doi.org/10.1056/NEJMoa2025.\n"
    assert dr.extract_dois(text) == {"10.1136/bmj.n2387", "10.1056/NEJMoa2025"}


def test_extract_ignores_malformed_shape():
    # 3-digit registrant is not a well-formed DOI -> not extracted (that's
    # citation_cascade's malformed-shape BLOCK, not a resolution target).
    assert dr.extract_dois("doi: 10.999/x") == set()


# ---- resolution with a fake fetcher ---------------------------------------

def test_resolve_classifies_by_fetcher():
    def fake(doi):
        return ("unresolved", 404) if "invented" in doi else ("resolved", 200)

    cache: dict = {}
    dr.resolve_dois(["10.1136/bmj.n2387", "10.9999/invented.x"], cache, fetcher=fake)
    assert cache["10.1136/bmj.n2387"]["status"] == "resolved"
    assert cache["10.9999/invented.x"]["status"] == "unresolved"
    assert cache["10.9999/invented.x"]["http_status"] == 404
    assert "checked_at" in cache["10.1136/bmj.n2387"]


def test_resolve_skips_cached_unless_force():
    calls: list[str] = []

    def fake(doi):
        calls.append(doi)
        return ("resolved", 200)

    cache = {"10.1234/x": {"status": "resolved", "http_status": 200, "checked_at": "old"}}
    dr.resolve_dois(["10.1234/x"], cache, fetcher=fake)
    assert calls == []  # already resolved -> not re-checked

    dr.resolve_dois(["10.1234/x"], cache, fetcher=fake, force=True)
    assert calls == ["10.1234/x"]  # force re-checks


def test_resolve_retries_unknown():
    calls: list[str] = []

    def fake(doi):
        calls.append(doi)
        return ("unknown", None)

    cache = {"10.1234/x": {"status": "unknown", "http_status": None, "checked_at": "old"}}
    dr.resolve_dois(["10.1234/x"], cache, fetcher=fake)
    assert calls == ["10.1234/x"]  # unknown is transient -> always re-tried


# ---- cache round-trip + scan ----------------------------------------------

def test_cache_round_trip(tmp_path):
    cache = {"10.1234/x": {"status": "resolved", "http_status": 200, "checked_at": "t"}}
    p = tmp_path / "doi-cache.json"
    dr.save_cache(p, cache)
    assert dr.load_cache(p) == cache


def test_scan_repo_honors_skip_marker(tmp_path):
    (tmp_path / "good.md").write_text("doi: 10.1136/bmj.n2387\n", encoding="utf-8")
    (tmp_path / "fixture.md").write_text(
        "sentinel:skip-file\ndoi: 10.9999/invented.x\n", encoding="utf-8"
    )
    found = dr.scan_repo_dois(tmp_path)
    assert "10.1136/bmj.n2387" in found
    assert "10.9999/invented.x" not in found  # skip-file fixture not resolved


# ---- drift guard: DOI shape must match citation_cascade --------------------

def test_valid_doi_shape_matches_citation_cascade():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _sentinel_discovery as disc

    root = disc.find_sentinel_root()
    if root is None:
        pytest.skip("Sentinel not found; cannot check DOI-shape contract")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from sentinel.rules.plugins import citation_cascade as cc

    assert dr.VALID_DOI_RE.pattern == cc.VALID_DOI_RE.pattern
