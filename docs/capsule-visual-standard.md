# e156 Capsule Visual + Analytical Standard — Decision-Grade Spec

> Source: multi-agent visual audit (2026-06-02) of 12 rendered capsules + RapidMeta + allmeta
> benchmarks, scored against an NYT/OWID/FT-and-beyond dataviz rubric. Mean 57.1/100.
> Status note (2026-06-04): the suite now has assurance ribbons and inlined ChartKit/tokens
> across all 40 capsule files; the remaining gaps below are visual-density and communication
> targets to remeasure, not runtime blockers.

## 1. Verdict

**Runtime-consistent; visual standard still not fully closed.** Initial audit: Mean score **57.1/100** across 12 capsules (range 38–79; only `sglt2-hf` clears 75). Median capsule shows 5 plots and carries 6 defects. The top scorer (`sglt2-hf`, 79) still logs 5 defects, so even the best is a B-minus. Three systemic gaps — present in nearly every defect line — hold the set down:

- **G1 — Titles are labels, not claims.** Every capsule audited (`sglt2-hf`, `nma`, `dta`, …) titles figures structurally ("Forest plot", "Summary ROC", "The evidence network") instead of asserting the finding. A figure-only reader cannot reconstruct the argument. This is the single most repeated major defect.
- **G2 — Uncertainty is hidden or understated.** Prediction intervals missing on forests/ranking; CrIs stored only in `title` tooltips (vanish on print/screenshot — `nma` league table); τ²/I² shown as bare numbers with no CI; pooled diamonds without PI. The capsules overstate precision exactly where their own thesis warns against it.
- **G3 — Axes and legends are unreadable / encodings undocumented.** Funnel y-axes with 1–3 unlabeled ticks and no axis title (`sglt2-hf`, `dta` Deeks); LOO/ranking x-axes with only `[lo,1,hi]` or `[lo,hi]` ticks and no null line; bubble-size = weight, rankogram opacity×height, GOSH clouds — all unlabeled. Robustness asserted in prose, not drawn (`dta` per-study table instead of paired forest; `dta` meta-reg text-only).

Resolved since audit: the top assurance ribbon and live re-run pattern are now suite-level requirements. Still open against benchmarks: more at-a-glance verdict objects and live re-parameterization controls (CI/estimand toggles), with provenance surfaced close to each result rather than only in prose.

---

## 2. Design tokens (offline, dependency-free)

Ship as a single `tokens.css` `:root` block + a JS mirror `TOKENS` object. No web fonts beyond the system serif already in use.

```css
:root{
  /* Type — existing serif, modular scale 1.20 */
  --t-font-serif: Georgia, "Iowan Old Style", "Times New Roman", serif;
  --t-font-mono: "SFMono-Regular", Consolas, monospace; /* numerals in readouts */
  --t-fs-fig-title: 19px;  /* assertive figure claim */
  --t-fs-fig-sub:   14px;  /* estimand / n */
  --t-fs-axis:      12px;
  --t-fs-annot:     11px;  /* subordinate notes */
  --t-fs-tick:      10.5px;
  --t-lh-tight: 1.25; --t-lh-body: 1.5;
  --t-fw-title: 600; --t-fw-body: 400;

  /* Ink */
  --c-ink:    #1a1a1a;   /* primary text, data marks */
  --c-ink-2:  #555a5f;   /* axis labels, subtitles */
  --c-annot:  #7a8086;   /* accent grey — annotations, leader lines */
  --c-grid:   #e7e9ec;   /* hairline gridlines */
  --c-axis:   #c2c6cb;   /* axis spines */
  --c-null:   #9aa0a6;   /* no-effect reference line */
  --c-paper:  #ffffff; --c-panel: #fafbfc;

  /* Categorical — colorblind-safe (Okabe-Ito), max 7 series */
  --cat-1:#0072B2; --cat-2:#E69F00; --cat-3:#009E73; --cat-4:#CC79A7;
  --cat-5:#56B4E9; --cat-6:#D55E00; --cat-7:#000000;

  /* Sequential (low->high), perceptually ordered, CB-safe */
  --seq-1:#f0f4f8; --seq-2:#cfe0ec; --seq-3:#9dc3df; --seq-4:#5b9bcd;
  --seq-5:#2f74b3; --seq-6:#1a4f88;

  /* Semantic */
  --c-favours:   #0072B2;  /* favours treatment side */
  --c-against:   #D55E00;  /* favours control side */
  --c-estimate:  #1a1a1a;  /* point/diamond — eye lands here first */
  --c-pi:        #b9c2cb;  /* prediction interval band (lighter than CI) */
  --c-ci:        #1a1a1a;  /* CI whisker (darker = narrower claim) */
  --c-verdict-ok:#1f9d57; --c-verdict-warn:#E69F00; --c-verdict-bad:#D55E00;

  /* Spacing (4px base) */
  --s-1:4px; --s-2:8px; --s-3:12px; --s-4:16px; --s-6:24px; --s-8:32px;
  --fig-pad-l:120px; /* room for direct study labels */ --fig-pad-r:96px; /* room for value readout */
  --fig-pad-t:56px;  /* title+subtitle */ --fig-pad-b:40px;

  /* Hairlines */
  --hair-grid:1px; --hair-axis:1px; --hair-null:1.25px; /* null dashed 4 3 */
  --box-min:6px; --box-max:22px; /* weight-scaled marker side */
  --whisker-w:1.25px; --diamond-h:16px;
}
```

