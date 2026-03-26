# E156 Micro-Paper Tool Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-file HTML tool that showcases the E156 micro-paper format (Magazine mode) and provides a composer/validator (Workshop mode) with NYT editorial styling.

**Architecture:** Single HTML file (`index.html`) with all CSS and JS inline. Two DOM sections toggled via CSS classes. Vanilla JS for validation, localStorage persistence, and export. No build step, no dependencies.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript (ES2020+). No frameworks, no external fonts, no CDN dependencies.

**Spec:** `C:\E156\docs\superpowers\specs\2026-03-26-e156-design.md`

---

### Task 1: Create Example Micro-Papers (JSON)

Before building the HTML, we need the 3 example micro-papers that Magazine mode will display. Each must be exactly 7 sentences, exactly 156 words, following the E156 sentence schema.

**Files:**
- Create: `C:\E156\examples\fragility-atlas.json`
- Create: `C:\E156\examples\metarep.json`
- Create: `C:\E156\examples\clinical-ma.json`

- [ ] **Step 1: Write Fragility Atlas example**

```json
{
  "title": "Fragility of Cochrane Cardiovascular Meta-Analyses",
  "body": "...",
  "sentences": [
    { "role": "Question", "text": "..." },
    { "role": "Dataset", "text": "..." },
    { "role": "Method", "text": "..." },
    { "role": "Primary result", "text": "..." },
    { "role": "Robustness", "text": "..." },
    { "role": "Interpretation", "text": "..." },
    { "role": "Boundary", "text": "..." }
  ],
  "wordCount": 156,
  "sentenceCount": 7,
  "outsideNote": {
    "app": "https://fragility-atlas.example.org",
    "data": "Cochrane Library, 407 reviews",
    "code": "https://github.com/example/fragility-atlas",
    "doi": "",
    "version": "1.0",
    "date": "2026-03-26",
    "validationStatus": "DRAFT"
  },
  "meta": {
    "created": "2026-03-26",
    "valid": true,
    "schemaVersion": "0.1"
  }
}
```

Write the 156-word body for the Fragility Atlas. Topic: multiverse analysis of fragility across 407 Cochrane cardiovascular meta-analyses. The body paragraph must be exactly 156 words, 7 sentences, following the sentence schema. Use the word count algorithm from spec §3.7: `text.trim().split(/\s+/).filter(Boolean).length`.

- [ ] **Step 2: Write MetaRep example**

Same JSON structure. Topic: a novel replication probability method for meta-analyses. 156 words, 7 sentences.

- [ ] **Step 3: Write clinical MA example**

Same JSON structure. Topic: a clinical trial meta-analysis in cardiology (e.g., SGLT2 inhibitors and heart failure). 156 words, 7 sentences.

- [ ] **Step 4: Validate all three examples**

For each JSON file, verify:
- `body` field is exactly 156 words (use the algorithm)
- `body` splits into exactly 7 sentences (use the sentence detection algorithm from spec §3.6)
- `sentences` array has 7 entries matching the roles
- JSON is valid

Run: open each JSON in a text editor or use `python -c "import json; d=json.load(open('examples/fragility-atlas.json')); print(len(d['body'].strip().split()))"` for each.

- [ ] **Step 5: Commit**

```bash
cd /c/E156
git add examples/
git commit -m "content: add 3 example E156 micro-papers (fragility, metarep, clinical)"
```

---

### Task 2: HTML Skeleton + CSS Foundation

Build the HTML structure for both modes and all the CSS. No JS yet — just the static layout.

**Files:**
- Create: `C:\E156\index.html`

- [ ] **Step 1: Write the HTML skeleton**

Create `index.html` with:
- `<!DOCTYPE html>`, charset UTF-8, viewport meta, `<title>E156 — The Micro-Paper Standard</title>`
- Skip link: `<a href="#composer" class="skip-link">Skip to composer</a>`
- `<div id="magazine-mode">` — all Magazine mode content
- `<div id="workshop-mode" class="hidden">` — all Workshop mode content
- Both modes exist in DOM simultaneously; only one is visible

Magazine mode structure:
```html
<div id="magazine-mode">
  <header class="masthead">
    <h1>E156</h1>
    <p class="subtitle">The micro-paper standard</p>
  </header>
  <section class="argument"><!-- ~150 words editorial pitch --></section>
  <section class="examples">
    <div class="example-card" data-example="fragility-atlas">
      <h3 class="example-title"></h3>
      <blockquote class="micro-paper-body"></blockquote>
      <div class="sentence-annotations"></div>
    </div>
    <!-- repeat for metarep, clinical-ma (each has .example-title, .micro-paper-body, .sentence-annotations) -->
  </section>
  <section class="rules"><!-- sentence schema + house style --></section>
  <section class="prompt-shell">
    <details>
      <summary>Prompt shell for LLMs</summary>
      <pre><!-- prompt text from spec.md --><button class="copy-prompt">Copy</button></pre>
    </details>
  </section>
  <div class="cta">
    <button id="btn-write" aria-label="Open the E156 composer">Write one &rarr;</button>
  </div>
</div>
```

