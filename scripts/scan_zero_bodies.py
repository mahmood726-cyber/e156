# sentinel:skip-file  (P0-hardcoded-local-path: portfolio-management script with intentional external project paths)
"""Scan all 51 remaining zero-body projects and extract key info."""
import os, json, re

projects = [
    ('3dvitreous-grapher', 'C:/Projects/3dvitreous-grapher'),
    ('area1_small_sample_analysis', 'C:/Projects/area1_small_sample_analysis'),
    ('asreview_5star', 'C:/Projects/asreview_5star'),
    ('AsSirat', 'C:/Models/AsSirat'),
    ('cbamm-project2', 'C:/Projects/cbamm-project2'),
    ('childnajia', 'C:/Projects/childnajia'),
    ('CINeMA', 'C:/Models/CINeMA'),
    ('claude-rct-work', 'C:/Projects/claude-rct-work'),
    ('Denominator_Calibrated_Living_NMA', 'C:/Models/Denominator_Calibrated_Living_NMA'),
    ('EvidenceGapMap', 'C:/EvidenceGapMap'),
    ('EvidenceOracle', 'C:/Models/EvidenceOracle'),
    ('experimental-meta-analysis', 'C:/Projects/experimental-meta-analysis'),
    ('Fatiha-Course', 'C:/Projects/Fatiha-Course'),
    ('finalpaper', 'C:/Projects/finalpaper'),
    ('GRADEPro', 'C:/Models/GRADEPro'),
    ('HFN786', 'C:/Projects/HFN786'),
    ('hfpef_registry_calibration', 'C:/Projects/hfpef_registry_calibration'),
    ('HTML-Misc', 'C:/Projects/HTML-Misc'),
    ('hub', 'C:/HTML apps/hub'),
    ('IPD Zahid', 'C:/Projects/IPD Zahid'),
    ('ipd_qma_project', 'C:/Projects/ipd_qma_project'),
    ('IPDSimulator', 'C:/Models/IPDSimulator'),
    ('KMextract', 'C:/KMextract'),
    ('lec_phase0_bundle', 'C:/Projects/lec_phase0_bundle'),
    ('lec_phase0_project', 'C:/Projects/lec_phase0_project'),
    ('LFAHFN', 'C:/Projects/LFAHFN'),
    ('Living metas', 'C:/Living metas'),
    ('LivingMA', 'C:/Models/LivingMA'),
    ('LivingMeta_Watchman_Amulet', 'C:/Projects/LivingMeta_Watchman_Amulet'),
    ('MAConverter', 'C:/Models/MAConverter'),
    ('MAFI', 'C:/Projects/MAFI'),
    ('MAFI-Continuation', 'C:/Projects/MAFI-Continuation'),
    ('MASampleSize', 'C:/Models/MASampleSize'),
    ('meta-frontier-bibliography', 'C:/Projects/meta-frontier-bibliography'),
    ('meta-frontier-readiness-atlas', 'C:/Projects/meta-frontier-readiness-atlas'),
    ('minireview', 'C:/Projects/minireview'),
    ('new-app', 'C:/Projects/new-app'),
    ('NMA', 'C:/Projects/NMA'),
    ('oman', 'C:/Projects/oman'),
    ('Pairwise humble', 'C:/Projects/Pairwise humble'),
    ('PFA_AF_LivingMeta', 'C:/Projects/PFA_AF_LivingMeta'),
    ('rayyanreplacement', 'C:/Projects/rayyanreplacement'),
    ('research-orbit-control', 'C:/Projects/research-orbit-control'),
    ('Scripts', 'C:/Projects/Scripts'),
    ('Stories', 'C:/Projects/Stories'),
    ('superapp', 'C:/Projects/superapp'),
    ('tower', 'C:/Projects/tower'),
    ('tower_js', 'C:/Projects/tower_js'),
    ('Tricuspid_TEER_LivingMeta', 'C:/Projects/Tricuspid_TEER_LivingMeta'),
    ('truthcert-openclaw-supermemory-stack', 'C:/Projects/truthcert-openclaw-supermemory-stack'),
    ('TruthCert-Validation-Papers', 'C:/Projects/TruthCert-Validation-Papers'),
    ('TruthCert_v3.1.0_modeling', 'C:/Projects/TruthCert_v3.1.0_modeling'),
    ('TSA', 'C:/Models/TSA'),
]

for name, path in projects:
    if not os.path.isdir(path):
        print(f'{name}|NOT FOUND|{path}|0')
        continue
    files = os.listdir(path)

    # Look for paper.json
    title = ''
    desc = ''
    estimand = ''
    data_src = ''
    paper_path = os.path.join(path, 'paper.json')
    if os.path.exists(paper_path):
        try:
            with open(paper_path, 'r', encoding='utf-8') as f:
                pj = json.load(f)
            title = pj.get('title', '')[:120]
            desc = pj.get('abstract', pj.get('description', ''))[:300]
            estimand = pj.get('estimand', '')[:80]
            data_src = pj.get('data', pj.get('dataset', ''))[:120]
        except:
            pass

    # Try README
    if not desc:
        for rname in ['README.md', 'readme.md']:
            rpath = os.path.join(path, rname)
            if os.path.exists(rpath):
                try:
                    with open(rpath, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read(3000)
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#') and not line.startswith('```') and not line.startswith('|') and not line.startswith('-') and len(line) > 20:
                            desc = line[:300]
                            break
                except:
                    pass
                break

    # Try HTML title
    if not title:
        for hf in files:
            if hf.endswith('.html'):
                try:
                    with open(os.path.join(path, hf), 'r', encoding='utf-8', errors='replace') as f:
                        hcontent = f.read(3000)
                    m = re.search(r'<title>(.*?)</title>', hcontent)
                    if m:
                        title = m.group(1)[:120]
                except:
                    pass
                break

    # Count lines of main file
    main_lines = 0
    for hf in files:
        if hf.endswith('.html') and os.path.isfile(os.path.join(path, hf)):
            try:
                with open(os.path.join(path, hf), 'r', encoding='utf-8', errors='replace') as f:
                    main_lines = sum(1 for _ in f)
            except:
                pass
            break

    print(f'{name}|{title}|{desc[:200]}|{estimand}|{data_src}|{len(files)}f|{main_lines}L')