Rules: gridlines `--c-grid` at `--hair-grid`, behind data, no fill. Axis spine bottom/left only. Null line dashed `4 3` in `--c-null`. Annotation type always `--t-fs-annot` / `--c-annot` (never competes with data ink). Never use red/green as the *only* categorical distinction.

---

## 3. Chart-kit — reusable SVG primitives

One module `chartkit.js`, pure functions `render<Name>(svgEl, data, opts)`, no dependencies. Shared internals: `scaleLinear`/`scaleLog`, `niceTicks(min,max,~6)`, `addAnnotation(layer,{x,y,text,leader})`, `addTooltip(el,html)`, responsive `viewBox` + `preserveAspectRatio="xMidYMid meet"`. **Every primitive ships all four NYT-grade defaults: direct labels (no detached legend where avoidable), an annotation layer, a hover tooltip, and a responsive viewBox.**

| Primitive | Serves the inference | NYT-grade default it must ship |
|---|---|---|
| `renderForest` | pooled effect + study detail + heterogeneity | direct study labels left, weight-scaled boxes, **diamond + lighter PI band**, dashed null line, in-plot pooled callout, favours-X/Y cue |
| `renderFunnel` | small-study / publication bias | SE y-axis with 4–5 labeled ticks + rotated title, **0.05/0.01/0.001 significance contour bands** (labeled), Egger/PET-PEESE line + p annotated in situ, flag highest-leverage point |
| `renderDensity` | posterior / prior-sensitivity | shaded HPD, median + CrI direct-labeled, overlay multiple priors with categorical palette |
| `renderSROC` | threshold-confounded DTA | summary point with **solid 95% CI ellipse vs dashed 95% PI ellipse** (in-plot legend), study points sized by weight, in-plot Se/Sp callout |
| `renderPairedForest` | DTA study-level Se \| Sp | two side-by-side panels, point+CP whisker per study, summary diamond row, striping |
| `renderNetwork` | NMA geometry | node radius ∝ n, edge width ∝ #trials, direct node labels, multi-arm cue |
| `renderRanking` | NMA SUCRA/league | **PI band behind CrI whisker**, 5–6 log-nice ticks, OR=1 distinct, POTH annotation; league cells render CrI inline (two-line) + shade if CrI excludes 1 |
| `renderRankogram` | rank uncertainty | **height-only** P(rank) encoding, labeled `P(rank) 0–1` axis (drop opacity-doubling) |
| `renderCalibration` | Bayesian/risk-model fit | 45° reference, binned obs-vs-pred with CI, Brier/slope annotation |
| `renderCEplane` | cost-effectiveness | quadrant labels, WTP threshold line(s), ICER callout, density of PSA cloud, CEAC companion |
| `renderKM` | survival | step function + CI band, **at-risk table under x-axis**, median + RMST(τ*) annotation, censoring ticks |
| `renderBubble` | meta-regression | **bubble area = weight (with size legend)**, WLS fitted line + shaded CI band, slope-per-unit + p annotated, direct-labeled line |
| `renderBaujat` | influence | x=Q-contribution, y=Δpooled, label high-influence studies in situ |
| `renderDrapery` | p-value function / robustness over α | confidence curve, MID + significance threshold crossings marked |
| `renderLOO` | leave-one-out stability | **fixed null line at no-effect**, nice ticks (0.7,0.8,0.9,1.0), per-row omitted-trial label, range callout |