Workshop mode structure:
```html
<div id="workshop-mode" class="hidden">
  <nav class="workshop-nav">
    <a href="#" id="btn-back" aria-label="Return to E156 showcase">&larr; Back to E156</a>
  </nav>
  <div class="workshop-layout">
    <div class="editor-panel">
      <textarea id="body-input" aria-label="Micro-paper body"
        placeholder="S1: State the question...&#10;S2: Describe the evidence base...&#10;S3: State the method...&#10;S4: Report the primary result with interval...&#10;S5: Report robustness or heterogeneity...&#10;S6: Give a restrained interpretation...&#10;S7: State a limitation or boundary..."></textarea>
      <details id="outside-note-toggle">
        <summary>Add outside note block</summary>
        <div class="outside-note-fields">
          <label>App <input type="text" id="note-app"></label>
          <label>Data <input type="text" id="note-data"></label>
          <label>Code <input type="text" id="note-code"></label>
          <label>DOI <input type="text" id="note-doi"></label>
          <label>Version <input type="text" id="note-version"></label>
          <label>Date <input type="date" id="note-date"></label>
          <label>Validation Status <input type="text" id="note-validation" placeholder="PASS / DRAFT / PENDING"></label>
        </div>
      </details>
      <div class="export-bar">
        <button id="btn-copy" disabled title="Write something first">Copy Body</button>
        <button id="btn-md" disabled title="Write something first">Download .md</button>
        <button id="btn-json" disabled title="Write something first">Download .json</button>
        <button id="btn-print" disabled title="Write something first">Print View</button>
        <button id="btn-clear" class="btn-danger">Clear Draft</button>
      </div>
    </div>
    <aside class="validation-panel" aria-live="polite">
      <div class="counter word-counter"><span id="word-count">0</span>/156</div>
      <div class="counter sentence-counter"><span id="sentence-count">0</span>/7</div>
      <div id="sentence-map" class="sentence-map"></div>
      <ul id="style-checks" class="style-checks"></ul>
      <div id="causal-warning" class="causal-warning hidden"></div>
      <div id="status-badge" role="status" class="status-badge empty">EMPTY</div>
    </aside>
  </div>
</div>
```

- [ ] **Step 2: Write all CSS**

Inside a single `<style>` block at the top of `<head>`. Key rules:

```css
/* -- Reset & base -- */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: Georgia, Charter, 'Times New Roman', serif;
  background: #faf9f6;
  color: #1a1a1a;
  line-height: 1.75;
  -webkit-font-smoothing: antialiased;
}

/* -- Skip link -- */
.skip-link {
  position: absolute; top: -40px; left: 0;
  background: #1a1a1a; color: #faf9f6; padding: 8px 16px;
  z-index: 100; transition: top 0.2s;
}
.skip-link:focus { top: 0; }

/* -- Centered column (NYT width) -- */
.masthead, .argument, .examples, .rules, .prompt-shell, .cta {
  max-width: 680px; margin: 0 auto; padding: 0 24px;
}

/* -- Masthead -- */
.masthead { text-align: center; padding-top: 80px; padding-bottom: 40px; }
.masthead h1 { font-size: 4rem; font-weight: 700; letter-spacing: -0.02em; }
.masthead .subtitle { font-size: 1.25rem; color: #666; font-style: italic; margin-top: 8px; }

/* -- Argument section -- */
.argument p { font-size: 1.1rem; margin-bottom: 16px; }

/* -- Rules section -- */
.rules ol { padding-left: 24px; margin: 16px 0; }
.rules li { margin-bottom: 8px; }
.rules p { margin-top: 16px; }

/* -- Example cards -- */
.example-title { font-size: 1rem; font-weight: 600; margin-bottom: 12px; color: #444; font-family: system-ui, sans-serif; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.8rem; }
.example-card { border-left: 3px solid #1a1a1a; padding: 24px 32px; margin: 40px 0; }
.micro-paper-body { font-size: 1.1rem; line-height: 1.8; font-style: normal; }
.sentence-annotations { margin-top: 16px; display: flex; flex-wrap: wrap; gap: 8px; }
.sentence-annotations .tag {
  font-size: 0.75rem; padding: 2px 8px; border-radius: 3px;
  background: #f0ede8; color: #666; font-family: system-ui, sans-serif;
}

/* -- CTA button -- */
.cta { text-align: center; padding: 60px 0; }
.cta button {
  font-family: Georgia, serif; font-size: 1.1rem;
  background: #1a1a1a; color: #faf9f6;
  border: none; padding: 14px 36px; cursor: pointer;
  transition: background 0.2s;
}
.cta button:hover { background: #333; }
.cta button:focus-visible { outline: 2px solid #1a1a1a; outline-offset: 3px; }

/* -- Mode switching -- */
.hidden { display: none; }
.fade-in { animation: fadeIn 0.3s ease-in; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

/* -- Workshop layout -- */
.workshop-nav { max-width: 1100px; margin: 0 auto; padding: 16px 24px; }
.workshop-nav a { color: #1a1a1a; text-decoration: none; font-size: 0.95rem; }
.workshop-nav a:hover { text-decoration: underline; }
.workshop-layout {
  max-width: 1100px; margin: 0 auto; padding: 0 24px;
  display: flex; gap: 32px;
}
.editor-panel { flex: 3; }
.validation-panel { flex: 2; position: sticky; top: 24px; align-self: flex-start; }

/* -- Textarea -- */
#body-input {
  width: 100%; min-height: 280px; padding: 20px;
  font-family: Georgia, serif; font-size: 1.05rem; line-height: 1.75;
  border: 1px solid #ddd; background: #fff; resize: vertical;
  border-radius: 2px;
}
#body-input:focus { outline: 2px solid #1a1a1a; outline-offset: 1px; border-color: transparent; }
#body-input::placeholder { color: #bbb; }

/* -- Outside note block -- */
.outside-note-fields { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 12px; }
.outside-note-fields label {
  display: flex; flex-direction: column; font-size: 0.85rem;
  font-family: system-ui, sans-serif; color: #666;
}
.outside-note-fields input {
  margin-top: 4px; padding: 8px; border: 1px solid #ddd;
  font-family: Georgia, serif; font-size: 0.95rem;
}

/* -- Export bar -- */
.export-bar { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; }
.export-bar button {
  font-family: Georgia, serif; font-size: 0.9rem;
  background: #fff; color: #1a1a1a; border: 1px solid #ccc;
  padding: 8px 16px; cursor: pointer; transition: background 0.15s;
}
.export-bar button:hover:not(:disabled) { background: #f0ede8; }
.export-bar button:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-danger { color: #c62828 !important; border-color: #c62828 !important; }

/* -- Validation panel -- */
.counter { font-size: 2rem; font-weight: 700; font-family: system-ui, sans-serif; margin-bottom: 8px; }
.counter.valid { color: #2e7d32; }
.counter.invalid { color: #c62828; }
.sentence-map { margin: 16px 0; }
.sentence-map .role-tag {
  display: inline-block; font-size: 0.8rem; padding: 3px 10px;
  margin: 3px 4px 3px 0; border-radius: 3px;
  font-family: system-ui, sans-serif;
}
.style-checks { list-style: none; margin: 16px 0; }
.style-checks li { font-size: 0.9rem; font-family: system-ui, sans-serif; padding: 4px 0; }
.style-checks .pass::before { content: "\2713 "; color: #2e7d32; }
.style-checks .fail::before { content: "\2717 "; color: #c62828; }
.causal-warning {
  background: #fff3e0; border-left: 3px solid #e65100;
  padding: 8px 12px; margin: 12px 0; font-size: 0.85rem;
  font-family: system-ui, sans-serif; color: #e65100;
}
.status-badge {
  display: inline-block; padding: 6px 16px; border-radius: 3px;
  font-size: 0.9rem; font-weight: 700; font-family: system-ui, sans-serif;
  margin-top: 16px;
}
.status-badge.empty { background: #eee; color: #999; }
.status-badge.draft { background: #fff3e0; color: #e65100; }
.status-badge.valid { background: #e8f5e9; color: #2e7d32; }

/* -- Toast notification -- */
.toast {
  position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
  background: #1a1a1a; color: #faf9f6; padding: 10px 24px;
  border-radius: 4px; font-family: system-ui, sans-serif; font-size: 0.9rem;
  z-index: 1000; animation: toastIn 0.3s ease, toastOut 0.3s ease 1.7s forwards;
}
@keyframes toastIn { from { opacity: 0; transform: translateX(-50%) translateY(20px); } }
@keyframes toastOut { to { opacity: 0; transform: translateX(-50%) translateY(20px); } }

/* -- Prompt shell collapsible -- */
.prompt-shell details { margin: 24px 0; }
.prompt-shell summary {
  cursor: pointer; font-family: system-ui, sans-serif;
  font-size: 0.9rem; color: #666;
}
.prompt-shell pre {
  background: #f5f3ef; padding: 16px; margin-top: 12px;
  font-size: 0.85rem; line-height: 1.6; white-space: pre-wrap;
  border-radius: 3px; position: relative;
}
.prompt-shell .copy-prompt {
  position: absolute; top: 8px; right: 8px;
  background: #1a1a1a; color: #faf9f6; border: none;
  padding: 4px 10px; font-size: 0.75rem; cursor: pointer;
  border-radius: 2px;
}

/* -- Print CSS -- */
@media print {
  body { background: #fff; }
  #workshop-mode .workshop-nav,
  #workshop-mode .export-bar,
  #workshop-mode .validation-panel,
  #workshop-mode #outside-note-toggle summary,
  #magazine-mode,
  .skip-link,
  .btn-danger { display: none !important; }
  #body-input {
    border: none; font-size: 14pt; line-height: 1.8;
    max-width: 600px; margin: 40px auto; padding: 0;
    resize: none; overflow: hidden;
  }
  .outside-note-fields {
    max-width: 600px; margin: 24px auto;
    border-top: 1px solid #ccc; padding-top: 16px;
    font-size: 10pt;
  }
}

/* -- Mobile responsive -- */
@media (max-width: 768px) {
  .workshop-layout { flex-direction: column; }
  .validation-panel { position: static; }
  .masthead h1 { font-size: 2.5rem; }
  .outside-note-fields { grid-template-columns: 1fr; }
}
```

- [ ] **Step 3: Embed the 3 example JSON blocks**

At the bottom of the HTML, before `</body>`, add:
```html
<script type="application/json" id="example-fragility-atlas">
  <!-- paste contents of examples/fragility-atlas.json -->
</script>
<script type="application/json" id="example-metarep">
  <!-- paste contents of examples/metarep.json -->
</script>
<script type="application/json" id="example-clinical-ma">
  <!-- paste contents of examples/clinical-ma.json -->
</script>
```

- [ ] **Step 4: Open in browser, verify both modes render**

