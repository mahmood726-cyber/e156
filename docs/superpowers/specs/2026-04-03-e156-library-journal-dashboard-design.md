# E156 Library + Journal Vol.1 + Seven Signs Dashboard

**Date:** 2026-04-03
**Author:** Mahmood Ahmad
**Status:** Approved

## Overview

A single-file HTML application (~4,500 lines) combining three lazy-loaded sections into one unified showcase for 331 E156 micro-papers. Built from the rewrite workbook by a Python build script. NYT editorial styling matching the existing E156 composer. Fully offline, no dependencies.

## Architecture

### Approach

Single HTML file with embedded data (Approach 3). Three sections accessed via fixed top navigation with smooth-scroll. Each section lazy-renders on first visit to keep initial load fast.

### Output

- **File:** `C:\E156\e156-library.html`
- **Size:** ~4,500 lines estimated
- **Dependencies:** None (self-contained HTML/CSS/JS)
- **Browser support:** Chrome, Firefox, Safari, Edge
- **Offline:** Yes

### Build Pipeline

A Python script (`scripts/build_library.py`) that:

1. Parses `rewrite-workbook.txt` — extracts all 331 entries (id, title, type, estimand, data, path, body, rewrite, wordCount, sentenceCount)
2. Enriches with metadata from `paper.json` files at each project path (test counts, manuscript status, validation grade where available)
3. Generates tags from title keywords (NMA, Bayesian, GRADE, CT.gov, living, DTA, Cochrane, browser, R package, etc.)
4. Injects the data as a JS const into a template file
5. Emits the final `e156-library.html`

**Rebuild command:** `python C:/E156/scripts/build_library.py`
**Build time:** <5 seconds

### File Structure

```
C:\E156\
├── e156-library.html              ← Final output
├── templates/
│   └── library-template.html      ← HTML/CSS/JS template with __DATA_PLACEHOLDER__
├── scripts/
│   ├── build_library.py           ← Build script
│   └── (existing scripts unchanged)
├── rewrite-workbook.txt           ← Source data (331 entries)
└── index.html                     ← Existing E156 composer (unchanged)
```

## Section 1: Data Layer

Each paper is a JS object:

```js
{
  id: 303,
  slug: "ActionableEvidence",
  title: "ActionableEvidence: GO/NO-GO Verdicts for Cochrane Meta-Analyses...",
  type: "methods",       // methods | clinical | audit
  estimand: "Actionability classification (GO/CAUTION/NO-GO)",
  data: "Pairwise70 Cochrane meta-analysis recomputations",
  path: "C:\\Models\\ActionableEvidence",
  body: "What fraction of...",          // CURRENT BODY from workbook
  rewrite: "What fraction of...",       // YOUR REWRITE from workbook
  wordCount: 136,
  sentenceCount: 7,
  tags: ["Cochrane", "audit", "GRADE"]  // auto-generated from title
}
```

**Categories:** Methods (navy `#2c3e50`), Clinical (crimson `#8b1a1a`), Audit (slate `#4a5568`)

**Tags:** Auto-extracted from title keywords. Known keyword list: NMA, Bayesian, GRADE, CT.gov, living, DTA, Cochrane, browser, R package, IPD, SGLT2, finerenone, HTA, publication bias, fragility, heterogeneity, network, dose-response, diagnostic, survival, transportability, equity, qualitative, trial sequential, copula, entropy, topology, spectral, hyperbolic, information geometry.

## Section 2: Library View

The default view when the file opens.

### Masthead

- Title: "E156 Library"
- Subtitle: "331 Micro-Papers in Evidence Synthesis"
- Author: "Mahmood Ahmad"
- NYT-style centered layout, Georgia serif

### Controls Bar

- **Search box:** Filters title + body + tags in real-time (debounced 200ms)
- **Category pills:** All | Methods | Clinical | Audit — click to filter, multiple selection
- **Sort dropdown:** A-Z | Newest (by ID desc) | Word Count
- **View toggle:** Grid | List | Reading — three icon buttons

### Grid View (Default)

3-column responsive card grid. Each card:
- Category color bar (3px top border)
- Title (truncated to 2 lines with CSS `line-clamp`)
- First sentence of rewrite (the research question)
- Word count badge + up to 3 tag pills
- Click opens Reading View for that paper

### List View

Compact table layout. Columns: #, Title, Type, Estimand, Words. Click any row opens Reading View. Sortable by clicking column headers.

### Reading View

Full-width single-paper display (max-width 680px centered, matching E156 composer):
- Title as headline (Georgia, 2rem)
- Metadata line: `type | estimand | dataset` in small caps sans-serif
- Rewrite body in Georgia serif, 1.1rem, 1.8 line-height
- S1-S7 sentence annotation tags below body (subtle pill badges: Question, Dataset, Method, Result, Robustness, Interpretation, Boundary)
- "Copy Citation" button — copies formatted citation to clipboard
- "Copy BibTeX" button — copies BibTeX entry
- Path displayed as monospace link
- Back arrow / ESC returns to previous view
- Left/Right arrow keys navigate between papers

## Section 3: Journal View

### Journal Header

- "E156: The Journal of Micro-Papers in Evidence Synthesis"
- "Volume 1 — April 2026"
- "Editor: Mahmood Ahmad"
- Placeholder ISSN line

