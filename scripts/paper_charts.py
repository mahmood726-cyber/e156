"""Paper-specific SVG chart + infobox generators for E156 per-paper pages.

Each paper gets 5 tiles chosen from ~14 generators. Every generator returns
`(svg_or_html, score, why)`:
  score 0 → cannot render for this paper, skip
  score 1 → generic fallback-grade but informative (NYT-style infobox)
  score 2 → type-appropriate generic
  score 3 → paper-specific with parsed numbers

For each paper we:
  1. detect its kind (methods / living-ma / other)
  2. run the kind's generator pool
  3. pick the top 5 by (score desc, registered order asc)

No CDN, no JS — pure inline SVG + a small HTML infobox variant. Dark-theme
palette matches students.html. "NYT-style" = serif-bold headline numbers,
sans caption, minimal chrome.
"""
from __future__ import annotations
import html as htmlmod
import re
from typing import Callable

# ─── Palette ──────────────────────────────────────────────────────────────
W = 520
H = 240
MARGIN_L = 48
MARGIN_R = 24
MARGIN_T = 36
MARGIN_B = 36

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
SERIF = "'Georgia','Cambria','Times New Roman',serif"
SANS = "system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"


def _esc(s: str) -> str:
    return htmlmod.escape(s or "", quote=True)


def _svg_wrap(title: str, subtitle: str, body: str, fg: str = ACCENT) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{_esc(title)}">\n'
        f'  <rect x="0" y="0" width="{W}" height="{H}" fill="{CARD}" rx="6"/>\n'
        f'  <text x="14" y="22" fill="{fg}" font-family="{SANS}" '
        f'font-size="11.5" font-weight="700" letter-spacing="0.08em" '
        f'text-transform="uppercase" style="text-transform:uppercase">{_esc(title).upper()}</text>\n'
        f'  <text x="14" y="{H-10}" fill="{FAINT}" font-family="{SANS}" '
        f'font-size="10.5">{_esc(subtitle)}</text>\n'
        f'  {body}\n</svg>'
    )


# ─── Data extractors (regex) ──────────────────────────────────────────────
_SENT_END_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")
_EFFECT_RE = re.compile(
    r"\b(odds ratio|hazard ratio|risk ratio|relative risk|rate ratio|"
    r"standardi[sz]ed mean difference|mean difference|pooled (?:SMD|MD|OR|RR|HR|AUC|sensitivity|specificity)|"
    r"\b(?:OR|RR|HR|SMD|MD|AUC|RMST|NNT))\s+"
    r"(?:was|of|=|:)?\s*(-?\d+\.?\d*)\s*"
    r"\(\s*95%\s*(?:CI|credible interval|HKSJ\s*CI|confidence interval|HPD|CrI)\s*"
    r"(-?\d+\.?\d*)\s*(?:to|-|–|,)\s*(-?\d+\.?\d*)",
    re.IGNORECASE,
)
_N_SAMPLES_RE = re.compile(
    r"([\d,]+)\s+(patients|participants|subjects|cases|reviews|trials|studies|RCTs|records|comparisons)",
    re.IGNORECASE,
)
_K_STUDIES_RE = re.compile(r"\b(\d+)\s+(?:RCTs|trials|studies|reviews|cohorts|datasets|comparisons)\b", re.IGNORECASE)
_I2_RE = re.compile(r"I[-\s]?squared\s+(?:was\s+)?(-?[\d.]+)\s*(?:percent|%)", re.IGNORECASE)
_REF_YEAR_RE = re.compile(r"\b(19\d{2}|20\d{2})\b")
_VALIDATION_RE = re.compile(r"validat\w+\s+against\s+([A-Za-z][A-Za-z\s/,]{3,60})", re.IGNORECASE)
_BIG_NUM_RE = re.compile(r"([\d,]{3,})(?!\s*(?:percent|%|CI|\(|-))\b")
_PERCENT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:percent|%)", re.IGNORECASE)


def split_sentences(body: str) -> list[str]:
    body = (body or "").strip()
    if not body:
        return []
    parts = _SENT_END_RE.split(body)
    return [p.strip() for p in parts if p.strip()]


