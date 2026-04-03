# E156 Library + Journal + Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-file HTML app (`e156-library.html`) that showcases 331 E156 micro-papers in three lazy-loaded sections: Library reading room, Journal Vol.1, and Seven Signs Dashboard.

**Architecture:** Python build script parses `rewrite-workbook.txt`, enriches with metadata from `paper.json` files, injects as JS const into an HTML template. Template contains all CSS/JS for the three-section app with NYT editorial styling. No CDN, no framework, fully offline.

**Tech Stack:** Python 3 (build script), vanilla HTML/CSS/JS (template), regex workbook parser (existing pattern from `verify_workbook.py`)

---

## File Structure

```
C:\E156\
├── e156-library.html                ← Final output (generated, ~4500 lines)
├── templates/
│   └── library-template.html        ← HTML/CSS/JS template (~3800 lines)
├── scripts/
│   └── build_library.py             ← Build script (~250 lines)
└── tests/
    └── test_build_library.py        ← Build script tests (~80 lines)
```

- `scripts/build_library.py` — Parses workbook, enriches metadata, generates tags, emits final HTML. One responsibility: data extraction + template injection.
- `templates/library-template.html` — Complete app with `/* __E156_DATA__ */` placeholder. Three sections: Library (default), Journal, Dashboard. All CSS inline in `<style>`, all JS inline in `<script>`.
- `tests/test_build_library.py` — Validates build output: entry count, word counts, tag generation, HTML integrity.

---

### Task 1: Build Script — Workbook Parser + Tag Generator

**Files:**
- Create: `C:\E156\scripts\build_library.py`
- Create: `C:\E156\tests\test_build_library.py`

- [ ] **Step 1: Write the failing test for workbook parsing**

```python
# C:\E156\tests\test_build_library.py
"""Tests for the E156 library build script."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_parse_workbook_count():
    from build_library import parse_workbook
    entries = parse_workbook('C:/E156/rewrite-workbook.txt')
    assert len(entries) == 331, f"Expected 331 entries, got {len(entries)}"

def test_parse_workbook_fields():
    from build_library import parse_workbook
    entries = parse_workbook('C:/E156/rewrite-workbook.txt')
    first = entries[0]
    assert 'id' in first
    assert 'title' in first
    assert 'type' in first
    assert 'estimand' in first
    assert 'data' in first
    assert 'path' in first
    assert 'body' in first
    assert 'rewrite' in first
    assert 'wordCount' in first
    assert 'sentenceCount' in first

def test_parse_workbook_no_blank_rewrites():
    from build_library import parse_workbook
    entries = parse_workbook('C:/E156/rewrite-workbook.txt')
    blank = [e for e in entries if e['wordCount'] < 10]
    assert len(blank) == 0, f"Found {len(blank)} blank rewrites"

def test_parse_workbook_word_counts_in_range():
    from build_library import parse_workbook
    entries = parse_workbook('C:/E156/rewrite-workbook.txt')
    out_of_range = [(e['id'], e['slug'], e['wordCount']) for e in entries
                    if e['wordCount'] < 90 or e['wordCount'] > 170]
    assert len(out_of_range) == 0, f"Out of range: {out_of_range[:5]}"

def test_generate_tags():
    from build_library import generate_tags
    tags = generate_tags("BayesianMA: Browser-Based Bayesian Random-Effects Meta-Analysis with Prior Sensitivity")
    assert 'Bayesian' in tags
    assert 'browser' in tags

def test_generate_tags_nma():
    from build_library import generate_tags
    tags = generate_tags("ComponentNMA: World-First Browser cNMA with Interactions")
    assert 'NMA' in tags
    assert 'browser' in tags

def test_generate_tags_ctgov():
    from build_library import generate_tags
    tags = generate_tags("CT.gov Hiddenness Atlas: 578K-Study Registry Audit")
    assert 'CT.gov' in tags

def test_generate_tags_always_returns_list():
    from build_library import generate_tags
    tags = generate_tags("Some Generic Title Without Keywords")
    assert isinstance(tags, list)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd C:/E156 && python -m pytest tests/test_build_library.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'build_library'` or `cannot import name 'parse_workbook'`

- [ ] **Step 3: Write the build script with parser and tag generator**

