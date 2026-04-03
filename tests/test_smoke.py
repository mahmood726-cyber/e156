import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import audit_all_projects  # noqa: E402
import repair_p2_backlog  # noqa: E402
import run_generated_smoke_tests  # noqa: E402
import run_maintenance_cycle  # noqa: E402
import run_verification_suite  # noqa: E402
import validate_e156  # noqa: E402


def _write_submission_config(project_dir: Path) -> dict:
    submission_dir = project_dir / "e156-submission"
    submission_dir.mkdir(parents=True, exist_ok=True)
    body = " ".join(["token"] * 156)
    config = {
        "title": "Example Title",
        "summary": "Example summary",
        "type": "methods",
        "primary_estimand": "Odds ratio",
        "body": body,
        "sentences": [{"role": f"S{i}", "text": f"Sentence {i}"} for i in range(1, 8)],
        "notes": {
            "app": "Example App",
            "data": "Example dataset for testing",
            "code": "https://github.com/example/repo",
        },
    }
    (submission_dir / "config.json").write_text(json.dumps(config), encoding="utf-8")
    return config


def test_build_manuscript_text_uses_submission_metadata(tmp_path):
    project_dir = tmp_path / "repo"
    config = _write_submission_config(project_dir)

    manuscript = repair_p2_backlog.build_manuscript_text(project_dir)

    assert config["title"] in manuscript
    assert "Example summary." in manuscript
    assert "Primary estimand: Odds ratio" in manuscript
    assert "App: Example App" in manuscript
    assert "Data: Example dataset for testing" in manuscript
    assert config["body"] in manuscript


def test_repair_p2_project_matches_filters(tmp_path):
    project_dir = tmp_path / "ctgov-alpha"
    assert repair_p2_backlog.project_matches(project_dir, ["ctgov"]) is True
    assert repair_p2_backlog.project_matches(project_dir, ["other"]) is False


def test_ensure_manuscript_upgrades_placeholder_but_preserves_custom(tmp_path):
    project_dir = tmp_path / "repo"
    _write_submission_config(project_dir)
    manuscript_path = project_dir / "paper" / "manuscript.md"
    manuscript_path.parent.mkdir(parents=True, exist_ok=True)

    manuscript_path.write_text(
        "# Placeholder\n\n"
        "This repository currently ships an E156 micro-paper and supporting application artifacts.\n",
        encoding="utf-8",
    )
    assert repair_p2_backlog.ensure_manuscript(project_dir) == "updated"
    updated = manuscript_path.read_text(encoding="utf-8")
    assert "## E156 Capsule" in updated
    assert "Example Title" in updated

    manuscript_path.write_text("# Custom manuscript\n\nKeep me.\n", encoding="utf-8")
    assert repair_p2_backlog.ensure_manuscript(project_dir) is None
    assert manuscript_path.read_text(encoding="utf-8") == "# Custom manuscript\n\nKeep me.\n"


def test_ensure_smoke_test_upgrades_legacy_template_but_preserves_custom(tmp_path):
    project_dir = tmp_path / "repo"
    tests_dir = project_dir / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    test_path = tests_dir / "test_smoke.py"

    test_path.write_text(repair_p2_backlog.OLD_SMOKE_TEST, encoding="utf-8")
    assert repair_p2_backlog.ensure_smoke_test(project_dir) == "updated"
    updated = test_path.read_text(encoding="utf-8")
    assert "REQUIRED_SUBMISSION_FILES" in updated
    assert "json.loads" in updated

    test_path.write_text("def test_custom():\n    assert True\n", encoding="utf-8")
    assert repair_p2_backlog.ensure_smoke_test(project_dir) is None
    assert test_path.read_text(encoding="utf-8") == "def test_custom():\n    assert True\n"