def extract_effect(body: str) -> dict | None:
    m = _EFFECT_RE.search(body or "")
    if not m:
        return None
    try:
        point = float(m.group(2)); lo = float(m.group(3)); hi = float(m.group(4))
    except (ValueError, IndexError):
        return None
    if hi < lo: lo, hi = hi, lo
    label = m.group(1)
    up = label.upper()
    is_ratio = any(k in up for k in (" OR", "ODDS", " RR", "RISK", "RATE", " HR", "HAZARD"))
    if any(k in up for k in ("AUC", "SENSITIVITY", "SPECIFICITY")):
        is_ratio = False
    return {"label": label, "point": point, "lo": lo, "hi": hi, "is_ratio": is_ratio}


def extract_samples(body: str) -> list[tuple[int, str]]:
    out = []
    for m in _N_SAMPLES_RE.finditer(body or ""):
        try:
            n = int(m.group(1).replace(",", ""))
        except ValueError:
            continue
        if 2 <= n <= 10_000_000:
            out.append((n, m.group(2).lower()))
    return out


def extract_k(body: str) -> int | None:
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
    if not m: return None
    try: return float(m.group(1))
    except ValueError: return None


def extract_big_numbers(body: str) -> list[int]:
    nums = []
    for m in _BIG_NUM_RE.finditer(body or ""):
        try:
            n = int(m.group(1).replace(",", ""))
            if 100 <= n <= 10_000_000:
                nums.append(n)
        except ValueError:
            pass
    return nums


def ref_years(refs: list[str]) -> list[int]:
    years = []
    for r in refs or []:
        m = _REF_YEAR_RE.search(r)
        if m:
            y = int(m.group(1))
            if 1960 <= y <= 2030:
                years.append(y)
    return years


def detect_kind(entry: dict) -> str:
    # Meta-analysis check runs FIRST so methods-papers-about-MA land here
    # (matches build_students_page.py kindOf).
    typ = (entry.get("type") or "").lower().split("|")[0].strip()
    full_type = (entry.get("type") or "").lower()
    title = (entry.get("title") or "").lower()
    body = (entry.get("body") or "").lower()
    is_ma = (
        any(k in typ for k in ("living-ma", "meta-analysis", "pairwise", "network"))
        or typ.startswith("meta-") or typ == "meta"
        or "meta-analysis" in title or "meta analysis" in title
        or "living meta" in title or "network meta" in title
        or " nma " in full_type
        or "meta-analysis" in body
    )
    if is_ma:
        return "livingma"
    if "methods" in typ or "methodological" in typ or "tool" in typ:
        return "methods"
    if "clinical" in typ:
        if extract_effect(body):
            return "livingma"
    return "other"


# ═══ Chart generators — each returns (svg_str, score, why) ═══════════════

def c_anatomy(e: dict) -> tuple[str, int, str]:
    sents = split_sentences(e.get("body", ""))
    if not sents: return "", 0, "no body"
    counts = [len(s.split()) for s in sents]
    max_c = max(counts); n = len(counts); total = sum(counts); avg = total / n
    plot_w = W - MARGIN_L - MARGIN_R; plot_h = H - MARGIN_T - MARGIN_B
    bar_w = plot_w / n * 0.72; gap = plot_w / n * 0.28
    bars = []
    for i, c in enumerate(counts):
        x = MARGIN_L + i * (bar_w + gap) + gap / 2
        h_ = (c / max_c) * plot_h; y = MARGIN_T + (plot_h - h_)
        col = ACCENT if (n == 7 and c <= 35) else (WARN if c > 35 else BLUE)
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h_:.1f}" '
            f'fill="{col}" opacity="0.88"><title>S{i+1}: {c} words</title></rect>'
            f'<text x="{x + bar_w/2:.1f}" y="{MARGIN_T + plot_h + 14:.1f}" fill="{FAINT}" '
            f'font-size="10" text-anchor="middle" font-family="{MONO}">S{i+1}</text>'
            f'<text x="{x + bar_w/2:.1f}" y="{y - 4:.1f}" fill="{FG}" font-size="10" '
            f'text-anchor="middle" font-family="{SANS}">{c}</text>'
        )
    mean_y = MARGIN_T + plot_h - (avg / max_c) * plot_h
    bars.append(
        f'<line x1="{MARGIN_L}" y1="{mean_y:.1f}" x2="{W-MARGIN_R}" y2="{mean_y:.1f}" '
        f'stroke="{DIM}" stroke-dasharray="3,3" opacity="0.5"/>'
    )
    status = "7 sentences ✓" if n == 7 else f"{n} sentences"
    return _svg_wrap("Paper anatomy · words per sentence",
                     f"{total} words · {status} · target ≤156w, 7s", "\n".join(bars)), 3, "anatomy"


