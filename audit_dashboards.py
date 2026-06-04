#!/usr/bin/env python
"""Static quality audit of the e156 dashboards + flagship stat capsules."""
import glob
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
FILES = (["e156-library.html", "flagship/index.html", "e156-submission/index.html"]
         + sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "flagship", "*-capsule.html"))))

PLACE = re.compile(r"\{\{[^}]+\}\}|REPLACE_ME|__PLACEHOLDER__|\bPLACEHOLDER\b"
                   r"|\bTODO\b|\bFIXME\b|lorem ipsum", re.I)
LOCAL = re.compile(r"[A-Za-z]:\\Users|file:///|/Users/[a-z]|/home/[a-z]")
CDN = re.compile(r'(?:src|href)="https?://(?!fonts\.googleapis|fonts\.gstatic)[^"]+\.(?:js|css)"')
NANTXT = re.compile(r">\s*(?:NaN|undefined|null)\s*<")


def main():
    issues = {}
    ok = 0
    for rel in FILES:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            issues[rel] = ["MISSING FILE"]
            continue
        raw = open(p, "rb").read()
        bom = raw[:3] == b"\xef\xbb\xbf"
        t = raw.decode("utf-8", "replace")
        probs = []
        ph = [m.group(0)[:24] for m in PLACE.finditer(t)]
        if ph:
            probs.append(f"placeholders={len(ph)}:{ph[:2]}")
        # broken script: a literal </script> inside a <script> body would make
        # </script> count exceed <script count
        if t.count("</script>") > t.count("<script"):
            probs.append("extra </script> (template-literal break?)")
        db = len(re.findall(r"<div[\s>]", t)) - t.count("</div>")
        if db != 0:
            probs.append(f"div_balance={db}")
        if LOCAL.search(t):
            probs.append(f"localpath={len(LOCAL.findall(t))}")
        cdn = CDN.findall(t)
        if cdn:
            probs.append(f"external_cdn={len(cdn)}:{[c[:46] for c in cdn[:1]]}")
        nan = len(NANTXT.findall(t))
        if nan:
            probs.append(f"NaN/undef_in_text={nan}")
        if "</html>" not in t.lower():
            probs.append("no </html>")
        if "<body" not in t.lower():
            probs.append("no <body>")
        if bom:
            probs.append("BOM")
        if probs:
            issues[rel] = probs
        else:
            ok += 1
    print(f"audited {len(FILES)} files: {ok} clean, {len(issues)} with findings\n")
    for f, p in sorted(issues.items()):
        print(f"  {f}")
        for x in p:
            print(f"       - {x}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
