"""Paper-specific SVG chart generators for the E156 per-paper dashboards.

Every paper gets 5 charts, all data-derived from its workbook entry so
each chart is unique to the paper. No CDN / no JS library — pure inline
SVG so pages render offline and on low-bandwidth connections.

Each chart function returns a string of the form `<svg ...>...</svg>`.
All charts include a fallback rendering so they always produce visible
output even when the paper's body doesn't yield the expected data.
"""
from __future__ import annotations
import html as htmlmod
import re
from typing import Any

W = 520      # chart width in px
H = 240      # chart height in px
MARGIN_L = 48
MARGIN_R = 24
MARGIN_T = 36
MARGIN_B = 36

# Dark-theme palette (matches students.html)
FG = "#e5e7eb"
DIM = "#9ca3af"
FAINT = "#6b7280"
BG = "#111827"
CARD = "#1a2236"
BORDER = "#2a3244"
ACCENT = "#22c55e"
BLUE = "#3b82f6"
WARN = "#eab308"
RED = "#ef4444"
PURPLE = "#a855f7"


def _esc(s: str) -> str:
    return htmlmod.escape(s or "", quote=True)


def _svg_wrap(title: str, subtitle: str, body: str, fg: str = ACCENT) -> str:
    """Wrap chart body in an SVG with title + footer banner."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{_esc(title)}">\n'
        f'  <rect x="0" y="0" width="{W}" height="{H}" fill="{CARD}" rx="6"/>\n'
        f'  <text x="14" y="22" fill="{fg}" font-family="system-ui,sans-serif" '
        f'font-size="13" font-weight="600">{_esc(title)}</text>\n'
        f'  <text x="14" y="{H-10}" fill="{FAINT}" font-family="system-ui,sans-serif" '
        f'font-size="10.5">{_esc(subtitle)}</text>\n'
        f'  {body}\n'
        f'</svg>'
    )


def _fallback(title: str, message: str, fg: str = FAINT) -> str:
    body = (
        f'<text x="{W/2}" y="{H/2}" fill="{DIM}" '
        f'font-family="system-ui,sans-serif" font-size="13" '
        f'text-anchor="middle">{_esc(message)}</text>'
    )
    return _svg_wrap(title, "(no data extractable from workbook)", body, fg=fg)


# --------------------------------------------------------------------------
# Data extractors
# --------------------------------------------------------------------------

_SENT_END_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")
_EFFECT_RE = re.compile(
    r"\b(odds ratio|hazard ratio|risk ratio|relative risk|rate ratio|"
    r"standardi[sz]ed mean difference|mean difference|pooled (?:SMD|MD|OR|RR|HR|AUC|sensitivity|specificity)|"
    r"\b(?:OR|RR|HR|SMD|MD|AUC|RMST|NNT))\s+"
    r"(?:was|of|=|:)?\s*"
    r"(-?\d+\.?\d*)\s*"
    r"\(\s*95%\s*(?:CI|credible interval|HKSJ\s*CI|confidence interval|HPD)\s*"
    r"(-?\d+\.?\d*)\s*(?:to|-|–|,)\s*(-?\d+\.?\d*)",
    re.IGNORECASE,
)
_N_SAMPLES_RE = re.compile(r"([\d,]+)\s+(patients|participants|subjects|cases|reviews|trials|studies|RCTs|records)", re.IGNORECASE)
_K_STUDIES_RE = re.compile(r"\b(\d+)\s+(?:RCTs|trials|studies|reviews|cohorts|datasets)\b", re.IGNORECASE)
_I2_RE = re.compile(r"I[-\s]?squared\s+(?:was\s+)?(-?[\d.]+)\s*(?:percent|%)", re.IGNORECASE)
_PERCENT_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*(?:percent|%)", re.IGNORECASE)
_REF_YEAR_RE = re.compile(r"\b(19\d{2}|20\d{2})\b")


def split_sentences(body: str) -> list[str]:
    body = (body or "").strip()
    if not body:
        return []
    parts = _SENT_END_RE.split(body)
    return [p.strip() for p in parts if p.strip()]


def extract_effect(body: str) -> dict | None:
    """Primary effect size + 95% CI. Returns {label, point, lo, hi, is_ratio}."""
    m = _EFFECT_RE.search(body or "")
    if not m:
        return None
    label_raw = m.group(1)
    try:
        point = float(m.group(2))
        lo = float(m.group(3))
        hi = float(m.group(4))
    except (ValueError, IndexError):
        return None
    if hi < lo:
        lo, hi = hi, lo
    # Ratio measures have a null at 1; difference measures at 0
    label_up = label_raw.upper()
    is_ratio = any(k in label_up for k in (" OR", "ODDS", " RR", "RISK", "RATE", " HR", "HAZARD"))
    # Common case: "OR was 0.78" → ratio
    if any(k in label_up for k in ("AUC", "SENSITIVITY", "SPECIFICITY")):
        is_ratio = False  # null at 0.5 handled elsewhere
    return {"label": label_raw, "point": point, "lo": lo, "hi": hi, "is_ratio": is_ratio}


def extract_sample_sizes(body: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for m in _N_SAMPLES_RE.finditer(body or ""):
        try:
            n = int(m.group(1).replace(",", ""))
        except ValueError:
            continue
        if 2 <= n <= 10_000_000:
            out.append((n, m.group(2).lower()))
    return out


def extract_k_studies(body: str) -> int | None:
    m = _K_STUDIES_RE.search(body or "")
    if not m:
        return None
    try:
        k = int(m.group(1))
        return k if 1 <= k <= 5000 else None
    except ValueError:
        return None


def extract_i2(body: str) -> float | None:
    m = _I2_RE.search(body or "")
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def extract_percent(body: str) -> list[float]:
    out = []
    for m in _PERCENT_RE.finditer(body or ""):
        try:
            out.append(float(m.group(1)))
        except ValueError:
            pass
    return [p for p in out if -100 <= p <= 200]


def ref_years(refs: list[str]) -> list[int]:
    years: list[int] = []
    for r in refs or []:
        m = _REF_YEAR_RE.search(r)
        if m:
            y = int(m.group(1))
            if 1960 <= y <= 2030:
                years.append(y)
    return years


# --------------------------------------------------------------------------
# Chart 1 — paper anatomy (sentence word counts)
# --------------------------------------------------------------------------

def chart_anatomy(entry: dict) -> str:
    """Bars of words-per-sentence. Aims at 7 bars for E156-compliant bodies."""
    sents = split_sentences(entry.get("body", ""))
    if not sents:
        return _fallback("Paper anatomy — words per sentence",
                         "No body text available")
    counts = [len(s.split()) for s in sents]
    max_c = max(counts) or 1
    n = len(counts)
    total = sum(counts)
    avg = total / n

    plot_w = W - MARGIN_L - MARGIN_R
    plot_h = H - MARGIN_T - MARGIN_B
    bar_w = plot_w / max(n, 1) * 0.7
    gap = plot_w / max(n, 1) * 0.3

    bars = []
    for i, c in enumerate(counts):
        x = MARGIN_L + i * (bar_w + gap) + gap / 2
        bar_h = (c / max_c) * plot_h
        y = MARGIN_T + (plot_h - bar_h)
        col = ACCENT if (n == 7 and c <= 35) else (WARN if c > 35 else BLUE)
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" '
            f'fill="{col}" opacity="0.85"><title>S{i+1}: {c} words</title></rect>'
            f'<text x="{x + bar_w/2:.1f}" y="{MARGIN_T + plot_h + 14:.1f}" '
            f'fill="{FAINT}" font-size="10" text-anchor="middle" '
            f'font-family="ui-monospace,monospace">S{i+1}</text>'
            f'<text x="{x + bar_w/2:.1f}" y="{y - 4:.1f}" fill="{FG}" '
            f'font-size="10" text-anchor="middle">{c}</text>'
        )
    # Axis and mean line
    mean_y = MARGIN_T + plot_h - (avg / max_c) * plot_h
    bars.append(
        f'<line x1="{MARGIN_L}" y1="{mean_y:.1f}" x2="{W-MARGIN_R}" y2="{mean_y:.1f}" '
        f'stroke="{DIM}" stroke-dasharray="3,3" opacity="0.5"/>'
        f'<text x="{W-MARGIN_R-4}" y="{mean_y-4:.1f}" fill="{DIM}" font-size="10" '
        f'text-anchor="end">mean {avg:.1f}w</text>'
    )
    status = "7 sentences ✓" if n == 7 else f"{n} sentences"
    subtitle = f"{total} words total · {status} · target ≤156w, 7 sentences"
    return _svg_wrap("Paper anatomy — words per sentence (S1–S7)", subtitle, "\n".join(bars))


# --------------------------------------------------------------------------
# Chart 2 — effect size forest (primary estimand)
# --------------------------------------------------------------------------

def chart_effect(entry: dict) -> str:
    body = entry.get("body", "")
    eff = extract_effect(body)
    estimand = entry.get("estimand", "")
    if eff is None:
        return _fallback(
            f"Primary effect — {estimand}" if estimand else "Primary effect",
            "No parseable effect size in the 156-word body",
        )
    label, point, lo, hi = eff["label"], eff["point"], eff["lo"], eff["hi"]
    is_ratio = eff["is_ratio"]
    null_val = 1.0 if is_ratio else 0.0

    # Axis range
    x_min = min(lo, null_val) * 0.9 if is_ratio else min(lo, null_val) - 0.1
    x_max = max(hi, null_val) * 1.1 if is_ratio else max(hi, null_val) + 0.1
    if x_max - x_min < 0.05:
        x_min -= 0.2; x_max += 0.2

    plot_w = W - MARGIN_L - MARGIN_R
    y_center = MARGIN_T + (H - MARGIN_T - MARGIN_B) / 2

    def px(v: float) -> float:
        return MARGIN_L + (v - x_min) / (x_max - x_min) * plot_w

    # Null line
    null_x = px(null_val)
    elements = [
        f'<line x1="{null_x:.1f}" y1="{MARGIN_T+8}" x2="{null_x:.1f}" y2="{H-MARGIN_B}" '
        f'stroke="{DIM}" stroke-dasharray="4,4" opacity="0.7"/>',
        f'<text x="{null_x:.1f}" y="{MARGIN_T+4}" fill="{DIM}" font-size="10" '
        f'text-anchor="middle">null = {null_val:g}</text>',
        # CI line
        f'<line x1="{px(lo):.1f}" y1="{y_center:.1f}" x2="{px(hi):.1f}" y2="{y_center:.1f}" '
        f'stroke="{ACCENT}" stroke-width="2.5"/>',
        # Point
        f'<rect x="{px(point)-9:.1f}" y="{y_center-9:.1f}" width="18" height="18" '
        f'fill="{ACCENT}" transform="rotate(45 {px(point):.1f} {y_center:.1f})"/>',
        # Labels
        f'<text x="{px(lo):.1f}" y="{y_center+28:.1f}" fill="{DIM}" font-size="10" '
        f'text-anchor="middle">{lo:g}</text>',
        f'<text x="{px(hi):.1f}" y="{y_center+28:.1f}" fill="{DIM}" font-size="10" '
        f'text-anchor="middle">{hi:g}</text>',
        f'<text x="{px(point):.1f}" y="{y_center-18:.1f}" fill="{ACCENT}" '
        f'font-size="14" font-weight="700" text-anchor="middle">{point:g}</text>',
    ]
    # Favors annotation
    if is_ratio:
        left_txt, right_txt = "favors intervention", "favors control"
        if point > null_val:
            left_txt, right_txt = right_txt, left_txt
    else:
        left_txt, right_txt = "negative", "positive"
    elements.append(
        f'<text x="{MARGIN_L+4}" y="{H-MARGIN_B+18:.1f}" fill="{FAINT}" font-size="10">← {left_txt}</text>'
        f'<text x="{W-MARGIN_R-4}" y="{H-MARGIN_B+18:.1f}" fill="{FAINT}" font-size="10" '
        f'text-anchor="end">{right_txt} →</text>'
    )
    sig = "non-null" if (null_val < lo) or (null_val > hi) else "crosses null"
    subtitle = f"{label}: {point:g} (95% CI {lo:g} to {hi:g}) · {sig}"
    return _svg_wrap(f"Primary effect ({estimand or label})", subtitle, "\n".join(elements))


# --------------------------------------------------------------------------
# Chart 3 — reference-year histogram
# --------------------------------------------------------------------------

def chart_refs_timeline(entry: dict) -> str:
    refs = entry.get("references", []) or []
    years = ref_years(refs)
    if not years:
        return _fallback("References by year",
                         f"{len(refs)} references in workbook, no parseable years")
    y_min = min(years)
    y_max = max(years)
    if y_max == y_min:
        y_min -= 1; y_max += 1
    bucket_w = max(1, (y_max - y_min) // 12)
    buckets: dict[int, int] = {}
    for y in years:
        b = ((y - y_min) // bucket_w) * bucket_w + y_min
        buckets[b] = buckets.get(b, 0) + 1
    sorted_buckets = sorted(buckets.items())
    max_n = max(buckets.values())
    plot_w = W - MARGIN_L - MARGIN_R
    plot_h = H - MARGIN_T - MARGIN_B
    n = len(sorted_buckets)
    bar_w = plot_w / max(n, 1) * 0.82
    gap = plot_w / max(n, 1) * 0.18
    bars = []
    for i, (b, c) in enumerate(sorted_buckets):
        x = MARGIN_L + i * (bar_w + gap) + gap / 2
        h_ = (c / max_n) * plot_h
        y = MARGIN_T + (plot_h - h_)
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h_:.1f}" '
            f'fill="{BLUE}" opacity="0.85"><title>{b}{("–"+str(b+bucket_w-1)) if bucket_w > 1 else ""}: {c} refs</title></rect>'
            f'<text x="{x + bar_w/2:.1f}" y="{MARGIN_T + plot_h + 14:.1f}" '
            f'fill="{FAINT}" font-size="9" text-anchor="middle" '
            f'font-family="ui-monospace,monospace">{b if bucket_w == 1 else str(b)[-2:]}</text>'
            f'<text x="{x + bar_w/2:.1f}" y="{y - 4:.1f}" fill="{FG}" '
            f'font-size="10" text-anchor="middle">{c}</text>'
        )
    range_txt = f"{y_min}–{y_max}" if y_max > y_min else str(y_min)
    subtitle = f"{len(years)} dated refs · range {range_txt} · {bucket_w}-year buckets"
    return _svg_wrap("References by publication year", subtitle, "\n".join(bars), fg=BLUE)


# --------------------------------------------------------------------------
# Chart 4 — sample-size / scale
# --------------------------------------------------------------------------

def chart_scale(entry: dict) -> str:
    body = entry.get("body", "") or ""
    samples = extract_sample_sizes(body)
    k = extract_k_studies(body)
    data_str = entry.get("data", "")

    # Aggregate unique (n, unit) pairs, keep top by n
    seen = set()
    dedup = []
    for n, u in samples:
        if (n, u) in seen:
            continue
        seen.add((n, u))
        dedup.append((n, u))
    dedup.sort(key=lambda x: -x[0])
    dedup = dedup[:5]

    if not dedup and k is None and not data_str:
        return _fallback("Evidence base — scale",
                         "No sample-size or study-count info parseable")

    # Build a horizontal bar chart of sample counts
    rows = []
    if k is not None:
        rows.append((f"{k} studies / trials", k, "k"))
    for n, u in dedup:
        rows.append((f"{n:,} {u}", n, u))
    if not rows:
        # Fall back to showing DATA string as an info box
        body_svg = (
            f'<text x="{W/2}" y="{H/2-10}" fill="{FG}" font-size="12" '
            f'text-anchor="middle" font-weight="600">Dataset</text>'
            f'<text x="{W/2}" y="{H/2+16}" fill="{DIM}" font-size="11" '
            f'text-anchor="middle">{_esc(data_str[:70])}</text>'
        )
        return _svg_wrap("Evidence base — scale",
                         "Descriptive only (no numeric counts in body)", body_svg, fg=PURPLE)

    max_n = max(r[1] for r in rows)
    plot_w = W - MARGIN_L - MARGIN_R - 60  # leave room for right-side labels
    plot_h = H - MARGIN_T - MARGIN_B
    bar_h = min(26, plot_h / max(len(rows), 1) * 0.7)
    gap = (plot_h - bar_h * len(rows)) / max(len(rows) + 1, 1)

    bars = []
    for i, (lbl, n, u) in enumerate(rows):
        y = MARGIN_T + gap + i * (bar_h + gap)
        w_ = (n / max_n) * plot_w
        bars.append(
            f'<rect x="{MARGIN_L}" y="{y:.1f}" width="{w_:.1f}" height="{bar_h:.1f}" '
            f'fill="{PURPLE}" opacity="0.85"/>'
            f'<text x="{MARGIN_L + w_ + 8:.1f}" y="{y + bar_h/2 + 4:.1f}" '
            f'fill="{FG}" font-size="11">{_esc(lbl)}</text>'
        )
    return _svg_wrap("Evidence base — scale", _esc(data_str[:90]) if data_str else "counts parsed from body",
                     "\n".join(bars), fg=PURPLE)


# --------------------------------------------------------------------------
# Chart 5 — topic fingerprint (TYPE-aware)
# --------------------------------------------------------------------------

def chart_type_fingerprint(entry: dict) -> str:
    typ = (entry.get("type") or "").lower()
    estimand = entry.get("estimand", "") or ""
    i2 = extract_i2(entry.get("body", ""))

    # Decide schematic based on TYPE
    if "methods" in typ:
        # Schematic: Input → Method → Output
        body = (
            f'<rect x="30" y="80" width="130" height="80" fill="{BG}" stroke="{ACCENT}" rx="6"/>'
            f'<text x="95" y="110" fill="{FG}" font-size="11" text-anchor="middle" font-weight="600">INPUT</text>'
            f'<text x="95" y="130" fill="{DIM}" font-size="10" text-anchor="middle">data + metadata</text>'
            f'<text x="95" y="148" fill="{DIM}" font-size="10" text-anchor="middle">{_esc(entry.get("data","")[:18])}</text>'
            f'<rect x="195" y="70" width="130" height="100" fill="{BG}" stroke="{BLUE}" rx="6"/>'
            f'<text x="260" y="100" fill="{FG}" font-size="11" text-anchor="middle" font-weight="600">METHOD</text>'
            f'<text x="260" y="120" fill="{DIM}" font-size="10" text-anchor="middle">{_esc(entry.get("name","")[:20])}</text>'
            f'<text x="260" y="138" fill="{DIM}" font-size="9" text-anchor="middle">{_esc(typ.split("|")[0][:25])}</text>'
            f'<rect x="360" y="80" width="130" height="80" fill="{BG}" stroke="{WARN}" rx="6"/>'
            f'<text x="425" y="110" fill="{FG}" font-size="11" text-anchor="middle" font-weight="600">OUTPUT</text>'
            f'<text x="425" y="130" fill="{DIM}" font-size="10" text-anchor="middle">{_esc(estimand[:20] or "estimate")}</text>'
            f'<text x="425" y="148" fill="{DIM}" font-size="10" text-anchor="middle">+ audit trail</text>'
            # Arrows
            f'<path d="M160 120 L195 120" stroke="{FG}" stroke-width="1.5" marker-end="url(#a)"/>'
            f'<path d="M325 120 L360 120" stroke="{FG}" stroke-width="1.5" marker-end="url(#a)"/>'
            f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="{FG}"/></marker></defs>'
        )
        return _svg_wrap("Method schematic", f"{_esc(typ)[:80]}", body)

    if "living-ma" in typ or "living" in typ or "meta-analysis" in typ or "ma" in typ.split("|")[0]:
        # Heterogeneity thermometer: I² if extracted, else just show "random-effects pooled"
        if i2 is not None:
            i2_clamped = max(0.0, min(100.0, i2))
            bar_x = MARGIN_L + 40
            bar_y = MARGIN_T + 40
            bar_w_max = W - MARGIN_R - bar_x - 60
            fill_w = bar_w_max * (i2_clamped / 100)
            col = ACCENT if i2_clamped < 30 else (WARN if i2_clamped < 60 else RED)
            tier = "low" if i2_clamped < 30 else ("moderate" if i2_clamped < 60 else "substantial")
            body = (
                f'<text x="{bar_x}" y="{bar_y - 12}" fill="{DIM}" font-size="11">Heterogeneity (I²)</text>'
                f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w_max:.1f}" height="30" fill="{BG}" stroke="{BORDER}"/>'
                f'<rect x="{bar_x}" y="{bar_y}" width="{fill_w:.1f}" height="30" fill="{col}" opacity="0.85"/>'
                f'<text x="{bar_x + fill_w + 10:.1f}" y="{bar_y + 20}" fill="{FG}" font-size="14" font-weight="700">{i2_clamped:g}%</text>'
                f'<text x="{bar_x}" y="{bar_y + 55}" fill="{DIM}" font-size="10">0%</text>'
                f'<text x="{bar_x + bar_w_max/3:.1f}" y="{bar_y + 55}" fill="{DIM}" font-size="10" text-anchor="middle">30% (low|mod)</text>'
                f'<text x="{bar_x + 2*bar_w_max/3:.1f}" y="{bar_y + 55}" fill="{DIM}" font-size="10" text-anchor="middle">60% (mod|sub)</text>'
                f'<text x="{bar_x + bar_w_max:.1f}" y="{bar_y + 55}" fill="{DIM}" font-size="10" text-anchor="end">100%</text>'
                f'<text x="{bar_x}" y="{bar_y + 85}" fill="{col}" font-size="12" font-weight="600">{tier} between-study heterogeneity</text>'
                f'<text x="{bar_x}" y="{bar_y + 102}" fill="{DIM}" font-size="10">random-effects pooling recommended · prediction interval should be reported alongside CI</text>'
            )
        else:
            body = (
                f'<text x="{W/2}" y="{H/2-10}" fill="{FG}" font-size="13" text-anchor="middle" font-weight="600">Living meta-analysis</text>'
                f'<text x="{W/2}" y="{H/2+10}" fill="{DIM}" font-size="11" text-anchor="middle">{_esc(estimand[:40])}</text>'
                f'<text x="{W/2}" y="{H/2+28}" fill="{DIM}" font-size="10" text-anchor="middle">I² not stated in 156-word body — check source code</text>'
            )
        return _svg_wrap("Meta-analysis fingerprint", _esc(estimand[:80]) or "living MA", body, fg=WARN)

    # Default / review type: reference-network style
    refs = entry.get("references") or []
    body = (
        f'<text x="{W/2}" y="{MARGIN_T + 22}" fill="{FG}" font-size="13" text-anchor="middle" font-weight="600">Review scope</text>'
        f'<text x="{W/2}" y="{MARGIN_T + 44}" fill="{DIM}" font-size="11" text-anchor="middle">{_esc(typ[:80])}</text>'
        f'<text x="{W/2}" y="{MARGIN_T + 80}" fill="{ACCENT}" font-size="32" font-weight="700" text-anchor="middle">{len(refs)}</text>'
        f'<text x="{W/2}" y="{MARGIN_T + 100}" fill="{DIM}" font-size="11" text-anchor="middle">references in workbook</text>'
    )
    return _svg_wrap("Topic fingerprint", _esc(typ)[:80] or "review", body, fg=PURPLE)


# --------------------------------------------------------------------------
# Entry point — render all 5 charts for an entry
# --------------------------------------------------------------------------

def render_all_charts(entry: dict) -> str:
    """Return HTML containing 5 paper-specific SVG charts."""
    charts = [
        chart_anatomy(entry),
        chart_effect(entry),
        chart_refs_timeline(entry),
        chart_scale(entry),
        chart_type_fingerprint(entry),
    ]
    return (
        '<section class="charts">'
        '<h2>Paper dashboard — 5 views</h2>'
        '<div class="chart-grid">'
        + "".join(f'<div class="chart-tile">{c}</div>' for c in charts)
        + '</div></section>'
    )