def c_effect_forest(e: dict) -> tuple[str, int, str]:
    eff = extract_effect(e.get("body", ""))
    if eff is None: return "", 0, "no effect"
    label, point, lo, hi = eff["label"], eff["point"], eff["lo"], eff["hi"]
    null_val = 1.0 if eff["is_ratio"] else 0.0
    x_min = min(lo, null_val) * 0.9 if eff["is_ratio"] else min(lo, null_val) - 0.1
    x_max = max(hi, null_val) * 1.1 if eff["is_ratio"] else max(hi, null_val) + 0.1
    if x_max - x_min < 0.05: x_min -= 0.2; x_max += 0.2
    plot_w = W - MARGIN_L - MARGIN_R; yc = MARGIN_T + (H - MARGIN_T - MARGIN_B) / 2
    def px(v: float) -> float: return MARGIN_L + (v - x_min) / (x_max - x_min) * plot_w
    nx = px(null_val)
    els = [
        f'<line x1="{nx:.1f}" y1="{MARGIN_T+8}" x2="{nx:.1f}" y2="{H-MARGIN_B}" stroke="{DIM}" stroke-dasharray="4,4" opacity="0.7"/>',
        f'<text x="{nx:.1f}" y="{MARGIN_T+4}" fill="{DIM}" font-size="10" text-anchor="middle" font-family="{SANS}">null = {null_val:g}</text>',
        f'<line x1="{px(lo):.1f}" y1="{yc:.1f}" x2="{px(hi):.1f}" y2="{yc:.1f}" stroke="{ACCENT}" stroke-width="2.5"/>',
        f'<rect x="{px(point)-9:.1f}" y="{yc-9:.1f}" width="18" height="18" fill="{ACCENT}" transform="rotate(45 {px(point):.1f} {yc:.1f})"/>',
        f'<text x="{px(lo):.1f}" y="{yc+28:.1f}" fill="{DIM}" font-size="10" text-anchor="middle" font-family="{MONO}">{lo:g}</text>',
        f'<text x="{px(hi):.1f}" y="{yc+28:.1f}" fill="{DIM}" font-size="10" text-anchor="middle" font-family="{MONO}">{hi:g}</text>',
        f'<text x="{px(point):.1f}" y="{yc-18:.1f}" fill="{ACCENT}" font-size="22" font-weight="700" text-anchor="middle" font-family="{SERIF}">{point:g}</text>',
    ]
    if eff["is_ratio"]:
        left, right = ("favors intervention", "favors control")
        if point > null_val: left, right = right, left
    else:
        left, right = "negative", "positive"
    els.append(
        f'<text x="{MARGIN_L+4}" y="{H-MARGIN_B+18:.1f}" fill="{FAINT}" font-size="10" font-family="{SANS}">← {left}</text>'
        f'<text x="{W-MARGIN_R-4}" y="{H-MARGIN_B+18:.1f}" fill="{FAINT}" font-size="10" text-anchor="end" font-family="{SANS}">{right} →</text>'
    )
    sig = "non-null" if (null_val < lo) or (null_val > hi) else "crosses null"
    return _svg_wrap(f"Primary effect · {e.get('estimand','')[:40] or label}",
                     f"{label}: {point:g} (95% CI {lo:g} to {hi:g}) · {sig}",
                     "\n".join(els)), 3, "effect"


