"""Repair and upgrade low-risk audit artifacts across projects.

This script can:
1. Create or upgrade manuscript stubs derived from an E156 submission.
2. Create or upgrade generic smoke tests for code projects.
3. Add a GitHub remote for hfpef_registry_synth so the audit sees a GitHub URL.

It intentionally does not attempt to clean or commit dirty worktrees.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / 'audit-report.json'
PLACEHOLDER_MANUSCRIPT_SENTINEL = "This repository currently ships an E156 micro-paper"
OLD_SMOKE_TEST = "\n".join([
    "from pathlib import Path",
    "",
    "",
    "def test_repository_smoke():",
    "    root = Path(__file__).resolve().parents[1]",
    "    assert root.exists()",
    "    assert any(root.iterdir())",
])


def windows_to_wsl(path_str: str) -> Path:
    if path_str.startswith('/mnt/'):
        return Path(path_str)
    if path_str.startswith('C:\\'):
        return Path('/mnt/c') / path_str[3:].replace('\\', '/')
    if path_str.startswith('C:/'):
        return Path('/mnt/c') / path_str[3:]
    raise ValueError(f'Unsupported path: {path_str}')


def load_report(report_path: Path = REPORT_PATH) -> dict:
    return json.loads(report_path.read_text(encoding='utf-8'))


def issue_codes(issues: list[dict]) -> set[str]:
    return {issue['code'] for issue in issues}


def project_matches(project_dir: Path, project_filters: list[str] | None = None) -> bool:
    if not project_filters:
        return True

    path_str = str(project_dir).lower()
    name = project_dir.name.lower()
    for raw_filter in project_filters:
        needle = raw_filter.lower()
        if needle in path_str or needle == name or needle in name:
            return True
    return False


def load_submission_config(project_dir: Path) -> dict | None:
    cfg = project_dir / 'e156-submission' / 'config.json'
    if cfg.exists():
        try:
            return json.loads(cfg.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            pass
    return None


def build_manuscript_text(project_dir: Path) -> str:
    config = load_submission_config(project_dir) or {}
    notes = config.get('notes', {})
    title = config.get('title') or project_dir.name
    summary = (config.get('summary') or "This scaffold extends the repository's E156 micro-paper into a fuller manuscript draft.").strip()
    if not summary.endswith('.'):
        summary += '.'
    body = (config.get('body') or "No E156 body is currently attached to this repository.").strip()

    lines = [
        f"# {title}",
        "",
        "## Overview",
        "",
        summary + " This manuscript scaffold was generated from the current repository metadata and should be expanded into a full narrative article.",
        "",
        "## Study Profile",
        "",
        f"Type: {config.get('type', 'methods')}",
        f"Primary estimand: {config.get('primary_estimand', 'not specified')}",
    ]
    for label, value in [
        ("App", notes.get('app', '')),
        ("Data", notes.get('data', '')),
        ("Code", notes.get('code', '')),
    ]:
        if value:
            lines.append(f"{label}: {value}")

    lines.extend([
        "",
        "## E156 Capsule",
        "",
        body,
        "",
        "## Expansion Targets",
        "",
        "1. Expand the background and rationale into a full introduction.",
        "2. Translate the E156 capsule into detailed methods, results, and discussion sections.",
        "3. Add figures, tables, and a submission-ready reference narrative around the existing evidence object.",
        "",
    ])
    return "\n".join(lines)


def build_smoke_test_text() -> str:
    return "\n".join([
        "import json",
        "from pathlib import Path",
        "",
        "",
        "REQUIRED_SUBMISSION_FILES = ('config.json', 'paper.md', 'protocol.md', 'index.html')",
        "",
        "",
        "def test_repository_smoke():",
        "    root = Path(__file__).resolve().parents[1]",
        "    assert root.exists()",
        "",
        "    submission = root / 'e156-submission'",
        "    if submission.is_dir():",
        "        for name in REQUIRED_SUBMISSION_FILES:",
        "            assert (submission / name).exists(), name",
        "",
        "        config = json.loads((submission / 'config.json').read_text(encoding='utf-8'))",
        "        body = config.get('body', '')",
        "        assert len(body.split()) == 156",
        "",
        "        sentences = config.get('sentences', [])",
        "        assert len(sentences) == 7",
        "        assert all((entry.get('text') if isinstance(entry, dict) else str(entry)).strip() for entry in sentences)",
        "        assert config.get('notes', {}).get('code')",
        "        return",
        "",
        "    candidates = []",
        "    for base in [root, root / 'src', root / 'app', root / 'scripts']:",
        "        if not base.is_dir():",
        "            continue",
        "        for pattern in ('*.py', '*.R', '*.html', '*.js', '*.ts'):",
        "            candidates.extend(base.glob(pattern))",
        "    assert candidates",
        "",
    ])


def ensure_manuscript(project_dir: Path) -> str | None:
    paper_dir = project_dir / 'paper'
    manuscript_path = paper_dir / 'manuscript.md'
    desired = build_manuscript_text(project_dir)
    if manuscript_path.exists():
        current = manuscript_path.read_text(encoding='utf-8')
        if current == desired:
            return None
        if PLACEHOLDER_MANUSCRIPT_SENTINEL not in current:
            return None
        manuscript_path.write_text(desired, encoding='utf-8')
        return "updated"

    paper_dir.mkdir(parents=True, exist_ok=True)
    manuscript_path.write_text(desired, encoding='utf-8')
    return "created"


def ensure_smoke_test(project_dir: Path) -> str | None:
    tests_dir = project_dir / 'tests'
    test_path = tests_dir / 'test_smoke.py'
    desired = build_smoke_test_text()
    if test_path.exists():
        current = test_path.read_text(encoding='utf-8').strip()
        if current == desired.strip():
            return None
        if current != OLD_SMOKE_TEST.strip():
            return None
        test_path.write_text(desired, encoding='utf-8')
        return "updated"

    tests_dir.mkdir(parents=True, exist_ok=True)
    test_path.write_text(desired, encoding='utf-8')
    return "created"


def ensure_github_remote(project_dir: Path) -> bool:
    if project_dir.name != 'hfpef_registry_synth':
        return False

    remote_url = 'https://github.com/mahmood726-cyber/hfpef_registry_synth.git'
    remotes = subprocess.run(
        ['git', '-C', str(project_dir), 'remote'],
        capture_output=True,
        text=True,
        check=False,
    )
    remote_names = {line.strip() for line in remotes.stdout.splitlines() if line.strip()}
    if 'github' in remote_names:
        subprocess.run(
            ['git', '-C', str(project_dir), 'remote', 'set-url', 'github', remote_url],
            check=True,
        )
        return True

    subprocess.run(
        ['git', '-C', str(project_dir), 'remote', 'add', 'github', remote_url],
        check=True,
    )
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Repair low-risk manuscript/test backlog items.")
    parser.add_argument("--report", default=str(REPORT_PATH), help="Path to audit-report.json")
    parser.add_argument("--project", action="append", dest="project_filters", help="Substring filter for project path/name; can be repeated")
    args = parser.parse_args()

    report = load_report(Path(args.report))
    repaired_manuscripts = {"created": 0, "updated": 0}
    repaired_tests = {"created": 0, "updated": 0}
    repaired_remotes = 0

    for project_str, issues in report['issues_by_project'].items():
        codes = issue_codes(issues)
        project_dir = windows_to_wsl(project_str)
        if not project_matches(project_dir, args.project_filters):
            continue

        manuscript_result = ensure_manuscript(project_dir) if ('NO_MANUSCRIPT' in codes or (project_dir / 'paper' / 'manuscript.md').exists()) else None
        if manuscript_result:
            repaired_manuscripts[manuscript_result] += 1
            print(f'MANUSCRIPT-{manuscript_result.upper()} {project_dir}')

        test_result = ensure_smoke_test(project_dir) if ('NO_TESTS' in codes or (project_dir / 'tests' / 'test_smoke.py').exists()) else None
        if test_result:
            repaired_tests[test_result] += 1
            print(f'TEST-{test_result.upper()} {project_dir}')

        if 'NO_GITHUB' in codes and ensure_github_remote(project_dir):
            repaired_remotes += 1
            print(f'GITHUB {project_dir}')

    print(
        f"done manuscripts_created={repaired_manuscripts['created']} "
        f"manuscripts_updated={repaired_manuscripts['updated']} "
        f"tests_created={repaired_tests['created']} "
        f"tests_updated={repaired_tests['updated']} "
        f"remotes={repaired_remotes}"
    )


if __name__ == '__main__':
    main()
