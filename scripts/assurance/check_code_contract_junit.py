"""Fail-closed JUnit coverage gate for the checkout-free E156 synthetic CI.

Only synthetic source-rights contract modules are permitted. This validates
pytest's actual report, not its exit code or untrusted article-derived data.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

# Exact reviewed test inventory. Deliberate changes must update this contract.
EXPECTED_MODULE_COUNTS = {
    "test_assurance_source_rights_preflight": 35,
    "test_code_contract_junit": 12,
}


class ContractReportError(ValueError):
    """JUnit evidence was missing, inconsistent, incomplete or untrusted."""


def _number(element: ET.Element, name: str, *, required: bool = True) -> int | None:
    raw = element.get(name)
    if raw is None:
        if required:
            raise ContractReportError(f"missing {element.tag}.{name}")
        return None
    if not raw.isdecimal():
        raise ContractReportError(f"invalid {element.tag}.{name}: {raw!r}")
    return int(raw)


def verify_report(path: Path) -> dict[str, int]:
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        raise ContractReportError("missing or invalid synthetic JUnit report") from exc

    if root.tag == "testsuite":
        suites = [root]
    elif root.tag == "testsuites":
        suites = list(root)
        if len(suites) != 1 or suites[0].tag != "testsuite":
            raise ContractReportError("expected exactly one synthetic pytest suite")
    else:
        raise ContractReportError("unrecognized JUnit root")
    suite = suites[0]
    cases = list(suite)
    if not cases or any(case.tag != "testcase" for case in cases):
        raise ContractReportError("unexpected or missing JUnit testcase elements")

    total = sum(EXPECTED_MODULE_COUNTS.values())
    if _number(suite, "tests") != len(cases) or len(cases) != total:
        raise ContractReportError("omitted, added, or inconsistent test count")
    for field in ("skipped", "failures", "errors"):
        if _number(suite, field) != 0:
            raise ContractReportError(f"nonzero {field} in synthetic suite")
    if _number(suite, "disabled", required=False) not in (None, 0):
        raise ContractReportError("disabled tests declared")

    if root is not suite:
        for field in ("tests", "skipped", "failures", "errors", "disabled"):
            value = _number(root, field, required=False)
            if value is not None and value != (total if field == "tests" else 0):
                raise ContractReportError(f"inconsistent root {field}")

    modules: Counter[str] = Counter()
    identities: set[tuple[str, str]] = set()
    for case in cases:
        klass, name = case.get("classname", ""), case.get("name", "")
        module = klass.rsplit(".", 1)[-1]
        if not klass or not name or module not in EXPECTED_MODULE_COUNTS:
            raise ContractReportError("unknown or unnamed synthetic test")
        identity = (klass, name)
        if identity in identities:
            raise ContractReportError("duplicate test identity")
        identities.add(identity)
        if list(case):
            raise ContractReportError("skipped, failed, errored, or modified testcase")
        modules[module] += 1
    if dict(modules) != EXPECTED_MODULE_COUNTS:
        raise ContractReportError(f"missing required synthetic test module coverage: {dict(modules)}")
    return dict(modules)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        modules = verify_report(args.report)
    except ContractReportError as exc:
        parser.exit(1, f"SOURCE_RIGHTS_HOLD: invalid synthetic CI evidence: {exc}\n")
    print(f"PASS: {sum(modules.values())} reviewed synthetic contracts; zero skipped, disabled or omitted cases")


if __name__ == "__main__":
    main()
