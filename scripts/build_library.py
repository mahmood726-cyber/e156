"""E156 Library Build Script.

Parses the rewrite workbook, generates tags, enriches with project metadata,
and builds the final library HTML file.
"""
import json
import os
import re

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WORKBOOK_PATH = 'C:/E156/rewrite-workbook.txt'
TEMPLATE_PATH = 'C:/E156/templates/library-template.html'
OUTPUT_PATH = 'C:/E156/e156-library.html'

TAG_KEYWORDS = {
    'NMA': [r'\bNMA\b', r'NMA\b', r'\bnetwork meta'],
    'Bayesian': [r'\bBayes'],
    'GRADE': [r'\bGRADE\b'],
    'CT.gov': [r'CT\.gov', r'ClinicalTrials\.gov', r'\bAACT\b'],
    'living': [r'\bliving\b'],
    'DTA': [r'\bDTA\b', r'\bdiagnostic test accuracy\b', r'\bSROC\b'],
    'Cochrane': [r'\bCochrane\b'],
    'browser': [r'\bbrowser\b'],
    'R package': [r'\bR package\b', r'\bmetafor\b', r'\brpact\b'],
    'IPD': [r'\bIPD\b', r'\bindividual participant\b'],
    'HTA': [r'\bHTA\b', r'\bhealth technology\b', r'\bcost-effective'],
    'publication bias': [r'\bpublication bias\b', r'\bfunnel\b', r'\btrim.and.fill\b'],
    'fragility': [r'\bfragility\b', r'\bfragile\b'],
    'heterogeneity': [r'\bheterogeneity\b', r'\btau.squared\b', r'\bI.squared\b'],
    'dose-response': [r'\bdose.response\b'],
    'survival': [r'\bsurvival\b', r'\bKaplan.Meier\b', r'\bhazard\b'],
    'transportability': [r'\btransport'],
    'equity': [r'\bequity\b', r'\bPROGRESS\b'],
    'qualitative': [r'\bqualitative\b', r'\bmeta.ethnograph'],
    'trial sequential': [r'\btrial sequential\b', r'\bTSA\b'],
    'forensic': [r'\bforensic\b', r'\bBenford\b', r'\bGRIM\b', r'\bfabrication\b'],
    'SGLT2': [r'\bSGLT2\b'],
    'finerenone': [r'\bfinerenone\b'],
    'cardiovascular': [r'\bcardiovasc', r'\bcardio\b', r'\bheart\b'],
}

# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------


def count_words(text):
    """Count words in text."""
    return len(text.split())


def count_sentences(text):
    """Count sentences using approximate heuristic (handles abbreviations)."""
    # Neutralize common abbreviations
    t = text.replace('e.g.', 'eg').replace('i.e.', 'ie')
    t = t.replace('vs.', 'vs').replace('et al.', 'etal')
    t = t.replace('approx.', 'approx')
    sents = re.split(r'(?<=[.?!])\s+(?=[A-Z])', t)
    return len([s for s in sents if s.strip()])


def generate_tags(title):
    """Generate a list of tags from a title string using TAG_KEYWORDS patterns."""
    tags = []
    for tag, patterns in TAG_KEYWORDS.items():
        for pattern in patterns:
            if re.search(pattern, title, re.IGNORECASE):
                tags.append(tag)
                break
    return tags


def classify_type(type_str):
    """Normalize a type string to one of: methods, clinical, audit."""
    t = type_str.strip().lower()
    if t in ('methods', 'pairwise', 'showcase'):
        return 'methods'
    if t in ('clinical',):
        return 'clinical'
    if t in ('meta-epidemiology', 'meta-research', 'empirical', 'data'):
        return 'audit'
    return 'methods'


def is_placeholder_text(text):
    """Return True for workbook placeholder rows that should not enter the library."""
    stripped = text.strip()
    return (
        not stripped
        or stripped.startswith('[Pending')
        or stripped.startswith('[No E156 body generated yet]')
    )


# ---------------------------------------------------------------------------
# Workbook parser
# ---------------------------------------------------------------------------