### Editorial

Static embedded text (~200 words) explaining the E156 format: why 7 sentences, why 156 words, the discipline of compression, the relationship between constraint and clarity. Written by the build script author (me) and editable in the template.

### Table of Contents

Organized by category (Methods, Clinical, Audit), then alphabetical within each category. Each entry:
- Paper number
- Title (clickable — navigates to Library Reading View for that paper)
- Type badge (colored pill)
- Estimand (truncated to 60 chars)

### Citation Export

Top-level buttons:
- "Export all citations (.bib)" — downloads BibTeX file for all 331 papers
- "Export all citations (.ris)" — downloads RIS file for Zotero/EndNote

Individual paper citation format:
```
Ahmad M. [Title]. E156 J Micro-Papers Evid Synth. 2026;1:[paper#].
```

DOI placeholder: `doi:10.5281/zenodo.XXXXXXX` — user fills in after Zenodo deposit.

## Section 4: Seven Signs Dashboard

7 horizontal gauge rows spanning full width. Each sign is a labeled progress/status bar.

### Sign 1: E156 Complete
- Source: Count of entries with rewrite wordCount > 0
- Display: `331/331` — solid green bar (100%)

### Sign 2: Tests Passing
- Source: Parsed from memory files and paper.json (test counts where available)
- Display: Total test count across portfolio + bar showing % of projects with tests
- Color: Green (has tests) / Gray (no test data)

### Sign 3: Manuscript Status
- Source: Best-available from memory files (draft/review/submitted/accepted)
- Display: Stacked horizontal bar with 4 colors:
  - Draft (light gray), Review (amber), Submitted (blue), Accepted (green)
- Default: "unknown" for projects without manuscript data

### Sign 4: Validation Grade
- Source: Whether project has R-matched validation noted in memory or paper.json
- Display: Two-segment bar — validated (green) vs unvalidated (gray)

### Sign 5: Fragility
- Source: Projects with fragility index computed
- Display: Count of projects with FI data + median FI value

### Sign 6: Freshness
- Source: Computed at build time from last git commit date per project path (where available)
- Display: Heat strip — green (<30 days), amber (30-90 days), red (>90 days), gray (unknown)

### Sign 7: Citation Readiness
- Source: Has DOI, Zenodo deposit, paper.json with title/abstract
- Display: Progress bar toward full citation metadata

### Summary Line
Bottom of dashboard: one-line aggregate verdict
> "Portfolio health: X% — 331 papers, Y validated, Z manuscripts in review"

## Section 5: Styling

### Color Palette
- Background: `#faf9f6` (warm cream)
- Text: `#1a1a1a`
- Category accents:
  - Methods: `#2c3e50` (navy)
  - Clinical: `#8b1a1a` (crimson)
  - Audit: `#4a5568` (slate)
- Dashboard gauges: green `#2d6a4f`, amber `#d4a017`, red `#9b2226`
- Card hover shadow: `rgba(0,0,0,0.08)`

### Typography
- Body/reading: Georgia, Charter, 'Times New Roman', serif
- UI/controls: system-ui, -apple-system, sans-serif
- Stats/counts: Menlo, Consolas, monospace

### Navigation
Fixed bar at page top:
- Left: "E156" wordmark (bold Georgia)
- Center: Library | Journal | Dashboard (nav links)
- Right: Search icon (Library only)
- Active section: subtle 2px underline
- Smooth-scroll between sections
- Lazy-render: each section only builds its DOM on first navigation

### Responsive Breakpoints
- Desktop (>1024px): 3-column grid, full dashboard gauges
- Tablet (768-1024px): 2-column grid
- Mobile (<768px): 1-column stack, dashboard gauges stack vertically

### Print
`@media print`:
- Hide nav bar, search, dashboard
- Render Journal TOC + all 331 papers in reading format
- Page breaks between papers
- Produces a printable Volume 1

## Section 6: Keyboard & Accessibility

- Tab navigation through all interactive elements
- ESC closes reading view
- Left/Right arrows navigate between papers in reading view
- Search box: Ctrl+K / Cmd+K shortcut
- `role="navigation"` on nav bar
- `role="search"` on search
- `aria-label` on all buttons
- Category pills are toggleable with Enter/Space
- Color contrast: WCAG AA (4.5:1 minimum)

## Section 7: Testing Strategy

### Build Script Tests
- Parse all 331 entries from workbook — assert count == 331
- Validate all entries have non-empty rewrite — assert 0 blank
- Validate word counts in range 90-170
- Validate tag generation produces at least 1 tag per entry
- Output HTML is valid (no unclosed divs, no broken script tags)

### Browser Smoke Tests (Manual)
- Open file in Chrome — all 3 sections render
- Search filters correctly
- Category pills filter correctly
- Reading view opens/closes
- Journal TOC links navigate to correct paper
- Citation copy works
- Dashboard gauges display
- Print preview produces readable output
- Mobile responsive at 375px width

## Non-Goals

- No server-side rendering
- No user accounts or authentication
- No editing capability (that's the existing E156 composer)
- No real-time data — dashboard reflects build-time snapshot
- No CDN dependencies (fully self-contained)
- Sub-projects B and C (Reversals, Curriculum, Multilingual) are separate future work