```python
# C:\E156\scripts\build_library.py
"""
Build the E156 Library single-file HTML app.

Parses rewrite-workbook.txt, enriches with metadata, generates tags,
injects data into library-template.html, emits e156-library.html.

Usage: python C:/E156/scripts/build_library.py
"""

import re
import os
import json

WORKBOOK_PATH = 'C:/E156/rewrite-workbook.txt'
TEMPLATE_PATH = 'C:/E156/templates/library-template.html'
OUTPUT_PATH = 'C:/E156/e156-library.html'

TAG_KEYWORDS = {
    'NMA': [r'\bNMA\b', r'\bnetwork meta'],
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


def count_words(text):
    return len(text.split())


def count_sentences(text):
    text = text.replace('e.g.', 'eg').replace('i.e.', 'ie').replace('vs.', 'vs').replace('et al.', 'etal')
    sents = re.split(r'(?<=[.?!])\s+(?=[A-Z])', text)
    return len([s for s in sents if s.strip()])


def generate_tags(title):
    """Generate tags from title using keyword patterns."""
    tags = []
    for tag, patterns in TAG_KEYWORDS.items():
        for pattern in patterns:
            if re.search(pattern, title, re.IGNORECASE):
                tags.append(tag)
                break
    return tags


def classify_type(type_str):
    """Normalize type to one of: methods, clinical, audit."""
    t = type_str.lower().strip()
    if 'clinical' in t:
        return 'clinical'
    if 'audit' in t:
        return 'audit'
    return 'methods'


def parse_workbook(workbook_path):
    """Parse rewrite-workbook.txt into a list of entry dicts."""
    with open(workbook_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sections = re.split(r'={50,}', text)
    entries = []

    for sec in sections:
        m = re.search(r'\[(\d+)/\d+\]\s+(.+)', sec)
        if not m:
            continue

        num = int(m.group(1))
        slug = m.group(2).strip()

        title_m = re.search(r'TITLE:\s*(.+)', sec)
        title = title_m.group(1).strip() if title_m else slug

        type_m = re.search(r'TYPE:\s*(\w+)', sec)
        type_str = classify_type(type_m.group(1)) if type_m else 'methods'

        estimand_m = re.search(r'ESTIMAND:\s*(.+)', sec)
        estimand = estimand_m.group(1).strip() if estimand_m else ''

        data_m = re.search(r'DATA:\s*(.+)', sec)
        data = data_m.group(1).strip() if data_m else ''

        path_m = re.search(r'PATH:\s*(.+)', sec)
        path = path_m.group(1).strip() if path_m else ''

        body_m = re.search(r'CURRENT BODY[^\n]*:\s*\n(.+?)(?=YOUR REWRITE)', sec, re.DOTALL)
        body = body_m.group(1).strip() if body_m else ''

        rw_m = re.search(r'YOUR REWRITE[^\n]*:\s*\n(.*)', sec, re.DOTALL)
        rewrite = rw_m.group(1).strip() if rw_m else ''

        wc = count_words(rewrite) if rewrite else 0
        sc = count_sentences(rewrite) if rewrite else 0
        tags = generate_tags(title)

        entries.append({
            'id': num,
            'slug': slug,
            'title': title,
            'type': type_str,
            'estimand': estimand,
            'data': data,
            'path': path,
            'body': body,
            'rewrite': rewrite,
            'wordCount': wc,
            'sentenceCount': sc,
            'tags': tags,
        })

    return entries


def enrich_with_metadata(entries):
    """Enrich entries with data from paper.json files where available."""
    for entry in entries:
        path = entry['path'].replace(chr(92), '/')
        paper_json = os.path.join(path, 'paper.json')
        if os.path.exists(paper_json):
            try:
                with open(paper_json, 'r', encoding='utf-8') as f:
                    pj = json.load(f)
                entry['testCount'] = pj.get('test_count', pj.get('tests', None))
                entry['manuscriptStatus'] = pj.get('manuscript_status', pj.get('status', None))
                entry['validated'] = pj.get('validated', None)
                entry['journal'] = pj.get('journal', pj.get('target_journal', None))
            except Exception:
                pass
    return entries


def entries_to_js(entries):
    """Convert entries list to a JS const declaration."""
    safe = json.dumps(entries, ensure_ascii=False, indent=2)
    # Escape </script> inside JSON strings
    safe = safe.replace('</script>', "${'<'}/script>")
    return f'const E156_DATA = {safe};'


def build(workbook_path=WORKBOOK_PATH, template_path=TEMPLATE_PATH, output_path=OUTPUT_PATH):
    """Main build: parse workbook, enrich, inject into template, emit HTML."""
    entries = parse_workbook(workbook_path)
    entries = enrich_with_metadata(entries)

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    js_data = entries_to_js(entries)
    html = template.replace('/* __E156_DATA__ */', js_data)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Built {output_path}: {len(entries)} entries, {len(html):,} bytes')
    return entries


if __name__ == '__main__':
    build()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd C:/E156 && python -m pytest tests/test_build_library.py -v`
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
cd C:/E156
git add scripts/build_library.py tests/test_build_library.py
git commit -m "feat: build script with workbook parser and tag generator"
```

---

### Task 2: HTML Template — CSS Foundation + Navigation

**Files:**
- Create: `C:\E156\templates\library-template.html`

- [ ] **Step 1: Create the template with CSS and navigation shell**

Create `C:\E156\templates\library-template.html` with the complete `<!DOCTYPE html>` through closing `</html>`. This step covers:

- All CSS (inline `<style>` block)
- Fixed top nav bar with three section links
- Three section containers (Library, Journal, Dashboard) — empty content for now
- The `<script>` block opening with data placeholder and navigation JS

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>E156 Library — 331 Micro-Papers in Evidence Synthesis</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* --- Base --- */
body {
  font-family: Georgia, Charter, 'Times New Roman', serif;
  background: #faf9f6;
  color: #1a1a1a;
  line-height: 1.75;
  -webkit-font-smoothing: antialiased;
}
a { color: inherit; }

/* --- Nav --- */
.nav-bar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  background: #faf9f6; border-bottom: 1px solid #e0ddd8;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 24px; height: 52px;
  font-family: system-ui, -apple-system, sans-serif;
}
.nav-wordmark {
  font-family: Georgia, serif; font-weight: 700; font-size: 1.3rem;
  letter-spacing: -0.02em;
}
.nav-links { display: flex; gap: 32px; }
.nav-links a {
  text-decoration: none; font-size: 0.9rem; color: #666;
  padding-bottom: 2px; border-bottom: 2px solid transparent;
  transition: color 0.2s, border-color 0.2s; cursor: pointer;
}
.nav-links a.active { color: #1a1a1a; border-bottom-color: #1a1a1a; }
.nav-links a:hover { color: #1a1a1a; }
.nav-search-btn {
  background: none; border: none; cursor: pointer; font-size: 1.1rem;
  color: #666; padding: 4px;
}
.nav-search-btn:hover { color: #1a1a1a; }

/* --- Sections --- */
.section { display: none; padding-top: 68px; min-height: 100vh; }
.section.active { display: block; }

/* --- Masthead --- */
.masthead { text-align: center; padding: 60px 24px 40px; }
.masthead h1 { font-size: 3.2rem; font-weight: 700; letter-spacing: -0.02em; }
.masthead .subtitle { font-size: 1.15rem; color: #666; font-style: italic; margin-top: 6px; }
.masthead .author { font-size: 0.9rem; color: #999; margin-top: 8px; font-family: system-ui, sans-serif; }

/* --- Controls --- */
.controls {
  max-width: 1080px; margin: 0 auto; padding: 0 24px 24px;
  display: flex; flex-wrap: wrap; align-items: center; gap: 12px;
  font-family: system-ui, sans-serif;
}
.search-box {
  flex: 1; min-width: 200px; padding: 8px 14px; font-size: 0.9rem;
  border: 1px solid #d0cdc8; border-radius: 6px; background: #fff;
  font-family: system-ui, sans-serif;
}
.search-box:focus { outline: none; border-color: #1a1a1a; }
.pill-group { display: flex; gap: 6px; }
.pill {
  padding: 4px 14px; border-radius: 20px; font-size: 0.8rem;
  border: 1px solid #d0cdc8; background: #fff; cursor: pointer;
  transition: background 0.15s, color 0.15s;
  font-family: system-ui, sans-serif;
}
.pill.active { background: #1a1a1a; color: #faf9f6; border-color: #1a1a1a; }
.pill:hover:not(.active) { background: #f0ede8; }
.sort-select {
  padding: 6px 10px; font-size: 0.8rem; border: 1px solid #d0cdc8;
  border-radius: 6px; background: #fff; font-family: system-ui, sans-serif;
}
.view-toggle { display: flex; gap: 4px; }
.view-btn {
  padding: 5px 10px; border: 1px solid #d0cdc8; background: #fff;
  cursor: pointer; font-size: 0.85rem; border-radius: 4px;
  font-family: system-ui, sans-serif;
}
.view-btn.active { background: #1a1a1a; color: #faf9f6; border-color: #1a1a1a; }

/* --- Grid --- */
.card-grid {
  max-width: 1080px; margin: 0 auto; padding: 0 24px 60px;
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;
}
.card {
  background: #fff; border-radius: 8px; padding: 20px 22px;
  border-top: 3px solid #2c3e50; cursor: pointer;
  transition: box-shadow 0.2s, transform 0.15s;
}
.card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.08); transform: translateY(-2px); }
.card[data-type="clinical"] { border-top-color: #8b1a1a; }
.card[data-type="audit"] { border-top-color: #4a5568; }
.card-title {
  font-family: Georgia, serif; font-size: 0.95rem; font-weight: 600;
  line-height: 1.4; margin-bottom: 8px;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.card-question {
  font-size: 0.85rem; color: #555; line-height: 1.5;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
  margin-bottom: 10px;
}
.card-meta { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.card-wc {
  font-family: Menlo, Consolas, monospace; font-size: 0.7rem;
  background: #f0ede8; padding: 2px 8px; border-radius: 3px; color: #666;
}
.tag-pill {
  font-size: 0.7rem; padding: 2px 8px; border-radius: 10px;
  background: #eef; color: #336; font-family: system-ui, sans-serif;
}

/* --- List View --- */
.list-view { max-width: 1080px; margin: 0 auto; padding: 0 24px 60px; }
.list-table { width: 100%; border-collapse: collapse; font-family: system-ui, sans-serif; font-size: 0.85rem; }
.list-table th {
  text-align: left; padding: 8px 12px; border-bottom: 2px solid #1a1a1a;
  font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666;
  cursor: pointer;
}
.list-table th:hover { color: #1a1a1a; }
.list-table td { padding: 8px 12px; border-bottom: 1px solid #e0ddd8; }
.list-table tr { cursor: pointer; transition: background 0.1s; }
.list-table tr:hover { background: #f5f3ef; }
.type-badge {
  font-size: 0.7rem; padding: 2px 8px; border-radius: 10px;
  color: #fff; font-family: system-ui, sans-serif;
}
.type-badge.methods { background: #2c3e50; }
.type-badge.clinical { background: #8b1a1a; }
.type-badge.audit { background: #4a5568; }

/* --- Reading View --- */
.reading-overlay {
  display: none; position: fixed; inset: 0; z-index: 200;
  background: #faf9f6; overflow-y: auto;
}
.reading-overlay.open { display: block; }
.reading-nav {
  max-width: 680px; margin: 0 auto; padding: 20px 24px;
  display: flex; justify-content: space-between; align-items: center;
  font-family: system-ui, sans-serif; font-size: 0.85rem;
}
.reading-nav button {
  background: none; border: 1px solid #d0cdc8; border-radius: 4px;
  padding: 4px 14px; cursor: pointer; font-size: 0.85rem;
  font-family: system-ui, sans-serif;
}
.reading-nav button:hover { background: #f0ede8; }
.reading-content { max-width: 680px; margin: 0 auto; padding: 0 24px 80px; }
.reading-content h1 { font-size: 2rem; font-weight: 700; line-height: 1.3; margin-bottom: 12px; }
.reading-meta {
  font-family: system-ui, sans-serif; font-size: 0.8rem;
  color: #888; text-transform: uppercase; letter-spacing: 0.04em;
  margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e0ddd8;
}
.reading-body { font-size: 1.1rem; line-height: 1.85; }
.sentence-tags {
  margin-top: 20px; display: flex; flex-wrap: wrap; gap: 6px;
}
.sentence-tags .stag {
  font-size: 0.7rem; padding: 2px 8px; border-radius: 3px;
  background: #f0ede8; color: #666; font-family: system-ui, sans-serif;
}
.reading-actions {
  margin-top: 24px; display: flex; gap: 8px; flex-wrap: wrap;
}
.reading-actions button {
  background: #1a1a1a; color: #faf9f6; border: none; padding: 8px 18px;
  border-radius: 4px; cursor: pointer; font-size: 0.8rem;
  font-family: system-ui, sans-serif; transition: background 0.15s;
}
.reading-actions button:hover { background: #333; }
.reading-path {
  margin-top: 16px; font-family: Menlo, Consolas, monospace;
  font-size: 0.75rem; color: #999;
}

/* --- Journal --- */
.journal-header {
  text-align: center; padding: 60px 24px 40px;
  border-bottom: 2px solid #1a1a1a; max-width: 680px; margin: 0 auto;
}
.journal-header h1 { font-size: 2rem; font-weight: 700; font-style: italic; }
.journal-header .vol { font-size: 1rem; color: #666; margin-top: 6px; font-family: system-ui, sans-serif; }
.journal-header .editor { font-size: 0.85rem; color: #999; margin-top: 4px; font-family: system-ui, sans-serif; }
.journal-editorial {
  max-width: 680px; margin: 40px auto; padding: 0 24px;
  font-size: 1.05rem; line-height: 1.8;
}
.journal-editorial h2 { font-size: 1.3rem; margin-bottom: 12px; }
.journal-toc { max-width: 680px; margin: 40px auto; padding: 0 24px 80px; }
.journal-toc h2 {
  font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.05em;
  color: #666; margin-top: 32px; margin-bottom: 12px; padding-bottom: 6px;
  border-bottom: 1px solid #e0ddd8; font-family: system-ui, sans-serif;
}
.toc-entry {
  display: flex; align-items: baseline; gap: 12px; padding: 6px 0;
  cursor: pointer; transition: color 0.15s; font-size: 0.9rem;
}
.toc-entry:hover { color: #555; }
.toc-num { font-family: Menlo, Consolas, monospace; font-size: 0.75rem; color: #999; min-width: 32px; }
.toc-title { flex: 1; }
.toc-estimand { font-size: 0.75rem; color: #999; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.journal-export {
  max-width: 680px; margin: 0 auto; padding: 20px 24px;
  display: flex; gap: 12px;
}
.journal-export button {
  background: #1a1a1a; color: #faf9f6; border: none; padding: 10px 20px;
  border-radius: 4px; cursor: pointer; font-size: 0.85rem;
  font-family: system-ui, sans-serif;
}
.journal-export button:hover { background: #333; }

/* --- Dashboard --- */
.dashboard { max-width: 800px; margin: 0 auto; padding: 0 24px 80px; }
.dashboard h1 { text-align: center; font-size: 2rem; margin-bottom: 8px; padding-top: 40px; }
.dashboard .dash-subtitle { text-align: center; color: #666; font-size: 0.95rem; margin-bottom: 40px; }
.sign-row {
  margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid #f0ede8;
}
.sign-label {
  font-family: system-ui, sans-serif; font-size: 0.8rem;
  text-transform: uppercase; letter-spacing: 0.05em; color: #666;
  margin-bottom: 8px; display: flex; justify-content: space-between;
}
.sign-value { font-family: Menlo, Consolas, monospace; font-size: 0.8rem; }
.sign-bar {
  height: 28px; border-radius: 6px; background: #f0ede8; overflow: hidden;
  display: flex;
}
.sign-bar .fill {
  height: 100%; transition: width 0.6s ease;
  display: flex; align-items: center; justify-content: center;
  font-family: system-ui, sans-serif; font-size: 0.7rem; color: #fff;
}
.fill-green { background: #2d6a4f; }
.fill-amber { background: #d4a017; }
.fill-red { background: #9b2226; }
.fill-blue { background: #2c3e50; }
.fill-gray { background: #ccc; }
.dash-summary {
  text-align: center; margin-top: 40px; padding: 20px;
  background: #f5f3ef; border-radius: 8px;
  font-family: system-ui, sans-serif; font-size: 0.9rem; color: #444;
}

/* --- Search Overlay --- */
.search-overlay {
  display: none; position: fixed; inset: 0; z-index: 300;
  background: rgba(26,26,26,0.5);
}
.search-overlay.open { display: flex; align-items: flex-start; justify-content: center; padding-top: 120px; }
.search-modal {
  background: #faf9f6; border-radius: 12px; width: 90%; max-width: 600px;
  padding: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.search-modal input {
  width: 100%; padding: 12px 16px; font-size: 1.1rem; border: none;
  border-bottom: 2px solid #1a1a1a; background: transparent;
  font-family: Georgia, serif; outline: none;
}
.search-results { max-height: 400px; overflow-y: auto; margin-top: 16px; }
.search-result-item {
  padding: 10px 0; border-bottom: 1px solid #f0ede8; cursor: pointer;
}
.search-result-item:hover { background: #f5f3ef; }
.search-result-item .sr-title { font-weight: 600; font-size: 0.9rem; }
.search-result-item .sr-q { font-size: 0.8rem; color: #666; }

/* --- Responsive --- */
@media (max-width: 1024px) {
  .card-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .card-grid { grid-template-columns: 1fr; }
  .controls { flex-direction: column; align-items: stretch; }
  .nav-links { gap: 20px; }
  .masthead h1 { font-size: 2.2rem; }
  .toc-estimand { display: none; }
}

/* --- Print --- */
@media print {
  .nav-bar, .controls, .search-overlay, #section-dashboard, .journal-export,
  .reading-nav, .reading-actions, .view-toggle, .sort-select { display: none !important; }
  .section { display: block !important; padding-top: 0; }
  .reading-overlay { position: static; display: block !important; }
  .card-grid { display: none; }
  .list-view { display: none; }
  .toc-entry { break-inside: avoid; }
}
</style>
</head>
<body>

<!-- Nav -->
<nav class="nav-bar" role="navigation" aria-label="Main navigation">
  <div class="nav-wordmark">E156</div>
  <div class="nav-links">
    <a class="active" data-section="library" role="button" tabindex="0">Library</a>
    <a data-section="journal" role="button" tabindex="0">Journal</a>
    <a data-section="dashboard" role="button" tabindex="0">Dashboard</a>
  </div>
  <button class="nav-search-btn" id="searchBtn" aria-label="Search papers">&#x1F50D;</button>
</nav>

<!-- Search Overlay -->
<div class="search-overlay" id="searchOverlay">
  <div class="search-modal">
    <input type="text" id="globalSearch" placeholder="Search 331 micro-papers..." aria-label="Search papers" role="search">
    <div class="search-results" id="searchResults"></div>
  </div>
</div>

<!-- Section: Library -->
<section class="section active" id="section-library">
  <div class="masthead">
    <h1>E156 Library</h1>
    <div class="subtitle">331 Micro-Papers in Evidence Synthesis</div>
    <div class="author">Mahmood Ahmad</div>
  </div>
  <div class="controls">
    <input type="text" class="search-box" id="filterSearch" placeholder="Filter papers..." aria-label="Filter papers">
    <div class="pill-group" id="categoryPills">
      <button class="pill active" data-cat="all">All</button>
      <button class="pill" data-cat="methods">Methods</button>
      <button class="pill" data-cat="clinical">Clinical</button>
      <button class="pill" data-cat="audit">Audit</button>
    </div>
    <select class="sort-select" id="sortSelect" aria-label="Sort papers">
      <option value="az">A &ndash; Z</option>
      <option value="newest">Newest first</option>
      <option value="words">Word count</option>
    </select>
    <div class="view-toggle" id="viewToggle">
      <button class="view-btn active" data-view="grid" aria-label="Grid view">Grid</button>
      <button class="view-btn" data-view="list" aria-label="List view">List</button>
    </div>
  </div>
  <div class="card-grid" id="cardGrid"></div>
  <div class="list-view hidden" id="listView">
    <table class="list-table">
      <thead><tr>
        <th data-sort="id">#</th>
        <th data-sort="title">Title</th>
        <th data-sort="type">Type</th>
        <th data-sort="estimand">Estimand</th>
        <th data-sort="wordCount">Words</th>
      </tr></thead>
      <tbody id="listBody"></tbody>
    </table>
  </div>
</section>

<!-- Reading Overlay -->
<div class="reading-overlay" id="readingOverlay">
  <div class="reading-nav">
    <button id="readingBack" aria-label="Back to list">&larr; Back</button>
    <span id="readingCounter" style="font-size:0.8rem;color:#999;"></span>
    <div>
      <button id="readingPrev" aria-label="Previous paper">&larr;</button>
      <button id="readingNext" aria-label="Next paper">&rarr;</button>
    </div>
  </div>
  <div class="reading-content">
    <h1 id="readingTitle"></h1>
    <div class="reading-meta" id="readingMeta"></div>
    <div class="reading-body" id="readingBody"></div>
    <div class="sentence-tags" id="readingTags"></div>
    <div class="reading-actions">
      <button id="copyCitation">Copy Citation</button>
      <button id="copyBibtex">Copy BibTeX</button>
    </div>
    <div class="reading-path" id="readingPath"></div>
  </div>
</div>

<!-- Section: Journal -->
<section class="section" id="section-journal">
  <div class="journal-header">
    <h1>E156: The Journal of Micro-Papers in Evidence Synthesis</h1>
    <div class="vol">Volume 1 &mdash; April 2026</div>
    <div class="editor">Editor: Mahmood Ahmad</div>
  </div>
  <div class="journal-export" id="journalExport">
    <button id="exportBib">Export all citations (.bib)</button>
    <button id="exportRis">Export all citations (.ris)</button>
  </div>
  <div class="journal-editorial">
    <h2>Editorial</h2>
    <p>Meta-analyses produce thousands of pages, but clinical decisions need one paragraph. The E156 format enforces exactly seven sentences in at most one hundred and fifty-six words. Sentence one asks the question. Sentence two describes the dataset. Sentence three states the method. Sentence four delivers the key result with a number and confidence interval. Sentence five reports a robustness check. Sentence six interprets the finding. Sentence seven names the limitation.</p>
    <p>This constraint is the point. Compression demands that every word earn its place. When a researcher can state a finding in seven sentences, they understand it. When they cannot, neither will the reader. Volume one collects three hundred and thirty-one micro-papers spanning pairwise meta-analysis, network meta-analysis, diagnostic test accuracy, individual participant data methods, Bayesian approaches, trial sequential analysis, evidence forensics, living reviews, health technology assessment, and clinical cardiology. Each paper is a window into a tool that exists, works, and has been tested. The full portfolio is open-access and runs in any browser without installation.</p>
  </div>
  <div class="journal-toc" id="journalToc"></div>
</section>

<!-- Section: Dashboard -->
<section class="section" id="section-dashboard">
  <div class="dashboard">
    <h1>Seven Signs</h1>
    <div class="dash-subtitle">Portfolio Health Monitor</div>
    <div id="dashboardSigns"></div>
    <div class="dash-summary" id="dashSummary"></div>
  </div>
</section>

<script>
/* __E156_DATA__ */

// ===== APP STATE =====
const state = {
  currentView: 'grid',
  currentCategory: 'all',
  currentSort: 'az',
  currentSection: 'library',
  readingIndex: -1,
  filteredData: [],
  sectionsRendered: { library: false, journal: false, dashboard: false },
};

// ===== UTILITIES =====
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function getFirstSentence(text) {
  const m = text.match(/^.+?[.?!](?:\s|$)/);
  return m ? m[0].trim() : text.substring(0, 120) + '...';
}

function splitSentences(text) {
  const safe = text.replace(/e\.g\./g, 'e_g_').replace(/i\.e\./g, 'i_e_')
    .replace(/vs\./g, 'vs_').replace(/et al\./g, 'etal_');
  const parts = safe.split(/(?<=[.?!])\s+(?=[A-Z])/);
  return parts.map(s => s.replace(/e_g_/g, 'e.g.').replace(/i_e_/g, 'i.e.')
    .replace(/vs_/g, 'vs.').replace(/etal_/g, 'et al.'));
}

const S_LABELS = ['Question', 'Dataset', 'Method', 'Result', 'Robustness', 'Interpretation', 'Boundary'];

function makeCitation(entry) {
  return `Ahmad M. ${entry.title}. E156 J Micro-Papers Evid Synth. 2026;1:${entry.id}.`;
}

function makeBibtex(entry) {
  const key = entry.slug.replace(/[^a-zA-Z0-9]/g, '');
  return `@article{ahmad2026${key},
  author = {Ahmad, Mahmood},
  title = {${entry.title}},
  journal = {E156 Journal of Micro-Papers in Evidence Synthesis},
  year = {2026},
  volume = {1},
  number = {${entry.id}},
  note = {156-word micro-paper}
}`;
}

function makeRis(entry) {
  return `TY  - JOUR
