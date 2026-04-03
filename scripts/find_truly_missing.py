"""Find projects that are truly missing from the workbook (not just different names)."""
import re

with open('C:/E156/rewrite-workbook.txt', 'r', encoding='utf-8') as f:
    text = f.read()

sections = re.split(r'={50,}', text)
wb_names = set()
wb_paths = set()
for sec in sections:
    nm = re.search(r'\[\d+/302\]\s+(.+)', sec)
    pm = re.search(r'PATH:\s*(.+)', sec)
    if nm:
        wb_names.add(nm.group(1).strip().lower())
    if pm:
        p = pm.group(1).strip().replace(chr(92), '/').lower()
        wb_paths.add(p)

missing_candidates = [
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
    ('MetaReproducer', 'C:/MetaReproducer'),
    ('MetaShift', 'C:/MetaShift'),
    ('OutcomeReportingBias', 'C:/OutcomeReportingBias'),
    ('OverlapDetector', 'C:/OverlapDetector'),
    ('PredictionGap', 'C:/PredictionGap'),
]

truly_missing = []
already_present = []
for name, path in missing_candidates:
    name_lower = name.lower().replace('-', '').replace('_', '')
    found = False
    for wb in wb_names:
        wb_clean = wb.replace('-', '').replace('_', '')
        if name_lower == wb_clean or name.lower() == wb:
            found = True
            break
    path_lower = path.lower().replace(chr(92), '/')
    if not found:
        for wp in wb_paths:
            if path_lower in wp or wp in path_lower:
                found = True
                break

    if found:
        already_present.append(name)
    else:
        truly_missing.append((name, path))

print(f'Already in workbook: {len(already_present)}')
for n in already_present:
    print(f'  {n}')
print(f'\nTruly missing: {len(truly_missing)}')
for n, p in truly_missing:
    print(f'  {n} -> {p}')