Open `C:\E156\index.html` in Chrome. Verify:
- Magazine mode shows with masthead, argument, example cards, rules, prompt shell, CTA button
- Workshop mode is hidden
- Typography is serif, column is centered ~680px
- Mobile: resize to 375px width, verify stacked layout

- [ ] **Step 5: Commit**

```bash
cd /c/E156
git add index.html
git commit -m "feat: HTML skeleton + CSS foundation (magazine + workshop modes)"
```

---

### Task 3: Magazine Mode Content

Populate all static content in Magazine mode.

**Files:**
- Modify: `C:\E156\index.html` (Magazine mode sections)

- [ ] **Step 1: Write the argument section**

~150 words explaining why E156 exists. Editorial tone, NYT style. Key points:
- Meta-analyses produce forests of data but decisions need a paragraph
- 156 words forces discipline: every word earns its place
- 7 sentences enforce structure: question, evidence, method, result, robustness, interpretation, limitation
- The constraint IS the feature

- [ ] **Step 2: Render example micro-papers from embedded JSON**

Write a small init function in `<script>` that:
1. Parses each `<script type="application/json">` block
2. For each example, populates the `.micro-paper-body` blockquote with the `body` field
3. Generates sentence annotation tags from the `sentences` array
4. Adds a title above each card

```javascript
function initExamples() {
  const examples = ['fragility-atlas', 'metarep', 'clinical-ma'];
  examples.forEach(id => {
    const data = JSON.parse(document.getElementById('example-' + id).textContent);
    const card = document.querySelector('[data-example="' + id + '"]');
    if (!card) return;
    card.querySelector('.example-title').textContent = data.title;
    card.querySelector('.micro-paper-body').textContent = data.body;
    const annot = card.querySelector('.sentence-annotations');
    data.sentences.forEach((s, i) => {
      const tag = document.createElement('span');
      tag.className = 'tag';
      tag.textContent = 'S' + (i + 1) + ': ' + s.role;
      annot.appendChild(tag);
    });
  });
}
```

- [ ] **Step 3: Write the rules section**

Render the sentence schema as a numbered list and the house style as a paragraph. Use the text from spec.md §2.2 and §2.4.

- [ ] **Step 4: Write the prompt shell section**

A `<details>` element with the prompt shell text from spec.md. Include a "Copy" button that copies the prompt text to clipboard.

- [ ] **Step 5: Verify in browser**

Open `index.html`. Verify:
- Argument reads well, editorial tone
- All 3 examples render with body text and sentence tags
- Rules section shows numbered list + paragraph
- Prompt shell expands/collapses, copy button works

- [ ] **Step 6: Commit**

```bash
cd /c/E156
git add index.html
git commit -m "feat: magazine mode content (argument, examples, rules, prompt shell)"
```

---

### Task 4: Mode Switching + URL Hash

Wire up the Magazine ↔ Workshop transitions.

**Files:**
- Modify: `C:\E156\index.html` (add JS at bottom of `<script>` block)

- [ ] **Step 1: Write mode switching functions**

```javascript
function showWorkshop() {
  const mag = document.getElementById('magazine-mode');
  const ws = document.getElementById('workshop-mode');
  mag.classList.add('hidden');
  mag.classList.remove('fade-in');
  ws.classList.remove('hidden');
  ws.classList.add('fade-in');
  document.getElementById('body-input').focus();
  window.location.hash = 'compose';
}

function showMagazine() {
  const ws = document.getElementById('workshop-mode');
  const mag = document.getElementById('magazine-mode');
  ws.classList.add('hidden');
  ws.classList.remove('fade-in');
  mag.classList.remove('hidden');
  mag.classList.add('fade-in');
  document.getElementById('btn-write').focus();
  window.location.hash = '';
}
```

- [ ] **Step 2: Wire event listeners**

```javascript
document.getElementById('btn-write').addEventListener('click', showWorkshop);
document.getElementById('btn-back').addEventListener('click', (e) => {
  e.preventDefault();
  showMagazine();
});

// URL hash on load (Task 9 will move this into DOMContentLoaded and add hashchange listener)
if (window.location.hash === '#compose') {
  showWorkshop();
}
```

- [ ] **Step 3: Test mode switching**

Open `index.html`. Click "Write one →" — Workshop appears, textarea focused. Click "← Back to E156" — Magazine reappears, CTA focused. Navigate to `index.html#compose` — Workshop loads directly.

- [ ] **Step 4: Commit**

```bash
cd /c/E156
git add index.html
git commit -m "feat: mode switching with URL hash (#compose)"
```

---

### Task 5: Core Validation Engine (Word Count + Sentence Detection)

The heart of the tool. Implement the algorithms from spec §3.6 and §3.7.

**Files:**
- Modify: `C:\E156\index.html` (add functions in `<script>` block)

- [ ] **Step 1: Write the word count function**

```javascript
function countWords(text) {
  if (!text || !text.trim()) return 0;
  return text.trim().split(/\s+/).filter(Boolean).length;
}
```

- [ ] **Step 2: Write the sentence detection function**