def c_refs_timeline(e: dict) -> tuple[str, int, str]:
    years = ref_years(e.get("references", []))
    if not years: return "", 0, "no ref years"
    y_min = min(years); y_max = max(years)
    if y_max == y_min: y_min -= 1; y_max += 1
    bucket = max(1, (y_max - y_min) // 12)
    buckets: dict[int, int] = {}
    for y in years:
        b = ((y - y_min) // bucket) * bucket + y_min
        buckets[b] = buckets.get(b, 0) + 1
    items = sorted(buckets.items())
    max_n = max(buckets.values())
    plot_w = W - MARGIN_L - MARGIN_R; plot_h = H - MARGIN_T - MARGIN_B
    n = len(items); bar_w = plot_w / n * 0.82; gap = plot_w / n * 0.18
    bars = []
    for i, (b, c) in enumerate(items):
        x = MARGIN_L + i * (bar_w + gap) + gap / 2
        h_ = (c / max_n) * plot_h; y = MARGIN_T + (plot_h - h_)
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h_:.1f}" fill="{BLUE}" opacity="0.88"/>'
            f'<text x="{x + bar_w/2:.1f}" y="{MARGIN_T + plot_h + 14:.1f}" fill="{FAINT}" font-size="9" '
            f'text-anchor="middle" font-family="{MONO}">{b if bucket == 1 else str(b)[-2:]}</text>'
            f'<text x="{x + bar_w/2:.1f}" y="{y - 4:.1f}" fill="{FG}" font-size="10" text-anchor="middle" font-family="{SANS}">{c}</text>'
        )
    rng = f"{y_min}–{y_max}" if y_max > y_min else str(y_min)
    return _svg_wrap("References · publication year",
                     f"{len(years)} dated · {rng} · {bucket}-year buckets",
                     "\n".join(bars), fg=BLUE), 2, "ref years"


def c_scale_bars(e: dict) -> tuple[str, int, str]:
    samples = extract_samples(e.get("body", ""))
    k = extract_k(e.get("body", ""))
    # dedup + top 5 by n
    seen = set(); uniq = []
    for n, u in samples:
        if (n, u) in seen: continue
        seen.add((n, u)); uniq.append((n, u))
    uniq.sort(key=lambda x: -x[0])
    rows = []
    if k is not None: rows.append((f"{k} studies", k))
    for n, u in uniq[:4]: rows.append((f"{n:,} {u}", n))
    if not rows: return "", 0, "no counts"
    max_n = max(r[1] for r in rows)
    plot_w = W - MARGIN_L - MARGIN_R - 80; plot_h = H - MARGIN_T - MARGIN_B
    bar_h = min(26, plot_h / len(rows) * 0.7)
    gap = (plot_h - bar_h * len(rows)) / (len(rows) + 1)
    bars = []
    for i, (lbl, n) in enumerate(rows):
        y = MARGIN_T + gap + i * (bar_h + gap)
        w = (n / max_n) * plot_w
        bars.append(
            f'<rect x="{MARGIN_L}" y="{y:.1f}" width="{w:.1f}" height="{bar_h:.1f}" fill="{PURPLE}" opacity="0.88"/>'
            f'<text x="{MARGIN_L + w + 8:.1f}" y="{y + bar_h/2 + 4:.1f}" fill="{FG}" font-size="11" font-family="{SANS}">{_esc(lbl)}</text>'
        )
    return _svg_wrap("Evidence base · scale",
                     (e.get("data", "") or "counts parsed from body")[:80],
                     "\n".join(bars), fg=PURPLE), 3, "scale"


