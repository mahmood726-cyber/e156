"""Run the E156 verification suite and write a summary report."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

import run_generated_smoke_tests


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_PATH = ROOT / "verification-report.json"


def _base_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    return env


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_local_e156_tests(root: Path = ROOT) -> dict:
    started_at = iso_now()
    t0 = perf_counter()
    test_target = root / "tests" / "test_smoke.py"
    cmd = ["pytest", "-q", "-p", "no:cacheprovider", str(test_target)]
    proc = subprocess.run(
        cmd,
        cwd=root,
        text=True,
        capture_output=True,
        env=_base_env(),
        check=False,
    )
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "command": cmd,
        "cwd": str(root),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "target": str(test_target),
        "started_at": started_at,
        "duration_seconds": round(perf_counter() - t0, 3),
    }


def run_generated_suite(
    report_path: Path,
    project_filters: list[str] | None = None,
    max_tests: int = 0,
    jobs: int = run_generated_smoke_tests.DEFAULT_JOBS,
) -> dict:
    return run_generated_smoke_tests.run_suite(
        report_path,
        project_filters=project_filters,
        max_tests=max_tests,
        jobs=jobs,
    )


def build_suite_report(
    local_result: dict | None,
    generated_summary: dict | None,
    project_filters: list[str] | None = None,
    duration_seconds: float | None = None,
    started_at: str | None = None,
) -> dict:
    local_ok = local_result is None or local_result["ok"]
    generated_ok = generated_summary is None or generated_summary["failed"] == 0
    return {
        "overall_ok": local_ok and generated_ok,
        "local_e156_tests": local_result,
        "generated_smoke_tests": generated_summary,
        "project_filters": list(project_filters or []),
        "started_at": started_at,
        "duration_seconds": duration_seconds,
    }


def write_report(report: dict, path: Path) -> None:
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the E156 verification suite.")
    parser.add_argument("--audit-report", default=str(run_generated_smoke_tests.REPORT_PATH), help="Path to audit-report.json")
    parser.add_argument("--out", default=str(DEFAULT_REPORT_PATH), help="Path to write verification JSON")
    parser.add_argument("--project", action="append", dest="project_filters", help="Substring filter for generated smoke-test repos; can be repeated")
    parser.add_argument("--max-generated", type=int, default=0, help="Limit generated smoke tests after filtering")
    parser.add_argument("--generated-jobs", type=int, default=run_generated_smoke_tests.DEFAULT_JOBS, help="Parallel workers for generated smoke tests")
    parser.add_argument("--skip-local", action="store_true", help="Skip local E156 pytest checks")
    parser.add_argument("--skip-generated", action="store_true", help="Skip generated cross-repo smoke tests")
    parser.add_argument("--json", action="store_true", help="Print the full JSON report to stdout")
    args = parser.parse_args()

    started_at = iso_now()
    t0 = perf_counter()
    local_result = None if args.skip_local else run_local_e156_tests(ROOT)
    generated_summary = None if args.skip_generated else run_generated_suite(
        Path(args.audit_report),
        project_filters=args.project_filters,
        max_tests=args.max_generated,
        jobs=args.generated_jobs,
    )
    report = build_suite_report(
        local_result,
        generated_summary,
        project_filters=args.project_filters,
        duration_seconds=round(perf_counter() - t0, 3),
        started_at=started_at,
    )
    write_report(report, Path(args.out))

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        if local_result is not None:
            status = "PASS" if local_result["ok"] else "FAIL"
            print(f"{status} local {local_result['target']}")
        if generated_summary is not None:
            print(
                "generated "
                f"passed={generated_summary['passed']} "
                f"failed={generated_summary['failed']} "
                f"total={generated_summary['total']}"
            )
            print(f"generated_jobs={generated_summary['jobs']}")
        if report["project_filters"]:
            print(f"filters={','.join(report['project_filters'])}")
        if report["duration_seconds"] is not None:
            print(f"duration={report['duration_seconds']:.3f}s")
        print(f"overall_ok={report['overall_ok']}")
        print(f"report={Path(args.out)}")

    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