def test_generated_smoke_test_runs_from_repo_root(tmp_path):
    project_dir = tmp_path / "repo"
    _write_submission_config(project_dir)
    submission_dir = project_dir / "e156-submission"
    for name in ("paper.md", "protocol.md", "index.html"):
        (submission_dir / name).write_text("placeholder", encoding="utf-8")

    tests_dir = project_dir / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    test_path = tests_dir / "test_smoke.py"
    test_path.write_text(repair_p2_backlog.build_smoke_test_text(), encoding="utf-8")

    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    proc = subprocess.run(
        ["pytest", "-q", "-p", "no:cacheprovider", "--rootdir", str(project_dir), str(test_path)],
        cwd=project_dir,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_check_git_ignores_dirty_tree_when_remote_is_valid(tmp_path):
    project_dir = tmp_path / "repo"
    project_dir.mkdir()
    subprocess.run(["git", "init", str(project_dir)], check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "-C", str(project_dir), "remote", "add", "origin", "https://github.com/example/repo.git"],
        check=True,
        capture_output=True,
        text=True,
    )
    (project_dir / "untracked.txt").write_text("content", encoding="utf-8")

    issues = audit_all_projects.check_git(project_dir)
    codes = {code for _, code, _ in issues}

    assert "DIRTY_TREE" not in codes
    assert "NO_REMOTE" not in codes
    assert "NO_GITHUB" not in codes


def test_discover_projects_finds_nested_and_root_level_repos(tmp_path):
    top_repo = tmp_path / "TopRepo"
    top_repo.mkdir()
    (top_repo / ".git").mkdir()

    users_dir = tmp_path / "Users"
    users_dir.mkdir()
    skipped_repo = users_dir / "SkippedRepo"
    skipped_repo.mkdir()
    (skipped_repo / ".git").mkdir()

    model_repo = tmp_path / "Models" / "ModelRepo"
    model_repo.mkdir(parents=True)
    (model_repo / ".git").mkdir()

    project_submission = tmp_path / "Projects" / "ProjectRepo" / "e156-submission"
    project_submission.mkdir(parents=True)

    html_repo = tmp_path / "HTML apps" / "HtmlRepo"
    html_repo.mkdir(parents=True)
    (html_repo / ".git").mkdir()

    discovered = audit_all_projects.discover_projects(tmp_path)

    assert discovered == sorted([top_repo, model_repo, project_submission.parent, html_repo], key=str)


def test_safe_is_dir_handles_oserror(monkeypatch, tmp_path):
    blocked = tmp_path / "blocked"
    original = Path.is_dir

    def fake_is_dir(self):
        if self == blocked:
            raise PermissionError("blocked")
        return original(self)

    monkeypatch.setattr(Path, "is_dir", fake_is_dir)
    assert audit_all_projects.safe_is_dir(blocked) is False


def test_build_report_counts_issues_and_clean_projects(monkeypatch, tmp_path):
    repo_a = tmp_path / "repo_a"
    repo_b = tmp_path / "repo_b"
    repo_a.mkdir()
    repo_b.mkdir()

    def fake_audit(project_dir):
        if project_dir == repo_a:
            return [("P0", "NO_E156", "missing"), ("P2", "NO_MANUSCRIPT", "missing manuscript")]
        return []

    monkeypatch.setattr(audit_all_projects, "audit_project", fake_audit)
    report = audit_all_projects.build_report([repo_b, repo_a])

    assert report["total_projects"] == 2
    assert report["p0_count"] == 1
    assert report["p1_count"] == 0
    assert report["p2_count"] == 1
    assert report["clean_count"] == 1
    assert [item["code"] for item in report["issues_by_project"][str(repo_a)]] == ["NO_E156", "NO_MANUSCRIPT"]
    assert report["issues_by_project"][str(repo_b)] == []


def test_select_projects_applies_filters_and_limit(tmp_path):
    projects = [
        tmp_path / "alpha-study",
        tmp_path / "beta-study",
        tmp_path / "ctgov-cardio",
    ]

    selected = audit_all_projects.select_projects(projects, ["ctgov"], limit=1)

    assert selected == [tmp_path / "ctgov-cardio"]