Shared annotation contract: pooled/summary estimate called out **on the canvas at the mark** with value+CI; one high-leverage study flagged with a subordinate note; directional cue on the null line; threshold (significance / MID) marked. Leader lines thin `--c-annot`, never cross data.

---

## 4. Analytical-density target — minimum battery to BE the paper

Target **8–15 distinct analyses** (each changes a belief; restyled duplicates do not count). Mandatory arc for every capsule: **estimate → stability → bias → boundary.**

**Universal core (every capsule, ≥6):**
1. Primary pooled estimate (in-plot callout)
2. Forest with study-level detail **+ prediction interval**
3. Heterogeneity decomposition: τ² with Q-profile CI **+** I² with CI (not bare numbers)
4. Publication-bias panel: contour-enhanced funnel **+** Egger/PET-PEESE
5. Leave-one-out **with null line**
6. Subgroup or meta-regression **bubble** (drawn, not text)

**Add per method family:**
- **Pairwise / RCT-pooling** (`sglt2-hf`,`rct`,`fragility`): + cumulative-over-time forest, + Baujat/GOSH (k>10), + drapery/fragility-index curve. Target 9–12.
- **NMA** (`nma`): + network geometry, + ranking forest with PI, + rankogram (height-only), + comparison-adjusted funnel (Egger-extended, k<10 "low power" note not hidden), + league table with inline CrI. Target 10–13.
- **DTA** (`dta`): + SROC with CI vs PI ellipses, + **paired Se\|Sp forest**, + covariate **bubble** meta-reg, + Deeks funnel with Egger p in-plot, + Fagan nomogram. Target 9–12.
- **Bayesian** (`bayesian`): + prior×posterior overlay, + prior-sensitivity walk, + MCMC trace/R̂-ESS panel, + calibration. Target 8–11.
- **Survival** (`survival`,`markov`): + KM with at-risk table, + RMST(τ*) panel, + Schoenfeld/PH check, + state-occupancy (Markov). Target 8–11.
- **Cost-effectiveness** (`ce-plane`,`markov`): + CE-plane with PSA cloud, + CEAC, + tornado/one-way sensitivity, + Markov trace. Target 8–11.
- **DiD / causal** (`did`): + event-study plot with pre-trend, + parallel-trends check, + placebo/permutation. Target 7–10.

Audit-era shortfalls to remeasure and close first: `fragility` (1 plot → ≥8), `did` (2 → ≥7), `ce-plane`/`rct` (4 → ≥8).

---

## 5. Reference component — `renderForest`

Target-quality exemplar. Self-contained, no dependencies, accessible, responsive.

