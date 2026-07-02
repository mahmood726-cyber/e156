#!/usr/bin/env python3
"""
Extract ref-lists from local source JATS packages for submissions 160-171
whose citations table is empty. Outputs SQL INSERT statements.
"""
import re, os, sys

BASE = r'F:\E156\outputs'

# Map: submission_id -> (relative_path_to_local_jats, publication_id_on_server)
SOURCES = {
    160: (r'NICECardiology-final\package\manuscript.jats.xml',          311),
    161: (r'pactr-hiddenness-atlas-final\manuscript.jats.xml',           312),
    162: (r'malaria-ct-recon-final\galley\malaria-ct-recon.jats.xml',    313),
    163: (r'OutcomeSwitchDetector-final\OutcomeSwitchDetector.jats.xml', 314),
    164: (r'TrialDiversityAtlas-final\TrialDiversityAtlas-FINAL.jats.xml',315),
    165: (r'ctgov-structural-missingness-final\manuscript.jats.xml',      316),
    166: (r'BenfordMA-final\BenfordMA_JATS_variantA.xml',                317),
    167: (r'combined-evidence-reversals-final\manuscript.jats.xml',       318),
    168: (r'combined-evidence-integrity-final\manuscript.jats.xml',       319),
    169: (r'combined-cochrane-robustness-final\manuscript.jats.xml',      320),
    170: (r'combined-heterogeneity-structure-final\manuscript.jats.xml',  321),
    171: (r'laiba-integrity-transparency-merged-final\manuscript.jats.xml',322),
}

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()

rows = []
for sid in sorted(SOURCES):
    relpath, pub_id = SOURCES[sid]
    path = os.path.join(BASE, relpath)
    if not os.path.exists(path):
        print(f"MISSING #{sid}: {path}", file=sys.stderr)
        continue
    txt = open(path, encoding='utf-8', errors='replace').read()
    refs = re.findall(r'<ref(?:\s[^>]*)?>(?!-list)([\s\S]*?)</ref>', txt)
    # Exclude any accidental ref-list captures; also filter by actual ref id/label pattern
    refs = [r for r in refs if '<label>' in r or '<mixed-citation>' in r or '<element-citation>' in r or len(r.strip()) > 20]
    print(f"  #{sid} pub={pub_id}: {len(refs)} refs from {os.path.basename(path)}", file=sys.stderr)
    for i, ref_xml in enumerate(refs, 1):
        raw = strip_tags(ref_xml).strip()
        # Remove leading section title bleed-through ("References\n")
        raw = re.sub(r'^References\s*', '', raw, flags=re.IGNORECASE).strip()
        # Remove leading number/label
        raw = re.sub(r'^[\[\(]?\d+[\]\)\.:\s]+', '', raw).strip()
        raw = re.sub(r'^\s+', '', raw)
        if raw:
            rows.append((pub_id, i, raw))

# Write SQL
lines = ["-- Citations for submissions 160-171 extracted from local JATS packages"]
lines.append("-- Run: mysql -u ojsuser -p'OjsPass123!' ojs < insert_refs_160_171.sql")
lines.append("")
for pub_id, seq, raw in rows:
    escaped = raw.replace("\\", "\\\\").replace("'", "\\'")
    lines.append(f"INSERT INTO citations (publication_id, seq, raw_citation) VALUES ({pub_id}, {seq}, '{escaped}');")

lines.append(f"\n-- Total: {len(rows)} citation rows inserted")
sql_out = os.path.join(os.path.dirname(__file__), 'insert_refs_160_171.sql')
with open(sql_out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f"Written {len(rows)} rows to {sql_out}", file=sys.stderr)
print(f"SQL written to: {sql_out}")
