"""Master orchestrator — run the e156 generators in dependency order.

The generators in scripts/ have implicit dependencies:

    generate_rapidmeta_entries.py  ->  appends to rewrite-workbook.txt
        build_paper_pages.py       ->  reads workbook, writes paper/<N>.html
        build_students_page.py     ->  reads workbook, writes students.html
        build_library.py           ->  reads workbook, writes e156-library.html
    tests/test_no_placeholder_leak.py  ->  validates students.html + workbook

Before this script, those were called ad-hoc and the dependency order was
implicit. This script makes the order explicit, emits a JSON event log to
F:/e156/.run-cycle/<timestamp>.json for observability, and aborts the cycle
if any step fails (rather than running downstream generators against stale
state).

Idempotent: running twice with no source changes does not change any
output bytes (modulo whatever the generators themselves choose to emit).

Usage:
    python scripts/run_full_cycle.py                # run everything
    python scripts/run_full_cycle.py --dry-run      # print plan, don't execute
    python scripts/run_full_cycle.py --skip-sync    # skip rapidmeta sync (offline)
    python scripts/run_full_cycle.py --skip-tests   # skip validation gate (NOT recommended)
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
EVENT_DIR = E156 / ".run-cycle"


def _event(name, status, *, started_at, ended_at, stdout="", stderr="", rc=None, skipped=False):
    return {
        "step": name,
        "status": status,  # "ok" | "fail" | "skip"
        "started_at": started_at,
        "ended_at": ended_at,
        "duration_s": round(ended_at - started_at, 2),
        "skipped": skipped,
        "returncode": rc,
        "stdout_tail": (stdout or "")[-2000:],
        "stderr_tail": (stderr or "")[-2000:],
    }


def _run_step(name, cmd, *, skip=False, cwd=E156):
    started = time.time()
    if skip:
        print(f"[SKIP] {name}")
        return _event(name, "skip", started_at=started, ended_at=time.time(), skipped=True)
    print(f"[RUN ] {name}  ({' '.join(cmd)})")
    try:
        proc = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=900,
        )
    except subprocess.TimeoutExpired as e:
        ended = time.time()
        print(f"[FAIL] {name}  (timeout after {ended-started:.0f}s)")
        return _event(name, "fail", started_at=started, ended_at=ended,
                      stderr=f"TIMEOUT: {e!r}", rc=-1)
    ended = time.time()
    ok = proc.returncode == 0
    icon = "ok  " if ok else "FAIL"
    print(f"[{icon}] {name}  rc={proc.returncode}  ({ended-started:.1f}s)")
    if not ok:
        # surface the tail so the operator sees the error inline
        for line in (proc.stderr or proc.stdout or "").splitlines()[-15:]:
            print(f"    {line}")
    return _event(name, "ok" if ok else "fail", started_at=started, ended_at=ended,
                  stdout=proc.stdout, stderr=proc.stderr, rc=proc.returncode)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print plan, don't execute")
    ap.add_argument("--skip-sync", action="store_true",
                    help="skip the rapidmeta orphan sync (offline runs)")
    ap.add_argument("--skip-tests", action="store_true",
                    help="skip the validation gate (NOT recommended)")
    args = ap.parse_args(argv)

    plan = [
        ("rapidmeta-sync",
         [sys.executable, "scripts/generate_rapidmeta_entries.py"],
         args.skip_sync),
        ("paper-pages",
         [sys.executable, "scripts/build_paper_pages.py"],
         False),
        ("students-page",
         [sys.executable, "scripts/build_students_page.py"],
         False),
        ("library",
         [sys.executable, "scripts/build_library.py"],
         False),
        ("validate",
         [sys.executable, "-m", "pytest", "tests/test_no_placeholder_leak.py",
          "-q", "--maxfail=1"],
         args.skip_tests),
    ]

    if args.dry_run:
        print("Dry run — plan:")
        for name, cmd, skip in plan:
            tag = "SKIP" if skip else "RUN "
            print(f"  [{tag}] {name}  ({' '.join(cmd)})")
        return 0

    EVENT_DIR.mkdir(exist_ok=True)
    cycle_started = datetime.now(timezone.utc).isoformat()
    events = []

    for name, cmd, skip in plan:
        ev = _run_step(name, cmd, skip=skip)
        events.append(ev)
        if ev["status"] == "fail":
            print(f"\n[ABORT] {name} failed; downstream steps skipped to avoid stale-state propagation.")
            # mark remaining as skipped-by-abort
            remaining = [n for n, _, _ in plan[len(events):]]
            for n in remaining:
                events.append({"step": n, "status": "skip", "skipped": True,
                               "reason": f"aborted by upstream failure in {name}"})
            break

    cycle_ended = datetime.now(timezone.utc).isoformat()
    report = {
        "cycle_started_at": cycle_started,
        "cycle_ended_at": cycle_ended,
        "events": events,
        "overall_status": "ok" if all(e["status"] in ("ok", "skip") for e in events) else "fail",
    }
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = EVENT_DIR / f"{timestamp}.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\n[REPORT] {out_path}")
    print(f"[{report['overall_status'].upper()}] cycle finished")
    return 0 if report["overall_status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
