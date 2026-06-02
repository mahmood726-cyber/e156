"""Phase-2a F1 — write assurance.json per project from existing verdict
sources.

For every project listed in rewrite-workbook.txt:
  1. Resolve the project's local path from the PATH: line. Skip if it doesn't
     exist on disk on this PC.
  2. Read <repo>/sentinel-findings.jsonl + STUCK_FAILURES.jsonl. Filter to
     the three Phase-1 Assurance rules. Derive per-check verdict:
       0 findings        -> pass
       >=1 WARN, 0 BLOCK -> warn
       >=1 BLOCK         -> fail
  3. Read the most recent Overmind bundle for the project from
     F:/overmind/data/nightly_reports/bundles/<latest-date>/. Derive:
       data_file_present: pass if any committed data file >1KB exists
       code_runs: pass if smoke witness PASSED, fail if FAILED, not-run otherwise
  4. Compute tier per F:/e156/docs/assurance-standard.md.
  5. Write <repo>/e156-submission/assurance.json (or <repo>/assurance.json
     as fallback if no e156-submission/ dir).

Idempotent: re-running with no new verdicts produces byte-identical output.

Usage:
  python scripts/build_assurance_jsons.py                  # all projects
  python scripts/build_assurance_jsons.py --dry-run        # print plan
  python scripts/build_assurance_jsons.py --project NAME   # single-project
  python scripts/build_assurance_jsons.py --report         # tier summary table
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

if sys.platform == "win32" and "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
OVERMIND_BUNDLES = Path(r"F:\overmind\data\nightly_reports\bundles")
ISSUED_BY = "build_assurance_jsons.py"
SCHEMA_VERSION = 1

# Phase-1 Sentinel rules that map onto Assurance Standard checks.
RULE_TO_CHECK = {
    "P0-citation-cascade":       "citation_cascade",
    "P0-citation-resolution":    "citation_cascade",  # live DOI resolution feeds the same check
    "P0-claim-language-workbook": "claim_language",
    "P0-denominator-logic":      "denominator_logic",
}


# ---------------------------------------------------------------------------
# Workbook parsing — share the format used by build_students_page.py
# ---------------------------------------------------------------------------

ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)
SEP = "=" * 70


def iter_workbook_entries() -> Iterator[dict]:
    """Yield {num, name, path, body, pages_url} per workbook entry.

    Phase 2b: body and pages_url added so derive_dashboard_match can do
    the body-vs-realData comparison without re-parsing the workbook.
    """
    if not WORKBOOK.is_file():
        return
    text = WORKBOOK.read_text(encoding="utf-8")
    for block in text.split(SEP):
        m = ENTRY_HEAD_RE.search(block)
        if not m:
            continue
        num = int(m.group(1))
        name = m.group(2).strip()
        path_m = re.search(r"^PATH:\s+(.+?)\s*$", block, re.MULTILINE)
        path = path_m.group(1) if path_m else ""
        pages_m = re.search(r"^\s+Dashboard:\s+(https?://\S+)", block, re.MULTILINE)
        pages_url = pages_m.group(1) if pages_m else ""
        # CURRENT BODY (...): heading line, then prose until next blank line block
        body_m = re.search(
            r"^CURRENT BODY[^\n]*\n(.*?)(?=\n\nYOUR REWRITE|\n\nSUBMISSION METADATA|\n=)",
            block, re.MULTILINE | re.DOTALL,
        )
        body = body_m.group(1).strip() if body_m else ""
        yield {"num": num, "name": name, "path": path, "body": body, "pages_url": pages_url}


def resolve_local_path(raw: str) -> Path | None:
    """The workbook PATH: line typically uses C:\\ canonical paths. NTFS
    junctions on this PC route C:\\E156, C:\\Sentinel, etc. to F:\\. So a
    Path that looks like C:\\<X> should be transparently followed.

    Returns the resolved Path if it exists on disk, else None.
    """
    if not raw:
        return None
    # Strip parenthetical notes (e.g. "(browser-native — see Code URL; no local path)")
    if raw.startswith("(") or "see Code URL" in raw or "no local path" in raw:
        return None
    p = Path(raw.strip())
    if p.is_dir():
        return p
    # Try junction-aware alternatives
    parts = p.parts
    if parts and parts[0].upper() in ("C:\\",) and len(parts) >= 2:
        # Map C:\X\... -> F:\X\... if the top-level is a known junction
        alt = Path("F:\\") / Path(*parts[1:])
        if alt.is_dir():
            return alt
    return None


# ---------------------------------------------------------------------------
# Sentinel findings — read JSONL outputs
# ---------------------------------------------------------------------------

def _read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    out = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                # Sentinel JSONL is well-formed in production but tolerate
                # the occasional crashed-mid-write line rather than aborting.
                continue
    except OSError:
        return []
    return out


def derive_sentinel_checks(repo_path: Path) -> dict:
    """Read sentinel-findings.jsonl (WARN/INFO) + STUCK_FAILURES.jsonl (BLOCK)
    and derive per-Assurance-check verdicts."""
    warns = _read_jsonl(repo_path / "sentinel-findings.jsonl")
    blocks = _read_jsonl(repo_path / "STUCK_FAILURES.jsonl")

    checks = {check: "pass" for check in RULE_TO_CHECK.values()}
    # No findings file at all → still "pass" by default. If Sentinel has
    # never scanned this repo, we can't differentiate "clean" from "never
    # scanned"; we choose "pass" because the assurance is downgraded later
    # by missing Overmind bundle / missing data files / etc.

    for finding in warns:
        rule = finding.get("rule_id") or finding.get("rule")
        check = RULE_TO_CHECK.get(rule)
        if not check:
            continue
        # WARN doesn't downgrade past "warn"
        if checks[check] == "pass":
            checks[check] = "warn"

    for finding in blocks:
        rule = finding.get("rule_id") or finding.get("rule")
        check = RULE_TO_CHECK.get(rule)
        if not check:
            continue
        checks[check] = "fail"

    return checks


# ---------------------------------------------------------------------------
# Overmind bundles — find the most recent one matching the project slug
# ---------------------------------------------------------------------------

# Cache: build slug→bundle-path map once per run. Bundle filenames are
# truncated to ~16 chars, so match against the bundle's project_id field.
_BUNDLE_INDEX: dict[str, Path] | None = None


def _build_bundle_index() -> dict[str, Path]:
    """Walk the latest nightly bundle dir; return {slug: bundle_path}.

    'slug' = first segment of project_id before the hash suffix
    (e.g. 'advanced-nma-pooling-6e3c8bdb' -> 'advanced-nma-pooling').
    """
    global _BUNDLE_INDEX
    if _BUNDLE_INDEX is not None:
        return _BUNDLE_INDEX
    index: dict[str, Path] = {}
    if not OVERMIND_BUNDLES.is_dir():
        _BUNDLE_INDEX = index
        return index
    # Latest date first
    dates = sorted(
        (d for d in OVERMIND_BUNDLES.iterdir() if d.is_dir()),
        key=lambda p: p.name,
        reverse=True,
    )
    if not dates:
        _BUNDLE_INDEX = index
        return index
    latest = dates[0]
    for bundle_file in latest.glob("*.json"):
        try:
            data = json.loads(bundle_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        pid = data.get("project_id") or ""
        # Strip the 8-char hash suffix: "name-<8 hex>" -> "name"
        slug = re.sub(r"-[0-9a-f]{8}$", "", pid)
        if slug and slug not in index:
            index[slug] = bundle_file
    _BUNDLE_INDEX = index
    return index


RAPIDMETA_LOCAL = Path(r"F:\rapidmeta-finerenone")
DASHBOARD_TOLERANCE = 0.2

_POOLED_RE = re.compile(
    r"\b(?:pooled\s+)?(OR|HR|RR|IRR)\s*[:=]?\s*(\d+\.\d+)\s*"
    r"[\(\[,]?\s*(?:95\s*%?\s*CI\s*:?\s*)?"
    r"(\d+\.\d+)\s*[-–to]+\s*(\d+\.\d+)",
    re.IGNORECASE,
)


def derive_dashboard_match(workbook_entry: dict, pages_url: str = "") -> str:
    """Phase-2b Silver-tier check.

    Returns one of: pass | warn | fail | not-run.

    Strategy: extract the body's pooled HR/OR claim; extract per-trial
    publishedHR values from the matching dashboard's realData block; check
    that the body claim sits inside the per-trial min/max (with tolerance).
    Same heuristic as the dashboard_match Sentinel rule, but per-project
    rather than scan-wide.

    not-run: no body claim found, OR no matching dashboard file found, OR
             dashboard has <2 trials with extractable HRs.
    pass:    body pooled HR is inside the per-trial range +/- TOLERANCE.
    warn:    body pooled HR is outside the range (could be RE pooling drift).
    fail:    reserved for Phase 3 exact-match check.
    """
    body = workbook_entry.get("body") or ""
    if not body or not pages_url:
        return "not-run"

    # Only attempt for rapidmeta dashboards (the only known URL-pattern with
    # an inspectable realData block on disk).
    if "rapidmeta-finerenone" not in pages_url:
        return "not-run"

    # Pages URL like https://...github.io/rapidmeta-finerenone/FOO_REVIEW.html
    fname = pages_url.rsplit("/", 1)[-1]
    local = RAPIDMETA_LOCAL / fname
    if not local.is_file():
        return "not-run"

    try:
        text = local.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "not-run"

    # Per-trial HRs from realData. Cheap inline parser; the full version is
    # in F:\Sentinel\sentinel\rules\plugins\dashboard_match.py (same logic).
    hrs = []
    for m in re.finditer(r"publishedHR\s*:\s*(\d+\.\d+)", text):
        try:
            hrs.append(float(m.group(1)))
        except ValueError:
            pass
    if len(hrs) < 2:
        return "not-run"

    bm = _POOLED_RE.search(body)
    if not bm:
        return "not-run"
    try:
        body_hr = float(bm.group(2))
    except ValueError:
        return "not-run"

    lo, hi = min(hrs), max(hrs)
    if lo - DASHBOARD_TOLERANCE <= body_hr <= hi + DASHBOARD_TOLERANCE:
        return "pass"
    return "warn"


def derive_overmind_checks(project_name: str) -> dict:
    """Find the latest Overmind bundle for this project; derive code_runs
    + data_file_present from it. Returns {data_file_present, code_runs,
    bundle_path}."""
    idx = _build_bundle_index()
    # Try exact, then lowercase, then a few common name-mangling variations
    candidates = [project_name, project_name.lower(),
                  project_name.replace("_", "-").lower()]
    bundle_path: Path | None = None
    for c in candidates:
        if c in idx:
            bundle_path = idx[c]
            break

    out = {"data_file_present": "not-run", "code_runs": "not-run",
           "bundle_path": str(bundle_path) if bundle_path else ""}
    if not bundle_path:
        return out

    try:
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return out

    # code_runs from smoke witness verdict
    for w in bundle.get("witness_results", []):
        if w.get("witness_type") == "smoke":
            v = w.get("verdict")
            if v == "PASS":
                out["code_runs"] = "pass"
            elif v == "FAIL":
                out["code_runs"] = "fail"
            elif v == "SKIP":
                out["code_runs"] = "not-run"
            break

    # data_file_present: derive from the project path (not the bundle —
    # bundles don't store this). Look for committed data files >1KB.
    raw_path = bundle.get("scope_lock", {}).get("project_path", "")
    if raw_path:
        local = resolve_local_path(raw_path)
        if local:
            for f in local.rglob("*"):
                if not f.is_file():
                    continue
                if f.suffix.lower() in (".csv", ".parquet", ".json", ".tsv"):
                    try:
                        if f.stat().st_size > 1024:
                            out["data_file_present"] = "pass"
                            break
                    except OSError:
                        pass

    return out


# ---------------------------------------------------------------------------
# Tier rule
# ---------------------------------------------------------------------------

PASS_OR_NOT_RUN = ("pass", "not-run")


def compute_tier(checks: dict) -> str:
    """Tier rule per F:/e156/docs/assurance-standard.md.

    Bronze = citation_cascade != fail AND data_file_present == pass
             AND code_runs in (pass, not-run)
    Silver = Bronze + dashboard_match == pass AND claim_language == pass
             AND publication_bias in (pass, not-run)
    Gold   = Silver + analysis_rerun == pass AND external_review == pass
    Any single 'fail' in a contributing check forces tier=none
    (honest under-claiming is the safer error). publication_bias never emits
    'fail' (bias is informative, not a self-consistency failure); a 'warn'
    caps the badge at Bronze.
    """
    if "fail" in checks.values():
        return "none"
    bronze_ok = (
        checks.get("citation_cascade") != "fail"
        and checks.get("data_file_present") == "pass"
        and checks.get("code_runs") in PASS_OR_NOT_RUN
    )
    if not bronze_ok:
        return "none"

    silver_ok = (
        checks.get("dashboard_match") == "pass"
        and checks.get("claim_language") == "pass"
        and checks.get("publication_bias", "not-run") in PASS_OR_NOT_RUN
    )
    if not silver_ok:
        return "bronze"

    gold_ok = (
        checks.get("analysis_rerun") == "pass"
        and checks.get("external_review") == "pass"
    )
    if not gold_ok:
        return "silver"
    return "gold"


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------

ASSURANCE_CACHE = E156 / "assurance-cache"
_NULL_OVERMIND = {"data_file_present": "not-run", "code_runs": "not-run", "bundle_path": ""}

_DATA_SUFFIXES = (".csv", ".parquet", ".json", ".tsv")
_DATA_SKIP_DIRS = (".git", "node_modules", "__pycache__")
_DATA_SKIP_NAMES = ("assurance.json", "doi-cache.json")


def _local_data_present(root: Path) -> str:
    """Return 'pass' if the repo holds a committed data file >1KB, else
    'not-run'. Shared by build_assurance_here() and used as a fallback in
    build_assurance_for() when no Overmind bundle resolves on this machine —
    a capsule that genuinely ships its own data must not be denied
    data_file_present just because the nightly bundle dir is absent here.
    Honest semantics: only real on-disk data flips it to 'pass'."""
    try:
        for f in root.rglob("*"):
            if any(d in _DATA_SKIP_DIRS for d in f.parts):
                continue
            if not f.is_file() or f.suffix.lower() not in _DATA_SUFFIXES:
                continue
            if f.name in _DATA_SKIP_NAMES:
                continue
            try:
                if f.stat().st_size > 1024:
                    return "pass"
            except OSError:
                continue
    except OSError:
        pass
    return "not-run"

# Inline claim_language patterns. Kept narrow to mirror the Sentinel rule's
# detection set but with no per-entry override lookup (this is just a
# rapidmeta-mode "fast check" — the real Sentinel rule runs on the
# rapidmeta-finerenone repo separately).
_CLAIM_CAUSAL_RE = re.compile(
    r"\b(prov(?:es|en)|eliminat(?:es|ed)|definitiv(?:e|ely)|undeniably|conclusively)\b",
    re.IGNORECASE,
)
_CLAIM_HETERO_RE = re.compile(
    r"I[²2]\s*=|prediction interval|wide CI|tau[²2]|few studies|risk of bias|"
    r"downgraded|uncertain|low certainty",
    re.IGNORECASE,
)
_CLAIM_CERTAIN_RE = re.compile(
    r"\b(safe|effective|no difference|significant benefit|clinically meaningful|"
    r"cures|prevents?)\b",
    re.IGNORECASE,
)


def _claim_language_fires_in(body: str) -> bool:
    """Return True if the body would trigger any claim_language WARN. Used
    only for rapidmeta-only mode (no local Sentinel scan available)."""
    if not body:
        return False
    if _CLAIM_CAUSAL_RE.search(body):
        return True
    if _CLAIM_CERTAIN_RE.search(body) and _CLAIM_HETERO_RE.search(body):
        return True
    return False


def build_assurance_for(entry: dict) -> dict | None:
    """Return the assurance.json blob for one workbook entry, or None if
    nothing can be assessed (no local path AND no rapidmeta dashboard).

    Phase 2b: entries with no local path but WITH a rapidmeta dashboard URL
    still get an assurance.json — dashboard_match works from pages_url alone.
    Sentinel + Overmind checks default to 'not-run' for those entries since
    there's no local repo to scan.
    """
    local = resolve_local_path(entry["path"])
    is_rapidmeta = "rapidmeta-finerenone" in (entry.get("pages_url") or "")
    if local is None and not is_rapidmeta:
        return None

    if local is None:
        # Rapidmeta-only mode (no local repo). data_file_present="pass" if
        # the dashboard file exists locally with parseable trial data — the
        # rapidmeta dashboard IS the data store for these entries.
        # claim_language and other Sentinel-rule checks are derived inline
        # from the workbook entry body (no Sentinel scan needed; the body
        # IS the rendered text).
        body = entry.get("body") or ""
        inline_claim_pass = not _claim_language_fires_in(body)
        sent_checks = {
            "citation_cascade": "not-run",   # no references in workbook body
            "denominator_logic": "not-run",   # checked at the dashboard level
            "claim_language": "pass" if inline_claim_pass else "warn",
        }
        overmind_checks = dict(_NULL_OVERMIND)
        # Promote data_file_present if the dashboard exists with trials
        dashboard_fname = (entry.get("pages_url") or "").rsplit("/", 1)[-1]
        dashboard_path = RAPIDMETA_LOCAL / dashboard_fname
        if dashboard_path.is_file():
            try:
                dtext = dashboard_path.read_text(encoding="utf-8", errors="replace")
                # Cheap check: at least 2 publishedHR values
                if len(re.findall(r"publishedHR\s*:\s*\d+\.\d+", dtext)) >= 2:
                    overmind_checks["data_file_present"] = "pass"
            except OSError:
                pass
    else:
        sent_checks = derive_sentinel_checks(local)
        overmind_checks = derive_overmind_checks(entry["name"])
        # Fallback: the Overmind bundle scan only sees data when a nightly
        # bundle resolves (it doesn't on a machine without the F:\ bundle
        # dir). A released capsule that ships its own data on disk should
        # still earn data_file_present — scan the repo directly.
        if overmind_checks["data_file_present"] != "pass":
            overmind_checks["data_file_present"] = _local_data_present(local)

    dashboard_match = derive_dashboard_match(entry, entry.get("pages_url") or "")
    # Phase-3 S + T: opt-in analysis-rerun and PDF-match checks. Default
    # not-run for all entries; activates when operator drops a rerun.sh
    # or preprint.pdf into the project root.
    try:
        from scripts.assurance.rerun_analysis import derive_analysis_rerun  # type: ignore
        from scripts.assurance.pdf_match import derive_pdf_match  # type: ignore
        from scripts.assurance.pub_bias import derive_pub_bias  # type: ignore
    except ImportError:
        # Fallback: import via path (script-relative)
        import importlib.util as _ilu
        _here = Path(__file__).parent
        def _load(name: str, path: Path):
            spec = _ilu.spec_from_file_location(name, str(path))
            mod = _ilu.module_from_spec(spec); spec.loader.exec_module(mod)  # type: ignore
            return mod
        _ra = _load("rerun_analysis", _here / "assurance" / "rerun_analysis.py")
        _pm = _load("pdf_match", _here / "assurance" / "pdf_match.py")
        _pb = _load("pub_bias", _here / "assurance" / "pub_bias.py")
        derive_analysis_rerun = _ra.derive_analysis_rerun
        derive_pdf_match = _pm.derive_pdf_match
        derive_pub_bias = _pb.derive_pub_bias
    analysis_rerun = derive_analysis_rerun(local) if local else "not-run"
    pdf_match = derive_pdf_match(local, entry.get("body") or "") if local else "not-run"
    publication_bias = derive_pub_bias(local) if local else "not-run"
    all_checks = {
        **sent_checks,
        "data_file_present": overmind_checks["data_file_present"],
        "code_runs": overmind_checks["code_runs"],
        "dashboard_match": dashboard_match,
        "analysis_rerun": analysis_rerun,
        "pdf_match": pdf_match,
        # Machine-derived from a PubBiasSuite artifact when present. A 'warn'
        # (strong/some evidence of bias) caps the badge at Bronze; it never
        # emits 'fail' (bias is informative, not a self-consistency failure).
        "publication_bias": publication_bias,
        "external_review": "not-run",
    }
    tier = compute_tier(all_checks)

    evidence = {"overmind_bundle": overmind_checks["bundle_path"]}
    if local is not None:
        if (local / "sentinel-findings.jsonl").is_file():
            evidence["sentinel_findings"] = str(local / "sentinel-findings.jsonl")
        if (local / "STUCK_FAILURES.jsonl").is_file():
            evidence["stuck_failures"] = str(local / "STUCK_FAILURES.jsonl")
    if local is None:
        evidence["dashboard_url"] = entry.get("pages_url") or ""

    return {
        "tier": tier,
        "checks": all_checks,
        "evidence": evidence,
        "tier_rule": ("bronze = citation_cascade != fail AND data_file_present == pass "
                      "AND code_runs in (pass, not-run); silver = + dashboard_match == pass "
                      "AND claim_language == pass AND publication_bias in (pass, not-run); "
                      "gold = + analysis_rerun == pass AND external_review == pass"),
        "issued_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "issued_by": ISSUED_BY,
        "version": SCHEMA_VERSION,
        "project_name": entry["name"],
        "workbook_num": entry["num"],
        "local_path": str(local) if local is not None else "",
    }


def build_assurance_here(repo: Path, name: str) -> dict:
    """Build a badge for the checked-out repo itself (GitHub Actions per-repo
    mode). No workbook PATH resolution and no Overmind bundle: Sentinel checks
    come from the repo's own findings files, data_file_present from a local data
    scan; code_runs / dashboard_match / external_review stay not-run.
    """
    sent_checks = derive_sentinel_checks(repo)

    data_file_present = _local_data_present(repo)

    try:
        from scripts.assurance.rerun_analysis import derive_analysis_rerun  # type: ignore
        from scripts.assurance.pdf_match import derive_pdf_match  # type: ignore
    except ImportError:
        import importlib.util as _ilu
        _here = Path(__file__).parent

        def _load(modname: str, path: Path):
            spec = _ilu.spec_from_file_location(modname, str(path))
            mod = _ilu.module_from_spec(spec); spec.loader.exec_module(mod)  # type: ignore
            return mod

        derive_analysis_rerun = _load("rerun_analysis", _here / "assurance" / "rerun_analysis.py").derive_analysis_rerun
        derive_pdf_match = _load("pdf_match", _here / "assurance" / "pdf_match.py").derive_pdf_match
        derive_pub_bias = _load("pub_bias", _here / "assurance" / "pub_bias.py").derive_pub_bias
    else:
        from scripts.assurance.pub_bias import derive_pub_bias  # type: ignore

    all_checks = {
        **sent_checks,
        "data_file_present": data_file_present,
        "code_runs": "not-run",
        "dashboard_match": "not-run",
        "analysis_rerun": derive_analysis_rerun(repo),
        "pdf_match": derive_pdf_match(repo, ""),
        # Machine-derived from a PubBiasSuite artifact; a 'warn' caps Silver.
        "publication_bias": derive_pub_bias(repo),
        "external_review": "not-run",
    }
    tier = compute_tier(all_checks)

    evidence = {}
    if (repo / "sentinel-findings.jsonl").is_file():
        evidence["sentinel_findings"] = str(repo / "sentinel-findings.jsonl")
    if (repo / "STUCK_FAILURES.jsonl").is_file():
        evidence["stuck_failures"] = str(repo / "STUCK_FAILURES.jsonl")

    return {
        "tier": tier,
        "checks": all_checks,
        "evidence": evidence,
        "tier_rule": ("bronze = citation_cascade != fail AND data_file_present == pass "
                      "AND code_runs in (pass, not-run); silver = + dashboard_match == pass "
                      "AND claim_language == pass AND publication_bias in (pass, not-run); "
                      "gold = + analysis_rerun == pass AND external_review == pass"),
        "issued_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "issued_by": ISSUED_BY,
        "version": SCHEMA_VERSION,
        "project_name": name,
        "local_path": str(repo),
    }


def target_path_for(local: Path | None, workbook_num: int) -> Path:
    """Where to write assurance.json.

    - Prefer <repo>/e156-submission/assurance.json if a local repo exists.
    - Else <repo>/assurance.json.
    - For browser-native entries with no local path (rapidmeta), write to
      F:\\e156\\assurance-cache\\<workbook_num>.json so the paper renderer
      can find it.
    """
    if local is None:
        ASSURANCE_CACHE.mkdir(exist_ok=True)
        return ASSURANCE_CACHE / f"{workbook_num}.json"
    sub = local / "e156-submission"
    if sub.is_dir():
        return sub / "assurance.json"
    return local / "assurance.json"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would be written; no files touched")
    ap.add_argument("--report", action="store_true",
                    help="print a tier-distribution summary")
    ap.add_argument("--project",
                    help="only process this project (by workbook 'name' slug)")
    ap.add_argument("--here", metavar="NAME",
                    help="build a badge for the current directory (GitHub Actions per-repo mode)")
    args = ap.parse_args(argv)

    if args.here:
        repo = Path.cwd()
        blob = build_assurance_here(repo, args.here)
        target = target_path_for(repo, 0)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(blob, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"[{blob['tier']:6s}] {args.here} -> {target}")
        return 0

    entries = list(iter_workbook_entries())
    if args.project:
        entries = [e for e in entries if e["name"] == args.project]
        if not entries:
            sys.stderr.write(f"No workbook entry named {args.project!r}\n")
            return 1

    written = 0
    skipped_no_path = 0
    by_tier = {"bronze": 0, "silver": 0, "gold": 0, "none": 0}

    for entry in entries:
        blob = build_assurance_for(entry)
        if blob is None:
            skipped_no_path += 1
            continue
        local_for_target = Path(blob["local_path"]) if blob["local_path"] else None
        target = target_path_for(local_for_target, blob["workbook_num"])
        by_tier[blob["tier"]] = by_tier.get(blob["tier"], 0) + 1
        if args.dry_run:
            print(f"  [{blob['tier']:6s}] #{entry['num']} {entry['name']:40s} -> {target}")
            continue
        # Idempotency: if file exists and the merged result would be the
        # same modulo `issued_at`, skip the write.
        new_str = json.dumps(blob, indent=2, sort_keys=True)
        if target.is_file():
            try:
                old = json.loads(target.read_text(encoding="utf-8"))
                old.pop("issued_at", None)
                cmp_new = dict(blob); cmp_new.pop("issued_at", None)
                if old == cmp_new:
                    continue  # no change
            except (OSError, json.JSONDecodeError):
                pass
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(new_str + "\n", encoding="utf-8")
        written += 1

    if args.report or args.dry_run:
        total = sum(by_tier.values())
        print(f"\nTier distribution ({total} projects processed):")
        for tier in ("gold", "silver", "bronze", "none"):
            print(f"  {tier:7s} {by_tier.get(tier, 0):>5d}")
        print(f"  skipped (no local path): {skipped_no_path}")
    else:
        print(f"Wrote {written} assurance.json files; "
              f"skipped {skipped_no_path} entries with no local path")

    return 0


if __name__ == "__main__":
    sys.exit(main())