```javascript
const ABBREVIATIONS = [
  'vs.', 'e.g.', 'i.e.', 'approx.',
  'et al.', 'Fig.', 'No.', 'Dr.', 'Prof.',
  'U.S.', 'U.K.'
];

function splitSentences(text) {
  if (!text || !text.trim()) return [];
  let working = text.trim();

  // Step 1: Replace abbreviations with placeholders
  const abbrevMap = [];
  ABBREVIATIONS.forEach((abbr, i) => {
    const placeholder = '\x00ABBR' + i + '\x00';
    while (working.includes(abbr)) {
      working = working.replace(abbr, placeholder);
      abbrevMap.push({ placeholder, abbr });
    }
  });

  // Step 2: Replace decimal numbers (e.g., 0.85, 2.13)
  const decimalMap = [];
  working = working.replace(/(\d+)\.(\d+)/g, (match, p1, p2, offset) => {
    const placeholder = '\x00DEC' + decimalMap.length + '\x00';
    decimalMap.push({ placeholder, original: match });
    return placeholder;
  });

  // Step 3: Match sentences (each ends with a period, preserving the period)
  // Use match instead of split to keep trailing periods on each sentence
  const raw = working.match(/[^]*?\.(?=\s|$|[")]))/g);
  if (!raw) return [working]; // no period found — treat entire text as one sentence

  // Check for trailing text after last period
  const joined = raw.join('');
  const remainder = working.slice(joined.length).trim();
  const sentences = remainder ? [...raw, remainder] : raw;

  // Step 4: Restore placeholders
  const restored = sentences.map(s => {
    let r = s;
    decimalMap.forEach(d => {
      while (r.includes(d.placeholder)) r = r.replace(d.placeholder, d.original);
    });
    abbrevMap.forEach(a => {
      while (r.includes(a.placeholder)) r = r.replace(a.placeholder, a.abbr);
    });
    return r;
  });

  // Step 5: Trim and filter empty
  return restored.map(s => s.trim()).filter(s => s.length > 0);
}
```

- [ ] **Step 3: Test against acceptance cases**

Add a temporary self-test function and run it in the browser console:

```javascript
function selfTest() {
  const cases = [
    { input: 'The pooled OR was 2.13. Heterogeneity was high.', expected: 2 },
    { input: 'Risk was elevated (OR 1.45, 95% CI 1.10\u20131.89). This suggests concern.', expected: 2 },
    { input: 'The result vs. placebo was clear. No benefit remained.', expected: 2 },
    { input: 'Smith et al. reported similar findings. The effect was modest.', expected: 2 },
    { input: 'Sensitivity was 95%. Specificity was 88%.', expected: 2 },
    { input: 'One sentence only.', expected: 1 },
    { input: 'Sentence one. Sentence two. Sentence three. Sentence four. Sentence five. Sentence six. Sentence seven.', expected: 7 },
  ];
  let pass = 0;
  cases.forEach((c, i) => {
    const result = splitSentences(c.input).length;
    const ok = result === c.expected;
    if (ok) pass++;
    console.log((ok ? 'PASS' : 'FAIL') + ' Case ' + (i+1) + ': got ' + result + ', expected ' + c.expected);
  });
  console.log(pass + '/' + cases.length + ' passed');
}
```

Run: open `index.html`, open DevTools console, call `selfTest()`.
Expected: 7/7 passed.

- [ ] **Step 4: Remove selfTest, commit**

Remove the `selfTest` function (it was for verification only). Keep `countWords` and `splitSentences`.

```bash
cd /c/E156
git add index.html
git commit -m "feat: core validation engine (word count + sentence detection)"
```

---

### Task 6: Live Validation UI

Wire the validation engine to the UI. Update counters, sentence map, style checks, and status badge on every keystroke (debounced 300ms).

**Files:**
- Modify: `C:\E156\index.html` (add validation UI functions)

- [ ] **Step 1: Write the house style checks**

```javascript
const CAUSAL_WORDS = [
  'caused', 'causes', 'prevents', 'leads to', 'due to',
  'resulted in', 'results in', 'because of', 'protective effect',
  'causal', 'proven to', 'proves'
];

function checkHouseStyle(text, sentences) {
  const checks = [];
  // No headings (lines starting with #)
  checks.push({ label: 'No headings', pass: !/^#+\s/m.test(text) });
  // No links (http:// or https:// or markdown links)
  checks.push({ label: 'No links', pass: !/https?:\/\/|\[.*\]\(/.test(text) });
  // No citations ([1], [2], (Author, Year))
  checks.push({ label: 'No citations', pass: !/\[\d+\]|\(\w+,?\s*\d{4}\)/.test(text) });
  // S4 contains a number and interval-like pattern
  const s4 = sentences[3] || '';
  const hasEstimate = /\d+\.?\d*/.test(s4) && /(CI|confidence interval|interval|\d+[\u2013\u2014-]\d+)/i.test(s4);
  checks.push({ label: 'Result (S4) has estimate + interval', pass: hasEstimate });
  // S7 exists (limitation)
  checks.push({ label: 'Limitation (S7) present', pass: sentences.length >= 7 });
  return checks;
}

function checkCausalLanguage(sentences) {
  const s6 = (sentences[5] || '').toLowerCase();
  const found = CAUSAL_WORDS.filter(w => {
    const regex = new RegExp('\\b' + w.replace(/\s+/g, '\\s+') + '\\b', 'i');
    return regex.test(s6);
  });
  return found;
}
```

- [ ] **Step 2: Write the shared validity check and main validate function**

