"""Phase-3 T: pdf_match check (opt-in per project via preprint.pdf).

For each project that has a PDF at `<project>/preprint.pdf` (or a known
sibling), extract its text and verify that the numeric claims quoted in
the workbook body also appear in the PDF (with a generous tolerance for
formatting differences).

Phase 3 status: shipped + wired into build_assurance_jsons.py. No project
currently has a `preprint.pdf` — the check returns `not-run` for all
entries until operators start dropping preprints into project dirs.

Tolerance: the PDF should contain EVERY numeric claim from the body
verbatim or within ±0.02 absolute / ±5% relative. Missing 1 number = warn.
Missing >2 = fail. Empty body = not-run.

Returns pass | warn | fail | not-run.

PyPDF2 is the parser. If not installed, returns not-run (operator can
`pip install pypdf2` to opt in).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


PDF_CANDIDATES = ("preprint.pdf", "manuscript.pdf", "paper.pdf")
# Match numeric claims in the body: standalone decimals, percentages, CIs
NUMBER_RE = re.compile(r"\b(\d+\.\d+|\d+\s?%|\d{2,})\b")
TOLERANCE_ABS = 0.02
TOLERANCE_REL = 0.05


def _extract_pdf_text(pdf_path: Path) -> str | None:
    """Return PDF text via PyPDF2 (or None if unavailable / unreadable)."""
    try:
        import pypdf  # noqa: F401
    except ImportError:
        try:
            import PyPDF2 as pypdf  # type: ignore[no-redef]  # noqa: F401
        except ImportError:
            return None
    try:
        import pypdf
        reader = pypdf.PdfReader(str(pdf_path))
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # type: ignore
            reader = PdfReader(str(pdf_path))
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        except Exception:
            return None
    except Exception:
        return None


def _find_pdf(local_path: Path) -> Path | None:
    for name in PDF_CANDIDATES:
        p = local_path / name
        if p.is_file():
            return p
    return None


def _number_matches(body_num: str, pdf_text: str) -> bool:
    """Return True if body_num appears in pdf_text exactly or numerically
    within tolerance."""
    if body_num in pdf_text:
        return True
    # Numeric comparison fallback (e.g. body says "0.78" but PDF says "0.780")
    try:
        if body_num.endswith("%"):
            v = float(body_num.rstrip("%").strip()) / 100.0
        else:
            v = float(body_num)
    except ValueError:
        return False
    pat = re.compile(r"\b(\d+\.\d+|\d+)\b")
    for m in pat.finditer(pdf_text):
        try:
            pv = float(m.group(0))
        except ValueError:
            continue
        if abs(pv - v) < TOLERANCE_ABS:
            return True
        if v != 0 and abs(pv - v) / abs(v) < TOLERANCE_REL:
            return True
    return False


def derive_pdf_match(local_path: Path | None, body: str) -> str:
    """Returns one of: pass | warn | fail | not-run."""
    if local_path is None or not local_path.is_dir():
        return "not-run"
    if not body or len(body) < 50:
        return "not-run"
    pdf = _find_pdf(local_path)
    if pdf is None:
        return "not-run"
    pdf_text = _extract_pdf_text(pdf)
    if pdf_text is None:
        # PyPDF2 not installed — operator must opt in
        return "not-run"

    body_numbers = NUMBER_RE.findall(body)
    if not body_numbers:
        return "not-run"

    missing = []
    for n in body_numbers:
        if not _number_matches(n, pdf_text):
            missing.append(n)

    if not missing:
        return "pass"
    if len(missing) <= 1:
        return "warn"
    return "fail"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: pdf_match.py <project_path> <body-text-or-quoted-string>",
              file=sys.stderr)
        sys.exit(2)
    p = Path(sys.argv[1])
    body = sys.argv[2]
    result = derive_pdf_match(p, body)
    print(result)
    sys.exit(0 if result == "pass" else 1)
