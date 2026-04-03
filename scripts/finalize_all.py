"""
E156 Submission Finalizer — one-pass update of ALL submissions.
1. Update author/affiliation/email in all
2. Remove markdown formatting from paper.md
3. Add 2-3 references per project (topic-matched)
4. Copy existing HTML apps/dashboards + figures into submission folders
5. Check/create GitHub repos and add links
"""

import json
import os
import sys
import re
import shutil
import glob
import subprocess
from pathlib import Path

# Author details — override via env vars if needed
AUTHOR = os.environ.get("E156_AUTHOR", "Mahmood Ahmad")
AFFILIATION = os.environ.get("E156_AFFILIATION", "Tahir Heart Institute")
EMAIL = os.environ.get("E156_EMAIL", "author@example.com")  # Set E156_EMAIL env var for real email
DATE = "2026-03-28"
GH_USER = os.environ.get("E156_GH_USER", "mahmood726-cyber")
AI_DISCLOSURE = (
    "This work represents a compiler-generated evidence micro-publication "
    "(i.e., a structured, pipeline-based synthesis output). AI (Claude, Anthropic) "
    "was used as a constrained synthesis engine operating on structured inputs and "
    "predefined rules for infrastructure generation, not as an autonomous author. "
    "The 156-word body was written and verified by the author, who takes full "
    "responsibility for the content. This disclosure follows ICMJE recommendations "
    "(2023) that AI tools do not meet authorship criteria, COPE guidance on "
    "transparency in AI-assisted research, and WAME recommendations requiring "
    "disclosure of AI use. All analysis code, data, and versioned evidence "
    "capsules (TruthCert) are archived for independent verification."
)

SCRIPT_DIR = Path(__file__).resolve().parent
GENERATOR = SCRIPT_DIR / "generate_submission.py"

# ─── REFERENCE DATABASE ───────────────────────────────────