def c_i2_therm(e: dict) -> tuple[str, int, str]:
    i2 = extract_i2(e.get("body", ""))
    if i2 is None: return "", 0, "no i2"
    v = max(0.0, min(100.0, i2))
    x = MARGIN_L + 40; y = MARGIN_T + 50
    w_max = W - MARGIN_R - x - 60
    fill = w_max * (v / 100)
    col = ACCENT if v < 30 else (WARN if v < 60 else RED)
    tier = "low" if v < 30 else ("moderate" if v < 60 else "substantial")
    body = (
        f'<text x="{x}" y="{y - 12}" fill="{DIM}" font-size="11" font-family="{SANS}">Between-study heterogeneity</text>'
        f'<rect x="{x}" y="{y}" width="{w_max:.1f}" height="30" fill="{BG}" stroke="{BORDER}"/>'
        f'<rect x="{x}" y="{y}" width="{fill:.1f}" height="30" fill="{col}" opacity="0.88"/>'
        f'<text x="{x + fill + 10:.1f}" y="{y + 22}" fill="{FG}" font-size="22" font-weight="700" font-family="{SERIF}">{v:g}%</text>'
        f'<text x="{x}" y="{y + 52}" fill="{DIM}" font-size="10" font-family="{MONO}">0%</text>'
        f'<text x="{x + w_max/3:.1f}" y="{y + 52}" fill="{DIM}" font-size="10" text-anchor="middle" font-family="{MONO}">30</text>'
        f'<text x="{x + 2*w_max/3:.1f}" y="{y + 52}" fill="{DIM}" font-size="10" text-anchor="middle" font-family="{MONO}">60</text>'
        f'<text x="{x + w_max:.1f}" y="{y + 52}" fill="{DIM}" font-size="10" text-anchor="end" font-family="{MONO}">100%</text>'
        f'<text x="{x}" y="{y + 84}" fill="{col}" font-size="13" font-weight="600" font-family="{SANS}">{tier} heterogeneity</text>'
        f'<text x="{x}" y="{y + 102}" fill="{DIM}" font-size="10" font-family="{SANS}">random-effects pooling · prediction interval recommended alongside CI</text>'
    )
    return _svg_wrap("Heterogeneity · I²", f"I² = {v:g}% (random-effects MA)", body, fg=WARN), 3, "i2"


def c_method_schematic(e: dict) -> tuple[str, int, str]:
    typ = (e.get("type") or "").split("|")[0].strip()
    body = (
        f'<rect x="30" y="80" width="130" height="90" fill="{BG}" stroke="{ACCENT}" stroke-width="1.5" rx="6"/>'
        f'<text x="95" y="110" fill="{FG}" font-size="11" text-anchor="middle" font-weight="600" font-family="{SANS}">INPUT</text>'
        f'<text x="95" y="132" fill="{DIM}" font-size="10" text-anchor="middle" font-family="{SANS}">{_esc(e.get("data","")[:20])}</text>'
        f'<text x="95" y="150" fill="{DIM}" font-size="9" text-anchor="middle" font-family="{SANS}">workbook metadata</text>'
        f'<rect x="195" y="70" width="130" height="110" fill="{BG}" stroke="{BLUE}" stroke-width="1.5" rx="6"/>'
        f'<text x="260" y="100" fill="{FG}" font-size="11" text-anchor="middle" font-weight="600" font-family="{SANS}">METHOD</text>'
        f'<text x="260" y="122" fill="{DIM}" font-size="10" text-anchor="middle" font-family="{SANS}">{_esc(e.get("name","")[:22])}</text>'
        f'<text x="260" y="140" fill="{DIM}" font-size="9" text-anchor="middle" font-family="{SANS}">{_esc(typ[:28])}</text>'
        f'<text x="260" y="158" fill="{DIM}" font-size="9" text-anchor="middle" font-family="{SANS}">browser / Python / R</text>'
        f'<rect x="360" y="80" width="130" height="90" fill="{BG}" stroke="{WARN}" stroke-width="1.5" rx="6"/>'
        f'<text x="425" y="110" fill="{FG}" font-size="11" text-anchor="middle" font-weight="600" font-family="{SANS}">OUTPUT</text>'
        f'<text x="425" y="132" fill="{DIM}" font-size="10" text-anchor="middle" font-family="{SANS}">{_esc((e.get("estimand","") or "estimate")[:20])}</text>'
        f'<text x="425" y="150" fill="{DIM}" font-size="9" text-anchor="middle" font-family="{SANS}">+ audit trail</text>'
        f'<path d="M160 125 L195 125" stroke="{FG}" stroke-width="1.5" marker-end="url(#a)"/>'
        f'<path d="M325 125 L360 125" stroke="{FG}" stroke-width="1.5" marker-end="url(#a)"/>'
        f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0 0 L10 5 L0 10 Z" fill="{FG}"/></marker></defs>'
    )
    return _svg_wrap("Method schematic · input → method → output",
                     "Auto-generated from TITLE/DATA/TYPE", body), 2, "schematic"


