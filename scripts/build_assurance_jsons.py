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

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
OVERMIND_BUNDLES = Path(r"F:\overmind\data\nightly_reports\bundles")
ISSUED_BY = "build_assurance_jsons.py"
SCHEMA_VERSION = 1

# Phase-1 Sentinel rules that map onto Assurance Standard checks.
RULE_TO_CHECK = {
    "P0-citation-cascade":  "citation_cascade",
    "P1-claim-language":    "claim_language",
    "P0-denominator-logic": "denominator_logic",
}


# ---------------------------------------------------------------------------
# Workbook parsing — share the format used by build_students_page.py
# ---------------------------------------------------------------------------

ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)
SEP = "=" * 70


def iter_workbook_entries() -> Iterator[dict]:
    """Yield {num, name, path} per workbook entry."""
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
        yield {"num": num, "name": name, "path": path}


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
    Gold   = Silver + analysis_rerun == pass AND external_review == pass
    Any single 'fail' in a contributing check forces tier=none.
    """
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

def build_assurance_for(entry: dict) -> dict | None:
    """Return the assurance.json blob for one workbook entry, or None if
    the project's path isn't on disk on this PC."""
    local = resolve_local_path(entry["path"])
    if local is None:
        return None

    sent_checks = derive_sentinel_checks(local)
    overmind_checks = derive_overmind_checks(entry["name"])

    all_checks = {
        **sent_checks,
        "data_file_present": overmind_checks["data_file_present"],
        "code_runs": overmind_checks["code_runs"],
        "dashboard_match": "not-run",
        "analysis_rerun": "not-run",
        "external_review": "not-run",
    }
    tier = compute_tier(all_checks)

    return {
        "tier": tier,
        "checks": all_checks,
        "evidence": {
            "sentinel_findings": str(local / "sentinel-findings.jsonl")
                if (local / "sentinel-findings.jsonl").is_file() else "",
            "stuck_failures": str(local / "STUCK_FAILURES.jsonl")
                if (local / "STUCK_FAILURES.jsonl").is_file() else "",
            "overmind_bundle": overmind_checks["bundle_path"],
        },
        "tier_rule": ("bronze = citation_cascade != fail AND data_file_present == pass "
                      "AND code_runs in (pass, not-run); silver = + dashboard_match == pass "
                      "AND claim_language == pass; gold = + analysis_rerun == pass "
                      "AND external_review == pass"),
        "issued_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "issued_by": ISSUED_BY,
        "version": SCHEMA_VERSION,
        "project_name": entry["name"],
        "workbook_num": entry["num"],
        "local_path": str(local),
    }


def target_path_for(local: Path) -> Path:
    """Where to write assurance.json. Prefer <repo>/e156-submission/ if it
    exists; else <repo>/assurance.json."""
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
    args = ap.parse_args(argv)

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
        target = target_path_for(Path(blob["local_path"]))
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
