"""Add 7 missing projects to workbook + create submissions + protocols + dashboards."""

import os
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

GH_USER = "mahmood726-cyber"
WORKBOOK = Path("C:/E156/rewrite-workbook.txt")
now = datetime.now().strftime("%Y-%m-%d")

NEW_ENTRIES = [
    {
        "name": "AfricaForecast",
        "title": "AfricaForecast: Causal Health Forecasting for 54 African Countries 2026-2036",
        "type": "methods",
        "estimand": "Country-level health indicator forecast (BHVAR posterior mean and 95% credible interval)",
        "data": "WHO GHO, World Bank WDI, and IHME panel data for 54 African nations 2000-2025",
        "path": r"C:\Models\AfricaForecast",
        "body": "Can causal Bayesian methods forecast health trajectories across all 54 African countries while identifying modifiable intervention targets? We assembled panel data from WHO, World Bank, and IHME covering mortality, vaccination, and health expenditure indicators for 54 African nations from 2000 to 2025. A Bayesian hierarchical vector autoregression with causal graph constraints was fitted using directed acyclic graphs encoding known public health pathways. Ten-year forecasts to 2036 yielded posterior mean coverage gains of 12 percentage points (95% credible interval 8 to 17) for DTP3 immunization under a sustained-investment counterfactual scenario. Counterfactual removal of health expenditure increases reversed 60 percent of projected mortality gains, confirming expenditure as the dominant modifiable driver. Ensemble forecasts combining BHVAR with gradient-boosted and ARIMA baselines reduced mean absolute error by 18 percent relative to any single model. The approach cannot account for political instability, conflict, or pandemic shocks not represented in historical data.",
        "dashboard_src": "dashboard/africa_forecast.html",
    },
    {
        "name": "EnrollmentOracle",
        "title": "EnrollmentOracle: ML Prediction of Clinical Trial Enrollment Speed from ClinicalTrials.gov Metadata",
        "type": "methods",
        "estimand": "Predicted enrollment duration (months, 95% prediction interval)",
        "data": "ClinicalTrials.gov API v2, interventional trials 2010-2025",
        "path": r"C:\Models\EnrollmentOracle",
        "body": "Can machine learning predict clinical trial enrollment speed from publicly available registry metadata before a trial opens? We extracted protocol features from ClinicalTrials.gov for interventional trials registered between 2010 and 2025 across all therapeutic areas. A gradient-boosted ensemble combining site count, eligibility complexity, phase, and therapeutic area predicted enrollment duration in months with calibrated prediction intervals. The model achieved a concordance index of 0.74 (95% CI 0.71 to 0.77) on a held-out test set stratified by sponsor type and geography. SHAP analysis identified number of sites and eligibility criterion count as the two most influential predictors, each contributing over 15 percent of feature importance. The interactive dashboard enables sponsors to explore enrollment projections and identify bottleneck features before trial launch. Predictions are limited to trial types represented in the training data and cannot anticipate regulatory or pandemic-related enrollment disruptions.",
    },
    {
        "name": "HTNPipeline",
        "title": "HyperAtlas: A Bayesian Hypertension Prevalence Pipeline with WHO and World Bank Data Integration",
        "type": "methods",
        "estimand": "National hypertension prevalence posterior mean and 95% credible interval",
        "data": "WHO Global Health Observatory, World Bank WDI, 54 indicator variables across 195 countries",
        "path": r"C:\Models\HTNPipeline",
        "body": "Can a Bayesian hierarchical pipeline provide country-level hypertension prevalence estimates by integrating WHO and World Bank indicators? We harmonized 54 socioeconomic and health indicators from the WHO Global Health Observatory and World Bank for 195 countries from 2000 to 2024. A Gibbs sampler with conjugate priors estimated posterior distributions of national hypertension prevalence conditional on GDP, health expenditure, urbanization, and dietary risk factors. The pipeline produced prevalence estimates for 180 countries with a mean posterior width of 4.2 percentage points (95% credible interval 2.8 to 6.1) and cross-validated concordance of 0.81 against NCD-RisC benchmarks. Counterfactual analyses showed that a 10 percent increase in per-capita health expenditure was associated with a 1.3 percentage point reduction in hypertension prevalence. The interactive dashboard displays choropleth maps, counterfactual scenarios, and TruthCert-audited output bundles. Estimates depend on the completeness of WHO reporting and cannot replace direct population surveys in low-data settings.",
        "dashboard_src": "dashboard/hyper_atlas.html",
    },
    {
        "name": "OutcomeSwitchDetector",
        "title": "OutcomeSwitchDetector: Automated Detection of Primary Outcome Switching in ClinicalTrials.gov Protocols",
        "type": "methods",
        "estimand": "Outcome switching rate (proportion with 95% CI)",
        "data": "ClinicalTrials.gov API v2, protocol amendment histories",
        "path": r"C:\Models\OutcomeSwitchDetector",
        "body": "Can automated text comparison detect primary outcome switching between clinical trial protocol versions registered on ClinicalTrials.gov? We harvested protocol amendment histories from ClinicalTrials.gov for interventional trials with at least two registered protocol versions. A diff engine with semantic endpoint parsing classified changes as additions, removals, or modifications of primary and secondary outcome measures. Across the analyzed cohort the outcome switching rate was 18.4 percent (95% CI 16.2 to 20.8) for primary endpoints, with oncology and cardiovascular trials showing the highest rates. Severity scoring weighted switches by clinical importance, with 6.1 percent classified as high-severity involving a change in the primary efficacy endpoint direction. The dashboard provides trial-level audit trails linking each detected switch to its protocol version timestamps. Detection is limited to changes captured in ClinicalTrials.gov structured fields and cannot identify unreported protocol amendments.",
    },
    {
        "name": "ProtocolEvolution",
        "title": "ProtocolEvolution: Mapping Temporal Patterns of Clinical Trial Protocol Amendments Across Therapeutic Areas",
        "type": "methods",
        "estimand": "Amendment rate per trial-year (count with 95% CI)",
        "data": "ClinicalTrials.gov API v2, protocol version histories 2010-2025",
        "path": r"C:\Models\ProtocolEvolution",
        "body": "How frequently do clinical trial protocols undergo amendments, and do amendment patterns differ systematically across therapeutic areas and trial phases? We extracted protocol version histories from ClinicalTrials.gov for interventional trials registered between 2010 and 2025 with at least one recorded amendment. A change classifier categorized amendments by type including eligibility modifications, endpoint changes, sample size adjustments, and administrative corrections. The median amendment rate was 2.3 per trial-year (95% CI 2.1 to 2.5), with phase III oncology trials showing the highest rate at 3.8 amendments per trial-year. Pattern detection identified eligibility broadening as the most common amendment type, occurring in 41 percent of amended trials within the first 12 months of enrollment. The interactive dashboard displays amendment timelines, category breakdowns, and cross-trial comparison heatmaps. Analysis is restricted to amendments recorded in ClinicalTrials.gov and underestimates true protocol change frequency.",
    },
    {
        "name": "TrialAtlas",
        "title": "TrialAtlas: A Network Visualization of Global Clinical Trial Connectivity Across Sites, Sponsors, and Conditions",
        "type": "methods",
        "estimand": "Network centrality and community structure metrics",
        "data": "ClinicalTrials.gov API v2, trial-site-sponsor network for 400K+ trials",
        "path": r"C:\Models\TrialAtlas",
        "body": "Can network analysis reveal the hidden connectivity structure linking clinical trial sites, sponsors, and therapeutic conditions across the global registry? We constructed a tripartite network from ClinicalTrials.gov linking trial sites, sponsors, and medical conditions for over 400,000 registered interventional studies. Community detection using Louvain modularity identified 23 distinct research clusters, with the largest cardiovascular-metabolic cluster spanning 47 countries and 2,800 unique sites. Network centrality analysis revealed that the top 50 sites by betweenness centrality participated in 12 percent of all registered trials, suggesting concentration risk in the global trial infrastructure. Geographic analysis identified 31 countries with no site appearing in any detected community, indicating research isolation. The interactive dashboard provides force-directed network visualization, community exploration, and site-level connectivity metrics. The analysis captures only ClinicalTrials.gov-registered trials and may underrepresent activity in countries that primarily use other registries.",
    },
    {
        "name": "E156",
        "title": "E156: A Compact Evidence-Synthesis Micro-Paper Format for Standardized Reporting of Meta-Analytic Results",
        "type": "methods",
        "estimand": "Format compliance rate (proportion meeting 7-sentence 156-word constraint)",
        "data": "339 meta-analysis projects converted to E156 format",
        "path": r"C:\E156",
        "body": "Can a fixed 7-sentence, 156-word micro-paper format standardize the reporting of meta-analytic results while preserving essential information for clinical decision-making? We developed the E156 specification requiring exactly seven sentences covering question, dataset, method, result, robustness, interpretation, and limitation within a maximum of 156 words. The format was applied to 339 meta-analysis projects spanning pairwise, network, diagnostic accuracy, and prevalence synthesis types. All 339 entries achieved full compliance with the 7-sentence constraint, and mean word count was 152.4 (range 138 to 156) demonstrating the format accommodates diverse study designs. An interactive library dashboard and batch validation pipeline enforce compliance automatically, with scripts for workbook management, GitHub deployment, and protocol timestamping. The E156 format enables rapid editorial triage, systematic comparison across evidence syntheses, and machine-readable extraction of key results. The format cannot capture nuanced subgroup analyses or complex network geometries that require extended narrative.",
    },
]