```js
/**
 * renderForest(svgEl, studies, opts) — NYT-grade SVG forest plot.
 * studies: [{ label, est, lo, hi, weight }]  (effect on natural scale; ratio measures pass opts.log=true)
 * opts: { measure:'HR', pooled:{est,lo,hi,pi_lo,pi_hi}, log:true,
 *         null:1, claim:'Pooled HR 0.77 (0.72–0.83); PI excludes 1.0',
 *         estimand:'Hazard ratio, random-effects (REML)',
 *         favoursLow:'favours treatment', favoursHigh:'favours control',
 *         flag:{label:'SOLOIST-WHF', note:'widest CI — highest leverage'} }
 */
function renderForest(svgEl, studies, opts = {}) {
  const NS = 'http://www.w3.org/2000/svg';
  const o = Object.assign({ log:false, null:1, measure:'effect', width:760,
    rowH:26, padL:150, padR:104, padT:60, padB:46 }, opts);
  const T = getComputedStyle(document.documentElement);
  const tok = (n,f)=> (T.getPropertyValue(n).trim() || f);
  const C = { ink:tok('--c-ink','#1a1a1a'), ink2:tok('--c-ink-2','#555'),
    annot:tok('--c-annot','#7a8086'), grid:tok('--c-grid','#e7e9ec'),
    axis:tok('--c-axis','#c2c6cb'), nul:tok('--c-null','#9aa0a6'),
    est:tok('--c-estimate','#1a1a1a'), pi:tok('--c-pi','#b9c2cb') };
  const n = studies.length;
  const plotH = n*o.rowH, W = o.width, H = o.padT + plotH + (o.pooled?44:0) + o.padB;
  const x0 = o.padL, x1 = W - o.padR;

  // --- scale (log for ratio measures) ---
  const all = studies.flatMap(s=>[s.lo,s.hi])
    .concat(o.pooled?[o.pooled.lo,o.pooled.hi,o.pooled.pi_lo,o.pooled.pi_hi]:[])
    .concat([o.null]).filter(v=>v!=null && (!o.log || v>0));
  const tx = v => o.log ? Math.log(v) : v;
  let dmin = Math.min(...all.map(tx)), dmax = Math.max(...all.map(tx));
  const pad=(dmax-dmin)*0.06; dmin-=pad; dmax+=pad;
  const sx = v => x0 + (tx(v)-dmin)/(dmax-dmin)*(x1-x0);
  const wmax = Math.max(...studies.map(s=>s.weight||1));
  const bmin=+tok('--box-min',6), bmax=+tok('--box-max',22);
  const boxSide = w => bmin + Math.sqrt((w||1)/wmax)*(bmax-bmin);

  // --- svg shell ---
  while (svgEl.firstChild) svgEl.removeChild(svgEl.firstChild);
  svgEl.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svgEl.setAttribute('preserveAspectRatio','xMidYMid meet');
  svgEl.setAttribute('role','img');
  svgEl.setAttribute('font-family', tok('--t-font-serif','Georgia,serif'));
  const aria = `Forest plot, ${o.measure}. ${o.claim||''} ${n} studies.`;
  svgEl.setAttribute('aria-label', aria);
  const el=(t,a={},p=svgEl)=>{const e=document.createElementNS(NS,t);
    for(const k in a) e.setAttribute(k,a[k]); p.appendChild(e); return e;};
  const txt=(x,y,s,a={})=>{const e=el('text',Object.assign({x,y},a));e.textContent=s;return e;};

  // --- title (assertion) + subtitle (estimand) ---
  txt(x0, 24, o.claim || `Forest plot of ${o.measure}`,
    {'font-size':tok('--t-fs-fig-title','19px'),'font-weight':tok('--t-fw-title','600'),fill:C.ink});
  if (o.estimand) txt(x0, 42, o.estimand,
    {'font-size':tok('--t-fs-fig-sub','14px'),fill:C.ink2});

  // --- gridlines + x ticks (nice, log-aware) ---
  const ticks = niceForestTicks(o.log?Math.exp(dmin):dmin, o.log?Math.exp(dmax):dmax, o.log);
  const yTop=o.padT, yBot=o.padT+plotH;
  ticks.forEach(v=>{ const x=sx(v);
    el('line',{x1:x,x2:x,y1:yTop,y2:yBot,stroke:C.grid,'stroke-width':tok('--hair-grid','1')});
    txt(x, yBot+16, fmt(v), {'font-size':tok('--t-fs-tick','10.5px'),fill:C.ink2,'text-anchor':'middle'});
  });
  // null reference (eye-distinct, dashed)
  const xn=sx(o.null);
  el('line',{x1:xn,x2:xn,y1:yTop,y2:yBot,stroke:C.nul,'stroke-width':tok('--hair-null','1.25'),'stroke-dasharray':'4 3'});

  // --- study rows ---
  studies.forEach((s,i)=>{
    const cy = yTop + i*o.rowH + o.rowH/2;
    const g = el('g',{tabindex:'0',role:'listitem',
      'aria-label':`${s.label}: ${o.measure} ${fmt(s.est)} (${fmt(s.lo)} to ${fmt(s.hi)}), weight ${(s.weight||0)}`});
    addTip(g, `<b>${s.label}</b><br>${o.measure} ${fmt(s.est)} (${fmt(s.lo)}–${fmt(s.hi)})<br>weight ${pct(s.weight,wmax)}`);
    txt(x0-10, cy+3.5, s.label, {'font-size':tok('--t-fs-axis','12px'),fill:C.ink,'text-anchor':'end'},g);
    el('line',{x1:sx(s.lo),x2:sx(s.hi),y1:cy,y2:cy,stroke:C.ink,'stroke-width':tok('--whisker-w','1.25')},g);
    const sd=boxSide(s.weight);
    el('rect',{x:sx(s.est)-sd/2,y:cy-sd/2,width:sd,height:sd,fill:C.est},g);
    txt(x1+12, cy+3.5, `${fmt(s.est)} (${fmt(s.lo)}–${fmt(s.hi)})`,
      {'font-size':tok('--t-fs-tick','10.5px'),fill:C.ink2},g);
  });

  // --- pooled diamond + prediction-interval band ---
  if (o.pooled){
    const p=o.pooled, cy=yBot+24;
    if (p.pi_lo!=null && p.pi_hi!=null)
      el('line',{x1:sx(p.pi_lo),x2:sx(p.pi_hi),y1:cy,y2:cy,
        stroke:C.pi,'stroke-width':'7','stroke-linecap':'round'}); // PI = lighter, wider, behind
    const dh=+tok('--diamond-h',16)/2, xe=sx(p.est);
    el('polygon',{points:`${sx(p.lo)},${cy} ${xe},${cy-dh} ${sx(p.hi)},${cy} ${xe},${cy+dh}`,fill:C.est});
    // in-situ callout at the diamond
    addAnnot(svgEl, xe, cy-dh-6, `Pooled ${fmt(p.est)} (${fmt(p.lo)}–${fmt(p.hi)})`, C.annot, 'middle');
  }

  // --- directional cue + leverage flag ---
  if (o.favoursLow) txt(xn-8, yBot+32, '◂ '+o.favoursLow,{'font-size':tok('--t-fs-annot','11px'),fill:C.annot,'text-anchor':'end'});
  if (o.favoursHigh) txt(xn+8, yBot+32, o.favoursHigh+' ▸',{'font-size':tok('--t-fs-annot','11px'),fill:C.annot});
  if (o.flag){ const idx=studies.findIndex(s=>s.label===o.flag.label);
    if(idx>=0){ const fy=yTop+idx*o.rowH+o.rowH/2;
      addAnnot(svgEl, x1+8, fy-10, o.flag.note, C.annot, 'start', {x:x1, y:fy}); } }

  // --- axis spine ---
  el('line',{x1:x0,x2:x1,y1:yBot,y2:yBot,stroke:C.axis,'stroke-width':tok('--hair-axis','1')});
  return svgEl;

  // ---- helpers (scoped) ----
  function fmt(v){ if(v==null)return ''; const a=Math.abs(v);
    return a>=100?v.toFixed(0):a>=10?v.toFixed(1):v.toFixed(2); }
  function pct(w,m){ return m?Math.round((w/studies.reduce((t,s)=>t+(s.weight||0),0))*100)+'%':'—'; }
  function addAnnot(p,x,y,s,col,anchor,leaderTo){
    if(leaderTo) el('line',{x1:leaderTo.x,y1:leaderTo.y,x2:x,y2:y+3,stroke:col,'stroke-width':'0.75'},p);
    const t=txt(x,y,s,{'font-size':tok('--t-fs-annot','11px'),fill:col});
    if(anchor) t.setAttribute('text-anchor',anchor); }
  function addTip(g,html){
    g.addEventListener('mouseenter',e=>showTip(e,html));
    g.addEventListener('mousemove',e=>moveTip(e));
    g.addEventListener('mouseleave',hideTip);
    g.addEventListener('focus',e=>showTip(e,html));
    g.addEventListener('blur',hideTip); }
}

// shared tick + tooltip helpers (chartkit.js scope) ---------------------------
function niceForestTicks(min,max,log){
  if(log){ const out=[]; const lo=Math.floor(Math.log2(min)), hi=Math.ceil(Math.log2(max));
    for(let p=lo;p<=hi;p++){const v=Math.pow(2,p); if(v>=min*0.9&&v<=max*1.1)out.push(v);}
    if(out.length<3)[0.5,1,2].forEach(v=>{if(v>=min&&v<=max&&!out.includes(v))out.push(v);});
    return out.sort((a,b)=>a-b); }
  const span=max-min, step=Math.pow(10,Math.floor(Math.log10(span)))*
    ([1,2,5,10].find(s=>span/(s*Math.pow(10,Math.floor(Math.log10(span))))<=6)||10);
  const out=[]; for(let v=Math.ceil(min/step)*step; v<=max; v+=step) out.push(+v.toFixed(6)); return out;
}
let _tip;
function showTip(e,html){ _tip=_tip||Object.assign(document.body.appendChild(document.createElement('div')),
  {className:'ck-tip'}); _tip.style.cssText='position:fixed;pointer-events:none;background:#1a1a1a;color:#fff;'+
  'font:11px Georgia,serif;padding:6px 8px;border-radius:4px;z-index:9999;max-width:240px';
  _tip.innerHTML=html; _tip.style.display='block'; moveTip(e); }
function moveTip(e){ if(_tip){ _tip.style.left=(e.clientX+12)+'px'; _tip.style.top=(e.clientY+12)+'px'; } }
function hideTip(){ if(_tip) _tip.style.display='none'; }
```