```javascript
// Shared validity logic — used by both the UI badge and JSON export
function isFullyValid(wordCount, sentences, styleChecks, notesFilled) {
  return wordCount === 156
    && sentences.length === 7
    && styleChecks.every(c => c.pass)
    && notesFilled;
}
```

```javascript
let validateTimer = null;

function validate() {
  const text = document.getElementById('body-input').value;
  const words = countWords(text);
  const sentences = splitSentences(text);
  const isEmpty = !text.trim();

  // Word counter
  const wc = document.getElementById('word-count');
  wc.textContent = words;
  wc.parentElement.className = 'counter word-counter ' + (words === 156 ? 'valid' : (isEmpty ? '' : 'invalid'));

  // Sentence counter
  const sc = document.getElementById('sentence-count');
  sc.textContent = sentences.length;
  sc.parentElement.className = 'counter sentence-counter ' + (sentences.length === 7 ? 'valid' : (isEmpty ? '' : 'invalid'));

  // Sentence role map
  const map = document.getElementById('sentence-map');
  const roles = ['Question', 'Dataset', 'Method', 'Primary result', 'Robustness', 'Interpretation', 'Boundary'];
  map.innerHTML = '';
  sentences.forEach((s, i) => {
    const tag = document.createElement('span');
    tag.className = 'role-tag';
    tag.style.background = i < 7 ? '#f0ede8' : '#fce4ec';
    tag.style.color = i < 7 ? '#666' : '#c62828';
    tag.textContent = 'S' + (i + 1) + ': ' + (roles[i] || 'Extra');
    tag.title = s.substring(0, 80) + (s.length > 80 ? '...' : '');
    map.appendChild(tag);
  });

  // House style checks
  const checks = checkHouseStyle(text, sentences);
  const ul = document.getElementById('style-checks');
  ul.innerHTML = '';
  checks.forEach(c => {
    const li = document.createElement('li');
    li.className = c.pass ? 'pass' : 'fail';
    li.textContent = c.label;
    ul.appendChild(li);
  });

  // Causal language warning
  const causalDiv = document.getElementById('causal-warning');
  const causalFound = checkCausalLanguage(sentences);
  if (causalFound.length > 0) {
    causalDiv.textContent = 'Causal language detected in interpretation: "' + causalFound.join('", "') + '" \u2014 verify this is warranted by study design.';
    causalDiv.classList.remove('hidden');
  } else {
    causalDiv.classList.add('hidden');
  }

  // Outside note block completeness
  const noteFields = ['note-app', 'note-data', 'note-code', 'note-doi', 'note-version', 'note-date', 'note-validation'];
  const notesFilled = noteFields.every(id => document.getElementById(id).value.trim() !== '');

  // Shared validity check (also used by JSON export)
  const allChecksPassed = isFullyValid(words, sentences, checks, notesFilled);

  // Status badge
  const badge = document.getElementById('status-badge');
  if (isEmpty) {
    badge.className = 'status-badge empty';
    badge.textContent = '';
  } else if (allChecksPassed) {
    badge.className = 'status-badge valid';
    badge.textContent = 'VALID';
  } else {
    badge.className = 'status-badge draft';
    badge.textContent = 'DRAFT';
  }

  // Enable/disable export buttons
  const hasContent = !isEmpty;
  document.getElementById('btn-copy').disabled = !hasContent;
  document.getElementById('btn-md').disabled = !hasContent;
  document.getElementById('btn-json').disabled = !hasContent;
  document.getElementById('btn-print').disabled = !hasContent;
  ['btn-copy', 'btn-md', 'btn-json', 'btn-print'].forEach(id => {
    document.getElementById(id).title = hasContent ? '' : 'Write something first';
  });
}

// Debounced input handler
document.getElementById('body-input').addEventListener('input', () => {
  clearTimeout(validateTimer);
  validateTimer = setTimeout(validate, 300);
});
// Also validate when outside note fields change
document.querySelectorAll('.outside-note-fields input').forEach(el => {
  el.addEventListener('input', () => {
    clearTimeout(validateTimer);
    validateTimer = setTimeout(validate, 300);
  });
});
```

- [ ] **Step 3: Test validation in browser**

Open `index.html#compose`. Type a 7-sentence, 156-word paragraph. Verify:
- Word counter goes green at 156
- Sentence counter goes green at 7
- Sentence role tags appear for each sentence
- Style checks show pass/fail
- Status badge shows DRAFT (without outside note block) then VALID (after filling all fields)
- Type a heading (`# test`) — "No headings" check fails
- Type a URL — "No links" check fails
- Add causal word "prevents" in S6 position — amber warning appears

- [ ] **Step 4: Commit**

```bash
cd /c/E156
git add index.html
git commit -m "feat: live validation UI (counters, sentence map, style checks, status badge)"
```

---

### Task 7: localStorage Persistence

Auto-save draft and restore on page load.

**Files:**
- Modify: `C:\E156\index.html`

- [ ] **Step 1: Write save/load functions**

```javascript
const STORAGE_KEY = 'e156_draft';

function saveDraft() {
  const draft = {
    body: document.getElementById('body-input').value,
    notes: {}
  };
  ['note-app', 'note-data', 'note-code', 'note-doi', 'note-version', 'note-date', 'note-validation'].forEach(id => {
    draft.notes[id] = document.getElementById(id).value;
  });
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(draft));
  } catch (e) { /* localStorage full or disabled — silent fail */ }
}

function loadDraft() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const draft = JSON.parse(raw);
    if (draft.body) document.getElementById('body-input').value = draft.body;
    if (draft.notes) {
      Object.entries(draft.notes).forEach(([id, val]) => {
        const el = document.getElementById(id);
        if (el) el.value = val;
      });
    }
    validate(); // update UI with loaded draft
  } catch (e) { /* corrupt data — ignore */ }
}
```

