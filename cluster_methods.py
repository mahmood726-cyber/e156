"""
Final clustering of 468 methods-paper E156 entries into 26 thematic groups.
Target 15-21 per cluster; slight overages accepted for highly coherent themes.
Zero MISC — every paper assigned to exactly one cluster.
"""
import csv, re, sys, io
from collections import defaultdict, OrderedDict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

rows = []
with open('unpublished_nonmeta_classification.csv', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)

mp = [r for r in rows if r['category'] == 'methods-paper']
assert len(mp) == 468, f"Expected 468, got {len(mp)}"

CLUSTERS = OrderedDict([
    ('C01', ('CT.gov Condition-Dimension Hiddenness',
             'Transparency-gap anatomy sliced by disease/condition family: '
             'ancient-backlog, enrollment-gap, narrative-gap, ghost-watchlist, '
             'text-asymmetry, overdue-debt, disease-geography gap.')),
    ('C02', ('CT.gov Country-Dimension Hiddenness',
             'Transparency-gap anatomy sliced by registration country: '
             'description black-box, ghost-watchlist, excess-watchlist, overdue-debt, '
             'text-asymmetry, cross-country and U.S.-vs-ex-U.S. comparison.')),
    ('C03', ('CT.gov Sponsor & Industry Repeaters',
             'Sponsor-level and modality/discipline-family missing-results accountability: '
             'excess stock, ghost protocols, backlog concentration, actual-discipline '
             'and modality-sponsor repeater identification.')),
    ('C04', ('CT.gov Registry Structure, Design & Black-Box',
             'System-level CT.gov transparency: rule-era gaps, black-box trials, stopped-trial '
             'disclosure, enrollment-size/intervention-type/design-purpose stratification, '
             'risk-adjusted hiddenness, publication-link rescue audit.')),
    ('C05', ('Network Meta-Analysis Statistical Methods',
             'NMA algorithms, consistency testing (sheaf-theoretic, design-by-treatment), '
             'treatment ranking, component NMA, indirect comparison, surrogate calibration, '
             'ensemble/spectral NMA, and living NMA with registry-first calibration.')),
    ('C06', ('Diagnostic Test Accuracy Evidence Synthesis',
             'Full DTA spectrum: classical bivariate/HSROC/SROC tools and datasets, automated '
             'DTA discovery, and the novel paradigm series (Aleph-Point, PEM-DTA, EES-DTA, '
             'Grand Diagnostic Synthesis, Evidence Manifold Spline, Omega-Tier OS).')),
    ('C08', ('Bayesian & Shrinkage Meta-Analysis',
             'Bayesian random-effects models, MAP meta-analytic priors, dynamic borrowing, '
             'Dirichlet-process MA, ROBMA model averaging, prior elicitation (SHELF), '
             'denominator-first Bayesian synthesis, and non-pooling causal alternatives.')),
    ('C09', ('Publication Bias, Correction & Fragility',
             'Funnel plot methods, PET-PEESE, MAFI fragility-bias calibration, excess-significance '
             'testing, robust pooling (GRMA, TGEP), outcome-reporting bias, bias-fingerprint '
             'discordance, fragility index calculation, and bias-correction simulation.')),
    ('C10', ('Heterogeneity, tau2 & Multilevel Meta-Analysis',
             'tau2/I2 estimators (REML, PM, HKSJ), small-sample corrections, conformal '
             'prediction intervals, adaptive shrinkage, heterogeneity decomposition, '
             'meta-analytic frontier methods, and three-level multilevel models with influence '
             'diagnostics across 501 Cochrane reviews.')),
    ('C12', ('IPD & Survival Meta-Analysis',
             'Individual participant data synthesis: IPD reconstruction (MaxEnt, KM digitisation, '
             'neural OCR), quantile treatment effects, federated/privacy-preserving MA, RMST '
             'pooling, prognostic MA, and survival reliability-growth meta-analysis.')),
    ('C14', ('Meta-Regression, Overfitting & Precision Methods',
             'Mixed-effects meta-regression, optimism-corrected R2, bootstrap aggregation, '
             'precision-weighted cross-validation, overfitting simulation, benchmark datasets, '
             'precision floor for fixed-effects reproduction, and responder-floor MID estimation.')),
    ('C15', ('Multiverse & Specification-Robustness Analysis',
             'Specification-multiverse analysis, analyst-choice sensitivity, spec-collapse '
             'false-robustness detection, Evidence Tribunal adversarial specification search, '
             'and SYNTHESIS 7-layer verification framework for fragile meta-analyses.')),
    ('C16', ('Reproducibility, Forensics & Data Integrity',
             'Forensic integrity screening (Asa seven-method screener, Benford digit analysis), '
             'TruthCert fail-closed certification, computational reproducibility audits of Cochrane, '
             'LLM output verification, trial integrity flag pipeline, outcome-switching detection.')),
    ('C17', ('Sequential Evidence, TSA & Adaptive Design',
             'Trial Sequential Analysis with alpha-spending and futility boundaries, e-values for '
             'anytime-valid inference, AlMizan cumulative equipoise monitoring, evidence half-life '
             'stability, changepoint detection in cumulative MA, and adaptive group-sequential '
             'trial simulators.')),
    ('C18', ('Living Evidence Synthesis Infrastructure',
             'Living meta-analysis engines, CT.gov-native dashboards for continuous updating, '
             'cardio living-meta portfolio (9 topic-specific reviews: PFA-AF, Watchman/Amulet, '
             'TEER, Inclisiran, Semaglutide, Leadless Pacing, CSP, IVL, CT-FFR), SAARC equity '
             'application, and LEC Phase-0 reproducibility bundles.')),
    ('C19', ('Empirical Cochrane Corpus Studies',
             'Large-scale empirical analyses of Cochrane reviews: MetaGenome phenotyping, overlap '
             'detection, evidence half-life, prediction gap, outcome-reporting bias, study overlap, '
             'retraction gravity, meta-ecosystem decay, trust-weighted meta-meta-analysis, '
             'and evidence gap maps.')),
    ('C20', ('HTA, Clinical Significance & Evidence Translation',
             'Health technology assessment platforms (41 analytical engines, Oman HTA, CRES), '
             'cost-effectiveness MA, net monetary benefit, value of information (EVPI/EVPPI), '
             'NNT with heterogeneity propagation, MCID mapping, effect size translation, '
             'equity-stratified MA, sample size and power for MA.')),
    ('C21', ('Transportability, Equity & External Validity',
             'Causal transportability index, efficacy leakage quantification, target trial emulation '
             'MA, shared-control platform trial MA, registry-first HFpEF calibration, African trial '
             'representativeness (ARAC, Tiba), causal evidence triangulation, global demographic '
             'calibration via multi-lake data.')),
    ('C22', ('Advanced Mathematical & Geometric Evidence Methods',
             'Topological data analysis (Betti numbers, persistent homology), spectral decomposition '
             'of between-study variance, information geometry on statistical manifolds, copula-based '
             'multivariate dependence, extreme value analysis (GEV), quantum meta-analysis, '
             'and the Aleph/HyperMeta evidence geometry engine.')),
    ('C23', ('GRADE, PRISMA & Systematic Review Reporting',
             'GRADE certainty assessment automation, SoF table generators, PRISMA 2020 compliance '
             'checking, RoB 2/ROBINS-I tools, umbrella review classifiers with CCA, evidence gap '
             'matrices, AI-assisted screening (ASReview 5-star), qualitative synthesis (CERQual), '
             'and the E156 micro-paper format specification.')),
    ('C24', ('Clinical Trial Registry Audit & Surveillance',
             'Automated cardiovascular trial landscape dashboards, ghost-protocol detection, '
             'enrollment duration prediction (ML), protocol amendment pattern mapping, global trial '
             'network visualisation, hypertension prevalence pipeline, ICU hemodynamic evidence map, '
             'modern non-parametric global health methods.')),
    ('C26', ('Research Automation, AI Tools & Infrastructure',
             'AI/ML-powered data extraction from PDFs and abstracts, LLM-assisted RCT extraction, '
             'evidence-inference classifier, automated Cochrane harvesting, EvidenceOracle instability '
             'prediction, CardioOracle trial outcome ML, pipeline build systems (Tower), Zenodo DOI '
             'publishing, portfolio dashboards, and the comprehensive everything-Claude-Code plugin '
             'framework.')),
    ('C27', ('Comprehensive MA Platforms & Integrated Suites',
             'Fully-integrated browser-based meta-analysis environments: MA Workbench hub (49 tools), '
             'Methods Suite (8 interoperable tools with MAIF), MetaGuard robust-forensic toolkit, '
             'EvidenceOS PRIME, experimental MA framework (300+ methods), frontier prototype lab, '
             'TruthCert pairwise MA engines, and a comprehensive pairwise pro platform.')),
    ('C28', ('Portfolio FAIR, Provenance & Data Infrastructure',
             'FAIR proxy scoring, provenance graphing (static lineage), RO-Crate metadata packaging, '
             'FHIR ArtifactAssessment export, and DrivePulse folder telemetry — tools that assess, '
             'structure, and interoperate research data for long-term reproducibility.')),
    ('C29', ('Portfolio Governance, Submission & Discovery',
             'Authorship/DOI ledger, citation packet generation, public portfolio catalog, operational '
             'fusion dashboard, editorial submission cockpit, rule-based triage lifecycle freezing, '
             'and research constellation status atlas — tools governing the research portfolio '
             'lifecycle from creation to submission.')),
    ('C31', ('Specialized Browser Tools & Research Productivity',
             'Single-purpose browser tools: dose-response MA (matching R accuracy), zero-install NMA '
             'with in-browser R cross-validation, NMA dose-response studio, meta-sprint autopilot, '
             'focus/pomodoro productivity timer, kanban task board, 3D graphing calculator, '
             'living-MA starter template, and narrative evidence communication.')),
])