Properties met: assertive title from `opts.claim`; weight-scaled `√`-area boxes; diamond pooled estimate; **lighter/wider PI band behind the CI** (G2); dashed eye-distinct null line; hairline gridlines from tokens; nice log/linear ticks (G3); in-situ pooled callout + leverage flag + favours-X/Y cue; keyboard-focusable rows with `aria-label` + hover/focus tooltip; responsive `viewBox`.

---

## 6. Rollout — 40 capsules onto the shared kit

**Constraint-safe mechanism (stays 100% offline / no CDN):** `chartkit.js` + `tokens.css` are **inlined**, not linked. As of 2026-06-04, all 40 capsule files include the inlined token and ChartKit blocks. Each capsule remains a single self-contained HTML file; future build automation should read the two source files and inject them between sentinel comments `<!-- CHARTKIT:BEGIN -->...<!-- CHARTKIT:END -->`. Re-running should replace only that block (idempotent: grep for the sentinel before inserting, per the idempotent-edits lesson). No runtime fetch, no external `<script src>`.

**Per-capsule refactor (mechanical, low-risk):**
1. Inline the kit block (build step).
2. Replace each bespoke `draw*` call with the matching `render*` and a small data adapter `toForestData(...)` — keep the old function as a `--dry-run` fallback until parity is confirmed.
3. Rewrite every figure title as a live-computed assertion (G1) and pass `pooled.pi_lo/pi_hi`, τ²/I² CIs, inline CrIs (G2).
4. Add `viewBox` + remove any fixed `width/height` px (responsiveness).
5. Visual-diff old vs new with the existing browser harness (`browser_rotator.py`, sequential, 60s timeout); accept only if every prior datum is still drawn.

