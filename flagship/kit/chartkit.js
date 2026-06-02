/* e156 capsule chart-kit — offline, dependency-free SVG primitives.
 * Exposes window.ChartKit. See docs/capsule-visual-standard.md §3 / §5.
 * First primitive: renderForest (the reference exemplar). More to follow.
 */
(function (global) {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';

  function tokGetter() {
    var T = getComputedStyle(document.documentElement);
    return function (n, f) { return (T.getPropertyValue(n).trim() || f); };
  }

  function fmt(v) {
    if (v == null || !isFinite(v)) return '';
    var a = Math.abs(v);
    return a >= 100 ? v.toFixed(0) : a >= 10 ? v.toFixed(1) : v.toFixed(2);
  }

  // Nice ticks: log-aware (ratio scales) or linear.
  function niceForestTicks(min, max, log) {
    var out = [], v, p;
    if (log) {
      // candidate ratio ticks spanning the range
      var cands = [0.1,0.125,0.2,0.25,0.33,0.5,0.67,0.8,1,1.25,1.5,2,2.5,3,4,5,8,10];
      for (var i = 0; i < cands.length; i++) {
        v = cands[i];
        if (v >= min * 0.97 && v <= max * 1.03) out.push(v);
      }
      if (out.indexOf(1) === -1 && min <= 1 && max >= 1) out.push(1);
      // thin to ~6
      while (out.length > 7) { out = out.filter(function (_, k) { return k % 2 === 0; }); }
      return out.sort(function (a, b) { return a - b; });
    }
    var span = max - min;
    if (span <= 0) return [min];
    var target = 6, step = Math.pow(10, Math.floor(Math.log10(span / target)));
    var err = span / target / step;
    if (err >= 7.5) step *= 10; else if (err >= 3) step *= 5; else if (err >= 1.5) step *= 2;
    for (v = Math.ceil(min / step) * step; v <= max + step * 1e-6; v += step) out.push(+v.toFixed(6));
    return out;
  }

  // Shared tooltip (one element, reused)
  var _tip;
  function showTip(e, html) {
    if (!_tip) {
      _tip = document.createElement('div');
      _tip.className = 'ck-tip';
      document.body.appendChild(_tip);
    }
    _tip.style.cssText = 'position:fixed;pointer-events:none;background:#1a1a1a;color:#fff;' +
      'font:11px/1.4 Georgia,serif;padding:6px 9px;border-radius:4px;z-index:9999;max-width:260px;' +
      'box-shadow:0 2px 8px rgba(0,0,0,.25)';
    _tip.innerHTML = html; _tip.style.display = 'block'; moveTip(e);
  }
  function moveTip(e) { if (_tip) { _tip.style.left = (e.clientX + 13) + 'px'; _tip.style.top = (e.clientY + 13) + 'px'; } }
  function hideTip() { if (_tip) _tip.style.display = 'none'; }

  /**
   * renderForest(svgEl, studies, opts)
   * studies: [{ label, est, lo, hi, weight }]  (natural scale; ratio measures pass opts.log=true)
   * opts: { measure, pooled:{est,lo,hi,pi_lo,pi_hi}, log, null, claim, estimand,
   *         favoursLow, favoursHigh, flag:{label,note} }
   */
  function renderForest(svgEl, studies, opts) {
    opts = opts || {};
    var o = Object.assign({ log: false, null: 1, measure: 'effect', width: 900,
      rowH: 28, padL: 205, padR: 134, padT: 62, padB: 54 }, opts);
    var tok = tokGetter();
    // numeric token: CSS values carry units ("6px") so unary + gives NaN — parse it.
    var ntok = function (n, f) { var v = parseFloat(tok(n, '')); return isFinite(v) ? v : f; };
    var C = {
      ink: tok('--c-ink', '#1a1a1a'), ink2: tok('--c-ink-2', '#555a5f'),
      annot: tok('--c-annot', '#7a8086'), grid: tok('--c-grid', '#e7e9ec'),
      axis: tok('--c-axis', '#c2c6cb'), nul: tok('--c-null', '#9aa0a6'),
      est: tok('--c-estimate', '#1a1a1a'), pi: tok('--c-pi', '#b9c2cb')
    };
    var n = studies.length;
    var W = o.width, x0 = o.padL, x1 = W - o.padR, yTop = o.padT;
    var gap = o.pooled ? 16 : 0;                 // separation before the overall row
    var studyBot = yTop + n * o.rowH;
    var pooledCy = studyBot + gap + o.rowH / 2;
    var yBot = o.pooled ? (studyBot + gap + o.rowH) : studyBot;
    var H = yBot + o.padB;

    var tx = function (v) { return o.log ? Math.log(v) : v; };
    var all = [];
    studies.forEach(function (s) { all.push(s.lo, s.hi); });
    if (o.pooled) all.push(o.pooled.lo, o.pooled.hi, o.pooled.pi_lo, o.pooled.pi_hi);
    if (o.refLine && o.refLine.x != null) all.push(o.refLine.x);
    all.push(o.null);
    all = all.filter(function (v) { return v != null && isFinite(v) && (!o.log || v > 0); }).map(tx);
    var dmin = Math.min.apply(null, all), dmax = Math.max.apply(null, all);
    var pad = (dmax - dmin) * 0.06 || 0.1; dmin -= pad; dmax += pad;
    var sx = function (v) { return x0 + (tx(v) - dmin) / (dmax - dmin) * (x1 - x0); };
    var wmax = Math.max.apply(null, studies.map(function (s) { return s.weight || 1; }));
    var wsum = studies.reduce(function (t, s) { return t + (s.weight || 0); }, 0);
    var bmin = ntok('--box-min', 6), bmax = ntok('--box-max', 22);
    var boxSide = function (w) { return bmin + Math.sqrt((w || 1) / wmax) * (bmax - bmin); };

    while (svgEl.firstChild) svgEl.removeChild(svgEl.firstChild);
    svgEl.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svgEl.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svgEl.setAttribute('role', 'img');
    svgEl.setAttribute('font-family', tok('--t-font-serif', 'Georgia,serif'));
    svgEl.setAttribute('aria-label', 'Forest plot, ' + o.measure + '. ' + (o.claim || '') + ' ' + n + ' studies.');

    function el(t, a, p) {
      var e = document.createElementNS(NS, t); a = a || {};
      for (var k in a) e.setAttribute(k, a[k]); (p || svgEl).appendChild(e); return e;
    }
    function txt(x, y, s, a, p) {
      var e = el('text', Object.assign({ x: x, y: y }, a || {}), p); e.textContent = s; return e;
    }
    function pct(w) { return wsum ? Math.round((w / wsum) * 100) + '%' : '—'; }
    function addAnnot(x, y, s, anchor, leaderTo, p) {
      if (leaderTo) el('line', { x1: leaderTo.x, y1: leaderTo.y, x2: x, y2: y + 3, stroke: C.annot, 'stroke-width': '0.75' }, p);
      var t = txt(x, y, s, { 'font-size': tok('--t-fs-annot', '11px'), fill: C.annot }, p);
      if (anchor) t.setAttribute('text-anchor', anchor);
    }
    function addTip(g, html) {
      g.addEventListener('mouseenter', function (e) { showTip(e, html); });
      g.addEventListener('mousemove', moveTip);
      g.addEventListener('mouseleave', hideTip);
      g.addEventListener('focus', function (e) { showTip(e, html); });
      g.addEventListener('blur', hideTip);
    }

    // title (assertion) + subtitle (estimand)
    txt(x0, 24, o.claim || ('Forest plot of ' + o.measure),
      { 'font-size': tok('--t-fs-fig-title', '19px'), 'font-weight': tok('--t-fw-title', '600'), fill: C.ink });
    if (o.estimand) txt(x0, 43, o.estimand, { 'font-size': tok('--t-fs-fig-sub', '14px'), fill: C.ink2 });

    // gridlines + ticks
    var ticks = niceForestTicks(o.log ? Math.exp(dmin) : dmin, o.log ? Math.exp(dmax) : dmax, o.log);
    ticks.forEach(function (v) {
      var x = sx(v);
      el('line', { x1: x, x2: x, y1: yTop, y2: yBot, stroke: C.grid, 'stroke-width': ntok('--hair-grid', 1) });
      txt(x, yBot + 16, fmt(v), { 'font-size': tok('--t-fs-tick', '10.5px'), fill: C.ink2, 'text-anchor': 'middle' });
    });
    // null reference (dashed, eye-distinct)
    var xn = sx(o.null);
    el('line', { x1: xn, x2: xn, y1: yTop, y2: yBot, stroke: C.nul, 'stroke-width': ntok('--hair-null', 1.25), 'stroke-dasharray': '4 3' });
    // optional secondary reference line (e.g. overall pooled, for LOO / cumulative)
    if (o.refLine && o.refLine.x != null) {
      var rx = sx(o.refLine.x);
      el('line', { x1: rx, x2: rx, y1: yTop, y2: yBot, stroke: C.est, 'stroke-width': '1', 'stroke-dasharray': '2 3', opacity: '0.5' });
      if (o.refLine.label) {
        var rl = txt(rx, yTop - 5, o.refLine.label, { 'font-size': tok('--t-fs-annot', '11px'), fill: C.annot, 'text-anchor': 'middle' });
        rl.setAttribute('font-style', 'italic');
      }
    }

    // study rows. Interactive mode: pass opts.onToggle(index, study) and each
    // study's `included` flag — excluded studies render muted and rows become
    // toggle buttons (click / Enter / Space), a superset of a display forest.
    var interactive = typeof o.onToggle === 'function';
    studies.forEach(function (s, i) {
      var cy = yTop + i * o.rowH + o.rowH / 2;
      var inc = s.included !== false;
      var ga = { tabindex: '0', 'data-i': String(i) };
      if (interactive) {
        ga.role = 'button'; ga['aria-pressed'] = String(inc);
        ga['aria-label'] = s.label + ': ' + o.measure + ' ' + fmt(s.est) + ' (' + fmt(s.lo) + ' to ' + fmt(s.hi) + '). ' +
          (inc ? 'Included — activate to exclude.' : 'Excluded — activate to include.');
      } else {
        ga.role = 'listitem';
        ga['aria-label'] = s.label + ': ' + o.measure + ' ' + fmt(s.est) + ' (' + fmt(s.lo) + ' to ' + fmt(s.hi) + '), weight ' + pct(s.weight);
      }
      var g = el('g', ga);
      if (!inc) g.setAttribute('opacity', '0.36');
      if (interactive) {
        g.style.cursor = 'pointer';
        g.addEventListener('click', function () { o.onToggle(i, s); });
        g.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') { e.preventDefault(); o.onToggle(i, s); }
        });
      }
      addTip(g, '<b>' + s.label + '</b><br>' + o.measure + ' ' + fmt(s.est) + ' (' + fmt(s.lo) + '–' + fmt(s.hi) + ')<br>weight ' + pct(s.weight) + (interactive ? '<br><i>' + (inc ? 'click to exclude' : 'click to include') + '</i>' : ''));
      txt(x0 - 10, cy + 3.5, s.label, { 'font-size': tok('--t-fs-axis', '12px'), fill: C.ink, 'text-anchor': 'end' }, g);
      el('line', { x1: sx(s.lo), x2: sx(s.hi), y1: cy, y2: cy, stroke: C.ink, 'stroke-width': ntok('--whisker-w', 1.25) }, g);
      var sd = boxSide(s.weight);
      el('rect', { x: sx(s.est) - sd / 2, y: cy - sd / 2, width: sd, height: sd, fill: C.est }, g);
      txt(x1 + 12, cy + 3.5, fmt(s.est) + ' (' + fmt(s.lo) + '–' + fmt(s.hi) + ')',
        { 'font-size': tok('--t-fs-tick', '10.5px'), fill: C.ink2 }, g);
    });

    // pooled: a clean labeled "Overall" row (PI band behind diamond + readout)
    if (o.pooled) {
      var p = o.pooled, cy2 = pooledCy;
      el('line', { x1: x0, x2: x1, y1: studyBot + gap / 2, y2: studyBot + gap / 2, stroke: C.grid, 'stroke-width': ntok('--hair-grid', 1) });
      if (p.pi_lo != null && p.pi_hi != null)
        el('line', { x1: sx(p.pi_lo), x2: sx(p.pi_hi), y1: cy2, y2: cy2, stroke: C.pi, 'stroke-width': '7', 'stroke-linecap': 'round' });
      var dh = ntok('--diamond-h', 16) / 2, xe = sx(p.est);
      el('polygon', { points: sx(p.lo) + ',' + cy2 + ' ' + xe + ',' + (cy2 - dh) + ' ' + sx(p.hi) + ',' + cy2 + ' ' + xe + ',' + (cy2 + dh), fill: C.est });
      txt(x0 - 10, cy2 + 3.5, o.pooledLabel || 'Overall · random-effects',
        { 'font-size': tok('--t-fs-axis', '12px'), 'font-weight': '600', fill: C.ink, 'text-anchor': 'end' });
      txt(x1 + 12, cy2 + 3.5, fmt(p.est) + ' (' + fmt(p.lo) + '–' + fmt(p.hi) + ')',
        { 'font-size': tok('--t-fs-tick', '10.5px'), 'font-weight': '600', fill: C.ink });
      if (p.pi_lo != null)                       // PI numbers under the readout (band shows it too)
        txt(x1 + 12, cy2 + 16, 'PI ' + fmt(p.pi_lo) + '–' + fmt(p.pi_hi),
          { 'font-size': tok('--t-fs-annot', '11px'), fill: C.annot });
    }

    // directional cues (below the axis ticks)
    if (o.favoursLow) txt(xn - 8, yBot + 34, '◂ ' + o.favoursLow, { 'font-size': tok('--t-fs-annot', '11px'), fill: C.annot, 'text-anchor': 'end' });
    if (o.favoursHigh) txt(xn + 8, yBot + 34, o.favoursHigh + ' ▸', { 'font-size': tok('--t-fs-annot', '11px'), fill: C.annot });

    // leverage flag — short italic note tucked under the flagged row (no clip, no overlap)
    if (o.flag) {
      var idx = studies.findIndex(function (s) { return s.label === o.flag.label; });
      if (idx >= 0) {
        var fy = yTop + idx * o.rowH + o.rowH / 2;
        var fn = txt(x0, fy + 13, o.flag.note, { 'font-size': tok('--t-fs-annot', '11px'), fill: C.annot });
        fn.setAttribute('font-style', 'italic');
      }
    }

    // axis spine
    el('line', { x1: x0, x2: x1, y1: yBot, y2: yBot, stroke: C.axis, 'stroke-width': ntok('--hair-axis', 1) });
    return svgEl;
  }

  /**
   * renderFunnel(svgEl, points, opts) — contour-enhanced funnel plot.
   * points: [{ label, x, se }]  (x = effect; log scale for ratios via opts.log)
   * opts: { measure, log, pooled (effect, same scale as x), egger:{p, intercept},
   *         width, height }
   */
  function renderFunnel(svgEl, points, opts) {
    opts = opts || {};
    var o = Object.assign({ log: false, measure: 'effect', width: 560, height: 360,
      padL: 70, padR: 134, padT: 56, padB: 50 }, opts);
    var tok = tokGetter();
    var ntok = function (n, f) { var v = parseFloat(tok(n, '')); return isFinite(v) ? v : f; };
    var C = { ink: tok('--c-ink', '#1a1a1a'), ink2: tok('--c-ink-2', '#555a5f'), annot: tok('--c-annot', '#7a8086'),
      grid: tok('--c-grid', '#e7e9ec'), axis: tok('--c-axis', '#c2c6cb'), nul: tok('--c-null', '#9aa0a6'),
      est: tok('--c-estimate', '#1a1a1a'), s1: tok('--seq-1', '#f0f4f8'), s2: tok('--seq-2', '#cfe0ec') };
    var W = o.width, H = o.height, x0 = o.padL, x1 = W - o.padR, yT = o.padT, yB = H - o.padB;
    var pooled = (o.pooled != null) ? o.pooled : 0, NULLE = 0;
    var maxSE = Math.max.apply(null, points.map(function (p) { return p.se; })) * 1.14 || 1;
    var effs = points.map(function (p) { return p.x; }).concat([pooled - 1.96 * maxSE, pooled + 1.96 * maxSE, NULLE]);
    var dmin = Math.min.apply(null, effs) - 0.04, dmax = Math.max.apply(null, effs) + 0.04;
    var sx = function (e) { return x0 + (e - dmin) / (dmax - dmin) * (x1 - x0); };
    var sy = function (se) { return yT + (se / maxSE) * (yB - yT); };

    while (svgEl.firstChild) svgEl.removeChild(svgEl.firstChild);
    svgEl.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svgEl.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svgEl.setAttribute('role', 'img');
    svgEl.setAttribute('font-family', tok('--t-font-serif', 'Georgia,serif'));
    svgEl.setAttribute('aria-label', 'Contour-enhanced funnel plot. ' + (o.claim || '') + ' ' + points.length + ' studies.');
    function el(t, a, p) { var e = document.createElementNS(NS, t); a = a || {}; for (var k in a) e.setAttribute(k, a[k]); (p || svgEl).appendChild(e); return e; }
    function txt(x, y, s, a, p) { var e = el('text', Object.assign({ x: x, y: y }, a || {}), p); e.textContent = s; return e; }
    function addTip(g, html) {
      g.addEventListener('mouseenter', function (e) { showTip(e, html); });
      g.addEventListener('mousemove', moveTip); g.addEventListener('mouseleave', hideTip);
      g.addEventListener('focus', function (e) { showTip(e, html); }); g.addEventListener('blur', hideTip);
    }
    // clip everything inside the plot rect (contours/funnel/points never overflow)
    var defs = el('defs'); var cid = 'ck-fc-' + (svgEl.id || 'x');
    var cp = el('clipPath', { id: cid }, defs);
    el('rect', { x: x0, y: yT, width: (x1 - x0), height: (yB - yT) }, cp);
    var plot = el('g', { 'clip-path': 'url(#' + cid + ')' });
    function tri(z, fill) {
      el('polygon', { points: sx(NULLE) + ',' + yT + ' ' + sx(NULLE - z * maxSE) + ',' + yB + ' ' + sx(NULLE + z * maxSE) + ',' + yB, fill: fill, 'fill-opacity': '0.55' }, plot);
    }

    // title + subtitle
    txt(x0, 24, o.claim || ('Funnel plot · ' + o.measure),
      { 'font-size': tok('--t-fs-fig-title', '19px'), 'font-weight': tok('--t-fw-title', '600'), fill: C.ink });
    if (o.estimand) txt(x0, 43, o.estimand, { 'font-size': tok('--t-fs-fig-sub', '14px'), fill: C.ink2 });

    // significance contours, centred on the null (nested: p<.01 band, then p>.05 core)
    tri(2.58, C.s1); tri(1.96, C.s2);
    txt(sx(NULLE), yB - 6, 'p > .05', { 'font-size': tok('--t-fs-annot', '11px'), fill: C.ink2, 'text-anchor': 'middle' }, plot);

    // y-axis (SE) gridlines + ticks + rotated title
    var seTicks = niceForestTicks(0, maxSE, false).filter(function (v) { return v >= 0 && v <= maxSE; });
    seTicks.forEach(function (se) {
      var y = sy(se);
      el('line', { x1: x0, x2: x1, y1: y, y2: y, stroke: C.grid, 'stroke-width': ntok('--hair-grid', 1) });
      txt(x0 - 8, y + 3.5, se.toFixed(2), { 'font-size': tok('--t-fs-tick', '10.5px'), fill: C.ink2, 'text-anchor': 'end' });
    });
    var yTitle = txt(16, (yT + yB) / 2, 'Standard error', { 'font-size': tok('--t-fs-axis', '12px'), fill: C.ink2, 'text-anchor': 'middle' });
    yTitle.setAttribute('transform', 'rotate(-90 16 ' + ((yT + yB) / 2) + ')');

    // pseudo-95% CI funnel, centred on the pooled estimate (dashed guides)
    el('line', { x1: sx(pooled), y1: yT, x2: sx(pooled - 1.96 * maxSE), y2: yB, stroke: C.nul, 'stroke-width': '1', 'stroke-dasharray': '4 3' }, plot);
    el('line', { x1: sx(pooled), y1: yT, x2: sx(pooled + 1.96 * maxSE), y2: yB, stroke: C.nul, 'stroke-width': '1', 'stroke-dasharray': '4 3' }, plot);
    // null vertical
    el('line', { x1: sx(NULLE), x2: sx(NULLE), y1: yT, y2: yB, stroke: C.nul, 'stroke-width': ntok('--hair-null', 1.25), 'stroke-dasharray': '4 3' }, plot);

    // x-axis (effect) ticks — back-transformed for ratio measures
    var xt = niceForestTicks(o.log ? Math.exp(dmin) : dmin, o.log ? Math.exp(dmax) : dmax, o.log);
    xt.forEach(function (v) {
      var e = o.log ? Math.log(v) : v, x = sx(e);
      if (x < x0 - 1 || x > x1 + 1) return;
      txt(x, yB + 16, fmt(v), { 'font-size': tok('--t-fs-tick', '10.5px'), fill: C.ink2, 'text-anchor': 'middle' });
    });
    txt((x0 + x1) / 2, yB + 36, o.measure + (o.log ? ' (log scale)' : ''), { 'font-size': tok('--t-fs-axis', '12px'), fill: C.ink2, 'text-anchor': 'middle' });

    // study points (flag the least-precise / highest-leverage one)
    var flagIdx = points.reduce(function (m, p, i, a) { return p.se > a[m].se ? i : m; }, 0);
    points.forEach(function (p, i) {
      var cx = sx(p.x), cy = sy(p.se);
      var g = el('g', { tabindex: '0', role: 'listitem', 'aria-label': p.label + ': ' + o.measure + ' ' + fmt(o.log ? Math.exp(p.x) : p.x) + ', SE ' + p.se.toFixed(2) }, plot);
      addTip(g, '<b>' + p.label + '</b><br>' + o.measure + ' ' + fmt(o.log ? Math.exp(p.x) : p.x) + '<br>SE ' + p.se.toFixed(3));
      el('circle', { cx: cx, cy: cy, r: i === flagIdx ? 5 : 4, fill: i === flagIdx ? C.est : C.ink2, stroke: '#fff', 'stroke-width': '1' }, g);
    });
    if (points.length) {
      var fp = points[flagIdx];
      txt(sx(fp.x) + 9, sy(fp.se) + 3.5, 'least precise', { 'font-size': tok('--t-fs-annot', '11px'), fill: C.annot }, plot).setAttribute('font-style', 'italic');
    }

    // Egger annotation — inside the plot, top-right (never collides with the title)
    if (o.egger && o.egger.p != null) {
      var eg = 'Egger p = ' + (o.egger.p < 0.001 ? '<.001' : o.egger.p.toFixed(3));
      var note = o.egger.p < 0.05 ? ' · asymmetry' : ' · no clear asymmetry';
      txt(x1 - 6, yT + 15, eg + note, { 'font-size': tok('--t-fs-fig-sub', '14px'), fill: o.egger.p < 0.05 ? tok('--c-verdict-warn', '#E69F00') : C.ink2, 'text-anchor': 'end' });
      if (points.length < 10) txt(x1 - 6, yT + 30, '(low power, k<10)', { 'font-size': tok('--t-fs-annot', '11px'), fill: C.annot, 'text-anchor': 'end' });
    }

    el('line', { x1: x0, x2: x1, y1: yB, y2: yB, stroke: C.axis, 'stroke-width': ntok('--hair-axis', 1) });
    el('line', { x1: x0, x2: x0, y1: yT, y2: yB, stroke: C.axis, 'stroke-width': ntok('--hair-axis', 1) });
    return svgEl;
  }

  /**
   * renderLOO(svgEl, rows, opts) — leave-one-out (or cumulative) stability forest.
   * rows: [{ label, est, lo, hi }] ; opts: { measure, log, null, overall:{x,label}, claim, estimand }
   * A thin specialisation of renderForest: uniform markers, a null line, and a
   * secondary reference line at the overall pooled estimate.
   */
  function renderLOO(svgEl, rows, opts) {
    opts = opts || {};
    var studies = rows.map(function (r) { return { label: r.label, est: r.est, lo: r.lo, hi: r.hi, weight: 1, included: true }; });
    return renderForest(svgEl, studies, Object.assign({ measure: 'effect', rowH: 24 }, opts, {
      pooled: null, refLine: opts.overall
    }));
  }

  // Cumulative meta-analysis is structurally identical to LOO: a forest of
  // sequential pooled rows with a null line and a reference at the final estimate.
  function renderCumulative(svgEl, rows, opts) { return renderLOO(svgEl, rows, opts); }

  /**
   * renderBubble(svgEl, points, opts) — meta-regression bubble plot.
   * points: [{ label, x (moderator), y (effect, natural scale), weight }]
   * opts: { measure, log, null, xlabel, claim, estimand,
   *         fit:{ b0, b1, xm, v00, v01, v11, slope, p } }  (coeffs on log/effect scale)
   */
  function renderBubble(svgEl, points, opts) {
    opts = opts || {};
    var o = Object.assign({ log: false, measure: 'effect', null: 1, xlabel: 'moderator',
      width: 640, height: 392, padL: 64, padR: 26, padT: 58, padB: 50 }, opts);
    var tok = tokGetter();
    var ntok = function (n, f) { var v = parseFloat(tok(n, '')); return isFinite(v) ? v : f; };
    var C = { ink: tok('--c-ink', '#1a1a1a'), ink2: tok('--c-ink-2', '#555a5f'), annot: tok('--c-annot', '#7a8086'),
      grid: tok('--c-grid', '#e7e9ec'), axis: tok('--c-axis', '#c2c6cb'), nul: tok('--c-null', '#9aa0a6'),
      est: tok('--c-estimate', '#1a1a1a'), line: tok('--cat-1', '#0072B2'), band: tok('--seq-2', '#cfe0ec') };
    var W = o.width, H = o.height, x0 = o.padL, x1 = W - o.padR, yT = o.padT, yB = H - o.padB;
    var ly = function (e) { return o.log ? Math.log(e) : e; };
    var fit = o.fit;
    function pred(xv) { var c = xv - (fit.xm || 0), mu = fit.b0 + fit.b1 * c,
      vp = Math.max(0, (fit.v00 || 0) + 2 * c * (fit.v01 || 0) + c * c * (fit.v11 || 0)), se = Math.sqrt(vp);
      return { mu: mu, lo: mu - 1.96 * se, hi: mu + 1.96 * se }; }

    var xs = points.map(function (p) { return p.x; });
    var xmin = Math.min.apply(null, xs), xmax = Math.max.apply(null, xs);
    var xpad = (xmax - xmin) * 0.08 || 1; xmin -= xpad; xmax += xpad;
    var evals = points.map(function (p) { return ly(p.y); }).concat([ly(o.null)]);
    if (fit) { var e0 = pred(xmin), e1 = pred(xmax); evals.push(e0.lo, e0.hi, e1.lo, e1.hi); }
    var ymin = Math.min.apply(null, evals), ymax = Math.max.apply(null, evals);
    var yp = (ymax - ymin) * 0.08 || 0.1; ymin -= yp; ymax += yp;
    var sx = function (x) { return x0 + (x - xmin) / (xmax - xmin) * (x1 - x0); };
    var sy = function (e) { return yT + (1 - (e - ymin) / (ymax - ymin)) * (yB - yT); };
    var wmax = Math.max.apply(null, points.map(function (p) { return p.weight || 1; }));

    while (svgEl.firstChild) svgEl.removeChild(svgEl.firstChild);
    svgEl.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svgEl.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svgEl.setAttribute('role', 'img');
    svgEl.setAttribute('font-family', tok('--t-font-serif', 'Georgia,serif'));
    svgEl.setAttribute('aria-label', 'Meta-regression bubble plot. ' + (o.claim || '') + ' ' + points.length + ' studies.');
    function el(t, a, p) { var e = document.createElementNS(NS, t); a = a || {}; for (var k in a) e.setAttribute(k, a[k]); (p || svgEl).appendChild(e); return e; }
    function txt(x, y, s, a, p) { var e = el('text', Object.assign({ x: x, y: y }, a || {}), p); e.textContent = s; return e; }
    function addTip(g, html) {
      g.addEventListener('mouseenter', function (e) { showTip(e, html); }); g.addEventListener('mousemove', moveTip);
      g.addEventListener('mouseleave', hideTip); g.addEventListener('focus', function (e) { showTip(e, html); }); g.addEventListener('blur', hideTip);
    }

    // title + subtitle
    txt(x0, 24, o.claim || ('Meta-regression · ' + o.measure), { 'font-size': tok('--t-fs-fig-title', '19px'), 'font-weight': tok('--t-fw-title', '600'), fill: C.ink });
    if (o.estimand) txt(x0, 43, o.estimand, { 'font-size': tok('--t-fs-fig-sub', '14px'), fill: C.ink2 });

    var cid = 'ck-bb-' + (svgEl.id || 'x');
    var defs = el('defs'); var cp = el('clipPath', { id: cid }, defs); el('rect', { x: x0, y: yT, width: (x1 - x0), height: (yB - yT) }, cp);
    var plot = el('g', { 'clip-path': 'url(#' + cid + ')' });

    // y gridlines + ticks (effect, back-transformed for ratios)
    var yt = niceForestTicks(o.log ? Math.exp(ymin) : ymin, o.log ? Math.exp(ymax) : ymax, o.log);
    yt.forEach(function (v) { var e = ly(v), y = sy(e); if (y < yT - 1 || y > yB + 1) return;
      el('line', { x1: x0, x2: x1, y1: y, y2: y, stroke: C.grid, 'stroke-width': ntok('--hair-grid', 1) }, plot);
      txt(x0 - 8, y + 3.5, fmt(v), { 'font-size': tok('--t-fs-tick', '10.5px'), fill: C.ink2, 'text-anchor': 'end' });
    });
    // null reference (horizontal, dashed)
    var yn = sy(ly(o.null));
    el('line', { x1: x0, x2: x1, y1: yn, y2: yn, stroke: C.nul, 'stroke-width': ntok('--hair-null', 1.25), 'stroke-dasharray': '4 3' }, plot);

    // fitted line + 95% CI band
    if (fit) {
      var N = 28, up = [], dn = [], mid = [];
      for (var i = 0; i <= N; i++) { var xv = xmin + (xmax - xmin) * i / N, pr = pred(xv);
        up.push(sx(xv) + ',' + sy(pr.hi)); dn.push(sx(xv) + ',' + sy(pr.lo)); mid.push(sx(xv) + ',' + sy(pr.mu)); }
      el('polygon', { points: up.concat(dn.reverse()).join(' '), fill: C.band, 'fill-opacity': '0.5' }, plot);
      el('polyline', { points: mid.join(' '), fill: 'none', stroke: C.line, 'stroke-width': '2' }, plot);
    }

    // bubbles (area proportional to weight)
    points.forEach(function (p) {
      var r = 4 + Math.sqrt((p.weight || 1) / wmax) * 11;
      var g = el('g', { tabindex: '0', role: 'listitem', 'aria-label': p.label + ': ' + o.xlabel + ' ' + p.x + ', ' + o.measure + ' ' + fmt(p.y) }, plot);
      addTip(g, '<b>' + p.label + '</b><br>' + o.xlabel + ': ' + p.x + '<br>' + o.measure + ' ' + fmt(p.y));
      el('circle', { cx: sx(p.x), cy: sy(ly(p.y)), r: r, fill: C.line, 'fill-opacity': '0.5', stroke: C.line, 'stroke-width': '1' }, g);
    });

    // x ticks + label (integer-aware for integer moderators like year — avoids
    // half-step ticks that round to duplicate labels)
    var span = xmax - xmin, allInt = points.every(function (p) { return p.x === Math.round(p.x); });
    var xt, xv;
    if (allInt && span <= 14) { xt = []; for (xv = Math.ceil(xmin); xv <= xmax; xv++) xt.push(xv); }
    else xt = niceForestTicks(xmin, xmax, false).filter(function (v) { return v >= xmin && v <= xmax; });
    xt.forEach(function (v) { txt(sx(v), yB + 16, allInt ? String(Math.round(v)) : fmt(v), { 'font-size': tok('--t-fs-tick', '10.5px'), fill: C.ink2, 'text-anchor': 'middle' }); });
    txt((x0 + x1) / 2, yB + 36, o.xlabel, { 'font-size': tok('--t-fs-axis', '12px'), fill: C.ink2, 'text-anchor': 'middle' });
    var yTitle = txt(15, (yT + yB) / 2, o.measure + (o.log ? ' (log)' : ''), { 'font-size': tok('--t-fs-axis', '12px'), fill: C.ink2, 'text-anchor': 'middle' });
    yTitle.setAttribute('transform', 'rotate(-90 15 ' + ((yT + yB) / 2) + ')');

    // slope + p annotation (in situ, top-right)
    if (fit && fit.slope != null) {
      var sl = 'slope ' + fit.slope.toFixed(3) + (fit.p != null ? ' · p ' + (fit.p < 0.001 ? '<.001' : fit.p.toFixed(3)) : '');
      txt(x1, 24, sl, { 'font-size': tok('--t-fs-fig-sub', '14px'), fill: (fit.p != null && fit.p < 0.05) ? tok('--c-verdict-warn', '#E69F00') : C.ink2, 'text-anchor': 'end' });
      if (points.length < 10) txt(x1, 40, '(exploratory, k<10)', { 'font-size': tok('--t-fs-annot', '11px'), fill: C.annot, 'text-anchor': 'end' });
    }

    el('line', { x1: x0, x2: x1, y1: yB, y2: yB, stroke: C.axis, 'stroke-width': ntok('--hair-axis', 1) });
    el('line', { x1: x0, x2: x0, y1: yT, y2: yB, stroke: C.axis, 'stroke-width': ntok('--hair-axis', 1) });
    return svgEl;
  }

  global.ChartKit = global.ChartKit || {};
  global.ChartKit.renderForest = renderForest;
  global.ChartKit.renderFunnel = renderFunnel;
  global.ChartKit.renderLOO = renderLOO;
  global.ChartKit.renderCumulative = renderCumulative;
  global.ChartKit.renderBubble = renderBubble;
  global.ChartKit.niceForestTicks = niceForestTicks;
})(window);