- [ ] **Step 2: Wire auto-save into validation debounce**

Modify the debounced input handler to also save:

```javascript
// Replace the existing input listeners with:
function debouncedUpdate() {
  clearTimeout(validateTimer);
  validateTimer = setTimeout(() => {
    validate();
    saveDraft();
  }, 300);
}

document.getElementById('body-input').addEventListener('input', debouncedUpdate);
document.querySelectorAll('.outside-note-fields input').forEach(el => {
  el.addEventListener('input', debouncedUpdate);
});
```

- [ ] **Step 3: Wire clear draft button**

```javascript
document.getElementById('btn-clear').addEventListener('click', () => {
  if (!confirm('Clear your draft? This cannot be undone.')) return;
  localStorage.removeItem(STORAGE_KEY);
  document.getElementById('body-input').value = '';
  ['note-app', 'note-data', 'note-code', 'note-doi', 'note-version', 'note-date', 'note-validation'].forEach(id => {
    document.getElementById(id).value = '';
  });
  validate();
});
```

- [ ] **Step 4: Call loadDraft on init**

Add to the initialization section (after DOM ready):
```javascript
loadDraft();
```

- [ ] **Step 5: Test persistence**

1. Open `index.html#compose`, type text, fill a note field
2. Close the tab
3. Reopen `index.html#compose`
4. Verify text and note fields are restored
5. Click "Clear Draft", confirm — verify all fields are empty and localStorage key is removed

- [ ] **Step 6: Commit**

```bash
cd /c/E156
git add index.html
git commit -m "feat: localStorage draft persistence (auto-save, restore, clear)"
```

---

### Task 8: Export Functions

Implement all four export mechanisms.

**Files:**
- Modify: `C:\E156\index.html`

- [ ] **Step 1: Write clipboard copy**

```javascript
async function copyBody() {
  const text = document.getElementById('body-input').value.trim();
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    showToast('Copied.');
  } catch (e) {
    // Fallback for insecure contexts
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      showToast('Copied.');
    } catch (e2) {
      showToast('Select All + Copy manually.');
    }
    document.body.removeChild(ta);
  }
}

function showToast(msg) {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2200);
}
```

- [ ] **Step 2: Write markdown download**

```javascript
function downloadMarkdown() {
  const body = document.getElementById('body-input').value.trim();
  if (!body) return;
  let md = body + '\n\n---\n\n';
  const fields = [
    ['App', 'note-app'], ['Data', 'note-data'], ['Code', 'note-code'],
    ['DOI', 'note-doi'], ['Version', 'note-version'], ['Date', 'note-date'],
    ['Validation Status', 'note-validation']
  ];
  fields.forEach(([label, id]) => {
    const val = document.getElementById(id).value.trim();
    if (val) md += label + '\n: ' + val + '\n\n';
  });
  downloadFile('e156-draft.md', md, 'text/markdown;charset=utf-8');
}
```

- [ ] **Step 3: Write JSON download**

```javascript
function downloadJSON() {
  const body = document.getElementById('body-input').value.trim();
  if (!body) return;
  const sentences = splitSentences(body);
  const roles = ['Question', 'Dataset', 'Method', 'Primary result', 'Robustness', 'Interpretation', 'Boundary'];
  const obj = {
    body: body,
    sentences: sentences.map((s, i) => ({ role: roles[i] || 'Extra', text: s })),
    wordCount: countWords(body),
    sentenceCount: sentences.length,
    outsideNote: {
      app: document.getElementById('note-app').value.trim(),
      data: document.getElementById('note-data').value.trim(),
      code: document.getElementById('note-code').value.trim(),
      doi: document.getElementById('note-doi').value.trim(),
      version: document.getElementById('note-version').value.trim(),
      date: document.getElementById('note-date').value.trim(),
      validationStatus: document.getElementById('note-validation').value.trim()
    },
    meta: {
      created: new Date().toISOString(),
      valid: isFullyValid(
        countWords(body),
        sentences,
        checkHouseStyle(body, sentences),
        ['note-app','note-data','note-code','note-doi','note-version','note-date','note-validation']
          .every(id => document.getElementById(id).value.trim() !== '')
      ),
      schemaVersion: '0.1'
    }
  };
  downloadFile('e156-draft.json', JSON.stringify(obj, null, 2), 'application/json;charset=utf-8');
}
```

- [ ] **Step 4: Write shared download helper**

```javascript
function downloadFile(filename, content, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
```

- [ ] **Step 5: Write print view trigger**

```javascript
function printView() {
  const details = document.getElementById('outside-note-toggle');
  const wasOpen = details.open;
  // Force open so print CSS can render the fields
  details.open = true;

  // Hide outside note block in print if all fields are empty
  const noteFields = ['note-app','note-data','note-code','note-doi','note-version','note-date','note-validation'];
  const allEmpty = noteFields.every(id => document.getElementById(id).value.trim() === '');
  if (allEmpty) details.style.display = 'none';

  window.print();

  // Restore original state
  details.open = wasOpen;
  details.style.display = '';
}
```

