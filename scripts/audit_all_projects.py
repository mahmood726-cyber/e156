"""
Pre-Submission Audit — scans ALL projects on C: for issues.
Checks: git status, E156 paper quality, test health, manuscript, HTML app, dependencies.
Outputs a prioritized issue report sorted by severity.
"""

import json
import os
import concurrent.futures
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
HOST_C_ROOT = Path("/mnt/c") if Path("/mnt/c").exists() else Path("C:/")
DEFAULT_REPORT_PATH = ROOT / "audit-report.json"
DEFAULT_AUDIT_JOBS = max(1, min(4, os.cpu_count() or 1))
SKIP_TOP_LEVEL_DIRS = {
    "Windows",
    "Program Files",
    "Program Files (x86)",
    "ProgramData",
    "Users",
    "Intel",
    "AMD",
    "$Recycle.Bin",
    "System Volume Information",
    "Recovery",
    "PerfLogs",
    "E156-backup-claude",
    "E156-framework-backup-codex",
    "E156-framework",
}
SCAN_SUBDIRS = ("Models", "Projects", "HTML apps")
WALK_SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    "htmlcov",
    "site-packages",
    "target",
    "tmp",
    "temp",
    "logs",
    "log",
    "cache",
    ".cache",
    ".next",
    ".ruff_cache",
    "data",
    "datasets",
    "outputs",
    "output",
}
CODE_SUFFIXES = {".py", ".r", ".html", ".js", ".ts"}
MANUSCRIPT_SUFFIXES = {".md", ".tex", ".rmd", ".docx"}

sys.path.insert(0, str(SCRIPT_DIR))
from validate_e156 import validate
from finalize_all import pick_refs, BASE_REFS


def check_git(project_dir):
    """Check git health."""
    issues = []
    git_dir = project_dir / ".git"
    if not git_dir.exists():
        issues.append(("P1", "NO_GIT", "Not a git repository"))
        return issues

    # Check for remote
    try:
        r = subprocess.run(["git", "-C", str(project_dir), "remote", "-v"],
                          capture_output=True, text=True, timeout=5)
        if not r.stdout.strip():
            issues.append(("P1", "NO_REMOTE", "No git remote configured"))
        elif "github.com" not in r.stdout:
            issues.append(("P2", "NO_GITHUB", "Remote exists but not on GitHub"))
    except:
        pass

    return issues


