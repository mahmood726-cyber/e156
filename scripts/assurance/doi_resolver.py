"""e156 Assurance — DOI resolution (Track B, risk class 1: made-up citations).

The commit-time citation_cascade rule only checks DOI *shape*. A structurally
valid but fabricated DOI (10.9999/invented.study) passes clean — the single
highest-impact false negative in the 2026-05-28 red-team. Closing it needs an
actual resolution against doi.org, which is slow and network-bound, so it must
NOT happen at commit time.

This module is the out-of-band resolver. It walks a repo's capsule docs,
extracts well-formed DOIs, resolves the uncached ones against doi.org, and
writes a committed `doi-cache.json`:

    { "10.1136/bmj.n2387": {"status": "resolved",   "http_status": 200, "checked_at": "..."},
      "10.9999/invented":  {"status": "unresolved", "http_status": 404, "checked_at": "..."} }

The cache doubles as provenance — proof that each DOI was checked, and when.
The Sentinel rule `citation_resolution` (offline) reads this cache and BLOCKs
any capsule DOI whose status is "unresolved". DOIs the resolver couldn't reach
(network error, paywalled publisher 403) are recorded "unknown" and never
block — honest under-claiming is the safer error.

The network fetcher is injectable so the logic is testable offline.

CLI:
  python -m scripts.assurance.doi_resolver --repo C:\\some\\repo
  python scripts/assurance/doi_resolver.py --repo . --dry-run
  python scripts/assurance/doi_resolver.py --repo . --force   # re-check all
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable

# DOI shape — must match citation_cascade.VALID_DOI_RE. A contract test in
# tests/test_doi_resolver.py asserts the two patterns stay identical.
VALID_DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")

# Finder for "doi:"/"DOI:"/"https://doi.org/" prefixed strings in prose. Mirror
# of citation_cascade.DOI_PREFIX_RE (same capture semantics).
_DOI_PREFIX_RE = re.compile(
    r"(?:^|[\s\(\[\{>;,])"
    r"(?:doi[:=]\s*|DOI[:=]\s*|https?://(?:dx\.)?doi\.org/)"
    r"(\S+?)"
    r"(?=[\s)\]}<;,\"']|\.\s|\.$|$)",
    re.MULTILINE,
)

_DOC_EXT = frozenset((".md", ".html", ".txt", ".rst", ".json"))
_DOC_NAMES = frozenset(("rewrite-workbook.txt",))
_EXCLUDE_DIRS = frozenset((
    "node_modules", "__pycache__", ".git", ".pytest_cache", ".venv",
    "venv", "build", "dist", ".tox", ".mypy_cache",
))
MAX_FILE_BYTES = 5_000_000
CACHE_NAME = "doi-cache.json"
# Files carrying this marker (test fixtures with example bad DOIs, vendored
# copies) must not be resolved into the cache — they would otherwise produce
# false "unresolved" verdicts on intentional negative-test material.
SKIP_MARKER = "sentinel:skip-file"

RESOLVED = "resolved"
UNRESOLVED = "unresolved"
UNKNOWN = "unknown"

Fetcher = Callable[[str], "tuple[str, int | None]"]


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _clean_candidate(raw: str) -> str:
    return raw.strip(".,)]\"'").rstrip(".")


def extract_dois(text: str) -> set[str]:
    """Return the set of well-formed DOIs that appear with a doi:/DOI:/doi.org
    prefix in the text."""
    out: set[str] = set()
    for m in _DOI_PREFIX_RE.finditer(text):
        cand = _clean_candidate(m.group(1))
        if VALID_DOI_RE.match(cand):
            out.add(cand)
    return out


def _iter_doc_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(d in _EXCLUDE_DIRS for d in path.parts):
            continue
        if path.name == CACHE_NAME:
            continue
        if path.name in _DOC_NAMES or path.suffix.lower() in _DOC_EXT:
            yield path


def scan_repo_dois(root: Path) -> set[str]:
    """All well-formed DOIs referenced across a repo's capsule docs."""
    dois: set[str] = set()
    for path in _iter_doc_files(root):
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if SKIP_MARKER in text:
            continue
        dois |= extract_dois(text)
    return dois


