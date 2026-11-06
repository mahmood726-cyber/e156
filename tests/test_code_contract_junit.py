"""Synthetic-only mutation coverage for the isolated E156 code-contract JUnit gate."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "assurance" / "check_code_contract_junit.py"
SPEC = importlib.util.spec_from_file_location("check_code_contract_junit", SCRIPT)
assert SPEC and SPEC.loader
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def report(tmp_path: Path) -> Path:
    root = ET.Element("testsuites")
    suite = ET.SubElement(root, "testsuite", {
        "tests": "47", "skipped": "0", "failures": "0", "errors": "0", "disabled": "0",
    })
    for module, count in checker.EXPECTED_MODULE_COUNTS.items():
        for i in range(count):
            ET.SubElement(suite, "testcase", {"classname": module, "name": f"test_{i}"})
    path = tmp_path / "synthetic-junit.xml"
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    return path


def test_valid_synthetic_report(tmp_path):
    assert checker.verify_report(report(tmp_path)) == checker.EXPECTED_MODULE_COUNTS


@pytest.mark.parametrize("mutation", [
    lambda root, suite: suite.set("disabled", "1"),
    lambda root, suite: suite.set("tests", "46"),
    lambda root, suite: suite.attrib.pop("tests"),
    lambda root, suite: suite.set("failures", "1"),
    lambda root, suite: suite.set("skipped", "1"),
    lambda root, suite: suite.set("errors", "-1"),
    lambda root, suite: suite.append(ET.Element("testcase", {"classname": "unknown", "name": "extra"})),
    lambda root, suite: suite[-1].set("name", suite[-2].get("name")),
    lambda root, suite: ET.SubElement(suite[0], "skipped"),
    lambda root, suite: suite[0].set("classname", "unreviewed_publication_test"),
    lambda root, suite: root.set("disabled", "1"),
])
def test_mutated_synthetic_report_refused(tmp_path, mutation):
    path = report(tmp_path)
    tree = ET.parse(path)
    root = tree.getroot()
    mutation(root, root[0])
    tree.write(path, encoding="utf-8", xml_declaration=True)
    with pytest.raises(checker.ContractReportError):
        checker.verify_report(path)