BASE_REFS = {
    "meta_general": [
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
        "Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. BMJ. 2003;327(7414):557-560.",
        "Cochrane Handbook for Systematic Reviews of Interventions. Version 6.4. Cochrane; 2023.",
    ],
    "nma": [
        "Salanti G. Indirect and mixed-treatment comparison, network, or multiple-treatments meta-analysis. Res Synth Methods. 2012;3(2):80-97.",
        "Rucker G, Schwarzer G. Ranking treatments in frequentist network meta-analysis. BMC Med Res Methodol. 2015;15:58.",
        "Dias S, Welton NJ, Caldwell DM, Ades AE. Checking consistency in mixed treatment comparison meta-analysis. Stat Med. 2010;29(7-8):932-944.",
    ],
    "bayesian": [
        "Roever C. Bayesian random-effects meta-analysis using the bayesmeta R package. J Stat Softw. 2020;93(6):1-51.",
        "Higgins JPT, Thompson SG, Spiegelhalter DJ. A re-evaluation of random-effects meta-analysis. J R Stat Soc Ser A. 2009;172(1):137-159.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "dta": [
        "Reitsma JB, Glas AS, Rutjes AW, et al. Bivariate analysis of sensitivity and specificity produces informative summary measures in diagnostic reviews. J Clin Epidemiol. 2005;58(10):982-990.",
        "Macaskill P, Gatsonis C, Deeks JJ, Harbord RM, Takwoingi Y. Cochrane Handbook for Systematic Reviews of Diagnostic Test Accuracy. Cochrane; 2023.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "pub_bias": [
        "Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. BMJ. 1997;315(7109):629-634.",
        "Duval S, Tweedie R. Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. Biometrics. 2000;56(2):455-463.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "hta": [
        "Drummond MF, Sculpher MJ, Claxton K, Stoddart GL, Torrance GW. Methods for the Economic Evaluation of Health Care Programmes. 4th ed. Oxford University Press; 2015.",
        "Briggs AH, Weinstein MC, Fenwick EAL, et al. Model parameter estimation and uncertainty analysis. Med Decis Making. 2012;32(5):722-732.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "ipd": [
        "Riley RD, Lambert PC, Abo-Zaid G. Meta-analysis of individual participant data: rationale, conduct, and reporting. BMJ. 2010;340:c221.",
        "Stewart LA, Tierney JF. To IPD or not to IPD? Advantages and disadvantages of systematic reviews using individual patient data. Eval Health Prof. 2002;25(1):76-97.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "r_package": [
        "Viechtbauer W. Conducting meta-analyses in R with the metafor package. J Stat Softw. 2010;36(3):1-48.",
        "Schwarzer G, Carpenter JR, Rucker G. Meta-Analysis with R. Springer; 2015.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "ml_extraction": [
        "Marshall IJ, Noel-Storr A, Kuber J, et al. Machine learning for identifying randomized controlled trials: an evaluation and practitioner's guide. Res Synth Methods. 2018;9(4):602-614.",
        "Jonnalagadda SR, Goyal P, Huffman MD. Automating data extraction in systematic reviews: a systematic review. Syst Rev. 2015;4:78.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "survival": [
        "Guyot P, Ades AE, Ouwens MJ, Welton NJ. Enhanced secondary analysis of survival data: reconstructing the data from published Kaplan-Meier survival curves. BMC Med Res Methodol. 2012;12:9.",
        "Tierney JF, Stewart LA, Ghersi D, Burdett S, Sydes MR. Practical methods for incorporating summary time-to-event data into meta-analysis. Trials. 2007;8:16.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "fragility": [
        "Walsh M, Srinathan SK, McAuley DF, et al. The statistical significance of randomized controlled trial results is frequently fragile: a case for a Fragility Index. J Clin Epidemiol. 2014;67(6):622-628.",
        "Atal I, Porcher R, Boutron I, Ravaud P. The statistical significance of meta-analyses is frequently fragile: definition of a fragility index for meta-analyses. J Clin Epidemiol. 2019;111:32-40.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "rob": [
        "Sterne JAC, Savovic J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. BMJ. 2019;366:l4898.",
        "Sterne JA, Hernan MA, Reeves BC, et al. ROBINS-I: a tool for assessing risk of bias in non-randomised studies of interventions. BMJ. 2016;355:i4919.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "prisma": [
        "Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 2021;372:n71.",
        "Moher D, Liberati A, Tetzlaff J, Altman DG. Preferred reporting items for systematic reviews and meta-analyses: the PRISMA statement. PLoS Med. 2009;6(7):e1000097.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "dose_response": [
        "Crippa A, Orsini N. Dose-response meta-analysis of differences in means. BMC Med Res Methodol. 2016;16:91.",
        "Greenland S, Longnecker MP. Methods for trend estimation from summarized dose-response data, with applications to meta-analysis. Am J Epidemiol. 1992;135(11):1301-1309.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "multilevel": [
        "Van den Noortgate W, Lopez-Lopez JA, Marin-Martinez F, Sanchez-Meca J. Three-level meta-analysis of dependent effect sizes. Behav Res Methods. 2013;45:576-594.",
        "Assink M, Wibbelink CJM. Fitting three-level meta-analytic models in R: a step-by-step tutorial. Quant Methods Psychol. 2016;12(3):154-174.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "power": [
        "Valentine JC, Pigott TD, Rothstein HR. How many studies do you need? A primer on statistical power for meta-analysis. J Educ Behav Stat. 2010;35(2):215-247.",
        "Jackson D, Turner R. Power analysis for random-effects meta-analysis. Res Synth Methods. 2017;8(3):290-302.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "prevalence": [
        "Barendregt JJ, Doi SA, Lee YY, Norman RE, Vos T. Meta-analysis of prevalence. J Epidemiol Community Health. 2013;67(11):974-978.",
        "Nyaga VN, Arbyn M, Aerts M. Metaprop: a Stata command to perform meta-analysis of binomial data. Arch Public Health. 2014;72:39.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "meta_regression": [
        "Thompson SG, Higgins JPT. How should meta-regression analyses be undertaken and interpreted? Stat Med. 2002;21(11):1559-1573.",
        "Viechtbauer W. Conducting meta-analyses in R with the metafor package. J Stat Softw. 2010;36(3):1-48.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "grade": [
        "Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. BMJ. 2008;336(7650):924-926.",
        "Schunemann HJ, Higgins JPT, Vist GE, et al. Completing 'Summary of findings' tables and grading the certainty of the evidence. Cochrane Handbook Chapter 14. Cochrane; 2023.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
    "forensic": [
        "Carlisle JB. Data fabrication and other reasons for non-random sampling in 5087 randomised, controlled trials in anaesthetic and general medical journals. Anaesthesia. 2017;72(8):944-952.",
        "Brown NJL, Heathers JAJ. The GRIM test: a simple technique detects numerous anomalies in the reporting of results in psychology. Soc Psychol Personal Sci. 2017;8(4):363-369.",
        "Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.",
    ],
}


def pick_refs(title, body, proj_type):
    """Select 3 references. Most-specific checks first to avoid greedy matching."""
    text = (title + " " + body + " " + proj_type).lower()

    # 1. GRADE / certainty of evidence (before pub_bias which matches "egger" in body)
    if "grade" in text and ("certainty" in text or "quality of evidence" in text):
        return BASE_REFS["grade"]

    # 2. Forensic / integrity screening
    if "benford" in text or "grim" in text or "forensic" in text or "integrity screen" in text:
        return BASE_REFS["forensic"]

    # 3. Fragility (before HTA which would match "value" in "p-value")
    if "fragil" in text:
        return BASE_REFS["fragility"]

    # 4. Risk of bias
    if "risk of bias" in text or "rob 2" in text or "robins-i" in text:
        return BASE_REFS["rob"]

    # 5. PRISMA
    if "prisma" in text:
        return BASE_REFS["prisma"]

    # 6. Dose-response (specific phrase)
    if "dose" in text and "response" in text:
        return BASE_REFS["dose_response"]

    # 7. Bayesian (before NMA — "bayesian" is more specific)
    if "bayesian" in text or "credible interval" in text or "posterior" in text:
        return BASE_REFS["bayesian"]

    # 8. Network MA (phrase-based to avoid partial matches)
    if "network meta" in text or " nma " in text or "nma " in text[:50]:
        return BASE_REFS["nma"]

    # 9. DTA (with fixed check — no regex literal)
    if "diagnostic test" in text or " dta " in text or ("sensitivity" in text and "specificity" in text):
        return BASE_REFS["dta"]

    # 10. Multilevel / three-level
    if "multilevel" in text or "three-level" in text or "3-level" in text:
        return BASE_REFS["multilevel"]

    # 11. Power / sample size
    if "power" in text and ("sample size" in text or "calculator" in text):
        return BASE_REFS["power"]

    # 12. Survival / KM / RMST (before pub_bias which might match "funnel" mentioned in body)
    if "kaplan" in text or "km curve" in text or "survival" in text or "rmst" in text:
        return BASE_REFS["survival"]

    # 13. Publication bias (phrase-based, not bare keywords)
    if "publication bias" in text or "trim and fill" in text:
        return BASE_REFS["pub_bias"]

    # 14. HTA (narrow keywords — no bare "cost" or "value")
    if "health technology" in text or "cost-effective" in text or "transportab" in text:
        return BASE_REFS["hta"]

    # 15. IPD (phrase-based)
    if "individual patient data" in text or "ipd meta" in text:
        return BASE_REFS["ipd"]

    # 16. Meta-regression (before ml_extraction since "regression" is common)
    if "meta-regression" in text or "meta regression" in text or "moderator analysis" in text:
        return BASE_REFS["meta_regression"]

    # 17. Prevalence / proportion
    if "prevalence" in text or "proportion meta" in text:
        return BASE_REFS["prevalence"]

    # 18. ML / extraction / automation (narrowed keywords)
    if "automated extract" in text or "data extraction pipeline" in text or " nlp " in text or " ocr " in text:
        return BASE_REFS["ml_extraction"]

    # 19. R package
    if "r package" in text:
        return BASE_REFS["r_package"]

    return BASE_REFS["meta_general"]


def get_github_url(project_path):
    """Check if project has a GitHub remote."""
    try:
        result = subprocess.run(
            ["git", "-C", str(project_path), "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            if url.startswith("git@github.com:"):
                url = url.replace("git@github.com:", "https://github.com/")
            if url.endswith(".git"):
                url = url[:-4]
            if "github.com" in url:
                return url
    except Exception:
        pass
    return None


def create_github_repo(project_path, repo_name):
    """Create a new GitHub repo and push. Checks return codes."""
    try:
        result = subprocess.run(
            ["gh", "repo", "create", f"{GH_USER}/{repo_name}",
             "--public", "--source", str(project_path), "--push"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return f"https://github.com/{GH_USER}/{repo_name}"
        if "already exists" in result.stderr:
            # Idempotent: set-url instead of add
            subprocess.run(
                ["git", "-C", str(project_path), "remote", "set-url", "origin",
                 f"https://github.com/{GH_USER}/{repo_name}.git"],
                capture_output=True, text=True, timeout=10
            )
            push = subprocess.run(
                ["git", "-C", str(project_path), "push", "-u", "origin", "master"],
                capture_output=True, text=True, timeout=120
            )
            if push.returncode == 0:
                return f"https://github.com/{GH_USER}/{repo_name}"
            print(f"    Push failed: {push.stderr[:100]}")
    except Exception as e:
        print(f"    GitHub error: {e}")
    return None


def copy_assets(project_path, submission_dir):
    """Copy HTML apps, dashboards, and figures into submission/assets/."""
    assets_dir = submission_dir / "assets"
    copied = []

    html_patterns = [
        "dashboard/*.html", "dashboard/**/*.html",
        "app/*.html", "dist/*.html",
        "E156/*.html",
        "*.html",
    ]
    for pat in html_patterns:
        for f in glob.glob(str(project_path / pat), recursive=True):
            fp = Path(f)
            if fp.is_symlink() or "e156-submission" in str(fp) or "node_modules" in str(fp):
                continue
            size = fp.stat().st_size
            if size < 1024 or size > 5 * 1024 * 1024:
                continue
            assets_dir.mkdir(parents=True, exist_ok=True)
            # Prefix parent dir to avoid name collisions
            parent_prefix = fp.parent.name if fp.parent != project_path else ""
            dest_name = f"{parent_prefix}_{fp.name}" if parent_prefix else fp.name
            dest = assets_dir / dest_name
            if not dest.exists():
                shutil.copy2(str(fp), str(dest))
                copied.append(dest_name)

    fig_patterns = [
        "figures/*.png", "figures/*.svg", "figures/*.jpg",
        "plots/*.png", "plots/*.svg",
        "fig*/*.png", "fig*/*.svg",
        "paper/figures/*.png", "paper/figures/*.svg",
        "output/*.png", "output/*.svg",
        "dashboard/*.png",
    ]
    for pat in fig_patterns:
        for f in glob.glob(str(project_path / pat), recursive=True):
            fp = Path(f)
            if fp.is_symlink() or "e156-submission" in str(fp):
                continue
            size = fp.stat().st_size
            if size > 10 * 1024 * 1024:
                continue
            assets_dir.mkdir(parents=True, exist_ok=True)
            parent_prefix = fp.parent.name if fp.parent != project_path else ""
            dest_name = f"{parent_prefix}_{fp.name}" if parent_prefix else fp.name
            dest = assets_dir / dest_name
            if not dest.exists():
                shutil.copy2(str(fp), str(dest))
                copied.append(dest_name)

    return copied


def write_clean_md(config, refs, github_url, out_path):
    """Write paper.md without any markdown formatting (* # **)."""
    title = config.get("title", "Untitled")
    body = config.get("body", "")
    notes = config.get("notes", {})

    lines = [
        AUTHOR,
        AFFILIATION,
        EMAIL,
        "",
        title,
        "",
        body,
        "",
        "Outside Notes",
        "",
    ]

    note_fields = [
        ("Type", config.get("type", "")),
        ("Primary estimand", config.get("primary_estimand", "")),
        ("App", notes.get("app", "")),
        ("Data", notes.get("data", "")),
        ("Code", github_url or notes.get("code", "")),
        ("DOI", notes.get("doi", "")),
        ("Version", notes.get("version", config.get("version", ""))),
        ("Certainty", notes.get("certainty", config.get("certainty", ""))),
        ("Validation", notes.get("validation", "DRAFT")),
    ]

    for label, value in note_fields:
        if value:
            lines.append(f"{label}: {value}")

    lines.extend(["", "References", ""])
    for i, ref in enumerate(refs, 1):
        lines.append(f"{i}. {ref}")

    lines.extend(["", "AI Disclosure", "", AI_DISCLOSURE])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_config(config, github_url, refs):
    """Update config with author details, GitHub URL, and references."""
    config["author"] = AUTHOR
    config["affiliation"] = AFFILIATION
    config["email"] = EMAIL
    config["date"] = config.get("date", DATE)
    config["references"] = refs

    if github_url:
        config.setdefault("notes", {})["code"] = github_url

    return config


def process_submission(submission_dir):
    """Process one e156-submission folder."""
    submission_dir = Path(submission_dir)
    project_dir = submission_dir.parent
    config_path = submission_dir / "config.json"

    if not config_path.exists():
        print(f"  SKIP (no config.json): {submission_dir}")
        return False

    # Load config with error handling
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  SKIP (bad JSON): {config_path}: {e}")
        return False

    title = config.get("title", "Untitled")
    body = config.get("body", "")
    proj_type = config.get("type", "methods")

    # 1. Get/create GitHub URL (skip with --no-github)
    github_url = get_github_url(project_dir)
    if not github_url and "--no-github" not in sys.argv:
        repo_name = re.sub(r"[^a-z0-9-]", "", project_dir.name.lower().replace(" ", "-").replace("_", "-"))
        if not repo_name:
            print(f"    Empty repo name after sanitization: {project_dir.name}")
        elif (project_dir / ".git").exists():
            github_url = create_github_repo(project_dir, repo_name)
            if github_url:
                print(f"    Created GitHub repo: {github_url}")
            else:
                print(f"    GitHub upload failed for {repo_name}")
        else:
            print(f"    Not a git repo: {project_dir}")

    # 2. Pick references
    refs = pick_refs(title, body, proj_type)

    # 3. Update config
    config = update_config(config, github_url, refs)
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

    # 4. Regenerate index.html via generator
    try:
        subprocess.run(
            [sys.executable, str(GENERATOR), str(config_path)],
            capture_output=True, text=True, timeout=30
        )
    except Exception as e:
        print(f"    Generator error: {e}")

    # 5. Write clean paper.md (overwrites generated one)
    write_clean_md(config, refs, github_url, submission_dir / "paper.md")

    # 6. Update paper.json with new fields
    pj_path = submission_dir / "paper.json"
    if pj_path.exists():
        try:
            pj = json.loads(pj_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pj = {}
        pj["author"] = AUTHOR
        pj["affiliation"] = AFFILIATION
        pj["email"] = EMAIL
        pj["references"] = refs
        pj.setdefault("schema", "e156-v0.2")
        if github_url:
            pj["github"] = github_url
        pj_path.write_text(json.dumps(pj, indent=2, ensure_ascii=False), encoding="utf-8")

    # 7. Copy HTML apps and figures
    copied = copy_assets(project_dir, submission_dir)
    if copied:
        print(f"    Copied {len(copied)} assets: {', '.join(copied[:5])}{'...' if len(copied) > 5 else ''}")

    return True


def main():
    from e156_utils import find_all_submissions
    submissions = find_all_submissions()

    print(f"Found {len(submissions)} e156-submission folders\n")

    ok = 0
    for i, sub in enumerate(submissions, 1):
        print(f"[{i}/{len(submissions)}] {sub.parent.name}...")
        if process_submission(sub):
            ok += 1

    print(f"\n{'=' * 60}")
    print(f"Updated {ok}/{len(submissions)} submissions")
    print(f"Author: {AUTHOR}")
    print(f"Affiliation: {AFFILIATION}")
    print(f"Email: {EMAIL}")


if __name__ == "__main__":
    main()