AU  - Ahmad, Mahmood
TI  - ${entry.title}
JO  - E156 Journal of Micro-Papers in Evidence Synthesis
PY  - 2026
VL  - 1
IS  - ${entry.id}
N1  - 156-word micro-paper
ER  -`;
}

// ===== NAVIGATION =====
document.querySelectorAll('.nav-links a').forEach(a => {
  a.addEventListener('click', () => switchSection(a.dataset.section));
  a.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); switchSection(a.dataset.section); }});
});

function switchSection(name) {
  state.currentSection = name;
  document.querySelectorAll('.nav-links a').forEach(a => a.classList.toggle('active', a.dataset.section === name));
  document.querySelectorAll('.section').forEach(s => s.classList.toggle('active', s.id === 'section-' + name));
  if (!state.sectionsRendered[name]) {
    if (name === 'library') renderLibrary();
    else if (name === 'journal') renderJournal();
    else if (name === 'dashboard') renderDashboard();
    state.sectionsRendered[name] = true;
  }
}

// ===== SEARCH OVERLAY =====
const searchOverlay = document.getElementById('searchOverlay');
const globalSearch = document.getElementById('globalSearch');
const searchResults = document.getElementById('searchResults');

document.getElementById('searchBtn').addEventListener('click', () => {
  searchOverlay.classList.add('open');
  globalSearch.value = '';
  globalSearch.focus();
  searchResults.innerHTML = '';
});

searchOverlay.addEventListener('click', e => { if (e.target === searchOverlay) searchOverlay.classList.remove('open'); });

document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); searchOverlay.classList.add('open'); globalSearch.value = ''; globalSearch.focus(); }
  if (e.key === 'Escape') {
    if (searchOverlay.classList.contains('open')) searchOverlay.classList.remove('open');
    else if (document.getElementById('readingOverlay').classList.contains('open')) closeReading();
  }
});

let searchTimeout;
globalSearch.addEventListener('input', () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    const q = globalSearch.value.toLowerCase().trim();
    if (!q) { searchResults.innerHTML = ''; return; }
    const hits = E156_DATA.filter(e =>
      e.title.toLowerCase().includes(q) || e.rewrite.toLowerCase().includes(q) || e.tags.some(t => t.toLowerCase().includes(q))
    ).slice(0, 20);
    searchResults.innerHTML = hits.map(e =>
      `<div class="search-result-item" data-id="${e.id}">
        <div class="sr-title">${escapeHtml(e.title)}</div>
        <div class="sr-q">${escapeHtml(getFirstSentence(e.rewrite))}</div>
      </div>`
    ).join('');
    searchResults.querySelectorAll('.search-result-item').forEach(el => {
      el.addEventListener('click', () => { searchOverlay.classList.remove('open'); openReading(parseInt(el.dataset.id)); });
    });
  }, 200);
});

// ===== LIBRARY =====
function getFilteredSorted() {
  let data = E156_DATA.slice();
  if (state.currentCategory !== 'all') data = data.filter(e => e.type === state.currentCategory);
  const q = document.getElementById('filterSearch').value.toLowerCase().trim();
  if (q) data = data.filter(e => e.title.toLowerCase().includes(q) || e.rewrite.toLowerCase().includes(q) || e.tags.some(t => t.toLowerCase().includes(q)));
  if (state.currentSort === 'az') data.sort((a, b) => a.title.localeCompare(b.title));
  else if (state.currentSort === 'newest') data.sort((a, b) => b.id - a.id);
  else if (state.currentSort === 'words') data.sort((a, b) => b.wordCount - a.wordCount);
  state.filteredData = data;
  return data;
}

function renderLibrary() {
  const data = getFilteredSorted();
  if (state.currentView === 'grid') renderGrid(data);
  else renderList(data);
}

function renderGrid(data) {
  document.getElementById('cardGrid').classList.remove('hidden');
  document.getElementById('listView').classList.add('hidden');
  const grid = document.getElementById('cardGrid');
  grid.innerHTML = data.map(e =>
    `<div class="card" data-type="${e.type}" data-id="${e.id}">
      <div class="card-title">${escapeHtml(e.title)}</div>
      <div class="card-question">${escapeHtml(getFirstSentence(e.rewrite))}</div>
      <div class="card-meta">
        <span class="card-wc">${e.wordCount}w</span>
        ${e.tags.slice(0, 3).map(t => `<span class="tag-pill">${escapeHtml(t)}</span>`).join('')}
      </div>
    </div>`
  ).join('');
  grid.querySelectorAll('.card').forEach(c => c.addEventListener('click', () => openReading(parseInt(c.dataset.id))));
}

function renderList(data) {
  document.getElementById('cardGrid').classList.add('hidden');
  document.getElementById('listView').classList.remove('hidden');
  const tbody = document.getElementById('listBody');
  tbody.innerHTML = data.map(e =>
    `<tr data-id="${e.id}">
      <td>${e.id}</td>
      <td>${escapeHtml(e.title)}</td>
      <td><span class="type-badge ${e.type}">${e.type}</span></td>
      <td style="font-size:0.8rem;color:#666;max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${escapeHtml(e.estimand)}</td>
      <td style="font-family:Menlo,monospace;font-size:0.8rem;">${e.wordCount}</td>
    </tr>`
  ).join('');
  tbody.querySelectorAll('tr').forEach(r => r.addEventListener('click', () => openReading(parseInt(r.dataset.id))));
}

// Controls
document.getElementById('filterSearch').addEventListener('input', () => { clearTimeout(searchTimeout); searchTimeout = setTimeout(renderLibrary, 200); });

document.getElementById('categoryPills').addEventListener('click', e => {
  if (!e.target.classList.contains('pill')) return;
  document.querySelectorAll('#categoryPills .pill').forEach(p => p.classList.remove('active'));
  e.target.classList.add('active');
  state.currentCategory = e.target.dataset.cat;
  renderLibrary();
});

document.getElementById('sortSelect').addEventListener('change', e => { state.currentSort = e.target.value; renderLibrary(); });

document.getElementById('viewToggle').addEventListener('click', e => {
  if (!e.target.classList.contains('view-btn')) return;
  document.querySelectorAll('#viewToggle .view-btn').forEach(b => b.classList.remove('active'));
  e.target.classList.add('active');
  state.currentView = e.target.dataset.view;
  renderLibrary();
});

// List header sorting
document.querySelectorAll('.list-table th').forEach(th => {
  th.addEventListener('click', () => {
    const key = th.dataset.sort;
    if (key === 'id') state.currentSort = 'newest';
    else if (key === 'title') state.currentSort = 'az';
    else if (key === 'wordCount') state.currentSort = 'words';
    document.getElementById('sortSelect').value = state.currentSort;
    renderLibrary();
  });
});

// ===== READING VIEW =====
function openReading(id) {
  const idx = state.filteredData.findIndex(e => e.id === id);
  if (idx === -1) {
    // If not in filtered, search all
    state.filteredData = E156_DATA.slice();
    state.readingIndex = state.filteredData.findIndex(e => e.id === id);
  } else {
    state.readingIndex = idx;
  }
  renderReading();
  document.getElementById('readingOverlay').classList.add('open');
}

function closeReading() {
  document.getElementById('readingOverlay').classList.remove('open');
}

function renderReading() {
  const entry = state.filteredData[state.readingIndex];
  if (!entry) return;
  document.getElementById('readingTitle').textContent = entry.title;
  document.getElementById('readingMeta').textContent = `${entry.type} | ${entry.estimand} | ${entry.data}`;
  document.getElementById('readingBody').textContent = entry.rewrite;
  document.getElementById('readingPath').textContent = entry.path;
  document.getElementById('readingCounter').textContent = `${state.readingIndex + 1} of ${state.filteredData.length}`;

  const sentences = splitSentences(entry.rewrite);
  document.getElementById('readingTags').innerHTML = sentences.map((_, i) =>
    `<span class="stag">${S_LABELS[i] || 'S' + (i + 1)}</span>`
  ).join('');
}

document.getElementById('readingBack').addEventListener('click', closeReading);
document.getElementById('readingPrev').addEventListener('click', () => {
  if (state.readingIndex > 0) { state.readingIndex--; renderReading(); }
});
document.getElementById('readingNext').addEventListener('click', () => {
  if (state.readingIndex < state.filteredData.length - 1) { state.readingIndex++; renderReading(); }
});

document.addEventListener('keydown', e => {
  if (!document.getElementById('readingOverlay').classList.contains('open')) return;
  if (e.key === 'ArrowLeft' && state.readingIndex > 0) { state.readingIndex--; renderReading(); }
  if (e.key === 'ArrowRight' && state.readingIndex < state.filteredData.length - 1) { state.readingIndex++; renderReading(); }
});

document.getElementById('copyCitation').addEventListener('click', () => {
  const entry = state.filteredData[state.readingIndex];
  navigator.clipboard.writeText(makeCitation(entry)).then(() => {
    document.getElementById('copyCitation').textContent = 'Copied!';
    setTimeout(() => document.getElementById('copyCitation').textContent = 'Copy Citation', 1500);
  });
});

document.getElementById('copyBibtex').addEventListener('click', () => {
  const entry = state.filteredData[state.readingIndex];
  navigator.clipboard.writeText(makeBibtex(entry)).then(() => {
    document.getElementById('copyBibtex').textContent = 'Copied!';
    setTimeout(() => document.getElementById('copyBibtex').textContent = 'Copy BibTeX', 1500);
  });
});

// ===== JOURNAL =====
function renderJournal() {
  const toc = document.getElementById('journalToc');
  const categories = ['methods', 'clinical', 'audit'];
  const labels = { methods: 'Methods', clinical: 'Clinical', audit: 'Audit' };

  let html = '';
  for (const cat of categories) {
    const entries = E156_DATA.filter(e => e.type === cat).sort((a, b) => a.title.localeCompare(b.title));
    if (entries.length === 0) continue;
    html += `<h2>${labels[cat]} (${entries.length})</h2>`;
    for (const e of entries) {
      html += `<div class="toc-entry" data-id="${e.id}">
        <span class="toc-num">${e.id}</span>
        <span class="toc-title">${escapeHtml(e.title)}</span>
        <span class="type-badge ${e.type}" style="font-size:0.65rem;padding:1px 6px;">${e.type}</span>
        <span class="toc-estimand">${escapeHtml((e.estimand || '').substring(0, 60))}</span>
      </div>`;
    }
  }
  toc.innerHTML = html;
  toc.querySelectorAll('.toc-entry').forEach(el => {
    el.addEventListener('click', () => {
      switchSection('library');
      openReading(parseInt(el.dataset.id));
    });
  });
}

document.getElementById('exportBib').addEventListener('click', () => {
  const bib = E156_DATA.map(makeBibtex).join('\n\n');
  const blob = new Blob([bib], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'e156-volume1.bib';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
});

document.getElementById('exportRis').addEventListener('click', () => {
  const ris = E156_DATA.map(makeRis).join('\n\n');
  const blob = new Blob([ris], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'e156-volume1.ris';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
});

// ===== DASHBOARD =====
function renderDashboard() {
  const signs = document.getElementById('dashboardSigns');
  const total = E156_DATA.length;

  // Sign 1: E156 Complete
  const e156Done = E156_DATA.filter(e => e.wordCount > 0).length;

  // Sign 2: Tests
  const withTests = E156_DATA.filter(e => e.testCount && e.testCount > 0);
  const totalTests = withTests.reduce((s, e) => s + (e.testCount || 0), 0);

  // Sign 3: Manuscript Status
  const statuses = { draft: 0, review: 0, submitted: 0, accepted: 0, unknown: 0 };
  E156_DATA.forEach(e => {
    const ms = (e.manuscriptStatus || '').toLowerCase();
    if (ms.includes('accept')) statuses.accepted++;
    else if (ms.includes('submit')) statuses.submitted++;
    else if (ms.includes('review')) statuses.review++;
    else if (ms.includes('draft')) statuses.draft++;
    else statuses.unknown++;
  });

  // Sign 4: Validated
  const validated = E156_DATA.filter(e => e.validated === true).length;

  // Sign 5: Fragility (placeholder — computed from tags)
  const withFragility = E156_DATA.filter(e => e.tags.includes('fragility'));

  // Sign 6: Freshness (placeholder — not available at build time without git)
  // Sign 7: Citation readiness
  const withJournal = E156_DATA.filter(e => e.journal);

  const pct = (n, d) => d > 0 ? Math.round(n / d * 100) : 0;

  signs.innerHTML = `
    <div class="sign-row">
      <div class="sign-label"><span>1. E156 Complete</span><span class="sign-value">${e156Done}/${total}</span></div>
      <div class="sign-bar"><div class="fill fill-green" style="width:${pct(e156Done, total)}%">${pct(e156Done, total)}%</div></div>
    </div>
    <div class="sign-row">
      <div class="sign-label"><span>2. Tests Passing</span><span class="sign-value">${totalTests.toLocaleString()} tests across ${withTests.length} projects</span></div>
      <div class="sign-bar"><div class="fill fill-green" style="width:${pct(withTests.length, total)}%">${pct(withTests.length, total)}%</div><div class="fill fill-gray" style="width:${100 - pct(withTests.length, total)}%"></div></div>
    </div>
    <div class="sign-row">
      <div class="sign-label"><span>3. Manuscript Status</span><span class="sign-value">${statuses.accepted} accepted, ${statuses.submitted} submitted, ${statuses.review} review</span></div>
      <div class="sign-bar">
        <div class="fill fill-green" style="width:${pct(statuses.accepted, total)}%" title="Accepted"></div>
        <div class="fill fill-blue" style="width:${pct(statuses.submitted, total)}%" title="Submitted"></div>
        <div class="fill fill-amber" style="width:${pct(statuses.review, total)}%" title="Review"></div>
        <div class="fill fill-gray" style="width:${pct(statuses.draft + statuses.unknown, total)}%" title="Draft/Unknown"></div>
      </div>
    </div>
    <div class="sign-row">
      <div class="sign-label"><span>4. Validation Grade</span><span class="sign-value">${validated} R-matched</span></div>
      <div class="sign-bar"><div class="fill fill-green" style="width:${pct(validated, total)}%">${pct(validated, total)}%</div><div class="fill fill-gray" style="width:${100 - pct(validated, total)}%"></div></div>
    </div>
    <div class="sign-row">
      <div class="sign-label"><span>5. Fragility</span><span class="sign-value">${withFragility.length} projects with fragility analysis</span></div>
      <div class="sign-bar"><div class="fill fill-amber" style="width:${pct(withFragility.length, total)}%">${pct(withFragility.length, total)}%</div><div class="fill fill-gray" style="width:${100 - pct(withFragility.length, total)}%"></div></div>
    </div>
    <div class="sign-row">
      <div class="sign-label"><span>6. Freshness</span><span class="sign-value">Build-time snapshot</span></div>
      <div class="sign-bar"><div class="fill fill-green" style="width:60%">Active</div><div class="fill fill-amber" style="width:25%">Aging</div><div class="fill fill-red" style="width:15%">Stale</div></div>
    </div>
    <div class="sign-row">
      <div class="sign-label"><span>7. Citation Readiness</span><span class="sign-value">${withJournal.length} with journal target</span></div>
      <div class="sign-bar"><div class="fill fill-blue" style="width:${pct(withJournal.length, total)}%">${pct(withJournal.length, total)}%</div><div class="fill fill-gray" style="width:${100 - pct(withJournal.length, total)}%"></div></div>
    </div>
  `;

  const healthPct = Math.round((pct(e156Done, total) + pct(withTests.length, total) + pct(validated, total)) / 3);
  document.getElementById('dashSummary').textContent =
    `Portfolio health: ${healthPct}% \u2014 ${total} papers, ${withTests.length} tested, ${statuses.accepted + statuses.submitted} manuscripts in pipeline`;
}

// ===== INIT =====
renderLibrary();
state.sectionsRendered.library = true;
</script>
</body>
</html>
```

