import csv, re, sys, io
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

rows = []
with open('unpublished_nonmeta_classification.csv', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)
mp = [r for r in rows if r['category'] == 'methods-paper']

def assign(r):
    n = r['name'].lower().strip()
    if re.search(r'^ctgov-condition-', n) or n == 'ctgov-disease-geography-gap': return 'C01'
    if re.search(r'^ctgov-country-', n) or n == 'ctgov-us-vs-exus-sponsor-classes': return 'C02'
    if re.search(r'^ctgov-sponsor-', n) or n in {
            'ctgov-actual-discipline-repeaters','ctgov-actual-field-discipline',
            'ctgov-industry-family-repeaters','ctgov-modality-sponsor-repeaters',
            'ctgov-narrative-gap-repeaters'}: return 'C03'
    if re.search(r'^ctgov-', n): return 'C04'
    if n in {'dta70','dta_pro_review','dta_pro_v2','dta-pro-v2','srocplotter','metasprint-dta',
             'qualsynth','meta-paradigm-shift','ems-dta','gds-dta','paradigm-battle-dta',
             'mpet-dta','eh-dta','sl12-dta','aleph-point-synthesis','aps-methodologist-review',
             'gma-dta','pem-dta','pem-methodologist-review','ees-dta','ees-methodologist-review',
             'aleph-point-synthesis-final','3dvitreous-grapher'}: return 'C06'
    if n in {'componentnma','component-nma','nmapaper111025','nmatransport','indirectcomparison',
             'cinema','sheafnma','sheaf-nma','repo300-enma-snma','enma-snma','surronma','nma',
             'hfn786','ipdnma','livingnma','advanced-nma-pooling','denominator_calibrated_living_nma'}: return 'C05'
    if n in {'bayesianma','mapriors','robma','cbamm-project2','lfa','dpma','waternajia','priorlab',
             'cbamm-lfa','truthcert-denominator-phase1','truthcert-denominator',
             'truthcert-meta2-prototype','truthcert-meta2','truthcert_denominator','truthcert_meta2',
             'dissonance-field-synthesis','nur-pce'}: return 'C08'
    if n in {'pub-bias-simulation','pubbiassuite','biasforensics','bias-forensics','mafi',
             'mafi-continuation','moneytrail','grma_paper','grma','tgep_development','tgep',
             'fragilityindex','fragility-index','pairwise70',
             'outcomereportingbias','outcome-reporting-bias'}: return 'C09'
    if n in {'new_heterogeneity_model','conformalma','conformal-ma','poolingsuite','pooling-suite',
             'metafolio','metamethods','area1_small_sample_analysis','metaverse-robust-ma',
             'metaverserobustma','meta-frontier-bibliography','meta-frontier-readiness-atlas',
             'metafusion-lab','metafusion_lab','501mlm','501mlm_submission','mlmresearch',
             'multilevelerror','multipledatameta'}: return 'C10'
    if n in {'ipd-meta-pro','ipd_qma','ipd-qma','ipd_qma_project','ipdsimulator','my-python-project',
             'worldipd','worldipd-private','maxent-reconstructor','federatedma','ipd-meta-pro-link',
             'lvad-reliability-growth-ma','rmstmeta','rmst-meta','rmstnma','kmcurve','kmdigitizer',
             'wasserstein','kmextract','prognostic-meta'}: return 'C12'
    if 'kmdigitizer' in n or 'kmextract' in n or 'kmcurve' in n: return 'C12'
    if n in {'metaregression','paper1','paper2.111025','claude2','chat2','chatpaper','repo100',
             'pwcvr2','precision-sweep-e156','cbamm-chat2','metaoverfit','metaoverfit-paper',
             'idea12','sglt2i-hfpef-demo','responder-floor-atlas'}: return 'C14'
    if n in {'multiversema','mes','fragility-atlas','fragilityatlas','evidencetribunal',
             'evidence-tribunal','fatiha_project','fatiha','spec-collapse-atlas','clauderepo',
             'metaaudit','fatiha-course-github-v2'}: return 'C15'
    if n in {'asa','metareproducer','meta-reproducer','burhan','truthcert-validation-papers',
             'truthcert_v3.1.0_modeling','truthcert-openclaw-supermemory-stack','truthcert1',
             'truthcert1_work','truthcert_pairwisepro_v2','truthcert-pairwisepro-v2',
             'integrity-guard-forensics','trial-truthfulness-atlas','outcome-switching-ma-hf',
             'benfordma'}: return 'C16'
    if n in {'tsa','safema','almizan','al-mizan','evidencehalflife','evidence-half-life',
             'metashift','evidencekm','retractionimpact','retraction-gravity','retractiongravity',
             'adaptsim','adap-tsim'}: return 'C17'
    if n in {'living-meta','living-meta-engine','livingma','livingma-pfa-af',
             'livingma-watchman-amulet','livingma-tricuspid-teer','livingma-inclisiran',
             'livingma-semaglutide-hfpef','livingma-leadless-pacing','livingma-csp',
             'livingma-coronary-ivl','livingma-ctffr','livingmaportfolio',
             'cardio-ctgov-living-meta-portfolio','saarce156students','lec_phase0_bundle',
             'lec_phase0_project','pairwiseai','pairwise humble'}: return 'C18'
    if n in {'metagenome','meta-genome','metarepair','meta-repair','overlapdetector',
             'overlap-detector','predictiongap','prediction-gap','evidencequality',
             'evidence-quality-concordance','evidencescore','evidence-score','actionableevidence',
             'contradictionmap','evidenceatlas','evidence-atlas','meta_ecosystem_model',
             'overlapmatrix','overlap-matrix','metarep','meta-rep','trustgate','trust-gate',
             'evidencemap','evidence-map','evidencegapmap','evidence-gap-map','evidencemappro'}: return 'C19'
    if n in {'hta','hta-oman','hta_evidence_integrity_suite','hta-evidence-integrity',
             'hta_transportability_engine','hta-transportability','hta_unified_intelligence_system',
             'hta-unified-intelligence','hta_artifact_standard_v2','hta-artifact-standard-v2',
             'costeffma','value_based_hta_engine','value-based-hta','voicalculator','metavoi',
             'oman','cres'}: return 'C20'
    if n in {'africarct','africa-rct','africaforecast','transportma','transportabilitycalc',
             'supertransportabilitymap','globaltransportabilityatlas','global-transportability-atlas',
             'targettrialma','platformtrialma','hfpef_registry_calibration','hfpef-registry-calibration',
             'hfpef_registry_synth','hfpef-registry-synth','registry-first-rct-meta',
             'registry_first_rct_meta','tiba (2026-05-06)','arac','causalsynth','causal-synth'}: return 'C21'
    if n in {'hypermeta','evidencetopology','tda_ma','tda-ma','infogema','evidencespectral',
             'evidenceextremes','evidencecopula','evidenceentropy','tda-meta','evidencecollapsar',
             'thealephengine','multivarma','ecobiasma'}: return 'C22'
    if n.startswith('infogeo'): return 'C22'
    if n in {'autograde','autograde-tool','gradepro','softable','prismachecker','prisma-checker',
             'prismaflow','robassessor','rob-assessor','autoreview','umbrellareview','evidence-board',
             'evidenceboard','asreview_5star','rayyanreplacement','e156','fatiha-course',
             'fatiha_course','as-sirat','assirat'}: return 'C23'
    if n in {'trialradar','cardiotrialaudit','cardio-trial-audit','cv-rct-analysis','enrollmentoracle',
             'protocolevolution','protocolevolutiondynamics','trialatlas','htnpipeline',
             'ihmedatalakehouse','whodatalakehouse','esc-acs-living-meta','shahzaib-icu-landscape',
             'modern-stats-global-health','cardiosynth','metasprint-cardio-universe'}: return 'C24'
    if n in {'masamplesize','mapowercalc','ma-power-calc','nntmapper','mcidmapper','maconverter',
             'patientma','equityma','nurpce','nur-pce'}: return 'C25'
    if n in {'dataextractor','metaextract','rct-extractor-v2','claude-rct-work','llm-meta-analysis',
             'evidence-inference','cochrane-data-extractor','evidenceoracle','cardiooracle',
             'everything-claude-code'}: return 'C26'
    if n in {'drivepulse','drive-pulse','evidencebridgefhir','evidence-bridge-fhir','evidencecrate',
             'evidence-crate','fairportfolio','fair-portfolio','provenanceatlas',
             'provenance-atlas'}: return 'C28'
    if n in {'authorshipledger','authorship-ledger','citationworkbench','citation-workbench',
             'portfoliocatalog','portfolio-catalog','portfolioops','portfolio-ops',
             'researchconstellation','submissioncockpit','submission-cockpit','triageworkbench',
             'triage-workbench'}: return 'C29'
    if n in {'zenodopipeline','figureengine','hub','researchorbitcontrol','research-orbit-control',
             'scripts','tower','tower_js','mahmood726-cyber.github.io','portfolio-site',
             'legacy-mahmood789-archive','finalpaper','lec_phase0_project',
             'lec phase0 project','livingmaportfolio'}: return 'C30'
    if n in {'methodssuite','methods-suite','maworkbench','ma-workbench','pairwise humble','superapp',
             'new-app','metaguard','experimental-meta-analysis','metafrontierlab','dosehtml',
             'metasprint-dose-response','stories','kanban-lab','focus-studio','html-misc','as-sirat',
             'metanew','nmahtml','nma-pro-v2','nma-dose-response-app','metasprint-nma','metasprintnma',
             'metasprint-autopilot','cbamm','cbamm-phase2','metareporter','pairwiseai'}: return 'C27'
    return 'MISC'

assigned = defaultdict(list)
for r in mp:
    assigned[assign(r)].append(r)

for cid in ['C06','C25','C26','C27','C30']:
    entries = assigned.get(cid, [])
    print(f"\n{cid} ({len(entries)} entries):")
    for r in entries:
        print(f"  [{r['idx']:>5}] {r['name']}")
