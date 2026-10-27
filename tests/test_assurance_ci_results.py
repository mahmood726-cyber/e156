"""Mutation tests: the assurance JUnit gate must refuse false-green cases."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest
import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "assurance" / "require_corpus_results.py"
SPEC = importlib.util.spec_from_file_location("require_corpus_results", SCRIPT)
assert SPEC and SPEC.loader
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


def _junit(tmp_path: Path, n: int = 14, *, defect: str | None = None,
           outside_skip: bool = False) -> Path:
    root = ET.Element("testsuite", {"tests": str(n + 1)})
    for i, name in enumerate(sorted(guard.REQUIRED_CORPUS_CASES)[:n]):
        case = ET.SubElement(root, "testcase", {
            "classname": "tests.test_assurance_corpus", "name": name,
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


def _full_junit(tmp_path: Path) -> Path:
    """Synthetic full-size CLI fixture, NOT a real hosted runner report."""
    path = _junit(tmp_path)
    tree = ET.parse(path)
    root = tree.getroot()
    existing = len(list(root.iter("testcase")))
    for i in range(guard.MIN_ASSURANCE_TESTS - existing):
        ET.SubElement(root, "testcase", {
            "classname": "tests.test_synthetic_fixture",
            "name": f"test_fixture_{i:03d}",
        })
    root.set("tests", str(len(list(root.iter("testcase")))))
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return path


def _alter(tmp_path: Path, change) -> Path:
    p = _junit(tmp_path)
    tree = ET.parse(p)
    change(list(tree.getroot().iter("testcase"))[:-1])
    tree.write(p, encoding="utf-8", xml_declaration=True)
    return p


def test_clean_corpus_and_unrelated_test_pass(tmp_path):
    assert guard.check_results(_junit(tmp_path)) == []


def test_missing_corpus_cases_are_refused(tmp_path):
    reasons = guard.check_results(_junit(tmp_path, n=13))
    assert any("only 13" in reason for reason in reasons)


def test_corpus_not_collected_is_refused(tmp_path):
    reasons = guard.check_results(_junit(tmp_path, n=0))
    assert any("only 0" in reason for reason in reasons)


def test_truncated_junit_report_cannot_mimic_complete_suite(tmp_path):
    # Negative XML fixture: all 14 real corpus identities are present, but a
    # declared 527-test run has been truncated to only 15 XML testcases.
    path = _junit(tmp_path)
    tree = ET.parse(path)
    tree.getroot().set("tests", "527")
    tree.write(path, encoding="utf-8", xml_declaration=True)
    reasons = guard.check_results(path)
    assert any("declares 527 tests but contains 15 testcase" in reason for reason in reasons)


@pytest.mark.parametrize("declared", [None, "", "unknown", "-1", "9" * 100])
def test_missing_or_invalid_junit_suite_count_is_refused(tmp_path, declared):
    path = _junit(tmp_path)
    tree = ET.parse(path)
    if declared is None:
        tree.getroot().attrib.pop("tests")
    else:
        tree.getroot().set("tests", declared)
    tree.write(path, encoding="utf-8", xml_declaration=True)
    reasons = guard.check_results(path)
    assert any("missing or invalid test count" in reason for reason in reasons)


def test_junit_without_testsuite_container_is_refused(tmp_path):
    path = _junit(tmp_path)
    tree = ET.parse(path)
    tree.getroot().tag = "not_a_testsuite"
    tree.write(path, encoding="utf-8", xml_declaration=True)
    assert any("no testsuite" in reason for reason in guard.check_results(path))


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


def test_cli_rejects_self_consistent_short_junit_report(tmp_path, capsys):
    # All 14 corpus names present, 15 XML elements, and declared tests=15.
    # Previously accepted as a complete suite despite omitted other tests.
    path = _junit(tmp_path)
    assert guard.check_results(path) == []  # Corpus-only helper intentionally permissive.
    assert guard.main([str(path)]) == 1
    assert "only 15 testcases" in capsys.readouterr().err


def test_cli_rejects_one_below_audited_floor_with_matching_xml_totals(tmp_path, capsys):
    path = _full_junit(tmp_path)
    tree = ET.parse(path)
    root = tree.getroot()
    root.remove(root[-1])
    root.set("tests", str(guard.MIN_ASSURANCE_TESTS - 1))
    tree.write(path, encoding="utf-8", xml_declaration=True)
    assert guard.main([str(path)]) == 1
    assert "audited whole-suite minimum" in capsys.readouterr().err


def test_cli_returns_failure_for_missing_report(tmp_path):
    assert guard.main([str(tmp_path / "missing.xml")]) == 1


def test_cli_returns_success_for_clean_report(tmp_path):
    assert guard.main([str(_full_junit(tmp_path))]) == 0


def require_junit_artifact_policy(workflow: str) -> None:
    """Refuse a PR gate that can silently omit the actual JUnit evidence."""
    steps = yaml.safe_load(workflow)["jobs"]["assurance-tests"]["steps"]
    uploads = [s for s in steps if s.get("uses", "").startswith("actions/upload-artifact@")]
    assert len(uploads) == 1, "One JUnit artifact upload is required"
    upload = uploads[0]
    assert upload.get("if") == "always()", "Upload must execute even after failures"
    assert upload.get("with", {}).get("path") == (
        "${{ runner.temp }}/e156-assurance-junit.xml"
    ), "Upload must preserve the actual test result"
    assert upload["with"].get("if-no-files-found") == "error", (
        "Missing JUnit evidence must fail the job, not warn"
    )


def test_assurance_pr_artifact_upload_fails_closed():
    workflow = (Path(__file__).resolve().parents[1] /
                ".github/workflows/assurance-pr.yml").read_text(encoding="utf-8")
    require_junit_artifact_policy(workflow)
    # Configuration failure injection, not a live failed GitHub-hosted upload.
    for weakened in (
        workflow.replace("if-no-files-found: error", "if-no-files-found: warn"),
        workflow.replace("if-no-files-found: error", ""),
        workflow.replace("if: always()", "if: success()"),
    ):
        assert weakened != workflow, "Mutation fixture no longer reaches target"
        with pytest.raises(AssertionError):
            require_junit_artifact_policy(weakened)


def test_repeated_one_test_name_cannot_mimic_fourteen_corpus_tests(tmp_path):
    p = _alter(tmp_path, lambda cases: [case.set("name", "test_malformed_doi_blocks") for case in cases])
    reasons = guard.check_results(p)
    assert any("only 1 unique" in reason for reason in reasons)
    assert any("duplicated case identities" in reason for reason in reasons)
    assert any("missing named cases" in reason for reason in reasons)


def test_spoofed_corpus_classname_substring_is_not_accepted(tmp_path):
    p = _alter(tmp_path, lambda cases: [case.set("classname", "tests.not_test_assurance_corpus_mock") for case in cases])
    reasons = guard.check_results(p)
    assert any("only 0 unique" in reason for reason in reasons)


def test_corpus_name_with_unrelated_source_file_is_not_accepted(tmp_path):
    p = _alter(tmp_path, lambda cases: [case.set("file", "tests/not_the_corpus.py") for case in cases])
    reasons = guard.check_results(p)
    assert any("only 0 unique" in reason for reason in reasons)


def test_unknown_names_cannot_mimic_required_corpus_coverage(tmp_path):
    p = _alter(tmp_path, lambda cases: [case.set("name", f"test_placeholder_{i}") for i, case in enumerate(cases)])
    reasons = guard.check_results(p)
    assert any("missing named cases" in reason for reason in reasons)


def test_one_missing_expected_name_replaced_by_invented_case_refused(tmp_path):
    p = _alter(tmp_path, lambda cases: cases[0].set("name", "test_invented_case"))
    reasons = guard.check_results(p)
    assert any("missing named cases" in reason for reason in reasons)


def test_corpus_file_windows_separators_still_accepted(tmp_path):
    p = _alter(tmp_path, lambda cases: [case.set("file", r"tests\test_assurance_corpus.py") for case in cases])
    assert guard.check_results(p) == []


def test_corpus_file_unix_separators_still_accepted(tmp_path):
    p = _alter(tmp_path, lambda cases: [case.set("file", "tests/test_assurance_corpus.py") for case in cases])
    assert guard.check_results(p) == []