def check_e156(submission_dir):
    """Check E156 paper quality."""
    issues = []
    if not submission_dir.exists():
        issues.append(("P0", "NO_E156", "No e156-submission folder"))
        return issues

    # Check files exist
    for f in ["paper.md", "protocol.md", "config.json", "index.html"]:
        if not (submission_dir / f).exists():
            issues.append(("P0", f"MISSING_{f.upper()}", f"Missing {f}"))

    cfg_path = submission_dir / "config.json"
    if not cfg_path.exists():
        return issues

    try:
        config = json.loads(cfg_path.read_text(encoding="utf-8"))
    except:
        try:
            config = json.loads(cfg_path.read_text(encoding="utf-8-sig"))
        except:
            issues.append(("P0", "BAD_JSON", "config.json is invalid JSON"))
            return issues

    body = config.get("body", "")
    title = config.get("title", "")
    notes = config.get("notes", {})
    structured_sentences = config.get("sentences", [])

    # Word count
    wc = len(body.split())
    if wc != 156:
        issues.append(("P0", "WRONG_WC", f"Body is {wc} words (need 156)"))

    # Sentence count
    result = validate(body, structured_sentences=structured_sentences)
    if result["sentence_count"] != 7:
        issues.append(("P0", "WRONG_SC", f"Body has {result['sentence_count']} sentences (need 7)"))

    # Validation checks
    for check in result.get("checks", []):
        if not check["ok"] and check["name"] in ("result sentence has interval", "result sentence has estimand"):
            issues.append(("P1", "S4_WEAK", f"S4 issue: {check['detail']}"))

    # Data source clarity
    data = notes.get("data", "")
    if not data or len(data) < 15:
        issues.append(("P1", "VAGUE_DATA", f"Data description too short: '{data[:30]}'"))

    # GitHub link
    code = notes.get("code", "")
    if "github.com" not in code:
        issues.append(("P1", "NO_GITHUB_LINK", "No GitHub URL in notes.code"))

    # Reference quality
    refs = config.get("references", [])
    if len(refs) < 2:
        issues.append(("P1", "FEW_REFS", f"Only {len(refs)} references"))

    # Check reference relevance
    expected_refs = pick_refs(title, body, config.get("type", "methods"))
    current_key = None
    for k, v in BASE_REFS.items():
        if refs == v:
            current_key = k
            break
    expected_key = None
    for k, v in BASE_REFS.items():
        if expected_refs == v:
            expected_key = k
            break
    if current_key and expected_key and current_key != expected_key:
        issues.append(("P1", "REF_MISMATCH", f"Refs are '{current_key}' but topic suggests '{expected_key}'"))

    # Check assets
    assets_dir = submission_dir / "assets"
    if not assets_dir.is_dir() or not any(assets_dir.iterdir()):
        issues.append(("P1", "NO_ASSETS", "No visual assets (HTML app or figures)"))

    # Author/affiliation
    author = config.get("author", "")
    if author != "Mahmood Ahmad":
        issues.append(("P2", "WRONG_AUTHOR", f"Author is '{author}' not 'Mahmood Ahmad'"))

    affil = config.get("affiliation", "")
    if "Tahir" not in affil:
        issues.append(("P2", "NO_AFFILIATION", "Missing Tahir Heart Institute affiliation"))

    # Protocol check
    proto = submission_dir / "protocol.md"
    if proto.exists():
        proto_text = proto.read_text(encoding="utf-8")
        if "AI Disclosure" not in proto_text:
            issues.append(("P2", "PROTO_NO_DISCLOSURE", "Protocol missing AI disclosure"))
    else:
        issues.append(("P1", "NO_PROTOCOL", "No protocol.md"))

    # Paper disclosure
    paper = submission_dir / "paper.md"
    if paper.exists():
        paper_text = paper.read_text(encoding="utf-8")
        if "AI Disclosure" not in paper_text:
            issues.append(("P2", "PAPER_NO_DISCLOSURE", "Paper missing AI disclosure"))

    return issues


def get_e156_submission_dirs(project_dir):
    """Return direct or repo-local release submission directories for a project."""
    submission_dirs = []
    root_submission = project_dir / "e156-submission"
    if root_submission.is_dir():
        submission_dirs.append(root_submission)

    releases_root = project_dir / "releases"
    if releases_root.is_dir():
        for submission_dir in sorted(releases_root.glob("*/e156-submission")):
            if submission_dir.is_dir():
                submission_dirs.append(submission_dir)

    return submission_dirs


def check_project_e156(project_dir):
    """Audit one or more E156 submission directories belonging to a project."""
    submission_dirs = get_e156_submission_dirs(project_dir)
    if not submission_dirs:
        return [("P0", "NO_E156", "No e156-submission folder")]

    # A project with multiple release submissions should be audited per submission,
    # but it should not fail just because there is no single root-level folder.
    if len(submission_dirs) == 1 and submission_dirs[0].parent == project_dir:
        return check_e156(submission_dirs[0])

    issues = []
    for submission_dir in submission_dirs:
        label = submission_dir.parent.name
        for severity, code, description in check_e156(submission_dir):
            issues.append((severity, code, f"[{label}] {description}"))
    return issues


def check_tests(project_dir):
    """Check if project has tests and basic code health."""
    issues = []

    has_tests, has_code = scan_for_tests_and_code(project_dir)

    if not has_tests:
        # Check if it's just a data/paper project (OK to not have tests)
        if has_code:
            issues.append(("P2", "NO_TESTS", "No test files found for code project"))

    return issues


def check_manuscript(project_dir):
    """Check for manuscript/paper files."""
    issues = []
    if not get_e156_submission_dirs(project_dir):
        return issues

    if has_manuscript(project_dir):
        return issues

    issues.append(("P2", "NO_MANUSCRIPT", "No full manuscript found (only E156 micro-paper)"))

    return issues


