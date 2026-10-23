"""Mutation tests: the assurance JUnit gate must refuse false-green cases."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from xml.etree import ElementTree as ET

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "assurance" / "require_corpus_results.py"
SPEC = importlib.util.spec_from_file_location("require_corpus_results", SCRIPT)
assert SPEC and SPEC.loader
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


def _junit(tmp_path: Path, n: int = 14, *, defect: str | None = None,
           outside_skip: bool = False) -> Path:
    root = ET.Element("testsuite", {"tests": str(n + 1)})
    for i in range(n):
        case = ET.SubElement(root, "testcase", {
            "classname": "tests.test_assurance_corpus", "name": f"test_case_{i}",
        })
        if defect and i == 0:
            ET.SubElement(case, defect, {"message": "planted defect"})
    ordinary = ET.SubElement(root, "testcase", {
        "classname": "tests.test_doi_resolver", "name": "test_other",
    })
    if outside_skip:
        ET.SubElement(ordinary, "skipped", {"message": "missing dependency"})
    path = tmp_path / "pytest.xml"
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    return path


def test_clean_corpus_and_unrelated_test_pass(tmp_path):
    assert guard.check_results(_junit(tmp_path)) == []


def test_missing_corpus_cases_are_refused(tmp_path):
    reasons = guard.check_results(_junit(tmp_path, n=13))
    assert any("only 13" in reason for reason in reasons)


def test_corpus_not_collected_is_refused(tmp_path):
    reasons = guard.check_results(_junit(tmp_path, n=0))
    assert any("only 0" in reason for reason in reasons)


def test_skipped_corpus_case_is_refused(tmp_path):
    reasons = guard.check_results(_junit(tmp_path, defect="skipped"))
    assert any("skipped" in reason for reason in reasons)


def test_non_corpus_skip_is_also_refused(tmp_path):
    reasons = guard.check_results(_junit(tmp_path, outside_skip=True))
    assert any("test_other: skipped" in reason for reason in reasons)


def test_failure_and_error_are_refused(tmp_path):
    for defect in ("failure", "error"):
        reasons = guard.check_results(_junit(tmp_path, defect=defect))
        assert any(defect in reason for reason in reasons)


def test_unreadable_or_invalid_junit_is_refused(tmp_path):
    p = tmp_path / "missing.xml"
    assert "Cannot read" in guard.check_results(p)[0]
    p.write_text("<broken", encoding="utf-8")
    assert "Cannot read" in guard.check_results(p)[0]


def test_zero_testcases_refused(tmp_path):
    p = tmp_path / "empty.xml"
    p.write_text("<testsuite tests='0'></testsuite>", encoding="utf-8")
    assert "zero test cases" in guard.check_results(p)[0]


def test_cli_returns_failure_for_missing_report(tmp_path):
    assert guard.main([str(tmp_path / "missing.xml")]) == 1


def test_cli_returns_success_for_clean_report(tmp_path):
    assert guard.main([str(_junit(tmp_path))]) == 0
