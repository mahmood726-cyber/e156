"""Enforce that the Sentinel golden corpus actually ran in assurance CI.

A green pytest exit code alone is insufficient: pytest reports success when
all rule tests are skipped because Sentinel cannot import. Read the JUnit
report produced by the *actual* test run rather than rerunning selected tests.
This is a CI coverage integrity gate, not independent scientific validation.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

MIN_CORPUS_CASES = 14


def check_results(path: Path, min_corpus: int = MIN_CORPUS_CASES) -> list[str]:
    problems: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        return [f"Cannot read assurance JUnit report {path}: {exc}"]

    cases = list(root.iter("testcase"))
    if not cases:
        return ["Assurance JUnit report contains zero test cases."]

    corpus = [
        case for case in cases
        if "test_assurance_corpus" in (
            (case.get("classname") or "") + "/" + (case.get("file") or "")
        )
    ]
    if len(corpus) < min_corpus:
        problems.append(
            f"Sentinel corpus executed only {len(corpus)} of at least "
            f"{min_corpus} required cases."
        )

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
    print("Assurance JUnit coverage checked: corpus present; no skipped, failed or errored cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