def audit_project(project_dir):
    """Run all checks on a project."""
    all_issues = []
    all_issues.extend(check_git(project_dir))
    all_issues.extend(check_project_e156(project_dir))
    all_issues.extend(check_tests(project_dir))
    all_issues.extend(check_manuscript(project_dir))

    return all_issues


def safe_is_dir(path: Path) -> bool:
    """Return True when the path is a readable directory."""
    try:
        return path.is_dir()
    except OSError:
        return False


def iter_dirs(root: Path):
    """Yield child directories while skipping unreadable entries."""
    try:
        entries = list(root.iterdir())
    except OSError:
        return
    for entry in entries:
        if safe_is_dir(entry):
            yield entry


def safe_exists(path: Path) -> bool:
    """Return True when the path exists and is readable."""
    try:
        return path.exists()
    except OSError:
        return False


def iso_now() -> str:
    """Return a UTC timestamp for report metadata."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def project_matches(project: Path, project_filters: list[str] | None = None) -> bool:
    """Match a project path against substring filters."""
    if not project_filters:
        return True

    path_str = str(project).lower()
    name = project.name.lower()
    for raw_filter in project_filters:
        needle = raw_filter.lower()
        if needle in path_str or needle == name or needle in name:
            return True
    return False


def select_projects(projects: list[Path], project_filters: list[str] | None = None, limit: int = 0) -> list[Path]:
    """Filter and optionally cap the discovered projects."""
    selected = [project for project in projects if project_matches(project, project_filters)]
    if limit > 0:
        selected = selected[:limit]
    return selected


def normalize_jobs(jobs: int, total_tasks: int, default_jobs: int = DEFAULT_AUDIT_JOBS) -> int:
    """Clamp worker count to a safe range for the current workload."""
    if total_tasks <= 0:
        return 1
    if jobs <= 0:
        jobs = default_jobs
    return max(1, min(jobs, total_tasks))


def glob_any(base: Path, *patterns: str) -> bool:
    """Return True when any glob pattern matches at least one path."""
    for pattern in patterns:
        try:
            next(base.glob(pattern))
            return True
        except StopIteration:
            continue
        except OSError:
            continue
    return False


def iter_repo_files(project_dir: Path):
    """Yield repo files while pruning known heavy or irrelevant directories."""
    skip_dirs = {name.lower() for name in WALK_SKIP_DIRS}
    try:
        walker = os.walk(project_dir, topdown=True, onerror=lambda _exc: None)
        for root, dirs, files in walker:
            dirs[:] = [name for name in dirs if name.lower() not in skip_dirs]
            yield Path(root), files
    except OSError:
        return


def scan_for_tests_and_code(project_dir: Path) -> tuple[bool, bool]:
    """Detect whether a repo has tests and code without full recursive globbing."""
    if glob_any(project_dir, "test_*.py", "*_test.py", "*.test.js", "*.test.ts", "test_*.R", "run_tests*", "selenium_test*"):
        return True, True

    for subdir_name in ("tests", "test"):
        subdir = project_dir / subdir_name
        if safe_is_dir(subdir) and glob_any(subdir, "*.py", "*.R", "*.js", "*.ts"):
            return True, True

    has_code = glob_any(project_dir, "*.py", "*.R", "*.html", "*.js", "*.ts")
    for root, files in iter_repo_files(project_dir):
        root_name = root.name.lower()
        for filename in files:
            lower = filename.lower()
            suffix = Path(filename).suffix.lower()
            if suffix in CODE_SUFFIXES:
                has_code = True
            if (
                lower.startswith("test_")
                or lower.startswith("selenium_test")
                or lower.startswith("run_tests")
                or lower.endswith("_test.py")
                or lower.endswith("_test.r")
                or lower.endswith(".test.js")
                or lower.endswith(".test.ts")
                or (root_name in {"tests", "test"} and suffix in CODE_SUFFIXES)
            ):
                return True, has_code
    return False, has_code


def has_manuscript(project_dir: Path) -> bool:
    """Detect manuscript artifacts with cheap direct checks first."""
    paper_dir = project_dir / "paper"
    if safe_is_dir(paper_dir) and glob_any(paper_dir, "*.md", "*.tex", "*.Rmd", "*.docx", "manuscript*"):
        return True

    if glob_any(project_dir, "manuscript*.md", "manuscript*.Rmd", "*.manuscript.*", "submission*.md", "submission*.tex", "submission*.Rmd", "submission*.docx"):
        return True

    for root, files in iter_repo_files(project_dir):
        for filename in files:
            lower = filename.lower()
            suffix = Path(filename).suffix.lower()
            if suffix not in MANUSCRIPT_SUFFIXES:
                continue
            if lower.startswith("manuscript") or "submission" in lower:
                return True
    return False


def discover_projects(scan_root: Path = HOST_C_ROOT) -> list[Path]:
    """Find git or E156 projects under the configured C-drive mirror."""
    projects = []
    if not safe_is_dir(scan_root):
        return projects

    for d in iter_dirs(scan_root):
        if d.name in SKIP_TOP_LEVEL_DIRS:
            continue
        if (d / ".git").exists() or (d / "e156-submission").is_dir():
            projects.append(d)

    for root in [scan_root / name for name in SCAN_SUBDIRS]:
        if safe_is_dir(root):
            for d in iter_dirs(root):
                if ((d / ".git").exists() or (d / "e156-submission").is_dir()) and d not in projects:
                    projects.append(d)

    return sorted(projects, key=lambda p: str(p))


def audit_projects(projects: list[Path], jobs: int = DEFAULT_AUDIT_JOBS) -> tuple[list[tuple[Path, list[tuple[str, str, str]]]], int]:
    """Audit projects with bounded parallelism while preserving sort order."""
    projects = sorted(projects, key=lambda p: str(p))
    jobs = normalize_jobs(jobs, len(projects))

    if jobs == 1:
        return [(proj, audit_project(proj)) for proj in projects], jobs

    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        results = list(executor.map(audit_project, projects))
    return list(zip(projects, results)), jobs


def build_report(projects: list[Path], jobs: int = DEFAULT_AUDIT_JOBS) -> dict:
    """Audit the provided projects and return the structured report."""
    audited_projects, jobs_used = audit_projects(projects, jobs)

    # Audit each project
    all_results = {}
    p0_total = p1_total = p2_total = 0
    clean_count = 0

    for proj, issues in audited_projects:
        all_results[str(proj)] = issues
        for sev, _, _ in issues:
            if sev == "P0": p0_total += 1
            elif sev == "P1": p1_total += 1
            else: p2_total += 1
        if not issues:
            clean_count += 1

    return {
        "total_projects": len(audited_projects),
        "p0_count": p0_total,
        "p1_count": p1_total,
        "p2_count": p2_total,
        "clean_count": clean_count,
        "audit_jobs": jobs_used,
        "issues_by_project": {
            str(p): [{"severity": s, "code": c, "description": d} for s, c, d in issues]
            for p, issues in all_results.items()
        },
    }


def run_audit(
    scan_root: Path = HOST_C_ROOT,
    project_filters: list[str] | None = None,
    limit: int = 0,
    jobs: int = DEFAULT_AUDIT_JOBS,
) -> dict:
    """Discover, filter, audit, and annotate projects in one call."""
    started_at = iso_now()
    t0 = perf_counter()
    discovered = discover_projects(scan_root)
    projects = select_projects(discovered, project_filters, limit)
    report = build_report(projects, jobs=jobs)
    report["generated_at"] = started_at
    report["duration_seconds"] = round(perf_counter() - t0, 3)
    report["scan_root"] = str(scan_root)
    report["project_filters"] = list(project_filters or [])
    report["project_limit"] = limit
    report["discovered_project_count"] = len(discovered)
    return report


def print_report(report: dict) -> None:
    """Print the audit summary and grouped issue counts."""
    total_projects = report["total_projects"]
    p0_total = report["p0_count"]
    p1_total = report["p1_count"]
    p2_total = report["p2_count"]
    clean_count = report["clean_count"]
    raw_results = report.get("issues_by_project", {})
    all_results = {
        project: [(item["severity"], item["code"], item["description"]) for item in issues]
        for project, issues in raw_results.items()
    }

    print(f"{'='*70}")
    print(f"PRE-SUBMISSION AUDIT: {total_projects} projects")
    print(f"{'='*70}")
    print(f"  P0 (must fix):   {p0_total}")
    print(f"  P1 (should fix): {p1_total}")
    print(f"  P2 (nice to fix): {p2_total}")
    print(f"  CLEAN:           {clean_count}/{total_projects}")
    if report.get("project_filters"):
        print(f"  FILTERS:         {', '.join(report['project_filters'])}")
    if report.get("project_limit"):
        print(f"  LIMIT:           {report['project_limit']}")
    if report.get("audit_jobs") is not None:
        print(f"  AUDIT_JOBS:      {report['audit_jobs']}")
    if report.get("duration_seconds") is not None:
        print(f"  DURATION:        {report['duration_seconds']:.3f}s")
    print()

    # P0 issues (grouped by type)
    p0_by_type = {}
    for proj, issues in all_results.items():
        for sev, code, desc in issues:
            if sev == "P0":
                p0_by_type.setdefault(code, []).append((Path(proj).name, desc))

    if p0_by_type:
        print("P0 — MUST FIX BEFORE SUBMISSION")
        print("-" * 50)
        for code, items in sorted(p0_by_type.items()):
            print(f"\n  {code} ({len(items)} projects):")
            for name, desc in items[:10]:
                print(f"    {name}: {desc}")
            if len(items) > 10:
                print(f"    ... and {len(items)-10} more")

    # P1 issues (grouped by type)
    p1_by_type = {}
    for proj, issues in all_results.items():
        for sev, code, desc in issues:
            if sev == "P1":
                p1_by_type.setdefault(code, []).append((Path(proj).name, desc))

    if p1_by_type:
        print(f"\n\nP1 — SHOULD FIX")
        print("-" * 50)
        for code, items in sorted(p1_by_type.items()):
            print(f"\n  {code} ({len(items)} projects):")
            for name, desc in items[:5]:
                print(f"    {name}: {desc}")
            if len(items) > 5:
                print(f"    ... and {len(items)-5} more")

    # P2 summary only
    p2_by_type = {}
    for proj, issues in all_results.items():
        for sev, code, desc in issues:
            if sev == "P2":
                p2_by_type.setdefault(code, []).append(Path(proj).name)

    if p2_by_type:
        print(f"\n\nP2 — NICE TO FIX (summary)")
        print("-" * 50)
        for code, names in sorted(p2_by_type.items()):
            print(f"  {code}: {len(names)} projects")

    # Clean projects
    clean_projects = [Path(p).name for p, issues in all_results.items() if not issues]
    if clean_projects:
        print(f"\n\nCLEAN — READY TO SUBMIT ({len(clean_projects)}):")
        print("-" * 50)
        for name in clean_projects:
            print(f"  {name}")

def save_report(report: dict, report_path: Path = DEFAULT_REPORT_PATH, announce: bool = True) -> None:
    """Persist the structured audit report."""
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    if announce:
        print(f"\nFull report saved to {report_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run the E156 cross-project audit.")
    parser.add_argument("--scan-root", default=str(HOST_C_ROOT), help="Root directory to scan for projects")
    parser.add_argument("--project", action="append", dest="project_filters", help="Substring filter for project path/name; can be repeated")
    parser.add_argument("--limit", type=int, default=0, help="Limit the number of selected projects after filtering")
    parser.add_argument("--jobs", type=int, default=DEFAULT_AUDIT_JOBS, help="Parallel workers for project audits")
    parser.add_argument("--report", default=str(DEFAULT_REPORT_PATH), help="Path to write audit-report.json")
    parser.add_argument("--json", action="store_true", help="Emit the full JSON report to stdout")
    args = parser.parse_args()

    report = run_audit(Path(args.scan_root), args.project_filters, args.limit, args.jobs)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)
    save_report(report, Path(args.report), announce=not args.json)


if __name__ == "__main__":
    main()
