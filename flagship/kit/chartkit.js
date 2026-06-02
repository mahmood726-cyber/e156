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
    var mag = Math.pow(10, Math.floor(Math.log10(span)));
    var step = mag * ([1, 2, 5, 10].find(function (s) { return span / (s * mag) <= 6; }) || 10);
    for (v = Math.ceil(min / step) * step; v <= max + 1e-9; v += step) out.push(+v.toFixed(6));
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

  global.ChartKit = global.ChartKit || {};
  global.ChartKit.renderForest = renderForest;
  global.ChartKit.niceForestTicks = niceForestTicks;
})(window);