def test_scan_for_tests_and_code_fast_path_detects_generated_smoke_test(tmp_path):
    repo = tmp_path / "repo"
    tests_dir = repo / "tests"
    tests_dir.mkdir(parents=True)
    (tests_dir / "test_smoke.py").write_text("def test_x():\n    assert True\n", encoding="utf-8")

    has_tests, has_code = audit_all_projects.scan_for_tests_and_code(repo)

    assert has_tests is True
    assert has_code is True


def test_has_manuscript_detects_paper_manuscript_fast_path(tmp_path):
    repo = tmp_path / "repo"
    paper_dir = repo / "paper"
    paper_dir.mkdir(parents=True)
    (paper_dir / "manuscript.md").write_text("# Manuscript\n", encoding="utf-8")

    assert audit_all_projects.has_manuscript(repo) is True


def test_validate_uses_structured_sentences_for_sentence_count():
    body = " ".join([
        "One sentence.",
        "Two sentence.",
        "Three sentence.",
        "Four sentence.",
        "Five sentence.",
        "Six sentence. Extra split.",
        "Seven sentence.",
    ])
    structured = [
        {"role": "Question", "text": "One sentence."},
        {"role": "Dataset", "text": "Two sentence."},
        {"role": "Method", "text": "Three sentence."},
        {"role": "Primary result", "text": "Four sentence."},
        {"role": "Robustness", "text": "Five sentence."},
        {"role": "Interpretation", "text": "Six sentence. Extra split."},
        {"role": "Boundary", "text": "Seven sentence."},
    ]

    result = validate_e156.validate(body, structured_sentences=structured)

    assert result["sentence_count"] == 7


def test_validate_accepts_descriptive_quantitative_sentence_four():
    sentences = [
        "Question sentence.",
        "Dataset sentence.",
        "Method sentence.",
        "Oncology formed the largest named family at 42,344 eligible older studies, creating the biggest absolute stock of hidden evidence.",
        "Robustness sentence.",
        "Interpretation sentence.",
        "Boundary sentence is limited by descriptive coding only.",
    ]
    body = " ".join(sentences)

    result = validate_e156.validate(body, structured_sentences=sentences)
    failed = {check["name"] for check in result["checks"] if not check["ok"]}

    assert "result sentence has interval" not in failed
    assert "result sentence has estimand" not in failed


def test_discover_generated_smoke_tests_filters_to_generated_template(tmp_path):
    repo_a = tmp_path / "repo_a"
    repo_a_test = repo_a / "tests" / "test_smoke.py"
    repo_a_test.parent.mkdir(parents=True, exist_ok=True)
    repo_a_test.write_text(repair_p2_backlog.build_smoke_test_text(), encoding="utf-8")

    repo_b = tmp_path / "repo_b"
    repo_b_test = repo_b / "tests" / "test_smoke.py"
    repo_b_test.parent.mkdir(parents=True, exist_ok=True)
    repo_b_test.write_text("def test_custom():\n    assert True\n", encoding="utf-8")

    report = {
        "issues_by_project": {
            "C:\\repo_a": [],
            "C:\\repo_b": [],
        }
    }

    original = run_generated_smoke_tests.windows_to_wsl
    mapping = {
        "C:\\repo_a": repo_a,
        "C:\\repo_b": repo_b,
    }
    run_generated_smoke_tests.windows_to_wsl = lambda raw: mapping[raw]
    try:
        discovered = run_generated_smoke_tests.discover_generated_smoke_tests(report)
    finally:
        run_generated_smoke_tests.windows_to_wsl = original

    assert discovered == [repo_a_test]


