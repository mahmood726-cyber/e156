"""Independent audit of rapidmeta-finerenone meta-analysis apps.

For every REVIEW.html file in the repo, extract:
  - title
  - declared k (number of studies/trials)
  - named trials (from text)
  - primary effect estimate + 95% CI

The goal is to compare each app's `k` against the published reference
meta-analysis for that therapy. Methodological defensibility is judged
manually after this audit produces structured rows.

Output: audit_output/rapidmeta_k_audit_<date>.json
"""
from __future__ import annotations
import datetime as dt
import io
import json
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
OUT = E156 / "audit_output" / f"rapidmeta_k_audit_{dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')}.json"

REPO = "mahmood726-cyber/rapidmeta-finerenone"
PAGES_BASE = "https://mahmood726-cyber.github.io/rapidmeta-finerenone"

K_PATTERNS = [
    r"k\s*=\s*(\d+)\s*(?:trials?|RCTs?|studies)",
    r"(\d+)\s+(?:RCTs?|randomi[sz]ed (?:controlled )?trials?|trials? included|studies included|pivotal trials)",
    r"included\s+(\d+)\s+(?:RCTs?|trials?|studies)",
    r"pooled\s+(\d+)\s+(?:RCTs?|trials?|studies)",
    r"(\d+)\s+phase\s*[23]\s+(?:RCTs?|trials?)",
]
N_PATTERN = re.compile(r"([\d,]{3,})\s+(patients|participants|subjects)", re.IGNORECASE)
EFFECT_PATTERN = re.compile(
    r"\b(HR|OR|RR|MD|SMD|RD|RMST)\s*[:=]?\s*(-?\d+\.?\d*)\s*"
    r"\(\s*95%\s*(?:CI|CrI|HKSJ\s*CI)[:,\s]*(-?\d+\.?\d*)\s*[–\-,to]+\s*(-?\d+\.?\d*)",
    re.IGNORECASE,
)
TRIAL_NAME_PATTERN = re.compile(
    r"\b([A-Z]{2,12}(?:[-_][A-Za-z0-9]{1,12}){0,4})\b"  # acronym style
)
TITLE_PATTERN = re.compile(r"<title>(.+?)</title>", re.IGNORECASE | re.DOTALL)


def list_reviews() -> list[str]:
    out = subprocess.check_output(
        ["gh", "api", f"repos/{REPO}/contents",
         "--jq", '.[] | select(.name | endswith("_REVIEW.html")) | .name'],
        text=True,
    )
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def fetch(name: str) -> str:
    try:
        req = urllib.request.Request(
            f"{PAGES_BASE}/{name}",
            headers={"User-Agent": "Mozilla/5.0 (E156 audit)"},
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"<!--FETCH ERROR: {e}-->"


def html_to_text(html: str) -> str:
    h = re.sub(r"<script\b.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    h = re.sub(r"<style\b.*?</style>", " ", h, flags=re.DOTALL | re.IGNORECASE)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", h)


def parse(name: str, html: str) -> dict:
    if html.startswith("<!--FETCH ERROR"):
        return {"file": name, "error": html}
    title_m = TITLE_PATTERN.search(html)
    title = title_m.group(1).strip() if title_m else name
    title = re.sub(r"\s+", " ", title)
    text = html_to_text(html)

    ks: list[int] = []
    for pat in K_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            try:
                v = int(m.group(1))
                if 1 <= v <= 200:
                    ks.append(v)
            except ValueError:
                pass

    # Most plausible k = the most-frequent value in the small-to-mid range
    from collections import Counter
    k_consensus = None
    if ks:
        most_common = Counter(ks).most_common()
        k_consensus = most_common[0][0]

    # Sample sizes
    n_matches = N_PATTERN.findall(text)
    ns = []
    for n_str, _ in n_matches:
        try:
            n = int(n_str.replace(",", ""))
            if 50 <= n <= 5_000_000:
                ns.append(n)
        except ValueError:
            pass

    # Effects
    effects = []
    for m in EFFECT_PATTERN.finditer(text):
        try:
            effects.append({
                "label": m.group(1).upper(),
                "point": float(m.group(2)),
                "lo": float(m.group(3)),
                "hi": float(m.group(4)),
            })
        except (ValueError, IndexError):
            pass

    # Candidate trial acronyms
    acronyms = TRIAL_NAME_PATTERN.findall(text)
    # Filter to plausible trial names — exclude common HTML acronyms
    deny = {"HTML", "CSS", "JS", "JSON", "API", "URL", "DOI", "PDF", "ORCID",
            "WHO", "FDA", "EMA", "NICE", "GRADE", "PRISMA", "PROSPERO",
            "RCT", "CI", "OR", "HR", "RR", "SMD", "MD", "AUC", "I2",
            "PI", "PRD", "USA", "UK", "EU", "AHA", "ACC", "ESC", "EASD",
            "RAW", "DARK", "MODE", "LIGHT", "SVG", "JPG", "PNG", "SCSS",
            "PFS", "OS", "CR", "PR", "PRR", "MA", "NMA", "DTA", "IPD",
            "SE", "SD", "ITT", "PP", "PFA", "DM", "T2D", "T1D", "BP",
            "HF", "HFREF", "HFPEF", "HFmrEF", "AF", "MI", "STEMI", "NSTEMI",
            "PCI", "AKI", "CKD", "CV", "CVD", "ESRD", "DLBCL", "AML", "CLL",
            "MM", "NHL", "TNBC", "HER2", "ER", "BRCA", "PARP", "PSA", "MRI",
            "CT", "PET", "ECG", "EEG", "FMR", "MR", "TR", "SR", "TIA",
    }
    trial_candidates = sorted(set(a for a in acronyms if a not in deny and len(a) <= 18))
    # Heuristic: keep only those that appear ≥ 2 times in text (likely a trial reference)
    cnt = Counter(acronyms)
    trial_likely = [a for a in trial_candidates if cnt[a] >= 2 and len(a) >= 3 and not a.isdigit()][:30]

    return {
        "file": name,
        "title": title,
        "k_candidates": sorted(set(ks)),
        "k_consensus": k_consensus,
        "n_max": max(ns) if ns else None,
        "n_count": len(set(ns)),
        "effects_first3": effects[:3],
        "trial_acronyms": trial_likely,
    }


def main() -> int:
    reviews = list_reviews()
    print(f"Auditing {len(reviews)} REVIEW.html files...", flush=True)
    rows = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(fetch, n): n for n in reviews}
        for i, f in enumerate(as_completed(futures), 1):
            name = futures[f]
            html = f.result()
            rows.append(parse(name, html))
            if i % 20 == 0:
                print(f"  {i}/{len(reviews)} fetched", flush=True)

    rows.sort(key=lambda r: r.get("file", ""))
    OUT.write_text(json.dumps({"reviews": rows}, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"\nWrote {OUT}")
    print(f"Reviews with k extracted: {sum(1 for r in rows if r.get('k_consensus'))}/{len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
