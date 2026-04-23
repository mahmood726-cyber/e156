# sentinel:skip-file  (P0-hardcoded-local-path: portfolio-management script with intentional external project paths)
"""Scan the 29 missing projects and extract key info for E156 bodies."""
import os, json, re

projects = [
    ('ActionableEvidence', 'C:/Models/ActionableEvidence'),
    ('AutoReview', 'C:/Models/AutoReview'),
    ('ContradictionMap', 'C:/Models/ContradictionMap'),
    ('EquityMA', 'C:/Models/EquityMA'),
    ('EvidenceAtlas', 'C:/Models/EvidenceAtlas'),
    ('EvidenceCopula', 'C:/Models/EvidenceCopula'),
    ('EvidenceEntropy', 'C:/Models/EvidenceEntropy'),
    ('EvidenceExtremes', 'C:/Models/EvidenceExtremes'),
    ('EvidenceKM', 'C:/Models/EvidenceKM'),
    ('EvidenceMap', 'C:/Models/EvidenceMap'),
    ('EvidenceScore', 'C:/Models/EvidenceScore'),
    ('EvidenceSpectral', 'C:/Models/EvidenceSpectral'),
    ('EvidenceTopology', 'C:/Models/EvidenceTopology'),
    ('HyperMeta', 'C:/Models/HyperMeta'),
    ('InfoGeoMA', 'C:/Models/InfoGeoMA'),
    ('MetaVoI', 'C:/Models/MetaVoI'),
    ('MoneyTrail', 'C:/Models/MoneyTrail'),
    ('PatientMA', 'C:/Models/PatientMA'),
    ('PriorLab', 'C:/Models/PriorLab'),
    ('QualSynth', 'C:/Models/QualSynth'),
    ('SROCPlotter', 'C:/Models/SROCPlotter'),
    ('SafeMA', 'C:/Models/SafeMA'),
    ('TherapyGraveyard', 'C:/Models/TherapyGraveyard'),
    ('TransportMA', 'C:/Models/TransportMA'),
    ('TrustGate', 'C:/Models/TrustGate'),
    ('Integrity-Guard-Forensics', 'C:/Integrity-Guard-Forensics'),
    ('MetaFrontierLab', 'C:/MetaFrontierLab'),
    ('ctgov-registry-survival', 'C:/Projects/ctgov-registry-survival'),
    ('surroNMA', 'C:/Projects/surroNMA'),
]

for name, path in projects:
    if not os.path.isdir(path):
        print(f'{name}|NOT FOUND|{path}|0')
        continue
    files = os.listdir(path)
    title = ''
    desc = ''
    estimand = ''
    data_src = ''
    lines = 0

    # paper.json
    pj_path = os.path.join(path, 'paper.json')
    if os.path.exists(pj_path):
        try:
            with open(pj_path, 'r', encoding='utf-8') as f:
                pj = json.load(f)
            title = pj.get('title', '')[:120]
            desc = pj.get('abstract', pj.get('description', ''))[:300]
            estimand = pj.get('estimand', '')[:80]
            data_src = pj.get('data', pj.get('dataset', ''))[:120]
        except:
            pass

    # README
    if not desc:
        for rn in ['README.md', 'readme.md']:
            rp = os.path.join(path, rn)
            if os.path.exists(rp):
                try:
                    with open(rp, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read(3000)
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#') and not line.startswith('```') and not line.startswith('|') and not line.startswith('-') and len(line) > 20:
                            desc = line[:300]
                            break
                except:
                    pass
                break

    # HTML title
    if not title:
        for hf in files:
            if hf.endswith('.html') and os.path.isfile(os.path.join(path, hf)):
                try:
                    with open(os.path.join(path, hf), 'r', encoding='utf-8', errors='replace') as f:
                        hc = f.read(3000)
                    m = re.search(r'<title>(.*?)</title>', hc)
                    if m:
                        title = m.group(1)[:120]
                except:
                    pass
                break

    # Line count of main HTML
    for hf in files:
        if hf.endswith('.html') and os.path.isfile(os.path.join(path, hf)):
            try:
                with open(os.path.join(path, hf), 'r', encoding='utf-8', errors='replace') as f:
                    lines = sum(1 for _ in f)
            except:
                pass
            break

    print(f'{name}|{title}|{desc[:200]}|{estimand}|{data_src}|{len(files)}f|{lines}L')
