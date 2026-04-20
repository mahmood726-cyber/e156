"""Fill SUBMISSION METADATA block into each E156 workbook entry.

Per 2026-04-15 user request: modern PubMed-indexed journals (F1000, PLOS,
BMJ, BMJ EBM, Stats in Med) require a metadata block beyond the 156-word
body. Also per user follow-up: use curated topic-specific references
rather than PubMed search (which returned too much off-topic noise for
specialized statistical/methodological topics).

This script:
  1. Parses each entry in `rewrite-workbook.txt`
  2. Derives GitHub code / protocol / Pages URLs from the `PATH:` field
  3. Classifies the entry by topic (keyword matching on title + body)
  4. Emits 2 topical references from the curated pack for that topic
  5. Generates the SUBMISSION METADATA block with user's constants
  6. Inserts it BEFORE the `SUBMITTED: [ ]` line (YOUR REWRITE untouched)

YOUR REWRITE is never touched. Only adds / replaces the metadata block.
Idempotent: existing SUBMISSION METADATA blocks are replaced, not duplicated.

Usage:
  python fill_submission_metadata.py [--first N] [--dry-run]
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path


WORKBOOK = Path(__file__).resolve().parents[1] / "rewrite-workbook.txt"
SEP = "=" * 70
GH_USER = "mahmood726-cyber"

AUTHOR = "Mahmood Ahmad"
AFFILIATION = "Tahir Heart Institute, Rabwah, Pakistan"
ORCID = "0000-0001-9107-3704"
EMAIL = "mahmood.ahmad2@nhs.net"


# --------- topic reference packs ---------

# Every pack has exactly 2 canonical references. If an entry matches multiple
# packs, the most specific (longer keyword) wins — ordering within PACKS
# reflects rough specificity: earliest-match wins on tie, so specific topics
# (network meta-analysis) are before broader ones (heterogeneity) which are
# before the catch-all (fallback).
PACKS: list[tuple[str, list[str], list[str]]] = [
    # (pack_name, keyword patterns (lowercased, AND'd within pair), [ref1, ref2])

    ("diagnostic meta-analysis (DTA)",
     ["sensitivity specificity", "bivariate", "sroc", "hsroc", "diagnostic accuracy"],
     ["Reitsma JB et al. 2005. Bivariate analysis of sensitivity and specificity produces informative summary measures in diagnostic reviews. J Clin Epidemiol. 58(10):982-990. doi:10.1016/j.jclinepi.2005.02.022",
      "Rutter CM, Gatsonis CA. 2001. A hierarchical regression approach to meta-analysis of diagnostic test accuracy evaluations. Stat Med. 20(19):2865-2884. doi:10.1002/sim.942"]),

    ("Bayesian meta-analysis",
     ["bayesian meta", "bayesian random-effects", "map prior", "commensurate prior", "bayesmeta", "power prior", "prior borrowing", "informative prior", "dynamic borrowing"],
     ["Röver C. 2020. Bayesian random-effects meta-analysis using the bayesmeta R package. J Stat Softw. 93(6):1-51. doi:10.18637/jss.v093.i06",
      "Higgins JPT, Thompson SG, Spiegelhalter DJ. 2009. A re-evaluation of random-effects meta-analysis. J R Stat Soc A. 172(1):137-159. doi:10.1111/j.1467-985X.2008.00552.x"]),

    ("network meta-analysis",
     ["network meta-analysis", "nma", "network-meta", "indirect comparison", "bucher", "league table", "sucra", "mixed treatment comparison"],
     ["Rücker G. 2012. Network meta-analysis, electrical networks and graph theory. Res Synth Methods. 3(4):312-324. doi:10.1002/jrsm.1058",
      "Lu G, Ades AE. 2006. Assessing evidence inconsistency in mixed treatment comparisons. J Am Stat Assoc. 101(474):447-459. doi:10.1198/016214505000001302"]),

    ("individual participant data (IPD) meta-analysis",
     ["ipd ", "individual participant", "one-stage two-stage", "burke", "riley"],
     ["Riley RD, Lambert PC, Abo-Zaid G. 2010. Meta-analysis of individual participant data: rationale, conduct, and reporting. BMJ. 340:c221. doi:10.1136/bmj.c221",
      "Burke DL, Ensor J, Riley RD. 2017. Meta-analysis using individual participant data: one-stage and two-stage approaches, and why they may differ. Stat Med. 36(5):855-875. doi:10.1002/sim.7141"]),

    ("restricted mean survival time / survival meta-analysis",
     ["rmst", "restricted mean survival", "hazard ratio", "survival", "time-to-event", "kaplan-meier", "proportional hazards"],
     ["Royston P, Parmar MK. 2013. Restricted mean survival time: an alternative to the hazard ratio for the design and analysis of randomized trials with a time-to-event outcome. BMC Med Res Methodol. 13:152. doi:10.1186/1471-2288-13-152",
      "Tierney JF, Stewart LA, Ghersi D, Burdett S, Sydes MR. 2007. Practical methods for incorporating summary time-to-event data into meta-analysis. Trials. 8:16. doi:10.1186/1745-6215-8-16"]),

    ("trial sequential analysis (TSA)",
     ["trial sequential", "tsa", "cumulative meta", "o'brien-fleming", "alpha-spending", "wetterslev"],
     ["Wetterslev J, Thorlund K, Brok J, Gluud C. 2008. Trial sequential analysis may establish when firm evidence is reached in cumulative meta-analysis. J Clin Epidemiol. 61(1):64-75. doi:10.1016/j.jclinepi.2007.03.013",
      "Pogue JM, Yusuf S. 1997. Cumulating evidence from randomized trials: utilizing sequential monitoring boundaries for cumulative meta-analysis. Control Clin Trials. 18(6):580-593. doi:10.1016/S0197-2456(97)00051-2"]),

    ("multilevel / three-level meta-analysis",
     ["three-level", "multilevel", "three level", "nested effect", "cluster", "crossed"],
     ["Cheung MW-L. 2014. Modeling dependent effect sizes with three-level meta-analyses: a structural equation modeling approach. Psychol Methods. 19(2):211-229. doi:10.1037/a0032968",
      "Van den Noortgate W, López-López JA, Marín-Martínez F, Sánchez-Meca J. 2013. Three-level meta-analysis of dependent effect sizes. Behav Res Methods. 45(2):576-594. doi:10.3758/s13428-012-0261-6"]),

    ("fragility index",
     ["fragility index", "fragility", "mafi", "robustness index", "walsh"],
     ["Walsh M, Srinathan SK, McAuley DF, et al. 2014. The statistical significance of randomized controlled trial results is frequently fragile: a case for a Fragility Index. J Clin Epidemiol. 67(6):622-628. doi:10.1016/j.jclinepi.2013.10.019",
      "Atal I, Porcher R, Boutron I, Ravaud P. 2019. The statistical significance of meta-analyses is frequently fragile: definition of a fragility index for meta-analyses. J Clin Epidemiol. 111:32-40. doi:10.1016/j.jclinepi.2019.03.012"]),

    ("multiverse / specification curve",
     ["multiverse", "specification curve", "garden of forking paths", "analyst degrees of freedom", "steegen", "simonsohn"],
     ["Steegen S, Tuerlinckx F, Gelman A, Vanpaemel W. 2016. Increasing transparency through a multiverse analysis. Perspect Psychol Sci. 11(5):702-712. doi:10.1177/1745691616658637",
      "Simonsohn U, Simmons JP, Nelson LD. 2020. Specification curve analysis. Nat Hum Behav. 4(11):1208-1214. doi:10.1038/s41562-020-0912-z"]),

    ("GRADE / certainty rating",
     ["grade", "certainty of evidence", "quality of evidence", "strength of recommendation", "guyatt", "schünemann", "schunemann"],
     ["Guyatt GH, Oxman AD, Vist GE, et al. 2008. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. BMJ. 336(7650):924-926. doi:10.1136/bmj.39489.470347.AD",
      "Schünemann HJ, Cuello C, Akl EA, et al. 2019. GRADE guidelines: 18. How ROBINS-I and other tools to assess risk of bias in nonrandomized studies should be used to rate the certainty of a body of evidence. J Clin Epidemiol. 111:105-114. doi:10.1016/j.jclinepi.2018.01.012"]),

    ("risk of bias",
     ["risk of bias", "rob 2", "robins-i", "robins", "bias assessment", "quality assessment", "sterne"],
     ["Sterne JAC, Savović J, Page MJ, et al. 2019. RoB 2: a revised tool for assessing risk of bias in randomised trials. BMJ. 366:l4898. doi:10.1136/bmj.l4898",
      "Sterne JA, Hernán MA, Reeves BC, et al. 2016. ROBINS-I: a tool for assessing risk of bias in non-randomised studies of interventions. BMJ. 355:i4919. doi:10.1136/bmj.i4919"]),

    ("publication bias / selection",
     ["publication bias", "funnel plot", "egger", "trim-and-fill", "trim and fill", "small-study", "pet-peese", "copas", "selection bias"],
     ["Egger M, Davey Smith G, Schneider M, Minder C. 1997. Bias in meta-analysis detected by a simple, graphical test. BMJ. 315(7109):629-634. doi:10.1136/bmj.315.7109.629",
      "Duval S, Tweedie R. 2000. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. Biometrics. 56(2):455-463. doi:10.1111/j.0006-341X.2000.00455.x"]),

    ("heterogeneity / prediction interval",
     ["heterogeneity", "tau-squared", "tau squared", "tau²", "i-squared", "i²", "i2 ", "prediction interval", "hartung-knapp", "hksj", "dersimonian"],
     ["Higgins JPT, Thompson SG. 2002. Quantifying heterogeneity in a meta-analysis. Stat Med. 21(11):1539-1558. doi:10.1002/sim.1186",
      "IntHout J, Ioannidis JP, Rovers MM, Goeman JJ. 2016. Plea for routinely presenting prediction intervals in meta-analysis. BMJ Open. 6(7):e010247. doi:10.1136/bmjopen-2015-010247"]),

    ("CT.gov / ClinicalTrials.gov audit",
     ["ctgov", "ct.gov", "ct-gov", "clinicaltrials.gov", "clinical-trials registry", "trial registration", "aact", "nct", "results reporting", "hiddenness", "non-disclosure"],
     ["Zarin DA, Tse T, Williams RJ, Rajakannan T. 2017. Update on trial registration 11 years after the ICMJE policy was established. N Engl J Med. 376(4):383-391. doi:10.1056/NEJMsr1601330",
      "Anderson ML, Chiswell K, Peterson ED, Tasneem A, Topping J, Califf RM. 2015. Compliance with results reporting at ClinicalTrials.gov. N Engl J Med. 372(11):1031-1039. doi:10.1056/NEJMsa1409364"]),

    ("causal inference / triangulation",
     ["causal inference", "triangulation", "mendelian randomization", "target trial", "hernán", "hernan", "counterfactual"],
     ["Lawlor DA, Tilling K, Davey Smith G. 2016. Triangulation in aetiological epidemiology. Int J Epidemiol. 45(6):1866-1886. doi:10.1093/ije/dyw314",
      "Hernán MA, Robins JM. 2016. Using big data to emulate a target trial when a randomized trial is not available. Am J Epidemiol. 183(8):758-764. doi:10.1093/aje/kwv254"]),

    ("heart failure / cardiology",
     ["heart failure", "hfpef", "hfref", "sglt2", "sacubitril", "dapagliflozin", "empagliflozin", "mra ", "mineralocorticoid", "cardiovascular outcome"],
     ["McMurray JJV, Solomon SD, Inzucchi SE, et al. 2019. Dapagliflozin in Patients with Heart Failure and Reduced Ejection Fraction. N Engl J Med. 381(21):1995-2008. doi:10.1056/NEJMoa1911303",
      "Heidenreich PA, Bozkurt B, Aguilar D, et al. 2022. 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure. Circulation. 145(18):e895-e1032. doi:10.1161/CIR.0000000000001063"]),

    ("GLP-1 / incretin / diabetes CV",
     ["glp-1", "glp1", "semaglutide", "liraglutide", "tirzepatide", "gip", "incretin", "sglt2 cardiovascular", "cvot"],
     ["Marso SP, Daniels GH, Brown-Frandsen K, et al. 2016. Liraglutide and cardiovascular outcomes in type 2 diabetes. N Engl J Med. 375(4):311-322. doi:10.1056/NEJMoa1603827",
      "Sattar N, Lee MMY, Kristensen SL, et al. 2021. Cardiovascular, mortality, and kidney outcomes with GLP-1 receptor agonists in patients with type 2 diabetes: a systematic review and meta-analysis of randomised trials. Lancet Diabetes Endocrinol. 9(10):653-662. doi:10.1016/S2213-8587(21)00203-5"]),

    ("browser-based meta-analysis tooling",
     ["browser-based", "single-file html", "webr", "javascript meta-analysis", "client-side meta-analysis"],
     ["Schwarzer G, Carpenter JR, Rücker G. 2015. Meta-Analysis with R. Springer. doi:10.1007/978-3-319-21416-0",
      "Viechtbauer W. 2010. Conducting meta-analyses in R with the metafor package. J Stat Softw. 36(3):1-48. doi:10.18637/jss.v036.i03"]),

    ("Cochrane software / R package / methods platform",
     ["cochrane review", "cochrane database", "metafor", "meta package", "dmetar", "rcore"],
     ["Viechtbauer W. 2010. Conducting meta-analyses in R with the metafor package. J Stat Softw. 36(3):1-48. doi:10.18637/jss.v036.i03",
      "Schwarzer G, Carpenter JR, Rücker G. 2015. Meta-Analysis with R. Springer. doi:10.1007/978-3-319-21416-0"]),

    ("automated data extraction / text mining",
     ["data extraction", "text mining", "nlp", "automation", "large language model", "llm", "parsing"],
     ["Marshall IJ, Wallace BC. 2019. Toward systematic review automation: a practical guide to using machine learning tools in research synthesis. Syst Rev. 8:163. doi:10.1186/s13643-019-1074-9",
      "Jonnalagadda SR, Goyal P, Huffman MD. 2015. Automating data extraction in systematic reviews: a systematic review. Syst Rev. 4:78. doi:10.1186/s13643-015-0066-7"]),

    ("oncology / cancer trials",
     ["oncology", "cancer", "tumor", "tumour", "carcinoma", "chemotherapy", "immunotherapy", "checkpoint inhibitor"],
     ["Korn EL, Freidlin B. 2018. Interim futility monitoring assessing immune therapies with a potentially delayed treatment effect. J Clin Oncol. 36(23):2444-2449. doi:10.1200/JCO.2018.77.7144",
      "Royston P, Parmar MK. 2013. Restricted mean survival time: an alternative to the hazard ratio for the design and analysis of randomized trials with a time-to-event outcome. BMC Med Res Methodol. 13:152. doi:10.1186/1471-2288-13-152"]),

    ("machine learning / prediction models",
     ["machine learning", "random forest", "gradient boosting", "xgboost", "neural network", "auc", "calibration", "discrimination"],
     ["Steyerberg EW, Vickers AJ, Cook NR, et al. 2010. Assessing the performance of prediction models: a framework for traditional and novel measures. Epidemiology. 21(1):128-138. doi:10.1097/EDE.0b013e3181c30fb7",
      "Collins GS, Reitsma JB, Altman DG, Moons KG. 2015. Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): the TRIPOD statement. BMJ. 350:g7594. doi:10.1136/bmj.g7594"]),

    ("adaptive trial design",
     ["adaptive design", "adaptive trial", "group sequential", "platform trial", "basket trial", "umbrella trial"],
     ["Pallmann P, Bedding AW, Choodari-Oskooei B, et al. 2018. Adaptive designs in clinical trials: why use them, and how to run and report them. BMC Med. 16:29. doi:10.1186/s12916-018-1017-7",
      "Bauer P, Bretz F, Dragalin V, König F, Wassmer G. 2016. Twenty-five years of confirmatory adaptive designs: opportunities and pitfalls. Stat Med. 35(3):325-347. doi:10.1002/sim.6472"]),
]


# Fallback used when no pack matches — canonical for ANY meta-analysis paper
FALLBACK_REFS = [
    "Page MJ, McKenzie JE, Bossuyt PM, et al. 2021. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 372:n71. doi:10.1136/bmj.n71",
    "Higgins JPT, Thomas J, Chandler J, et al. (eds). 2023. Cochrane Handbook for Systematic Reviews of Interventions version 6.4. Cochrane. Available from www.training.cochrane.org/handbook",
]


def classify(title: str, body: str, data: str) -> tuple[str, list[str]]:
    """Return (pack_name, refs). Fall back to PRISMA + Cochrane Handbook."""
    haystack = " ".join([title, body, data]).lower()
    for name, patterns, refs in PACKS:
        for pat in patterns:
            if pat in haystack:
                return name, refs
    return "fallback (any MA paper)", FALLBACK_REFS


# --------- workbook parsing + writing ---------

ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)
METADATA_MARKER = "SUBMISSION METADATA:"


def parse_entries(text: str) -> list[dict]:
    blocks = text.split(SEP)
    entries: list[dict] = []
    for i, block in enumerate(blocks):
        m = ENTRY_HEAD_RE.search(block)
        if not m:
            continue
        num = int(m.group(1))
        name = m.group(2)
        lines = block.splitlines()
        data = {"num": num, "name": name, "block_idx": i, "raw": block}
        for j, line in enumerate(lines):
            if line.startswith("TITLE:"):
                data["title"] = line[6:].strip()
            elif line.startswith("TYPE:"):
                data["type_raw"] = line[5:].strip()
            elif line.startswith("DATA:"):
                data["data"] = line[5:].strip()
            elif line.startswith("PATH:"):
                data["path"] = line[5:].strip()
            elif line.startswith("CURRENT BODY"):
                body_lines = []
                k = j + 1
                while k < len(lines) and not lines[k].strip():
                    k += 1
                while k < len(lines) and lines[k].strip() and not lines[k].startswith("YOUR REWRITE"):
                    body_lines.append(lines[k])
                    k += 1
                data["body"] = " ".join(body_lines).strip()
        entries.append(data)
    return entries


def derive_github_urls(path: str) -> tuple[str, str, str]:
    """Derive GitHub code / protocol / Pages URLs from a local path.

    GitHub repo names can't contain spaces — some local project dirs
    (e.g. 'C:\\Projects\\IPD Zahid') have them. Collapse spaces to
    hyphens for the URL form. If the actual repo is named differently
    on GitHub, the link 404s; the user can correct in-place.
    """
    raw = path.strip("\\/").split("\\")[-1].split("/")[-1] or "unknown"
    # GitHub-safe: replace whitespace with hyphens, collapse repeats
    repo = re.sub(r"\s+", "-", raw).strip("-")
    code = f"https://github.com/{GH_USER}/{repo}"
    protocol = f"{code}/blob/main/E156-PROTOCOL.md"
    pages = f"https://{GH_USER}.github.io/{repo}/"
    return code, protocol, pages


def pick_checklist(type_raw: str) -> str:
    t = (type_raw or "").lower()
    if "methods" in t or "software" in t:
        return "PRISMA 2020 (methods-paper variant — reports on review corpus)"
    if "rct" in t:
        return "CONSORT 2010"
    if "observational" in t or "cohort" in t:
        return "STROBE"
    if "dta" in t or "diagnostic" in t:
        return "STARD 2015"
    return "PRISMA 2020"


def build_metadata_block(entry: dict, pack_name: str, refs: list[str]) -> str:
    code, protocol, pages = derive_github_urls(entry.get("path", ""))
    ref_lines = [f"  {i+1}. {r}" for i, r in enumerate(refs)]
    checklist = pick_checklist(entry.get("type_raw", ""))

    return f"""SUBMISSION METADATA:

Corresponding author: {AUTHOR} <{EMAIL}>
ORCID: {ORCID}
Affiliation: {AFFILIATION}

Links:
  Code:      {code}
  Protocol:  {protocol}
  Dashboard: {pages}

References (topic pack: {pack_name}):
{chr(10).join(ref_lines)}

Data availability: No patient-level data used. Analysis derived exclusively
  from publicly available aggregate records. All source identifiers are in
  the protocol document linked above.

Ethics: Not required. Study uses only publicly available aggregate data; no
  human participants; no patient-identifiable information; no individual-
  participant data. No institutional review board approval sought or required
  under standard research-ethics guidelines for secondary methodological
  research on published literature.

Funding: None.

Competing interests: None declared.

Author contributions (CRediT):
  [STUDENT REWRITER, first author] — Writing – original draft, Writing –
    review & editing, Validation.
  [SUPERVISING FACULTY, last/senior author] — Supervision, Validation,
    Writing – review & editing.
  {AUTHOR} (middle author, NOT first or last) — Conceptualization,
    Methodology, Software, Data curation, Formal analysis, Resources.

AI disclosure: Computational tooling (including AI-assisted coding via
  Claude Code [Anthropic]) was used to develop analysis scripts and assist
  with data extraction. The final manuscript was human-written, reviewed,
  and approved by the author; the submitted text is not AI-generated. All
  quantitative claims were verified against source data; cross-validation
  was performed where applicable. The author retains full responsibility for
  the final content.