- [ ] **Step 6: Wire all export buttons**

```javascript
document.getElementById('btn-copy').addEventListener('click', copyBody);
document.getElementById('btn-md').addEventListener('click', downloadMarkdown);
document.getElementById('btn-json').addEventListener('click', downloadJSON);
document.getElementById('btn-print').addEventListener('click', printView);
```

- [ ] **Step 7: Test all exports**

1. Type text in the composer
2. Click "Copy Body" — paste into notepad, verify content matches
3. Click "Download .md" — verify file downloads, open in editor, check format
4. Click "Download .json" — verify JSON is valid, has all fields, `schemaVersion: "0.1"`
5. Click "Print View" — verify print dialog shows clean one-page layout
6. With empty textarea — verify all 4 buttons are disabled

- [ ] **Step 8: Commit**

```bash
cd /c/E156
git add index.html
git commit -m "feat: export functions (clipboard, markdown, JSON, print)"
```

---

### Task 9: Final Polish + Integration Testing

Tie up loose ends and run full acceptance testing.

**Files:**
- Modify: `C:\E156\index.html`

- [ ] **Step 1: Wire initialization**

Ensure all init code runs on DOM ready:

```javascript
document.addEventListener('DOMContentLoaded', () => {
  initExamples();
  loadDraft();
  // Hash routing
  if (window.location.hash === '#compose') {
    showWorkshop();
  }
  // Listen for hash changes (browser back/forward)
  window.addEventListener('hashchange', () => {
    if (window.location.hash === '#compose') showWorkshop();
    else showMagazine();
  });
});
```

- [ ] **Step 2: Prompt shell copy button**

```javascript
document.querySelector('.copy-prompt')?.addEventListener('click', async () => {
  const promptText = document.querySelector('.prompt-shell pre').textContent;
  try {
    await navigator.clipboard.writeText(promptText);
    showToast('Prompt copied.');
  } catch (e) {
    showToast('Could not copy.');
  }
});
```

- [ ] **Step 3: Div balance check**

Count opening `<div` and closing `</div>` tags in the HTML. They must match. Use:
```bash
cd /c/E156
python -c "t=open('index.html',encoding='utf-8').read(); print('open:', t.count('<div'), 'close:', t.count('</div>'))"
```
Expected: counts match.

- [ ] **Step 4: Script tag safety check**

Search for literal `</script>` inside `<script>` blocks:
```bash
cd /c/E156
python -c "
t=open('index.html',encoding='utf-8').read()
import re
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', t, re.DOTALL)
for i, s in enumerate(scripts):
    if '</script>' in s:
        print(f'DANGER: literal </script> in script block {i}')
    else:
        print(f'OK: script block {i}')
"
```
Expected: all OK.

- [ ] **Step 5: Full acceptance test**

Open `index.html` in Chrome. Walk through all 8 success criteria from spec §8:

1. Loads with no dependencies (no network requests in DevTools Network tab)
2. Magazine mode: masthead, argument, 3 examples with annotations, rules, prompt shell, CTA
3. Click "Write one →" — Workshop mode with textarea, validation panel
4. Type a 7-sentence, 156-word paragraph — all checks go green, badge shows VALID (after filling outside notes)
5. Export: copy, .md, .json, print — all work
6. Close tab, reopen — draft persisted
7. Resize to 375px — stacked layout
8. Ctrl+P — clean one-page printout

- [ ] **Step 6: Commit**

```bash
cd /c/E156
git add index.html
git commit -m "feat: final polish + integration (init, hash routing, prompt copy)"
```

---

### Task 10: Update Memory + Project Index

Register E156 in the project tracking systems.

**Files:**
- Create: `C:\Users\user\.claude\projects\C--Users-user\memory\e156.md`
- Modify: `C:\Users\user\.claude\projects\C--Users-user\memory\MEMORY.md`
- Modify: `C:\ProjectIndex\INDEX.md` (if accessible)

- [ ] **Step 1: Create E156 memory file**

```markdown
---
name: E156 Micro-Paper Standard
description: Compact 7-sentence, 156-word micro-paper format for meta-analyses, with interactive HTML composer/validator
type: project
---

E156 is a micro-paper format standard: exactly 7 sentences, 156 words, single paragraph.
Location: `C:\E156\`
Tool: single-file HTML app with NYT editorial styling.
Two modes: Magazine (showcase) + Workshop (composer/validator).
Exports: clipboard, .md, .json, print.
Status: MVP implementation.

**Why:** Meta-analyses produce thousands of pages but decisions need one paragraph. E156 enforces discipline through constraints.
**How to apply:** Use for summarizing any completed meta-analysis. Each of the 15+ submission-ready papers could get an E156 micro-paper.
```

- [ ] **Step 2: Add pointer to MEMORY.md**

Add under "Active Projects":
```
- [E156](e156.md) — Micro-paper standard + HTML composer, `C:\E156\`, NYT-styled
```

- [ ] **Step 3: Update ProjectIndex if accessible**

Add E156 entry to `C:\ProjectIndex\INDEX.md`.

- [ ] **Step 4: Commit memory update**

```bash
cd /c/Users/user
git add .claude/projects/C--Users-user/memory/e156.md .claude/projects/C--Users-user/memory/MEMORY.md
git commit -m "memory: add E156 micro-paper project"
```