def test_discover_generated_smoke_tests_applies_project_filters(tmp_path):
    repo_a = tmp_path / "ctgov-alpha"
    repo_a_test = repo_a / "tests" / "test_smoke.py"
    repo_a_test.parent.mkdir(parents=True, exist_ok=True)
    repo_a_test.write_text(repair_p2_backlog.build_smoke_test_text(), encoding="utf-8")

    repo_b = tmp_path / "other-beta"
    repo_b_test = repo_b / "tests" / "test_smoke.py"
    repo_b_test.parent.mkdir(parents=True, exist_ok=True)
    repo_b_test.write_text(repair_p2_backlog.build_smoke_test_text(), encoding="utf-8")

    report = {"issues_by_project": {"C:\\repo_a": [], "C:\\repo_b": []}}
    original = run_generated_smoke_tests.windows_to_wsl
    mapping = {"C:\\repo_a": repo_a, "C:\\repo_b": repo_b}
    run_generated_smoke_tests.windows_to_wsl = lambda raw: mapping[raw]
    try:
        discovered = run_generated_smoke_tests.discover_generated_smoke_tests(report, project_filters=["ctgov"])
    finally:
        run_generated_smoke_tests.windows_to_wsl = original

    assert discovered == [repo_a_test]


def test_run_one_uses_repo_rootdir_and_returns_result(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    test_path = repo / "tests" / "test_smoke.py"
    test_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.write_text(repair_p2_backlog.build_smoke_test_text(), encoding="utf-8")

    captured = {}

    class Result:
        returncode = 0
        stdout = ". [100%]\n"
        stderr = ""

    def fake_run(cmd, cwd, text, capture_output, env, check):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        captured["env"] = env
        captured["check"] = check
        return Result()

    monkeypatch.setattr(run_generated_smoke_tests.subprocess, "run", fake_run)
    result = run_generated_smoke_tests.run_one(test_path)

    assert captured["cmd"][:5] == ["pytest", "-q", "-p", "no:cacheprovider", "--rootdir"]
    assert captured["cmd"][5] == str(repo)
    assert captured["cmd"][6] == str(test_path)
    assert captured["cwd"] == repo
    assert captured["env"]["PYTHONDONTWRITEBYTECODE"] == "1"
    assert captured["env"]["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] == "1"
    assert captured["check"] is False
    assert result["ok"] is True
    assert result["repo"] == str(repo)
    assert "duration_seconds" in result
    assert "started_at" in result


def test_summarize_counts_failures():
    summary = run_generated_smoke_tests.summarize([
        {"ok": True},
        {"ok": False},
        {"ok": True},
    ])

    assert summary["total"] == 3
    assert summary["passed"] == 2
    assert summary["failed"] == 1


def test_run_generated_suite_forwards_filters_limit_and_jobs(monkeypatch, tmp_path):
    report_path = tmp_path / "audit-report.json"
    report_path.write_text("{}", encoding="utf-8")
    test_path = tmp_path / "repo" / "tests" / "test_smoke.py"
    test_path.parent.mkdir(parents=True)
    test_path.write_text("placeholder", encoding="utf-8")

    monkeypatch.setattr(run_generated_smoke_tests, "load_report", lambda path: {"issues_by_project": {}})
    captured = {}

    def fake_discover(report, existing_only=True, project_filters=None):
        captured["filters"] = project_filters
        return [test_path, test_path.with_name("test_other.py")]

    monkeypatch.setattr(run_generated_smoke_tests, "discover_generated_smoke_tests", fake_discover)
    def fake_run_tests(test_paths, jobs):
        captured["jobs"] = jobs
        captured["test_paths"] = list(test_paths)
        return [{"ok": True, "test_file": str(path), "repo": str(path.parents[1])} for path in test_paths]
    monkeypatch.setattr(run_generated_smoke_tests, "run_tests", fake_run_tests)

    summary = run_verification_suite.run_generated_suite(report_path, project_filters=["ctgov"], max_tests=1, jobs=3)

    assert captured["filters"] == ["ctgov"]
    assert captured["jobs"] == 1
    assert captured["test_paths"] == [test_path]
    assert summary["total"] == 1
    assert summary["passed"] == 1
    assert summary["project_filters"] == ["ctgov"]
    assert summary["max_tests"] == 1
    assert summary["jobs"] == 1


def test_normalize_jobs_bounds_worker_count():
    assert run_generated_smoke_tests.normalize_jobs(0, 0) == 1
    assert run_generated_smoke_tests.normalize_jobs(0, 2) >= 1
    assert run_generated_smoke_tests.normalize_jobs(8, 2) == 2
    assert run_generated_smoke_tests.normalize_jobs(1, 5) == 1


def test_run_local_e156_tests_uses_repo_root(monkeypatch, tmp_path):
    root = tmp_path / "e156"
    tests_dir = root / "tests"
    tests_dir.mkdir(parents=True)
    (tests_dir / "test_smoke.py").write_text("def test_x():\n    assert True\n", encoding="utf-8")

    captured = {}

    class Result:
        returncode = 0
        stdout = "ok\n"
        stderr = ""

    def fake_run(cmd, cwd, text, capture_output, env, check):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        captured["env"] = env
        captured["check"] = check
        return Result()

    monkeypatch.setattr(run_verification_suite.subprocess, "run", fake_run)
    result = run_verification_suite.run_local_e156_tests(root)

    assert captured["cmd"] == ["pytest", "-q", "-p", "no:cacheprovider", str(tests_dir / "test_smoke.py")]
    assert captured["cwd"] == root
    assert captured["env"]["PYTHONDONTWRITEBYTECODE"] == "1"
    assert captured["env"]["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] == "1"
    assert captured["check"] is False
    assert result["ok"] is True
    assert result["target"] == str(tests_dir / "test_smoke.py")


def test_build_suite_report_combines_local_and_generated_status():
    report = run_verification_suite.build_suite_report(
        {"ok": True, "target": "local"},
        {"passed": 3, "failed": 0, "total": 3, "results": []},
        project_filters=["ctgov"],
        duration_seconds=1.25,
        started_at="2026-03-30T00:00:00Z",
    )
    assert report["overall_ok"] is True
    assert report["project_filters"] == ["ctgov"]
    assert report["duration_seconds"] == 1.25

    failing = run_verification_suite.build_suite_report(
        {"ok": True, "target": "local"},
        {"passed": 2, "failed": 1, "total": 3, "results": []},
    )
    assert failing["overall_ok"] is False


def test_write_report_persists_json(tmp_path):
    path = tmp_path / "verification-report.json"
    payload = {"overall_ok": True, "local_e156_tests": None, "generated_smoke_tests": None}

    run_verification_suite.write_report(payload, path)

    assert json.loads(path.read_text(encoding="utf-8")) == payload


def test_build_maintenance_report_combines_audit_and_verification():
    report = run_maintenance_cycle.build_maintenance_report(
        {"total_projects": 10, "clean_count": 10, "p0_count": 0, "p1_count": 0, "p2_count": 0},
        {"overall_ok": True, "local_e156_tests": {"ok": True}, "generated_smoke_tests": {"total": 4, "passed": 4, "failed": 0}},
        Path("/tmp/audit-report.json"),
        Path("/tmp/verification-report.json"),
        project_filters=["ctgov"],
        duration_seconds=2.5,
        started_at="2026-03-30T00:00:00Z",
    )
    assert report["overall_ok"] is True
    assert report["audit_ok"] is True
    assert report["verification_ok"] is True
    assert report["verification_summary"]["generated_passed"] == 4
    assert report["project_filters"] == ["ctgov"]
    assert report["duration_seconds"] == 2.5

    failing = run_maintenance_cycle.build_maintenance_report(
        {"total_projects": 10, "clean_count": 9, "p0_count": 0, "p1_count": 0, "p2_count": 1},
        {"overall_ok": True, "local_e156_tests": {"ok": True}, "generated_smoke_tests": {"total": 4, "passed": 4, "failed": 0}},
        Path("/tmp/audit-report.json"),
        Path("/tmp/verification-report.json"),
    )
    assert failing["overall_ok"] is False
