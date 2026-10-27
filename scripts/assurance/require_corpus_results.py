"""Enforce that the Sentinel golden corpus actually ran in assurance CI.

A green pytest exit code alone is insufficient: pytest reports success when
all rule tests are skipped because Sentinel cannot import. Read the JUnit
report produced by the *actual* test run rather than rerunning selected tests.
This is a CI coverage integrity gate, not independent scientific validation.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

MIN_CORPUS_CASES = 14
# Stable, source-backed case names in tests/test_assurance_corpus.py. A minimum
# count by itself is not coverage: repeated or unrelated JUnit entries can
# otherwise stand in for missing Sentinel tests.
REQUIRED_CORPUS_CASES = frozenset({
    "test_malformed_doi_blocks",
    "test_locatorless_reference_warns",
    "test_valid_doi_clean",
    "test_fabricated_doi_blocked_via_resolution_cache",
    "test_citation_resolution_inert_without_cache",
    "test_citation_resolution_skips_skip_marker_files",
    "test_events_exceed_total_blocks",
    "test_ci_not_bracketing_hr_blocks",
    "test_consistent_data_clean",
    "test_consistent_but_wrong_pooled_estimate_is_caught",
    "test_causal_overclaim_word_fires",
    "test_certainty_plus_heterogeneity_fires",
    "test_hedged_claim_clean",
    "test_overclaim_without_trigger_word_is_caught",
})
CORPUS_CLASSNAMES = frozenset({"tests.test_assurance_corpus", "test_assurance_corpus"})
CORPUS_SOURCE = "tests/test_assurance_corpus.py"


def _is_corpus_case(case: ET.Element) -> bool:
    if (case.get("classname") or "") not in CORPUS_CLASSNAMES:
        return False
    source = (case.get("file") or "").replace("\\", "/")
    return not source or source == CORPUS_SOURCE



def check_results(path: Path, min_corpus: int = MIN_CORPUS_CASES) -> list[str]:
    problems: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        return [f"Cannot read assurance JUnit report {path}: {exc}"]

    cases = list(root.iter("testcase"))
    if not cases:
        return ["Assurance JUnit report contains zero test cases."]

    # A truncated but well-formed report can preserve all 14 named corpus
    # cases while omitting hundreds of other tests. Reconcile each JUnit
    # suite's declared total against its actual testcase elements, rather
    # than treating a partial report as complete evidence.
    suites = list(root.iter("testsuite"))
    if not suites:
        problems.append("Assurance JUnit report has no testsuite element.")
    for suite in suites:
        declared = suite.get("tests", "")
        actual = len(list(suite.iter("testcase")))
        if not (declared.isascii() and declared.isdecimal() and len(declared) <= 9):
            problems.append("Assurance JUnit testsuite has a missing or invalid test count.")
        elif int(declared) != actual:
            problems.append(
                f"Assurance JUnit testsuite declares {declared} tests but "
                f"contains {actual} testcase elements."
            )

    corpus = [case for case in cases if _is_corpus_case(case)]
    names = Counter(case.get("name") or "" for case in corpus)
    # Count unique cases, never raw XML elements: otherwise 14 copies of one
    # passing case would satisfy the historical threshold.
    if len(names) < min_corpus:
        problems.append(
            f"Sentinel corpus executed only {len(names)} unique of at least "
            f"{min_corpus} required cases."
        )
    missing = REQUIRED_CORPUS_CASES - names.keys()
    if missing:
        problems.append("Sentinel corpus missing named cases: " + ", ".join(sorted(missing)))
    repeated = sorted(name for name, count in names.items() if count > 1)
    if repeated:
        problems.append("Sentinel corpus duplicated case identities: " + ", ".join(repeated))

    for case in cases:
        label = f"{case.get('classname', '?')}.{case.get('name', '?')}"
        for kind in ("skipped", "failure", "error"):
            if case.find(kind) is not None:
                problems.append(f"Assurance test {label}: {kind}.")

    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("junit", type=Path, help="pytest --junitxml output")
    parser.add_argument("--min-corpus", type=int, default=MIN_CORPUS_CASES)
    args = parser.parse_args(argv)
    if args.min_corpus < 1:
        parser.error("--min-corpus must be positive")
    problems = check_results(args.junit, args.min_corpus)
    if problems:
        for issue in problems:
            print(f"ASSURANCE REFUSED: {issue}", file=sys.stderr)
        return 1
    print("Assurance JUnit coverage checked: named corpus present; no duplicate, skipped, failed or errored cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
