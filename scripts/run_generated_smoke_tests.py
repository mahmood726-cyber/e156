"""Run generated cross-repo smoke tests with safe pytest root handling."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "audit-report.json"
SENTINEL = "REQUIRED_SUBMISSION_FILES ="
DEFAULT_JOBS = max(1, min(4, os.cpu_count() or 1))


def windows_to_wsl(path_str: str) -> Path:
    if path_str.startswith("/mnt/"):
        return Path(path_str)
    if path_str.startswith("C:\\"):
        return Path("/mnt/c") / path_str[3:].replace("\\", "/")
    if path_str.startswith("C:/"):
        return Path("/mnt/c") / path_str[3:]
    raise ValueError(f"Unsupported path: {path_str}")


def load_report(report_path: Path = REPORT_PATH) -> dict:
    return json.loads(report_path.read_text(encoding="utf-8"))


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def project_matches(project_path: Path, project_filters: list[str] | None = None) -> bool:
    if not project_filters:
        return True

    path_str = str(project_path).lower()
    name = project_path.name.lower()
    for raw_filter in project_filters:
        needle = raw_filter.lower()
        if needle in path_str or needle == name or needle in name:
            return True
    return False


def is_generated_smoke_test(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    return SENTINEL in text


def discover_generated_smoke_tests(
    report: dict,
    existing_only: bool = True,
    project_filters: list[str] | None = None,
) -> list[Path]:
    discovered = []
    seen = set()
    for project_str in report.get("issues_by_project", {}):
        repo = windows_to_wsl(project_str)
        if not project_matches(repo, project_filters):
            continue
        test_path = repo / "tests" / "test_smoke.py"
        if existing_only and not test_path.exists():
            continue
        if not is_generated_smoke_test(test_path):
            continue
        key = str(test_path)
        if key in seen:
            continue
        seen.add(key)
        discovered.append(test_path)
    return sorted(discovered)


def run_one(test_path: Path) -> dict:
    repo = test_path.parents[1]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    started_at = iso_now()
    t0 = perf_counter()
    proc = subprocess.run(
        ["pytest", "-q", "-p", "no:cacheprovider", "--rootdir", str(repo), str(test_path)],
        cwd=repo,
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    return {
        "repo": str(repo),
        "test_file": str(test_path),
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "started_at": started_at,
        "duration_seconds": round(perf_counter() - t0, 3),
    }


def summarize(results: list[dict]) -> dict:
    passed = sum(1 for item in results if item["ok"])
    failed = len(results) - passed
    return {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "results": results,
    }


def normalize_jobs(jobs: int, total_tasks: int) -> int:
    if total_tasks <= 0:
        return 1
    if jobs <= 0:
        jobs = DEFAULT_JOBS
    return max(1, min(jobs, total_tasks))


def run_tests(test_paths: list[Path], jobs: int = DEFAULT_JOBS) -> list[dict]:
    jobs = normalize_jobs(jobs, len(test_paths))
    if jobs == 1:
        return [run_one(test_path) for test_path in test_paths]

    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        futures = [executor.submit(run_one, test_path) for test_path in test_paths]
        return [future.result() for future in futures]


def run_suite(
    report_path: Path = REPORT_PATH,
    project_filters: list[str] | None = None,
    max_tests: int = 0,
    jobs: int = DEFAULT_JOBS,
) -> dict:
    started_at = iso_now()
    t0 = perf_counter()
    report = load_report(report_path)
    tests = discover_generated_smoke_tests(report, project_filters=project_filters)
    if max_tests > 0:
        tests = tests[:max_tests]

    jobs = normalize_jobs(jobs, len(tests))
    results = run_tests(tests, jobs=jobs)
    summary = summarize(results)
    summary["started_at"] = started_at
    summary["duration_seconds"] = round(perf_counter() - t0, 3)
    summary["project_filters"] = list(project_filters or [])
    summary["max_tests"] = max_tests
    summary["jobs"] = jobs
    summary["report_path"] = str(report_path)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run generated smoke tests across cleaned repos.")
    parser.add_argument("--report", default=str(REPORT_PATH), help="Path to audit-report.json")
    parser.add_argument("--project", action="append", dest="project_filters", help="Substring filter for repo path/name; can be repeated")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    parser.add_argument("--max", type=int, default=0, help="Limit number of tests to run")
    parser.add_argument("--jobs", type=int, default=DEFAULT_JOBS, help="Parallel workers for generated smoke tests")
    args = parser.parse_args()

    summary = run_suite(Path(args.report), args.project_filters, args.max, args.jobs)
    results = summary["results"]

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        for item in results:
            status = "PASS" if item["ok"] else "FAIL"
            print(f"{status} {item['test_file']}")
        if summary["project_filters"]:
            print(f"filters={','.join(summary['project_filters'])}")
        print(f"jobs={summary['jobs']}")
        print(f"passed={summary['passed']} failed={summary['failed']} total={summary['total']}")
        print(f"duration={summary['duration_seconds']:.3f}s")

    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