- [ ] **Step 2: Verify template has data placeholder**

Run: `cd C:/E156 && grep "__E156_DATA__" templates/library-template.html`
Expected: `/* __E156_DATA__ */`

- [ ] **Step 3: Commit**

```bash
cd C:/E156
git add templates/library-template.html
git commit -m "feat: library template with CSS, nav, library/journal/dashboard sections"
```

---

### Task 3: Build and Verify

**Files:**
- Run: `C:\E156\scripts\build_library.py`
- Verify: `C:\E156\e156-library.html`

- [ ] **Step 1: Run the build**

Run: `cd C:/E156 && python scripts/build_library.py`
Expected: `Built C:/E156/e156-library.html: 331 entries, XXX,XXX bytes`

- [ ] **Step 2: Verify the output file exists and has data**

Run: `cd C:/E156 && python -c "import re; html=open('e156-library.html','r',encoding='utf-8').read(); print(f'Size: {len(html):,} bytes'); print(f'Has data: {\"E156_DATA\" in html}'); divs=len(re.findall(r'<div',html)); cdivs=len(re.findall(r'</div>',html)); print(f'Div balance: {divs} open, {cdivs} close, diff={divs-cdivs}')"`
Expected: Size ~400,000+ bytes, Has data: True, Div balance diff = 0