def parse_workbook(path):
    """Parse the rewrite workbook and return a list of entry dicts.

    Each dict has keys: id, slug, title, type, estimand, data, path,
    body, rewrite, wordCount, sentenceCount, tags.
    """
    if not os.path.isfile(path):
        print(f"Error: workbook not found at {path}")
        return []

    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    entries = []
    header_matches = list(re.finditer(r'(?m)^\[(\d+)/\d+\]\s+(.+)$', text))

    for idx, header_match in enumerate(header_matches):
        sec_start = header_match.start()
        sec_end = header_matches[idx + 1].start() if idx + 1 < len(header_matches) else len(text)
        sec = text[sec_start:sec_end]
        entry_id = int(header_match.group(1))
        slug = header_match.group(2).strip()

        # Extract TITLE
        title_m = re.search(r'TITLE:\s*(.+)', sec)
        title = title_m.group(1).strip() if title_m else slug

        # Extract TYPE and ESTIMAND from "TYPE: xxx  |  ESTIMAND: yyy"
        type_m = re.search(r'TYPE:\s*(.+?)\s*\|', sec)
        type_str = type_m.group(1).strip() if type_m else 'methods'

        estimand_m = re.search(r'ESTIMAND:\s*(.+)', sec)
        estimand = estimand_m.group(1).strip() if estimand_m else ''

        # Extract DATA
        data_m = re.search(r'DATA:\s*(.+)', sec)
        data = data_m.group(1).strip() if data_m else ''

        # Extract PATH
        path_m = re.search(r'PATH:\s*(.+)', sec)
        proj_path = path_m.group(1).strip() if path_m else ''

        # Extract CURRENT BODY
        body_m = re.search(
            r'CURRENT BODY[^\n]*:[^\S\n]*\n(.*?)(?=YOUR REWRITE)',
            sec, re.DOTALL
        )
        body = body_m.group(1).strip() if body_m else ''

        # Extract YOUR REWRITE
        rw_m = re.search(
            r'YOUR REWRITE[^\n]*:[^\S\n]*\n(.*?)(?=\n(?:SUBMITTED:|={10,})|\Z)',
            sec,
            re.DOTALL,
        )
        rewrite = rw_m.group(1).strip() if rw_m else ''

        # Use rewrite if available, fallback to body
        display_text = rewrite if len(rewrite) > 10 else body
        if is_placeholder_text(display_text):
            continue

        wc = count_words(display_text)
        sc = count_sentences(display_text)
        tags = generate_tags(title)

        entries.append({
            'id': entry_id,
            'slug': slug,
            'title': title,
            'type': classify_type(type_str),
            'estimand': estimand,
            'data': data,
            'path': proj_path,
            'body': body,
            'rewrite': rewrite,
            'wordCount': wc,
            'sentenceCount': sc,
            'tags': tags,
        })

    return entries


# ---------------------------------------------------------------------------
# Metadata enrichment
# ---------------------------------------------------------------------------


def enrich_with_metadata(entries):
    """Read paper.json at each project path for extra metadata.

    Adds: testCount, manuscriptStatus, validated, journal.
    """
    for entry in entries:
        proj_path = entry.get('path', '')
        if not proj_path:
            continue

        # Normalize path separators
        proj_path = proj_path.replace('\\', '/')

        paper_json = os.path.join(proj_path, 'paper', 'paper.json')
        if os.path.isfile(paper_json):
            try:
                with open(paper_json, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                entry['testCount'] = meta.get('testCount', None)
                entry['manuscriptStatus'] = meta.get('manuscriptStatus', None)
                entry['validated'] = meta.get('validated', False)
                entry['journal'] = meta.get('journal', None)
            except (json.JSONDecodeError, OSError):
                pass

        # Also check e156-submission/config.json
        config_json = os.path.join(proj_path, 'e156-submission', 'config.json')
        if os.path.isfile(config_json):
            try:
                with open(config_json, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                if 'testCount' not in entry or entry.get('testCount') is None:
                    entry['testCount'] = config.get('testCount', None)
                if 'journal' not in entry or entry.get('journal') is None:
                    entry['journal'] = config.get('journal', None)
            except (json.JSONDecodeError, OSError):
                pass

    return entries


# ---------------------------------------------------------------------------
# Output generation
# ---------------------------------------------------------------------------


def entries_to_js(entries):
    """Convert entries list to a JS const declaration string.

    Escapes </script> as ${'<'}/script> per html-apps.md rules.
    """
    json_str = json.dumps(entries, indent=2, ensure_ascii=False)
    # CRITICAL: escape </script> inside template literals / JS strings
    # HTML parser closes script block prematurely even inside JS
    json_str = json_str.replace('</script>', '<\\/script>')
    return f"const E156_DATA = {json_str};"


def build(workbook_path=None, template_path=None, output_path=None):
    """Main build function: parse workbook, enrich, generate output HTML."""
    workbook_path = workbook_path or WORKBOOK_PATH
    template_path = template_path or TEMPLATE_PATH
    output_path = output_path or OUTPUT_PATH

    # 1. Parse workbook
    entries = parse_workbook(workbook_path)
    print(f"Parsed {len(entries)} entries from workbook")

    # 2. Enrich with metadata
    entries = enrich_with_metadata(entries)

    # 3. Generate JS data
    js_data = entries_to_js(entries)

    # 4. Read template and inject data
    if os.path.isfile(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        output = template.replace('/* __E156_DATA__ */', js_data)
    else:
        # Minimal fallback if no template exists yet
        output = f"<script>\n{js_data}\n</script>"
        print(f"Warning: template not found at {template_path}, using minimal fallback")

    # 5. Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"Built library at {output_path} ({len(output):,} bytes)")

    return entries


if __name__ == '__main__':
    build()