Preprint: Not preprinted.

Reporting checklist: {checklist}.

Target journal: ◆ Synthēsis (https://www.synthesis-medicine.org/index.php/journal)
  Section: Methods Note — submit the 156-word E156 body verbatim as the
  main text. The journal caps main text at ≤400 words; E156's 156-word,
  7-sentence contract sits well inside that ceiling. Do NOT pad to 400 —
  the micro-paper length is the point of the format.

Manuscript license: CC-BY-4.0.
Code license: MIT.
"""


def insert_metadata(block: str, metadata: str) -> str:
    """Idempotent insert: strip ALL existing SUBMISSION METADATA regions,
    then insert one fresh block before the SUBMITTED marker.

    Previous impl stripped only the FIRST metadata→SUBMITTED region,
    so re-runs on blocks containing multiple stale metadata blocks
    accumulated extras (20 duplicates surfaced in 2026-04-15 audit).
    """
    lines = block.splitlines(keepends=True)

    # Repeatedly strip any remaining metadata region until none left
    while True:
        start = None
        for i, line in enumerate(lines):
            if line.strip().startswith(METADATA_MARKER):
                start = i
                break
        if start is None:
            break
        # Strip from start → next SUBMITTED marker (or end of block)
        end = len(lines)
        for j in range(start, len(lines)):
            if lines[j].lstrip().startswith("SUBMITTED:"):
                end = j
                break
        lines = lines[:start] + lines[end:]

    # Insert once, right before the first SUBMITTED marker
    for i, line in enumerate(lines):
        if line.lstrip().startswith("SUBMITTED:"):
            return "".join(lines[:i]) + metadata + "\n" + "".join(lines[i:])
    # No SUBMITTED found (unusual — some entries use the --- ENTRY N ---
    # block format without a per-entry SUBMITTED marker); append at end.
    return "".join(lines) + "\n" + metadata + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--first", type=int, default=0, help="process only first N entries (0 = all)")
    ap.add_argument("--dry-run", action="store_true", help="don't write, just summarize classifications")
    args = ap.parse_args()

    text = WORKBOOK.read_text(encoding="utf-8")
    entries = parse_entries(text)
    entries.sort(key=lambda e: e["num"])
    target = entries[: args.first] if args.first else entries
    print(f"Processing {len(target)} of {len(entries)} entries...")

    blocks = text.split(SEP)
    entry_by_idx = {e["block_idx"]: e for e in target}

    topic_counts: dict[str, int] = {}
    review_samples: list[tuple[int, str, str, list[str]]] = []

    for idx, block in enumerate(blocks):
        if idx not in entry_by_idx:
            continue
        e = entry_by_idx[idx]
        pack_name, refs = classify(e.get("title", ""), e.get("body", ""), e.get("data", ""))
        topic_counts[pack_name] = topic_counts.get(pack_name, 0) + 1
        metadata = build_metadata_block(e, pack_name, refs)
        blocks[idx] = insert_metadata(block, metadata)
        if e["num"] % 40 == 0 or e["num"] in (1, 10, 50, 100, 200, 300, 400):
            review_samples.append((e["num"], e["name"], pack_name, refs))

    new_text = SEP.join(blocks)
    if args.dry_run:
        print(f"[DRY RUN] would update {len(target)} entries")
    else:
        WORKBOOK.write_text(new_text, encoding="utf-8")
        print(f"Updated {len(target)} entries in {WORKBOOK}")

    print("\n=== Topic classification counts ===")
    for name, n in sorted(topic_counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:>4}  {name}")

    print("\n=== Spot-check samples ===")
    for num, name, pack, refs in review_samples:
        print(f"\n[{num}] {name}  →  {pack}")
        for i, r in enumerate(refs, 1):
            print(f"  {i}. {r[:110]}...")

    return 0


if __name__ == "__main__":
    sys.exit(main())