**Batching:** 3–5 capsules per batch, commit after each (workflow rule). Start with the two highest-defect-density lifts (`did` 38, `ce-plane` 38, `rct` 41) where new primitives add the most score, then the mid-tier, then polish `sglt2-hf`/`nma`.

**Test gate:** one integration test per primitive (`renders N study rows`, `PI band present when pi_lo set`, `null line at opts.null`, `aria-label non-empty`) + a contract test that every capsule's adapter produces the kit's expected field names (prevents the field-name silent-corruption class). Run after each batch, report pass/fail counts before "done."

**3 quick wins (apply to all 40 in one sweep, no new primitives):**
1. **Title→claim codemod** (G1): replace structural `<h*>`/`aria-label` figure headings with computed assertions from the already-present numbers. Highest score-per-effort; fixes the most-repeated major defect across every capsule.
2. **PI band + inline-CrI patch** (G2): add the lighter PI band behind existing forest diamonds and render `nma` league-table CrIs inline from the values already stored in `title` tooltips — pure render change, no new data.
3. **Axis-tick + null-line fix** (G3): swap `[lo,1,hi]`/`[lo,hi]` tick arrays for `niceForestTicks(...)` and add the fixed null reference line to every funnel/LOO/ranking axis (`sglt2-hf` funnel y-title, `dta` Deeks ticks, LOO null line).

Files of record: `chartkit.js`, `tokens.css`, `inline-kit.js` (build), `test/chartkit.spec.js` (primitive + contract tests).
