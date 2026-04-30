"""Compare each rapidmeta-finerenone app's k against the published reference MA.

For each landmark therapy with a well-known canonical k, count occurrences
of each trial name in the live REVIEW.html. A trial is "included" if it
appears ≥ 3 times (≤ 2 = passing mention). Compare to the published k.

Output: a chat-ready report flagging mismatches that aren't methodologically
defensible.
"""
from __future__ import annotations
import io
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PAGES = "https://mahmood726-cyber.github.io/rapidmeta-finerenone"

# Each entry: (app_slug, published_ref_description, expected_k, [canonical_trials])
LANDMARKS: list[tuple[str, str, int, list[str]]] = [
    ("SGLT2_HF",
     "Vaduganathan 2022 IPD-MA: 5 SGLT2-in-HF trials (DAPA-HF, EMPEROR-Red, EMPEROR-Pres, DELIVER, SOLOIST-WHF)",
     5, ["DAPA-HF", "EMPEROR-Reduced", "EMPEROR-Preserved", "DELIVER", "SOLOIST-WHF"]),
    ("SGLT2_CKD",
     "Nuffield SGLT2-MA Lancet 2022 CKD subset: usually 4-6 (DAPA-CKD, EMPA-KIDNEY, CREDENCE, SCORED, +/- SUSTAIN-3, +/- VERTIS-CV)",
     4, ["DAPA-CKD", "EMPA-KIDNEY", "CREDENCE", "SCORED"]),
    ("SGLT2_MACE_CVOT",
     "4 SGLT2 CVOTs canonical: EMPA-REG, CANVAS, DECLARE, VERTIS-CV (+/- SCORED)",
     4, ["EMPA-REG", "CANVAS", "DECLARE", "VERTIS-CV"]),
    ("FINERENONE",
     "FIDELITY pre-specified pooled = 2 (FIDELIO + FIGARO); +/- ARTS-DN",
     2, ["FIDELIO", "FIGARO"]),
    ("PCSK9",
     "FOURIER + ODYSSEY OUTCOMES = 2 (hard CV outcome); +/- SPIRE-1/2 = 4",
     2, ["FOURIER", "ODYSSEY"]),
    ("BEMPEDOIC_ACID",
     "CLEAR Outcomes pivotal; CLEAR Harmony, Wisdom, Serenity, Tranquility for LDL = 5",
     5, ["CLEAR Outcomes", "CLEAR Harmony", "CLEAR Wisdom", "CLEAR Serenity", "CLEAR Tranquility"]),
    ("INCLISIRAN",
     "ORION-9 / -10 / -11 = 3 (Phase III LDL trials)",
     3, ["ORION-9", "ORION-10", "ORION-11"]),
    ("GLP1_CVOT",
     "GLP-1 RA CVOT canon: ELIXA, LEADER, SUSTAIN-6, EXSCEL, REWIND, PIONEER-6, AMPLITUDE-O = ~7",
     7, ["LEADER", "SUSTAIN-6", "REWIND", "EXSCEL", "ELIXA", "PIONEER-6", "AMPLITUDE-O"]),
    ("COLCHICINE_CVD",
     "COLCOT + LoDoCo2 = 2 (hard CV outcome); some MAs include LoDoCo, COPS, CLEAR-SYNERGY",
     2, ["COLCOT", "LoDoCo2"]),
    ("MAVACAMTEN_HCM",
     "EXPLORER-HCM + VALOR-HCM (+/- MAVERICK) = 2-3",
     2, ["EXPLORER-HCM", "VALOR-HCM", "MAVERICK"]),
    ("DOAC_AF",
     "RE-LY + ROCKET-AF + ARISTOTLE + ENGAGE-AF = 4 NOAC pivotal AF",
     4, ["RE-LY", "ROCKET-AF", "ARISTOTLE", "ENGAGE-AF"]),
    ("RIVAROXABAN_VASC",
     "COMPASS + VOYAGER PAD = 2 (vascular protection)",
     2, ["COMPASS", "VOYAGER"]),
    ("TAVR_LOWRISK",
     "PARTNER 3 + Evolut Low Risk (+/- NOTION) = 2-3",
     2, ["PARTNER 3", "Evolut Low Risk", "NOTION"]),
    ("MITRAL_FUNCMR",
     "COAPT + MITRA-FR (+/- RESHAPE-HF2) = 2-3",
     2, ["COAPT", "MITRA-FR", "RESHAPE-HF"]),
    ("INCRETIN_HFpEF",
     "STEP-HFpEF + STEP-HFpEF-DM + SUMMIT = 3",
     3, ["STEP-HFpEF", "STEP-HFpEF-DM", "SUMMIT"]),
    ("SEMAGLUTIDE_OBESITY",
     "STEP 1-5 + STEP TEENS = 5-6",
     5, ["STEP 1", "STEP 2", "STEP 3", "STEP 4", "STEP 5", "STEP TEENS"]),
    ("TIRZEPATIDE_OBESITY",
     "SURMOUNT-1 + SURMOUNT-2 + SURMOUNT-3 + SURMOUNT-4 = 4",
     4, ["SURMOUNT-1", "SURMOUNT-2", "SURMOUNT-3", "SURMOUNT-4"]),
    ("CART_DLBCL",
     "ZUMA-7 + TRANSFORM + BELINDA = 3 (2L 3rd-gen CAR-T)",
     3, ["ZUMA-7", "TRANSFORM", "BELINDA"]),
    ("CART_MM",
     "KarMMa-3 + CARTITUDE-4 = 2 (Phase III BCMA CAR-T)",
     2, ["KarMMa-3", "CARTITUDE-4"]),
    ("TDXD_HER2LOW_BC",
     "DESTINY-Breast04 + DESTINY-Breast06 = 2",
     2, ["DESTINY-Breast04", "DESTINY-Breast06"]),
    ("VENETOCLAX_AML",
     "VIALE-A + VIALE-C = 2",
     2, ["VIALE-A", "VIALE-C"]),
    ("EVT_BASILAR",
     "BASICS + ATTENTION + BAOCHE = 3",
     3, ["BASICS", "ATTENTION", "BAOCHE"]),
    ("EVT_LARGECORE",
     "SELECT2 + RESCUE-Japan-LIMIT + ANGEL-ASPECT + TENSION + LASTE + TESLA = 6",
     6, ["SELECT2", "RESCUE-Japan-LIMIT", "ANGEL-ASPECT", "TENSION", "LASTE", "TESLA"]),
    ("EVT_EXTENDED_WINDOW",
     "DAWN + DEFUSE-3 = 2",
     2, ["DAWN", "DEFUSE-3"]),
    ("ANTIAMYLOID_AD",
     "Lecanemab CLARITY + Donanemab TRAILBLAZER-ALZ 2 (+/- Aducanumab EMERGE/ENGAGE) = 2-4",
     2, ["CLARITY", "TRAILBLAZER-ALZ", "EMERGE", "ENGAGE"]),
    ("PATISIRAN_POLYNEUROPATHY",
     "APOLLO + APOLLO-B = 2",
     2, ["APOLLO", "APOLLO-B"]),
    ("ATTR_CM",
     "ATTR-ACT + ATTRibute-CM + HELIOS-B + APOLLO-B = 4",
     4, ["ATTR-ACT", "ATTRibute-CM", "HELIOS-B", "APOLLO-B"]),
    ("DOAC_CANCER_VTE",
     "Hokusai-VTE Cancer + SELECT-D + Caravaggio + ADAM-VTE = 4",
     4, ["Hokusai", "SELECT-D", "Caravaggio", "ADAM-VTE"]),
    ("IV_IRON_HF",
     "FAIR-HF + CONFIRM-HF + AFFIRM-AHF + IRONMAN + HEART-FID = 5",
     4, ["FAIR-HF", "CONFIRM-HF", "AFFIRM-AHF", "IRONMAN", "HEART-FID"]),
]