def c_validation(e: dict) -> tuple[str, int, str]:
    m = _VALIDATION_RE.search(e.get("body", ""))
    if not m: return "", 0, "no validation"
    target = m.group(1).strip().rstrip(".,;").split(" and ")[0][:50]
    body = (
        f'<text x="{W/2}" y="{MARGIN_T + 40}" fill="{DIM}" font-size="11" text-anchor="middle" font-family="{SANS}">Validated against</text>'
        f'<text x="{W/2}" y="{MARGIN_T + 86}" fill="{ACCENT}" font-size="28" font-weight="700" text-anchor="middle" font-family="{SERIF}">{_esc(target)}</text>'
        f'<line x1="{W/2-80}" y1="{MARGIN_T+108}" x2="{W/2+80}" y2="{MARGIN_T+108}" stroke="{BORDER}"/>'
        f'<text x="{W/2}" y="{MARGIN_T + 134}" fill="{DIM}" font-size="11" text-anchor="middle" font-family="{SANS}">reference implementation / benchmark</text>'
    )
    return _svg_wrap("External validation",
                     "Cross-checked against an established implementation", body, fg=ACCENT), 3, "validation"


# ─── NYT-style infoboxes ──────────────────────────────────────────────────

def _big_stat(headline: str, caption: str, context: str, fg: str = ACCENT) -> str:
    body = (
        f'<text x="{W/2}" y="{MARGIN_T + 70}" fill="{fg}" font-size="48" '
        f'font-weight="700" text-anchor="middle" font-family="{SERIF}">{_esc(headline)}</text>'
        f'<line x1="{W/2-60}" y1="{MARGIN_T + 92}" x2="{W/2+60}" y2="{MARGIN_T + 92}" stroke="{BORDER}"/>'
        f'<text x="{W/2}" y="{MARGIN_T + 115}" fill="{FG}" font-size="13" '
        f'text-anchor="middle" font-family="{SANS}">{_esc(caption)}</text>'
        f'<text x="{W/2}" y="{MARGIN_T + 135}" fill="{DIM}" font-size="10.5" '
        f'text-anchor="middle" font-family="{SANS}">{_esc(context)}</text>'
    )
    return body


def c_big_number(e: dict) -> tuple[str, int, str]:
    """NYT-style: largest number from body, with contextual caption."""
    nums = extract_big_numbers(e.get("body", ""))
    if not nums: return "", 0, "no big number"
    n = max(nums)
    # Find the unit near the number by re-scanning
    body_text = e.get("body", "")
    m = re.search(rf"{n:,}\s+(\w+(?:\s+\w+)?)".replace(",", r",?"), body_text)
    context = m.group(1)[:50] if m else "count referenced in body"
    svg_body = _big_stat(f"{n:,}", context, "— from the 156-word body", fg=PURPLE)
    return _svg_wrap("By the numbers", "A headline count from this paper",
                     svg_body, fg=PURPLE), 2, "big num"


def c_reference_count(e: dict) -> tuple[str, int, str]:
    refs = e.get("references", []) or []
    if not refs: return "", 0, "no refs"
    svg_body = _big_stat(str(len(refs)), "reference(s) in the workbook",
                         "the starter topic-pack the student should build on", fg=BLUE)
    return _svg_wrap("Evidence pedigree",
                     f"{len(refs)} curated references · Vancouver / NLM style",
                     svg_body, fg=BLUE), 2, "ref count"


def c_estimand_card(e: dict) -> tuple[str, int, str]:
    est = (e.get("estimand") or "").strip()
    if not est: return "", 0, "no estimand"
    # Wrap the estimand across up to 3 lines
    words = est.split(); lines = []; cur = ""
    for w in words:
        if len(cur) + len(w) + 1 > 42 and cur:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur: lines.append(cur)
    lines = lines[:3]
    body = (
        f'<text x="{W/2}" y="{MARGIN_T + 40}" fill="{DIM}" font-size="11" '
        f'text-anchor="middle" font-family="{SANS}">Primary estimand</text>'
    )
    y0 = MARGIN_T + 84
    for i, ln in enumerate(lines):
        body += (
            f'<text x="{W/2}" y="{y0 + i*28:.1f}" fill="{FG}" font-size="20" '
            f'font-weight="700" text-anchor="middle" font-family="{SERIF}">{_esc(ln)}</text>'
        )
    body += (
        f'<text x="{W/2}" y="{MARGIN_T + 145:.1f}" fill="{DIM}" font-size="10.5" '
        f'text-anchor="middle" font-family="{SANS}">the quantity the paper reports</text>'
    )
    return _svg_wrap("The estimand", (e.get("type") or "")[:60], body, fg=ACCENT), 2, "estimand"


