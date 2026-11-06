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
        "tests": str(sum(checker.EXPECTED_MODULE_COUNTS.values())), "skipped": "0", "failures": "0", "errors": "0", "disabled": "0",
    })
    for module, names in checker.EXPECTED_TEST_NAMES.items():
        for name in sorted(names):
            ET.SubElement(suite, "testcase", {"classname": module, "name": name})
    path = tmp_path / "synthetic-junit.xml"
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    return path


def test_valid_synthetic_report(tmp_path):
    assert checker.verify_report(report(tmp_path)) == checker.EXPECTED_MODULE_COUNTS


@pytest.mark.parametrize("mutation", [
    lambda root, suite: suite.set("disabled", "1"),
    lambda root, suite: suite.set("tests", str(int(suite.get("tests")) - 1)),
    lambda root, suite: suite.attrib.pop("tests"),
    lambda root, suite: suite.set("failures", "1"),
    lambda root, suite: suite.set("skipped", "1"),
    lambda root, suite: suite.set("errors", "-1"),
    lambda root, suite: suite.append(ET.Element("testcase", {"classname": "unknown", "name": "extra"})),
    lambda root, suite: suite[-1].set("name", suite[-2].get("name")),
    lambda root, suite: ET.SubElement(suite[0], "skipped"),
    lambda root, suite: suite[0].set("classname", "unreviewed_publication_test"),
    lambda root, suite: root.set("disabled", "1"),
    # Previously accepted: replacing a reviewed test preserves case counts.
    lambda root, suite: suite[0].set("name", "test_unreviewed_replacement"),
    # Previously accepted: matching only the module name after the last dot.
    lambda root, suite: suite[0].set("classname", "shadow.test_assurance_source_rights_preflight"),
])
def test_mutated_synthetic_report_refused(tmp_path, mutation):
    path = report(tmp_path)
    tree = ET.parse(path)
    root = tree.getroot()
    mutation(root, root[0])
    tree.write(path, encoding="utf-8", xml_declaration=True)
    with pytest.raises(checker.ContractReportError):
        checker.verify_report(path)