def assign(r):
    n = r['name'].lower().strip()

    # ── CT.gov clusters (most-specific pattern first) ─────────────────────────
    if re.search(r'^ctgov-condition-', n) or n == 'ctgov-disease-geography-gap':
        return 'C01'
    if re.search(r'^ctgov-country-', n) or n == 'ctgov-us-vs-exus-sponsor-classes':
        return 'C02'
    if re.search(r'^ctgov-sponsor-', n) or n in {
            'ctgov-actual-discipline-repeaters', 'ctgov-actual-field-discipline',
            'ctgov-industry-family-repeaters', 'ctgov-modality-sponsor-repeaters',
            'ctgov-narrative-gap-repeaters'}:
        return 'C03'
    if re.search(r'^ctgov-', n):
        return 'C04'

    # ── C06: DTA (classical tools + paradigm series) ──────────────────────────
    if n in {'dta70', 'dta_pro_review', 'dta_pro_v2', 'dta-pro-v2', 'srocplotter',
             'metasprint-dta', 'qualsynth', '3dvitreous-grapher',
             'meta-paradigm-shift', 'ems-dta', 'gds-dta', 'paradigm-battle-dta',
             'mpet-dta', 'eh-dta', 'sl12-dta', 'aleph-point-synthesis',
             'aps-methodologist-review', 'gma-dta', 'pem-dta', 'pem-methodologist-review',
             'ees-dta', 'ees-methodologist-review', 'aleph-point-synthesis-final'}:
        return 'C06'

    # ── C05: NMA statistical methods ──────────────────────────────────────────
    if n in {'componentnma', 'component-nma', 'nmapaper111025', 'nmatransport',
             'indirectcomparison', 'cinema', 'sheafnma', 'sheaf-nma',
             'repo300-enma-snma', 'enma-snma', 'surronma', 'nma', 'hfn786',
             'ipdnma', 'livingnma', 'advanced-nma-pooling',
             'denominator_calibrated_living_nma'}:
        return 'C05'

    # ── C08: Bayesian & shrinkage ─────────────────────────────────────────────
    if n in {'bayesianma', 'mapriors', 'robma', 'cbamm-project2', 'lfa',
             'dpma', 'waternajia', 'priorlab', 'cbamm-lfa',
             'truthcert-denominator-phase1', 'truthcert-denominator',
             'truthcert-meta2-prototype', 'truthcert-meta2',
             'truthcert_denominator', 'truthcert_meta2',
             'dissonance-field-synthesis', 'nur-pce'}:
        return 'C08'

    # ── C09: Publication bias, correction & fragility ─────────────────────────
    if n in {'pub-bias-simulation', 'pubbiassuite', 'biasforensics', 'bias-forensics',
             'mafi', 'mafi-continuation', 'moneytrail',
             'grma_paper', 'grma', 'tgep_development', 'tgep',
             'fragilityindex', 'fragility-index',
             'pairwise70', 'outcomereportingbias', 'outcome-reporting-bias'}:
        return 'C09'

    # ── C10: Heterogeneity + multilevel (merged) ──────────────────────────────
    if n in {'new_heterogeneity_model', 'conformalma', 'conformal-ma',
             'poolingsuite', 'pooling-suite',
             'metafolio', 'metamethods',
             'area1_small_sample_analysis',
             'metaverse-robust-ma', 'metaverserobustma',
             'meta-frontier-bibliography', 'meta-frontier-readiness-atlas',
             'metafusion-lab', 'metafusion_lab',
             '501mlm', '501mlm_submission', 'mlmresearch',
             'multilevelerror', 'multipledatameta'}:
        return 'C10'

    # ── C12: IPD & survival (merged) ──────────────────────────────────────────
    if n in {'ipd-meta-pro', 'ipd_qma', 'ipd-qma', 'ipd_qma_project',
             'ipdsimulator', 'my-python-project', 'worldipd', 'worldipd-private',
             'maxent-reconstructor', 'federatedma', 'ipd-meta-pro-link',
             'lvad-reliability-growth-ma',
             'rmstmeta', 'rmst-meta', 'rmstnma', 'kmcurve', 'kmdigitizer',
             'wasserstein', 'kmextract', 'prognostic-meta'}:
        return 'C12'
    if 'kmdigitizer' in n or 'kmextract' in n or 'kmcurve' in n:
        return 'C12'

    # ── C14: Meta-regression, overfitting & precision ─────────────────────────
    if n in {'metaregression', 'paper1', 'paper2.111025',
             'claude2', 'chat2', 'chatpaper', 'repo100', 'pwcvr2',
             'precision-sweep-e156', 'cbamm-chat2',
             'metaoverfit', 'metaoverfit-paper',
             'idea12', 'sglt2i-hfpef-demo', 'responder-floor-atlas'}:
        return 'C14'

    # ── C15: Multiverse & robustness ──────────────────────────────────────────
    if n in {'multiversema', 'mes', 'fragility-atlas', 'fragilityatlas',
             'evidencetribunal', 'evidence-tribunal',
             'fatiha_project', 'fatiha', 'spec-collapse-atlas',
             'clauderepo', 'metaaudit', 'fatiha-course-github-v2'}:
        return 'C15'

    # ── C16: Reproducibility, forensics & integrity ───────────────────────────
    if n in {'asa', 'metareproducer', 'meta-reproducer',
             'burhan', 'truthcert-validation-papers', 'truthcert_v3.1.0_modeling',
             'truthcert-openclaw-supermemory-stack',
             'truthcert_pairwisepro_v2', 'truthcert-pairwisepro-v2',
             'integrity-guard-forensics', 'trial-truthfulness-atlas',
             'outcome-switching-ma-hf', 'benfordma'}:
        return 'C16'

    # ── C17: Sequential evidence, TSA & adaptive design ──────────────────────
    if n in {'tsa', 'safema', 'almizan', 'al-mizan',
             'evidencehalflife', 'evidence-half-life',
             'metashift', 'evidencekm',
             'retractionimpact', 'retraction-gravity', 'retractiongravity',
             'adaptsim'}:
        return 'C17'

    # ── C18: Living evidence synthesis ────────────────────────────────────────
    if n in {'living-meta', 'living-meta-engine', 'livingma',
             'livingma-pfa-af', 'livingma-watchman-amulet', 'livingma-tricuspid-teer',
             'livingma-inclisiran', 'livingma-semaglutide-hfpef',
             'livingma-leadless-pacing', 'livingma-csp', 'livingma-coronary-ivl',
             'livingma-ctffr', 'livingmaportfolio', 'cardio-ctgov-living-meta-portfolio',
             'saarce156students', 'lec_phase0_bundle', 'lec_phase0_project',
             'pairwiseai'}:
        return 'C18'

    # ── C19: Empirical Cochrane corpus studies ────────────────────────────────
    if n in {'metagenome', 'meta-genome', 'metarepair', 'meta-repair',
             'overlapdetector', 'overlap-detector',
             'predictiongap', 'prediction-gap',
             'evidencequality', 'evidence-quality-concordance',
             'evidencescore', 'evidence-score',
             'actionableevidence', 'contradictionmap',
             'evidenceatlas', 'evidence-atlas',
             'meta_ecosystem_model', 'overlapmatrix', 'overlap-matrix',
             'metarep', 'meta-rep', 'trustgate', 'trust-gate',
             'evidencemap', 'evidence-map',
             'evidencegapmap', 'evidence-gap-map', 'evidencemappro'}:
        return 'C19'

    # ── C20: HTA, clinical significance & evidence translation ───────────────
    if n in {'hta', 'hta-oman', 'hta_evidence_integrity_suite', 'hta-evidence-integrity',
             'hta_transportability_engine', 'hta-transportability',
             'hta_unified_intelligence_system', 'hta-unified-intelligence',
             'hta_artifact_standard_v2', 'hta-artifact-standard-v2',
             'costeffma', 'value_based_hta_engine', 'value-based-hta',
             'voicalculator', 'metavoi', 'oman', 'cres',
             'masamplesize', 'mapowercalc', 'ma-power-calc',
             'nntmapper', 'mcidmapper', 'maconverter', 'patientma',
             'equityma', 'nurpce', 'nur-pce'}:
        return 'C20'

    # ── C21: Transportability, equity & external validity ─────────────────────
    if n in {'africarct', 'africa-rct',
             'africaforecast', 'transportma',
             'transportabilitycalc', 'supertransportabilitymap',
             'globaltransportabilityatlas', 'global-transportability-atlas',
             'targettrialma', 'platformtrialma',
             'hfpef_registry_calibration', 'hfpef-registry-calibration',
             'hfpef_registry_synth', 'hfpef-registry-synth',
             'registry-first-rct-meta', 'registry_first_rct_meta',
             'tiba (2026-05-06)', 'arac', 'causalsynth', 'causal-synth'}:
        return 'C21'

    # ── C22: Advanced mathematical/geometric methods ───────────────────────────
    if n in {'hypermeta', 'evidencetopology', 'tda_ma', 'tda-ma',
             'infogema', 'evidencespectral', 'evidenceextremes',
             'evidencecopula', 'evidenceentropy', 'tda-meta',
             'evidencecollapsar', 'thealephengine',
             'multivarma', 'ecobiasma'}:
        return 'C22'
    if n.startswith('infogeo'):
        return 'C22'

    # ── C23: GRADE, PRISMA & SR reporting ─────────────────────────────────────
    if n in {'autograde', 'autograde-tool', 'gradepro', 'softable',
             'prismachecker', 'prisma-checker', 'prismaflow',
             'robassessor', 'rob-assessor', 'autoreview',
             'umbrellareview', 'evidence-board', 'evidenceboard',
             'asreview_5star', 'rayyanreplacement',
             'e156', 'fatiha-course', 'fatiha_course',
             'as-sirat', 'assirat'}:
        return 'C23'

    # ── C24: Clinical trial audit & surveillance ──────────────────────────────
    if n in {'trialradar', 'cardiotrialaudit', 'cardio-trial-audit',
             'cv-rct-analysis', 'enrollmentoracle', 'protocolevolution',
             'protocolevolutiondynamics', 'trialatlas', 'htnpipeline',
             'ihmedatalakehouse', 'whodatalakehouse', 'esc-acs-living-meta',
             'shahzaib-icu-landscape', 'modern-stats-global-health',
             'cardiosynth', 'metasprint-cardio-universe'}:
        return 'C24'

    # ── C26: Research automation, AI tools & infrastructure ──────────────────
    if n in {'dataextractor', 'metaextract', 'rct-extractor-v2',
             'claude-rct-work', 'llm-meta-analysis', 'evidence-inference',
             'cochrane-data-extractor', 'evidenceoracle', 'cardiooracle',
             'everything-claude-code',
             'zenodopipeline', 'figureengine', 'hub', 'researchorbitcontrol',
             'research-orbit-control', 'scripts', 'tower', 'tower_js',
             'mahmood726-cyber.github.io', 'portfolio-site',
             'legacy-mahmood789-archive', 'finalpaper'}:
        return 'C26'

    # ── C28: Portfolio FAIR, provenance & data infrastructure ─────────────────
    if n in {'drivepulse', 'drive-pulse', 'evidencebridgefhir', 'evidence-bridge-fhir',
             'evidencecrate', 'evidence-crate', 'fairportfolio', 'fair-portfolio',
             'provenanceatlas', 'provenance-atlas'}:
        return 'C28'

    # ── C29: Portfolio governance, submission & discovery ─────────────────────
    if n in {'authorshipledger', 'authorship-ledger', 'citationworkbench',
             'citation-workbench', 'portfoliocatalog', 'portfolio-catalog',
             'portfolioops', 'portfolio-ops', 'researchconstellation',
             'submissioncockpit', 'submission-cockpit',
             'triageworkbench', 'triage-workbench'}:
        return 'C29'

    # ── C31: Specialized browser tools & productivity ─────────────────────────
    if n in {'dosehtml', 'metasprint-dose-response', 'nmahtml',
             'nma-pro-v2', 'nma-dose-response-app', 'metasprint-nma', 'metasprintnma',
             'metasprint-autopilot', 'focus-studio', 'kanban-lab',
             'stories', 'html-misc', 'superapp', 'new-app'}:
        return 'C31'

    # ── C27: Comprehensive MA platforms & suites ──────────────────────────────
    if n in {'methodssuite', 'methods-suite', 'maworkbench', 'ma-workbench',
             'pairwise humble', 'metaguard', 'metanew',
             'experimental-meta-analysis', 'metafrontierlab',
             'truthcert1', 'truthcert1_work',
             'cbamm', 'cbamm-phase2', 'metareporter'}:
        return 'C27'

    return 'MISC'


# ── Run and report ─────────────────────────────────────────────────────────────
assigned = defaultdict(list)
for r in mp:
    cid = assign(r)
    assigned[cid].append(r)

total = sum(len(v) for v in assigned.values())
print(f"Total assigned: {total} / 468")
print(f"Misc bucket:    {len(assigned.get('MISC', []))}")
print()
for cid, (ctitle, _) in CLUSTERS.items():
    n = len(assigned.get(cid, []))
    flag = " ** SMALL" if n < 12 else (" ** LARGE" if n > 24 else "")
    print(f"  {cid}: {ctitle:<60} n={n:3d}{flag}")
print()
if assigned.get('MISC'):
    print("MISC bucket:")
    for r in assigned['MISC']:
        print(f"  idx={r['idx']:>6}  name={r['name']}")

# ── Expose assigned dict for output scripts ────────────────────────────────────
if __name__ == '__main__' and '--check' not in sys.argv:
    pass  # reporting done above