def c_dataset_card(e: dict) -> tuple[str, int, str]:
    data = (e.get("data") or "").strip()
    if not data: return "", 0, "no data"
    # Pull a headline number from the dataset string if present
    mnum = re.search(r"([\d,]{2,})", data)
    headline = mnum.group(1) if mnum else "Dataset"
    caption = data[:60] if not mnum else data[:70]
    context = "the evidence base this paper analyses"
    svg_body = _big_stat(headline, caption, context, fg=WARN)
    return _svg_wrap("The dataset",
                     (e.get("type") or "")[:60] or "data source",
                     svg_body, fg=WARN), 2, "dataset"


def c_authorship_triangle(e: dict) -> tuple[str, int, str]:
    body = (
        f'<text x="{W/2}" y="{MARGIN_T + 24}" fill="{DIM}" font-size="11" '
        f'text-anchor="middle" font-family="{SANS}">Authorship roles · fixed across workbook</text>'
        # Three nodes
        f'<circle cx="100" cy="140" r="36" fill="{ACCENT}" opacity="0.85"/>'
        f'<text x="100" y="138" fill="{BG}" font-size="10.5" text-anchor="middle" font-weight="700" font-family="{SANS}">FIRST</text>'
        f'<text x="100" y="152" fill="{BG}" font-size="9.5" text-anchor="middle" font-family="{SANS}">student</text>'
        f'<text x="100" y="192" fill="{FG}" font-size="10" text-anchor="middle" font-family="{SANS}">+ corresponding</text>'
        f'<circle cx="260" cy="110" r="36" fill="{BLUE}" opacity="0.85"/>'
        f'<text x="260" y="108" fill="{BG}" font-size="10.5" text-anchor="middle" font-weight="700" font-family="{SANS}">MIDDLE</text>'
        f'<text x="260" y="122" fill="{BG}" font-size="9.5" text-anchor="middle" font-family="{SANS}">Mahmood</text>'
        f'<text x="260" y="160" fill="{FG}" font-size="10" text-anchor="middle" font-family="{SANS}">Conceptualization,</text>'
        f'<text x="260" y="174" fill="{FG}" font-size="10" text-anchor="middle" font-family="{SANS}">Methodology, Software</text>'
        f'<circle cx="420" cy="140" r="36" fill="{PURPLE}" opacity="0.85"/>'
        f'<text x="420" y="138" fill="{BG}" font-size="10.5" text-anchor="middle" font-weight="700" font-family="{SANS}">SENIOR</text>'
        f'<text x="420" y="152" fill="{BG}" font-size="9.5" text-anchor="middle" font-family="{SANS}">supervisor</text>'
        f'<text x="420" y="192" fill="{FG}" font-size="10" text-anchor="middle" font-family="{SANS}">faculty co-investigator</text>'
        # Edges
        f'<line x1="136" y1="135" x2="224" y2="118" stroke="{DIM}" stroke-width="1" opacity="0.5"/>'
        f'<line x1="296" y1="118" x2="384" y2="135" stroke="{DIM}" stroke-width="1" opacity="0.5"/>'
    )
    return _svg_wrap("Authorship",
                     "student (first + corresponding) → Mahmood (middle) → supervisor (senior)",
                     body, fg=PURPLE), 1, "authorship"