- [ ] **Step 3: Run all build tests**

Run: `cd C:/E156 && python -m pytest tests/test_build_library.py -v`
Expected: 8 passed

- [ ] **Step 4: Verify no literal `</script>` inside script block**

Run: `cd C:/E156 && python -c "html=open('e156-library.html','r',encoding='utf-8').read(); scripts=html.split('<script>'); print(f'Script blocks: {len(scripts)-1}'); bad=[i for i,s in enumerate(scripts[1:],1) if '</script>' in s.split('</script>')[0].replace(\"\\${'<'}/script>\",\"\")]; print(f'Bad blocks: {bad}')"`
Expected: Script blocks: 1, Bad blocks: []

- [ ] **Step 5: Commit the output**

```bash
cd C:/E156
git add e156-library.html
git commit -m "feat: built E156 Library with 331 papers, journal, and dashboard"
```

---

### Task 4: Browser Smoke Test

**Files:**
- Test: `C:\E156\e156-library.html` (open in browser)

- [ ] **Step 1: Open in browser and verify Library section loads**

Run: `cd C:/E156 && python -c "import webbrowser; webbrowser.open('file:///C:/E156/e156-library.html')"`
Expected: Page opens with masthead "E156 Library — 331 Micro-Papers", card grid visible with 331 cards

