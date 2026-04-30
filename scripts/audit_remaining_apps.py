"""Audit every non-NMA, not-yet-audited rapidmeta-finerenone app for k.

Pulls trial names directly from each app's JS data (`name: '...'` fields),
filters methodological labels, and prints a clean k-with-trial-list per app.
The compare-to-published step is done in chat from this output.
"""
from __future__ import annotations
import io
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PAGES = "https://mahmood726-cyber.github.io/rapidmeta-finerenone"
REPO = "mahmood726-cyber/rapidmeta-finerenone"

ALREADY_AUDITED = {
    "SGLT2_HF","SGLT2_CKD","SGLT2_MACE_CVOT","FINERENONE","PCSK9",
    "BEMPEDOIC_ACID","INCLISIRAN","GLP1_CVOT","COLCHICINE_CVD",
    "MAVACAMTEN_HCM","DOAC_AF","RIVAROXABAN_VASC","TAVR_LOWRISK",
    "MITRAL_FUNCMR","INCRETIN_HFpEF","SEMAGLUTIDE_OBESITY",
    "TIRZEPATIDE_OBESITY","CART_DLBCL","CART_MM","TDXD_HER2LOW_BC",
    "VENETOCLAX_AML","EVT_BASILAR","EVT_LARGECORE","EVT_EXTENDED_WINDOW",
    "ANTIAMYLOID_AD","PATISIRAN_POLYNEUROPATHY","ATTR_CM",
    "DOAC_CANCER_VTE","IV_IRON_HF",
}

# Names that appear inside `name: '...'` but are NOT trials
METH_NAMES = {
    # plot/UI labels
    "posterior","prior","adjusted","conditional power","80% threshold",
    "analysis executed","sufficient studies","complete data","hksj concordance",
    "heterogeneity","publication bias (egger)","prediction interval",
    "fragility index","bayesian posterior","trim-and-fill","data seal",
    "grade certainty","protocol locked","version snapshots","cross-validation",
    "evidence extraction","provenance chain","copas selection model","cook",
    "hat","rstudent","dfbetas","data.csv","validate_r.r","validate_python.py",
    "provenance.json","bias","hksj","kaplan-meier","forest","funnel","sroc",
    "leave-one-out","cumulative","loa","ip","lower","upper","point","central",
    "active","inactive","placebo","control","intervention","treatment","comparator",
    "active comparator","summary","total","pooled","sensitivity","subgroup",
    "main","baseline","week","month","year","day","title","subtitle","label",
    "footer","header","caption","tooltip","legend","axis","x","y","z",
    "text","html","svg","json","csv","raw","clean","output","input",
    "metafor","r","python","js","node","webr","stan","jags","brms",
    "egger","peters","peter","arcsine","logit","sm","tau2","i2","q",
    "df","ll","ul","k","n","alpha","beta","gamma",
    "default","custom","user","admin","page","tab","panel","modal",
    "ok","cancel","next","prev","close","open","yes","no","true","false",
}


def list_reviews() -> list[str]:
    out = subprocess.check_output(
        ["gh", "api", f"repos/{REPO}/contents",
         "--jq", '.[] | select(.name | endswith("_REVIEW.html")) | .name'],
        text=True,
    )
    return sorted(ln.strip() for ln in out.splitlines() if ln.strip())


def fetch(name: str) -> str:
    try:
        with urllib.request.urlopen(f"{PAGES}/{name}", timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"FETCH ERROR: {e}"


def extract_trials(html: str) -> list[str]:
    if html.startswith("FETCH ERROR"):
        return []
    raw = list(re.finditer(r"""name:\s*['"]([^'"]+)['"]""", html))
    seen = []
    for m in raw:
        nm = m.group(1).strip()
        nl = nm.lower()
        if not nm or nm in seen:
            continue
        if nl in METH_NAMES:
            continue
        # Skip slugs that are clearly the app's own filename root
        if re.fullmatch(r"[a-z0-9_]+_$", nm):
            continue
        # Skip files
        if "." in nm and nm.split(".")[-1].lower() in {"csv","json","r","py","md","html","txt"}:
            continue
        # Skip lone words like "Active" or "Bias"
        if " " not in nm and len(nm) <= 4:
            continue
        seen.append(nm)
    return seen[:25]


def main() -> int:
    reviews = list_reviews()
    todo = [r for r in reviews
            if r.replace("_REVIEW.html", "") not in ALREADY_AUDITED
            and "_NMA_" not in r]  # skip NMA apps per user
    print(f"Auditing {len(todo)} apps (skipped {len(reviews)-len(todo)} already-audited or NMA)\n",
          flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex:
        for app in todo:
            html = fetch(app)
            trials = extract_trials(html)
            slug = app.replace("_REVIEW.html", "")
            tcount = len(trials)
            print(f"{slug:30s}  k={tcount:>2d}   trials: {trials[:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