def c_contract_gauge(e: dict) -> tuple[str, int, str]:
    sents = split_sentences(e.get("body", ""))
    n = len(sents); words = sum(len(s.split()) for s in sents)
    sent_ok = n == 7; word_ok = words <= 156
    s_col = ACCENT if sent_ok else (WARN if abs(n - 7) <= 1 else RED)
    w_col = ACCENT if word_ok else (WARN if words <= 180 else RED)
    s_mark = "✓" if sent_ok else "✗"
    w_mark = "✓" if word_ok else "✗"
    body = (
        f'<text x="{W/2}" y="{MARGIN_T + 28}" fill="{DIM}" font-size="11" '
        f'text-anchor="middle" font-family="{SANS}">E156 contract · 7 sentences, ≤ 156 words</text>'
        f'<g transform="translate(150, 110)">'
        f'  <circle r="42" fill="none" stroke="{BORDER}" stroke-width="3"/>'
        f'  <circle r="42" fill="none" stroke="{s_col}" stroke-width="3" stroke-dasharray="{min(n,7) * 37.7:.1f} 1000"/>'
        f'  <text y="-4" fill="{s_col}" font-size="26" font-weight="700" text-anchor="middle" font-family="{SERIF}">{n}</text>'
        f'  <text y="14" fill="{DIM}" font-size="9" text-anchor="middle" font-family="{SANS}">sentences {s_mark}</text>'
        f'</g>'
        f'<g transform="translate(370, 110)">'
        f'  <circle r="42" fill="none" stroke="{BORDER}" stroke-width="3"/>'
        f'  <circle r="42" fill="none" stroke="{w_col}" stroke-width="3" stroke-dasharray="{min(words,156)/156 * 264:.1f} 1000"/>'
        f'  <text y="-4" fill="{w_col}" font-size="22" font-weight="700" text-anchor="middle" font-family="{SERIF}">{words}</text>'
        f'  <text y="14" fill="{DIM}" font-size="9" text-anchor="middle" font-family="{SANS}">words {w_mark}</text>'
        f'</g>'
        f'<text x="{W/2}" y="{H-MARGIN_B-2}" fill="{DIM}" font-size="10" '
        f'text-anchor="middle" font-family="{SANS}">outer ring fills at the target (7 sentences / 156 words)</text>'
    )
    return _svg_wrap("Format contract", "dual-ring progress · student should keep both green",
                     body, fg=ACCENT), 2, "contract"


# ═══ Pools by kind ════════════════════════════════════════════════════════
# Ordered roughly by relevance; tie-break uses this order.

POOL_METHODS: list[Callable] = [
    c_anatomy,
    c_method_schematic,
    c_validation,
    c_contract_gauge,
    c_big_number,
    c_scale_bars,
    c_effect_forest,
    c_refs_timeline,
    c_estimand_card,
    c_dataset_card,
    c_reference_count,
    c_authorship_triangle,
]

POOL_LIVINGMA: list[Callable] = [
    c_effect_forest,
    c_i2_therm,
    c_anatomy,
    c_scale_bars,
    c_refs_timeline,
    c_estimand_card,
    c_big_number,
    c_dataset_card,
    c_contract_gauge,
    c_reference_count,
    c_method_schematic,
    c_authorship_triangle,
]

POOL_OTHER: list[Callable] = [
    c_anatomy,
    c_effect_forest,
    c_scale_bars,
    c_refs_timeline,
    c_estimand_card,
    c_dataset_card,
    c_big_number,
    c_reference_count,
    c_contract_gauge,
    c_method_schematic,
    c_i2_therm,
    c_authorship_triangle,
]


def render_all_charts(entry: dict) -> str:
    """Pick the 5 highest-scoring charts for this paper's kind."""
    kind = detect_kind(entry)
    pool = {"methods": POOL_METHODS, "livingma": POOL_LIVINGMA}.get(kind, POOL_OTHER)
    results = []
    for order, fn in enumerate(pool):
        try:
            svg, score, why = fn(entry)
        except Exception as ex:  # defensive: never crash the build
            svg, score, why = "", 0, f"err:{ex}"
        if score > 0 and svg:
            results.append((score, -order, svg))  # high score first; ties by pool order
    results.sort(reverse=True)
    chosen = [r[2] for r in results[:5]]
    # Sanity: pad with authorship triangle if somehow fewer than 5 (shouldn't happen)
    while len(chosen) < 5:
        svg, _, _ = c_authorship_triangle(entry)
        chosen.append(svg)
    return (
        '<section class="charts">'
        f'<h2>Paper dashboard · 5 views (kind: {kind})</h2>'
        '<div class="chart-grid">'
        + "".join(f'<div class="chart-tile">{c}</div>' for c in chosen)
        + '</div></section>'
    )