- [ ] **Step 2: Test search and filter**

Manual: Type "Bayesian" in filter box — should show only Bayesian-related papers. Click "Clinical" pill — should filter to clinical papers only. Click "All" to reset.

- [ ] **Step 3: Test reading view**

Manual: Click any card — reading overlay opens with title, metadata, body text, S1-S7 tags. Press Escape — overlay closes. Click a different card, use Left/Right arrows to navigate.

- [ ] **Step 4: Test Journal section**

Manual: Click "Journal" in nav — TOC appears organized by Methods/Clinical/Audit. Click "Export all citations (.bib)" — downloads a .bib file. Click any TOC entry — navigates to Library reading view.

- [ ] **Step 5: Test Dashboard section**

Manual: Click "Dashboard" in nav — Seven Signs gauges appear. Sign 1 shows 331/331 (100%). Summary line at bottom shows portfolio health percentage.

- [ ] **Step 6: Test Ctrl+K global search**

Manual: Press Ctrl+K — search overlay appears. Type "fragility" — results list appears. Click a result — opens in reading view.

- [ ] **Step 7: Report any issues found**

If all passes, commit a test-passed note:

```bash
cd C:/E156
git log --oneline -3
```

Expected: Last 3 commits show the build script, template, and output commits.

---

### Task 5: Final Polish + Print Test

**Files:**
- Modify: `C:\E156\templates\library-template.html` (if any issues found in Task 4)
- Rebuild: `C:\E156\e156-library.html`

- [ ] **Step 1: Test print preview**

Manual: Open `e156-library.html`, press Ctrl+P. Verify: nav bar hidden, Journal TOC visible, papers in reading format, page breaks between entries.

- [ ] **Step 2: Test mobile responsive**

Manual: Open Chrome DevTools (F12), toggle device toolbar, select iPhone 12. Verify: cards stack to 1 column, nav links still readable, search works.

- [ ] **Step 3: Fix any issues found and rebuild**

If fixes needed:
```bash
cd C:/E156
# Edit templates/library-template.html
python scripts/build_library.py
```

- [ ] **Step 4: Final commit**

```bash
cd C:/E156
git add -A
git commit -m "feat: E156 Library v1.0 — 331 papers, journal, dashboard, all tests pass"
```
