"""Structural regression checks for the flagship capsule suite.

Every flagship `*-capsule.html` is a self-contained, offline single-file app.
These checks guard the invariants that have historically broken capsules:
div balance, a single real </script>, no Python->JS placeholder leaks, the
seeded-accent / localStorage / inspect-panel plumbing, the self-auditing
assurance ribbon, and full linkage from index.html. See rules/lessons.md
("Placeholder leaks", "</script> in template literals", "Div balance").
"""
import re
from pathlib import Path

import pytest

FLAGSHIP = Path(__file__).resolve().parent.parent / "flagship"
CAPSULES = sorted(FLAGSHIP.glob("*-capsule.html"))

# Patterns that signal an unfilled template or a Python None leaking into JS/HTML.
LEAK_PATTERNS = [
    r"REPLACE_ME",
    r"__PLACEHOLDER__",
    r"\{\{",
    r"\bNone\b",            # Python None rendered as a JS identifier / text
    r"\bn participants\b",  # unfilled f-string fallback (see lessons.md)
    r"None participants",
    r"None trials",
    r"/None\b",
]


def test_capsules_exist():
    # The suite is expected to be non-trivial; guard against an empty glob.
    assert len(CAPSULES) >= 40, f"expected >=40 capsules, found {len(CAPSULES)}"


@pytest.mark.parametrize("path", CAPSULES, ids=lambda p: p.name)
def test_div_balance(path):
    html = path.read_text(encoding="utf-8")
    opens = len(re.findall(r"<div[\s>]", html))
    closes = len(re.findall(r"</div>", html))
    assert opens == closes, f"{path.name}: <div>={opens} </div>={closes}"


@pytest.mark.parametrize("path", CAPSULES, ids=lambda p: p.name)
def test_single_script_closer(path):
    # A literal </script> inside a template literal would break the parser.
    html = path.read_text(encoding="utf-8")
    assert html.count("</script>") == 1, f"{path.name}: unexpected </script> count"


@pytest.mark.parametrize("path", CAPSULES, ids=lambda p: p.name)
def test_no_placeholder_leaks(path):
    html = path.read_text(encoding="utf-8")
    for pat in LEAK_PATTERNS:
        assert not re.search(pat, html), f"{path.name}: placeholder/leak pattern {pat!r}"


@pytest.mark.parametrize("path", CAPSULES, ids=lambda p: p.name)
def test_capsule_plumbing(path):
    """Seeded accent, local persistence, inspect panel, assurance ribbon, motto."""
    html = path.read_text(encoding="utf-8")
    assert "setProperty('--slug-hue'" in html, f"{path.name}: missing seeded accent hash"
    assert "e156:" in html, f"{path.name}: missing e156: localStorage namespace"
    assert "Function.toString" in html, f"{path.name}: missing inspect-the-computation panel"
    assert 'class="tier"' in html, f"{path.name}: missing assurance tier badge"
    assert "agree with itself" in html, f"{path.name}: missing capsule motto"


def test_index_links_every_capsule():
    index = (FLAGSHIP / "index.html").read_text(encoding="utf-8")
    missing = [p.name for p in CAPSULES if p.name not in index]
    assert not missing, f"capsules absent from index.html: {missing}"
