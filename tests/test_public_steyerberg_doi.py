"""Source-linked, bounded public Steyerberg reference correction.

Synthetic string tests plus exact committed HTML checks, not clinical
adjudication or a live network DOI check. The workbook is never modified.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_paper_pages import _public_reference  # noqa: E402

BAD_DOI = "10.1097/EDE.0b013e3181c30fb7"
GOOD_DOI = "10.1097/EDE.0b013e3181c30fb2"
CITATION_START = "Steyerberg EW, Vickers AJ, Cook NR,"
CASES = (100, 328, 494)


@pytest.mark.parametrize("paper_num", CASES)
def test_public_citation_correction_is_scoped_to_confirmed_pages(paper_num):
    source = CITATION_START + " et al. 2010. Epidemiology. " + BAD_DOI
    rendered = _public_reference(paper_num, source)
    assert rendered == source.replace(BAD_DOI, GOOD_DOI)
    assert _public_reference(paper_num, rendered) == rendered
    assert _public_reference(999, source) == source
    assert _public_reference(paper_num, "Other author " + BAD_DOI) == "Other author " + BAD_DOI


@pytest.mark.parametrize("paper_num", CASES)
def test_unverified_future_citation_change_must_be_reconciled(paper_num):
    with pytest.raises(ValueError, match="source reconciliation"):
        _public_reference(paper_num, CITATION_START + " another unexpected suffix")


@pytest.mark.parametrize("paper_num", CASES)
def test_all_three_committed_public_pages_use_verified_doi(paper_num):
    page = (ROOT / "paper" / f"{paper_num}.html").read_text(encoding="utf-8")
    assert GOOD_DOI in page
    assert BAD_DOI not in page
    assert "Assessing the performance of prediction models" in page