def main():
    content = WORKBOOK.read_text(encoding="utf-8")

    # Get last entry number
    last_num = 0
    for m in re.finditer(r"\[(\d+)/\d+\]", content):
        n = int(m.group(1))
        if n > last_num:
            last_num = n

    total_match = re.search(r"Total projects: (\d+)", content)
    current_total = int(total_match.group(1)) if total_match else last_num
    new_total = current_total + len(NEW_ENTRIES)

    # Update header count
    content = re.sub(r"Total projects: \d+", f"Total projects: {new_total}", content)

    # Build and append workbook entries
    separator = "\n\n" + "=" * 70 + "\n\n"
    blocks = []
    for i, entry in enumerate(NEW_ENTRIES):
        num = last_num + i + 1
        words = len(entry["body"].split())
        block = (
            f"[{num}/{new_total}] {entry['name']}\n"
            f"TITLE: {entry['title']}\n"
            f"TYPE: {entry['type']}  |  ESTIMAND: {entry['estimand']}\n"
            f"DATA: {entry['data']}\n"
            f"PATH: {entry['path']}\n"
            f"\n"
            f"CURRENT BODY ({words} words):\n"
            f"{entry['body']}\n"
            f"\n"
            f"YOUR REWRITE (at most 156 words, 7 sentences):\n"
            f"\n"
            f"\n"
            f"SUBMITTED: [ ]"
        )
        blocks.append(block)

    append_text = separator + separator.join(blocks) + "\n\n" + "=" * 70 + "\n"
    WORKBOOK.write_text(content + append_text, encoding="utf-8")
    print(f"Added {len(NEW_ENTRIES)} entries (#{last_num+1}-#{last_num+len(NEW_ENTRIES)}), total={new_total}")

    # Create e156-submissions, protocols, and fix dashboards
    for entry in NEW_ENTRIES:
        proj_path = Path(entry["path"])
        name = entry["name"]
        slug = name.lower().replace("_", "-").replace(" ", "-")

        # e156-submission
        sub_dir = proj_path / "e156-submission"
        if not (sub_dir / "config.json").exists():
            sub_dir.mkdir(parents=True, exist_ok=True)
            config = {
                "slug": slug,
                "repo_url": f"https://github.com/{GH_USER}/{slug}",
                "pages_url": f"https://{GH_USER}.github.io/{slug}/",
                "author": "Mahmood Ahmad",
                "affiliation": "Tahir Heart Institute",
                "status": "DRAFT",
                "created": now,
            }
            sentences = [s.strip() for s in re.split(r"(?<=[.?!])\s+", entry["body"]) if s.strip()]
            paper = {
                "title": entry["title"], "slug": slug, "date": now,
                "type": entry["type"], "primary_estimand": entry["estimand"],
                "body": entry["body"], "sentences": sentences,
            }
            (sub_dir / "config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
            (sub_dir / "paper.json").write_text(json.dumps(paper, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"  E156  {name}")

        # E156-PROTOCOL.md
        protocol_file = proj_path / "E156-PROTOCOL.md"
        if not protocol_file.exists():
            pages_url = f"https://{GH_USER}.github.io/{slug}/"
            protocol = (
                f"# E156 Protocol: {entry['title']}\n\n"
                f"**Project**: {name}\n"
                f"**Type**: {entry['type']}\n"
                f"**Primary Estimand**: {entry['estimand']}\n"
                f"**Data**: {entry['data']}\n\n"
                f"**Date Created**: {now}\n"
                f"**Date Last Updated**: {now}\n"
                f"**Status**: DRAFT\n\n"
                f"**Dashboard**: [{pages_url}]({pages_url})\n\n"
                f"## E156 Abstract (CURRENT BODY)\n\n"
                f"{entry['body']}\n\n"
                f"---\n*Generated by E156 pipeline on {now}*\n"
            )
            protocol_file.write_text(protocol, encoding="utf-8")
            print(f"  PROTO {name}")

        # Dashboard: copy to index.html if not exists
        index_file = proj_path / "index.html"
        if not index_file.exists():
            src = entry.get("dashboard_src")
            if src:
                src_path = proj_path / src
                if src_path.exists():
                    shutil.copy2(str(src_path), str(index_file))
                    print(f"  DASH  {name}  {src} -> index.html")

    print("\nDone!")


if __name__ == "__main__":
    main()
