"""Inline the e156 chart-kit (tokens.css + chartkit.js) into capsule HTML files,
staying 100% offline (no CDN, no <link>/<script src>). Idempotent: replaces the
content between the data-ck sentinel blocks if present, else inserts them.

Usage:
  python kit/inline_kit.py ../sglt2-hf-capsule.html [more-capsules.html ...]

Run from the flagship/ dir (paths are resolved relative to this file's kit/).
"""
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
TOKENS = (KIT / "tokens.css").read_text(encoding="utf-8")
CHARTKIT = (KIT / "chartkit.js").read_text(encoding="utf-8")

STYLE_BLOCK = '<style data-ck="CK:tokens">\n' + TOKENS + '\n</style>'
SCRIPT_BLOCK = '<script data-ck="CK:chartkit">\n' + CHARTKIT + '\n</script>'

_STYLE_RE = re.compile(r'<style data-ck="CK:tokens">.*?</style>', re.DOTALL)
_SCRIPT_RE = re.compile(r'<script data-ck="CK:chartkit">.*?</script>', re.DOTALL)


def inline(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    if "</script>" in CHARTKIT or "</style>" in TOKENS:
        raise SystemExit("kit source contains a literal closer — cannot inline safely")

    if _STYLE_RE.search(html):
        html, n = _STYLE_RE.subn(lambda _m: STYLE_BLOCK, html)
        style_action = f"updated ({n})"
    else:
        if html.count("</head>") != 1:
            raise SystemExit(f"{path.name}: need exactly one </head>")
        html = html.replace("</head>", STYLE_BLOCK + "\n</head>", 1)
        style_action = "inserted"

    if _SCRIPT_RE.search(html):
        html, n = _SCRIPT_RE.subn(lambda _m: SCRIPT_BLOCK, html)
        script_action = f"updated ({n})"
    else:
        i = html.index("<script")          # before the first (app) script
        html = html[:i] + SCRIPT_BLOCK + "\n" + html[i:]
        script_action = "inserted"

    path.write_text(html, encoding="utf-8")
    return f"tokens {style_action}, chartkit {script_action}"


def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    for p in argv:
        path = Path(p)
        if not path.is_file():
            print(f"  SKIP (missing): {p}")
            continue
        print(f"  {path.name}: {inline(path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