def fetch(app: str) -> str:
    try:
        with urllib.request.urlopen(f"{PAGES}/{app}_REVIEW.html", timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"FETCH ERROR: {e}"


def audit_one(app: str, refdesc: str, expected_k: int, trials: list[str]) -> dict:
    h = fetch(app)
    if h.startswith("FETCH ERROR"):
        return {"app": app, "error": h}
    counts = {t: h.count(t) for t in trials}
    # Threshold 2 = trial appears at least once as a JS data row (real
    # inclusion). Threshold 1 = passing mention only (e.g., reference list).
    included = [t for t, n in counts.items() if n >= 2]
    observed_k = len(included)
    # Verdict
    if observed_k == expected_k:
        verdict = "MATCH"
    elif observed_k >= expected_k:
        verdict = "MORE-than-published"
    elif observed_k > 0:
        verdict = "FEWER-than-published"
    else:
        verdict = "ZERO-DETECTED"
    return {
        "app": app,
        "ref": refdesc,
        "expected_k": expected_k,
        "observed_k": observed_k,
        "included": included,
        "missing": [t for t in trials if t not in included],
        "trial_counts": counts,
        "verdict": verdict,
    }


def main() -> int:
    print(f"Auditing {len(LANDMARKS)} landmark therapies...\n", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        for r in ex.map(lambda x: audit_one(*x), LANDMARKS):
            results.append(r)
    # Print structured table
    print(f"{'APP':30s} {'EXP':>4s} {'OBS':>4s}  VERDICT             INCLUDED")
    print("-" * 110)
    mismatches = []
    for r in results:
        if "error" in r:
            print(f"{r['app']:30s}  ERROR: {r['error']}")
            continue
        inc = ", ".join(r["included"]) or "—"
        print(f"{r['app']:30s} {r['expected_k']:>4d} {r['observed_k']:>4d}  "
              f"{r['verdict']:18s}  {inc[:55]}")
        if r["verdict"] != "MATCH":
            mismatches.append(r)
    print()
    print(f"Mismatches needing review: {len(mismatches)}/{len(results)}")
    print()
    for r in mismatches:
        print(f"--- {r['app']} ---")
        print(f"  Reference: {r['ref']}")
        print(f"  Expected k: {r['expected_k']}, observed: {r['observed_k']}")
        print(f"  Included:  {r['included']}")
        print(f"  Missing:   {r['missing']}")
        print(f"  Counts:    {r['trial_counts']}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