def http_head_fetcher(doi: str, timeout: float = 10.0, retries: int = 1) -> "tuple[str, int | None]":
    """Resolve a DOI against doi.org. Returns (status, http_status).

    doi.org returns 404 for a non-existent DOI *at its own level*, before any
    publisher redirect — so a fabricated DOI yields UNRESOLVED. A real but
    paywalled DOI redirects to a publisher that may answer 200 or 403; those
    map to RESOLVED / UNKNOWN respectively, never UNRESOLVED.
    """
    url = "https://doi.org/" + doi
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, method="HEAD",
                                         headers={"User-Agent": "e156-assurance-doi-resolver"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = getattr(resp, "status", None) or resp.getcode()
                return (RESOLVED, code)
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return (UNRESOLVED, e.code)
            if e.code in (301, 302, 303, 307, 308):
                return (RESOLVED, e.code)
            # 403 paywall, 405 method-not-allowed, 5xx, etc. — inconclusive.
            return (UNKNOWN, e.code)
        except (urllib.error.URLError, OSError, ValueError) as e:
            last_exc = e
            continue
    return (UNKNOWN, None)


def resolve_dois(
    dois: Iterable[str],
    cache: dict,
    fetcher: Fetcher = http_head_fetcher,
    force: bool = False,
) -> dict:
    """Populate `cache` with a verdict per DOI. Cached resolved/unresolved
    verdicts are kept unless `force`; UNKNOWN is always re-tried (transient)."""
    for doi in sorted(set(dois)):
        if not force:
            rec = cache.get(doi)
            if isinstance(rec, dict) and rec.get("status") in (RESOLVED, UNRESOLVED):
                continue
        status, code = fetcher(doi)
        cache[doi] = {"status": status, "http_status": code, "checked_at": _now_iso()}
    return cache


def load_cache(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def save_cache(path: Path, cache: dict) -> None:
    path.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Resolve capsule DOIs against doi.org into a committed cache.")
    ap.add_argument("--repo", default=".", help="Repo root to scan (default: cwd)")
    ap.add_argument("--cache", help="Cache path (default: <repo>/doi-cache.json)")
    ap.add_argument("--force", action="store_true", help="Re-check DOIs even if already cached resolved/unresolved")
    ap.add_argument("--dry-run", action="store_true", help="List DOIs that would be resolved; make no network calls, write nothing")
    args = ap.parse_args(argv)

    root = Path(args.repo).resolve()
    if not root.is_dir():
        sys.stderr.write(f"not a directory: {root}\n")
        return 2
    cache_path = Path(args.cache) if args.cache else root / CACHE_NAME

    dois = scan_repo_dois(root)
    cache = load_cache(cache_path)

    if args.dry_run:
        to_check = [d for d in sorted(dois)
                    if args.force or cache.get(d, {}).get("status") not in (RESOLVED, UNRESOLVED)]
        print(f"{len(dois)} DOIs found; {len(to_check)} would be resolved (cache: {cache_path})")
        for d in to_check:
            print(f"  CHECK {d}")
        return 0

    before = json.dumps(cache, sort_keys=True)
    cache = resolve_dois(dois, cache, force=args.force)
    after = json.dumps(cache, sort_keys=True)
    if before != after:
        save_cache(cache_path, cache)

    counts = {RESOLVED: 0, UNRESOLVED: 0, UNKNOWN: 0}
    for d in dois:
        st = cache.get(d, {}).get("status", UNKNOWN)
        counts[st] = counts.get(st, 0) + 1
    print(f"resolved={counts[RESOLVED]} unresolved={counts[UNRESOLVED]} "
          f"unknown={counts[UNKNOWN]} (of {len(dois)} DOIs) -> {cache_path}")
    if counts[UNRESOLVED]:
        print("UNRESOLVED DOIs (citation_resolution will BLOCK these):")
        for d in sorted(dois):
            if cache.get(d, {}).get("status") == UNRESOLVED:
                print(f"  {d}  (HTTP {cache[d].get('http_status')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
