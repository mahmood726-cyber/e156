"""Refresh audit and verification artifacts, then write a combined maintenance summary."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

import audit_all_projects
import run_verification_suite


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_PATH = ROOT / "maintenance-report.json"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def refresh_audit(
    report_path: Path = audit_all_projects.DEFAULT_REPORT_PATH,
    project_filters: list[str] | None = None,
    limit: int = 0,
) -> dict:
    report = audit_all_projects.run_audit(project_filters=project_filters, limit=limit)
    audit_all_projects.print_report(report)
    audit_all_projects.save_report(report, report_path)
    return report


def load_json_report(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def refresh_verification(
    audit_report_path: Path = audit_all_projects.DEFAULT_REPORT_PATH,
    report_path: Path = run_verification_suite.DEFAULT_REPORT_PATH,
    project_filters: list[str] | None = None,
    max_generated: int = 0,
    generated_jobs: int = run_verification_suite.run_generated_smoke_tests.DEFAULT_JOBS,
) -> dict:
    local_result = run_verification_suite.run_local_e156_tests(ROOT)
    generated_summary = run_verification_suite.run_generated_suite(
        audit_report_path,
        project_filters=project_filters,
        max_tests=max_generated,
        jobs=generated_jobs,
    )
    report = run_verification_suite.build_suite_report(
        local_result,
        generated_summary,
        project_filters=project_filters,
    )
    run_verification_suite.write_report(report, report_path)
    return report


def build_maintenance_report(
    audit_report: dict,
    verification_report: dict,
    audit_report_path: Path,
    verification_report_path: Path,
    project_filters: list[str] | None = None,
    duration_seconds: float | None = None,
    started_at: str | None = None,
) -> dict:
    audit_ok = (
        audit_report.get("p0_count", 0) == 0
        and audit_report.get("p1_count", 0) == 0
        and audit_report.get("p2_count", 0) == 0
    )
    verification_ok = bool(verification_report.get("overall_ok"))
    generated = verification_report.get("generated_smoke_tests") or {}
    local = verification_report.get("local_e156_tests") or {}
    return {
        "overall_ok": audit_ok and verification_ok,
        "audit_ok": audit_ok,
        "verification_ok": verification_ok,
        "audit_report_path": str(audit_report_path),
        "verification_report_path": str(verification_report_path),
        "project_filters": list(project_filters or []),
        "started_at": started_at,
        "duration_seconds": duration_seconds,
        "audit_summary": {
            "total_projects": audit_report.get("total_projects", 0),
            "clean_count": audit_report.get("clean_count", 0),
            "p0_count": audit_report.get("p0_count", 0),
            "p1_count": audit_report.get("p1_count", 0),
            "p2_count": audit_report.get("p2_count", 0),
        },
        "verification_summary": {
            "local_ok": bool(local.get("ok")),
            "generated_total": generated.get("total", 0),
            "generated_passed": generated.get("passed", 0),
            "generated_failed": generated.get("failed", 0),
        },
    }


def write_report(report: dict, path: Path) -> None:
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the E156 maintenance cycle.")
    parser.add_argument("--audit-report", default=str(audit_all_projects.DEFAULT_REPORT_PATH), help="Path to audit-report.json")
    parser.add_argument("--verification-report", default=str(run_verification_suite.DEFAULT_REPORT_PATH), help="Path to verification-report.json")
    parser.add_argument("--out", default=str(DEFAULT_REPORT_PATH), help="Path to write maintenance-report.json")
    parser.add_argument("--project", action="append", dest="project_filters", help="Substring filter for project path/name; can be repeated")
    parser.add_argument("--limit", type=int, default=0, help="Limit audited projects after filtering")
    parser.add_argument("--max-generated", type=int, default=0, help="Limit generated smoke tests after filtering")
    parser.add_argument("--generated-jobs", type=int, default=run_verification_suite.run_generated_smoke_tests.DEFAULT_JOBS, help="Parallel workers for generated smoke tests")
    parser.add_argument("--skip-audit", action="store_true", help="Reuse the existing audit report instead of refreshing it")
    parser.add_argument("--skip-verification", action="store_true", help="Reuse the existing verification report instead of refreshing it")
    parser.add_argument("--json", action="store_true", help="Print the full JSON report to stdout")
    args = parser.parse_args()

    audit_report_path = Path(args.audit_report)
    verification_report_path = Path(args.verification_report)
    maintenance_report_path = Path(args.out)

    started_at = iso_now()
    t0 = perf_counter()
    audit_report = load_json_report(audit_report_path) if args.skip_audit else refresh_audit(
        audit_report_path,
        project_filters=args.project_filters,
        limit=args.limit,
    )
    verification_report = (
        load_json_report(verification_report_path)
        if args.skip_verification
        else refresh_verification(
            audit_report_path,
            verification_report_path,
            project_filters=args.project_filters,
            max_generated=args.max_generated,
            generated_jobs=args.generated_jobs,
        )
    )
    report = build_maintenance_report(
        audit_report,
        verification_report,
        audit_report_path,
        verification_report_path,
        project_filters=args.project_filters,
        duration_seconds=round(perf_counter() - t0, 3),
        started_at=started_at,
    )
    write_report(report, maintenance_report_path)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(
            "audit "
            f"p0={report['audit_summary']['p0_count']} "
            f"p1={report['audit_summary']['p1_count']} "
            f"p2={report['audit_summary']['p2_count']} "
            f"clean={report['audit_summary']['clean_count']}/{report['audit_summary']['total_projects']}"
        )
        print(
            "verification "
            f"local_ok={report['verification_summary']['local_ok']} "
            f"generated={report['verification_summary']['generated_passed']}/"
            f"{report['verification_summary']['generated_total']}"
        )
        if report["project_filters"]:
            print(f"filters={','.join(report['project_filters'])}")
        if report["duration_seconds"] is not None:
            print(f"duration={report['duration_seconds']:.3f}s")
        print(f"overall_ok={report['overall_ok']}")
        print(f"report={maintenance_report_path}")

    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
