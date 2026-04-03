"""
Generate beautiful self-contained HTML dashboards for projects without visual assets.
Each dashboard includes: hero metrics, method flow diagram, key result chart,
sentence structure visualization, and project metadata — all in NYT editorial style.
"""

import json
import html as html_mod
import re
import os
import sys
from pathlib import Path


def h(s):
    """HTML-escape a string."""
    return html_mod.escape(str(s or ""))

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))


def extract_numbers(text):
    """Pull key numbers from paper body for visualization."""
    nums = []
    # Match patterns like "0.85 (95% CI 0.72-1.13)" or "34% (IQR 18-52%)"
    for m in re.finditer(r'(-?\d+\.?\d*)\s*(?:percent|%)?\s*\((?:9[059]%?\s*CI|IQR|CrI)\s*(-?[\d.]+)\s*(?:to|-|\u2013)\s*(-?[\d.]+)', text, re.I):
        nums.append({'value': float(m.group(1)), 'lo': float(m.group(2)), 'hi': float(m.group(3)),
                      'raw': m.group(0)})
    # Match standalone percentages
    for m in re.finditer(r'(\d+\.?\d*)\s*percent', text):
        val = float(m.group(1))
        if not any(abs(n['value'] - val) < 0.01 for n in nums):
            nums.append({'value': val, 'lo': None, 'hi': None, 'raw': m.group(0)})
    return nums


def extract_metrics(config):
    """Extract display metrics from config."""
    body = config.get('body', '')
    notes = config.get('notes', {})
    metrics = []

    # Test count
    data = notes.get('data', '')
    test_match = re.search(r'(\d+)\s*(?:tests?|checks?|validat)', data + ' ' + body, re.I)
    if test_match:
        metrics.append(('Tests', test_match.group(1), 'Validation checks passed'))

    # Study/dataset count
    study_match = re.search(r'(\d+)\s*(?:studi|reviews?|trials?|datasets?|papers?)', body, re.I)
    if study_match:
        metrics.append(('Studies', study_match.group(1), 'Evidence base'))

    # Participant count
    part_match = re.search(r'([\d,]+)\s*(?:participants?|patients?|subjects?)', body, re.I)
    if part_match:
        metrics.append(('Participants', part_match.group(1), 'Sample size'))

    # Primary number from S4
    nums = extract_numbers(body)
    if nums:
        n = nums[0]
        if n['lo'] is not None:
            metrics.append(('Primary Result', f"{n['value']}", f"CI: {n['lo']}–{n['hi']}"))
        else:
            metrics.append(('Key Metric', f"{n['value']}%", 'Primary finding'))

    # Ensure at least 3 metrics
    if len(metrics) < 2:
        metrics.append(('Type', config.get('type', 'methods').title(), 'Study design'))
    if len(metrics) < 3:
        wc = len(body.split())
        metrics.append(('Words', str(wc), 'E156 body length'))

    return metrics[:4]


def generate_dashboard(config):
    """Generate a self-contained HTML dashboard."""
    title = config.get('title', 'Untitled')
    body = config.get('body', '')
    notes = config.get('notes', {})
    estimand = config.get('primary_estimand', '')
    proj_type = config.get('type', 'methods')
    author = config.get('author', 'Mahmood Ahmad')
    date = config.get('date', '2026-03-28')
    code_url = notes.get('code', '')
    sentences = config.get('sentences', [])

    metrics = extract_metrics(config)
    nums = extract_numbers(body)

    # Build sentence labels
    role_names = ['Question', 'Dataset', 'Method', 'Primary Result', 'Robustness', 'Interpretation', 'Boundary']
    role_colors = ['#2E86C1', '#28B463', '#7D3C98', '#CB4335', '#D68910', '#148F77', '#85929E']

    sent_texts = []
    for s in sentences:
        sent_texts.append(s['text'] if isinstance(s, dict) else s)
    if not sent_texts and body:
        sent_texts = re.split(r'(?<=[.!?])\s+(?=[A-Z])', body)

    # Build method steps from S3
    method_text = sent_texts[2] if len(sent_texts) > 2 else 'Analysis pipeline'
    method_words = method_text.split()
    # Create 3-4 method steps
    steps = []
    if 'random-effects' in method_text.lower() or 'meta-analysis' in method_text.lower():
        steps = ['Data Extraction', 'Effect Size Computation', 'Random-Effects Pooling', 'Sensitivity Analysis']
    elif 'bayesian' in method_text.lower():
        steps = ['Prior Specification', 'Likelihood Construction', 'Posterior Sampling', 'Model Comparison']
    elif 'network' in method_text.lower() or 'nma' in method_text.lower():
        steps = ['Network Construction', 'Consistency Check', 'NMA Pooling', 'Ranking']
    elif 'simulation' in method_text.lower():
        steps = ['Parameter Setup', 'Scenario Generation', 'Simulation Runs', 'Performance Metrics']
    elif 'extract' in method_text.lower() or 'nlp' in method_text.lower():
        steps = ['Input Processing', 'Pattern Recognition', 'Entity Extraction', 'Validation']
    elif 'multilevel' in method_text.lower() or 'three-level' in method_text.lower():
        steps = ['Data Structuring', 'Variance Decomposition', 'REML Estimation', 'Profile Likelihood']
    else:
        steps = ['Input', 'Processing', 'Analysis', 'Output']

    # Build the chart SVG — bar chart of key metric or CI plot
    chart_svg = ''
    if nums:
        n = nums[0]
        if n['lo'] is not None and n['hi'] is not None:
            # CI/IQR plot
            val, lo, hi = n['value'], n['lo'], n['hi']
            # Determine scale
            all_vals = [lo, val, hi]
            span = max(all_vals) - min(all_vals)
            margin = max(span * 0.2, 0.1)  # at least 0.1 unit padding
            mn = min(all_vals) - margin
            mx = max(all_vals) + margin
            rng = max(mx - mn, 1e-10)
            def sx(v): return 80 + (v - mn) / rng * 400

            chart_svg = f'''<svg viewBox="0 0 560 120" style="width:100%;max-width:560px;height:auto" role="img" aria-label="Primary result confidence interval plot">
  <title>Primary result: {val} (CI {lo} to {hi})</title>
  <rect x="0" y="0" width="560" height="120" fill="#FDFCFA" rx="8"/>
  <text x="280" y="22" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#767676" letter-spacing="0.1em" text-transform="uppercase">PRIMARY RESULT WITH CONFIDENCE INTERVAL</text>
  <line x1="{sx(lo)}" y1="60" x2="{sx(hi)}" y2="60" stroke="#CB4335" stroke-width="3" stroke-linecap="round"/>
  <circle cx="{sx(val)}" cy="60" r="8" fill="#CB4335"/>
  <text x="{sx(val)}" y="52" text-anchor="middle" font-family="Georgia,serif" font-size="14" font-weight="700" fill="#1a1a1a">{val}</text>
  <text x="{sx(lo)}" y="85" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#767676">{lo}</text>
  <text x="{sx(hi)}" y="85" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#767676">{hi}</text>
  <text x="{sx(val)}" y="108" text-anchor="middle" font-family="system-ui,sans-serif" font-size="10" fill="#aaa">{estimand or "Effect estimate"}</text>
</svg>'''
        else:
            # Single metric bar
            val = n['value']
            bar_w = min(val / 100 * 400, 400) if val <= 100 else 300
            chart_svg = f'''<svg viewBox="0 0 560 90" style="width:100%;max-width:560px;height:auto" role="img" aria-label="Key metric: {val} percent">
  <title>Key metric: {val}%</title>
  <rect x="0" y="0" width="560" height="90" fill="#FDFCFA" rx="8"/>
  <text x="280" y="22" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#767676" letter-spacing="0.1em">KEY METRIC</text>
  <rect x="80" y="35" width="{bar_w}" height="24" fill="#CB4335" rx="4" opacity="0.85"/>
  <text x="{85+bar_w}" y="52" font-family="Georgia,serif" font-size="16" font-weight="700" fill="#1a1a1a"> {val}%</text>
  <text x="280" y="78" text-anchor="middle" font-family="system-ui,sans-serif" font-size="10" fill="#aaa">{estimand or "Primary metric"}</text>
</svg>'''

    # Sentence structure diagram
    sent_svg_items = ''
    for i, (rn, rc) in enumerate(zip(role_names[:len(sent_texts)], role_colors[:len(sent_texts)])):
        y = 30 + i * 38
        w = min(len(sent_texts[i].split()) * 8, 350) if i < len(sent_texts) else 100
        preview = sent_texts[i][:55] + '...' if i < len(sent_texts) and len(sent_texts[i]) > 55 else (sent_texts[i] if i < len(sent_texts) else '')
        sent_svg_items += f'''<rect x="130" y="{y}" width="{w}" height="26" fill="{rc}" opacity="0.15" rx="4"/>
  <rect x="130" y="{y}" width="4" height="26" fill="{rc}" rx="2"/>
  <text x="20" y="{y+17}" font-family="system-ui,sans-serif" font-size="10" font-weight="700" fill="{rc}" letter-spacing="0.05em">{rn.upper()}</text>
  <text x="142" y="{y+17}" font-family="Georgia,serif" font-size="11" fill="#333">{preview.replace("&","&amp;").replace("<","&lt;")}</text>
'''

    sent_svg = f'''<svg viewBox="0 0 560 300" style="width:100%;max-width:560px;height:auto">
  <rect x="0" y="0" width="560" height="300" fill="#FDFCFA" rx="8"/>
  <text x="280" y="18" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#767676" letter-spacing="0.1em">7-SENTENCE STRUCTURE</text>
  {sent_svg_items}
</svg>'''

    # Method flow diagram
    flow_items = ''
    for i, step in enumerate(steps):
        x = 20 + i * 135
        flow_items += f'''<rect x="{x}" y="35" width="120" height="40" fill="#8B6914" opacity="0.1" rx="6" stroke="#8B6914" stroke-width="1.5"/>
  <text x="{x+60}" y="59" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" font-weight="600" fill="#6d5210">{step}</text>'''
        if i < len(steps) - 1:
            flow_items += f'\n  <text x="{x+128}" y="58" font-family="system-ui,sans-serif" font-size="16" fill="#ccc">\u2192</text>'

    flow_svg = f'''<svg viewBox="0 0 560 90" style="width:100%;max-width:560px;height:auto">
  <rect x="0" y="0" width="560" height="90" fill="#FDFCFA" rx="8"/>
  <text x="280" y="20" text-anchor="middle" font-family="system-ui,sans-serif" font-size="11" fill="#767676" letter-spacing="0.1em">METHOD PIPELINE</text>
  {flow_items}
</svg>'''

    # Metrics cards HTML
    metrics_html = ''
    for label, value, desc in metrics:
        metrics_html += f'''<div style="flex:1;min-width:140px;background:#fff;border:1px solid #E5E0D6;border-top:3px solid #8B6914;border-radius:6px;padding:16px;text-align:center">
      <div style="font-family:system-ui,sans-serif;font-size:10px;letter-spacing:0.15em;text-transform:uppercase;color:#767676;margin-bottom:8px">{h(label)}</div>
      <div style="font-family:Georgia,serif;font-size:28px;font-weight:700;color:#1a1a1a;line-height:1.1">{h(value)}</div>
      <div style="font-family:system-ui,sans-serif;font-size:11px;color:#aaa;margin-top:4px">{h(desc)}</div>
    </div>'''

    # Full dashboard HTML
    esc_title = h(title)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc_title} — Dashboard</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Georgia,'Times New Roman',serif;background:#FDFCFA;color:#1a1a1a;line-height:1.7;-webkit-font-smoothing:antialiased}}
.page{{max-width:680px;margin:0 auto;padding:2.5rem 1.5rem 3rem}}
h1{{font-size:1.6rem;font-weight:700;line-height:1.3;margin-bottom:.5rem}}
.byline{{font-family:system-ui,sans-serif;font-size:.82rem;color:#777;margin-bottom:2rem;padding-bottom:1rem;border-bottom:3px double #E5E0D6}}
.section-label{{font-family:system-ui,sans-serif;font-size:.65rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#8B6914;margin-bottom:.8rem;padding-bottom:.4rem;border-bottom:1px solid #E5E0D6}}
.metrics{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:2rem}}
.chart-area{{margin-bottom:2rem;text-align:center}}
.body-text{{font-size:1.05rem;line-height:1.9;text-align:justify;margin-bottom:2rem;padding:1.2rem 1.5rem;background:#F5F3EE;border-radius:8px;border-left:3px solid #8B6914}}
.notes{{font-family:system-ui,sans-serif;font-size:.82rem;color:#555;display:grid;grid-template-columns:auto 1fr;gap:.3rem .8rem;margin-bottom:1.5rem}}
.notes dt{{font-weight:600;color:#333}}.notes dd a{{color:#2E6B8A;text-decoration:none}}
.footer{{font-family:system-ui,sans-serif;font-size:.7rem;color:#aaa;padding-top:1rem;border-top:1px solid #E5E0D6;text-align:center}}
@media(max-width:600px){{.metrics{{flex-direction:column}}.page{{padding:1.5rem 1rem}}h1{{font-size:1.3rem}}}}
@media print{{body{{background:#fff}}.page{{max-width:100%}}}}
</style>
</head>
<body>
<div class="page">
  <div style="font-family:system-ui,sans-serif;font-size:.6rem;font-weight:700;letter-spacing:.25em;text-transform:uppercase;color:#8B6914;margin-bottom:1rem">E156 Project Dashboard</div>
  <h1>{esc_title}</h1>
  <div class="byline">{h(author)} &middot; {h(date)} &middot; {h(proj_type.title())}</div>

  <div class="section-label">Key Metrics</div>
  <div class="metrics">{metrics_html}</div>

  <div class="section-label">Method Pipeline</div>
  <div class="chart-area">{flow_svg}</div>

  {"<div class='section-label'>Primary Result</div><div class='chart-area'>" + chart_svg + "</div>" if chart_svg else ""}

  <div class="section-label">Sentence Structure</div>
  <div class="chart-area">{sent_svg}</div>

  <div class="section-label">Paper Body (156 Words)</div>
  <div class="body-text">{body.replace("&","&amp;").replace("<","&lt;")}</div>

  <div class="section-label">Outside Notes</div>
  <dl class="notes">
    <dt>App</dt><dd>{h(notes.get("app","—"))}</dd>
    <dt>Data</dt><dd>{h(notes.get("data","—"))}</dd>
    <dt>Code</dt><dd>{"<a href='"+h(code_url)+"' target='_blank' rel='noopener noreferrer'>"+h(code_url)+"</a>" if code_url.startswith("http") else h(code_url) or "—"}</dd>
    <dt>Estimand</dt><dd>{h(estimand) or "—"}</dd>
  </dl>

  <div class="footer">E156 Micro-Paper Dashboard &middot; Generated {date}</div>
</div>
</body>
</html>'''

    return html


def main():
    from e156_utils import find_all_submissions
    subs = find_all_submissions()

    generated = 0
    for sub in subs:
        assets_dir = sub / 'assets'
        # Only generate for projects without existing assets
        if assets_dir.is_dir() and any(assets_dir.iterdir()):
            continue

        cfg = sub / 'config.json'
        if not cfg.exists():
            continue

        try:
            config = json.loads(cfg.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, ValueError, UnicodeDecodeError, OSError):
            try:
                config = json.loads(cfg.read_text(encoding='utf-8-sig'))
            except (json.JSONDecodeError, ValueError, UnicodeDecodeError, OSError):
                continue

        dashboard_html = generate_dashboard(config)
        assets_dir.mkdir(parents=True, exist_ok=True)
        (assets_dir / 'dashboard.html').write_text(dashboard_html, encoding='utf-8')
        generated += 1
        print(f'  {sub.parent.name}: dashboard.html ({len(dashboard_html)} bytes)')

    print(f'\nGenerated {generated} dashboards')

    # Now regenerate index.html for these projects so they pick up the new assets
    from generate_submission import generate_submission
    regen = 0
    for sub in subs:
        dashboard = sub / 'assets' / 'dashboard.html'
        if not dashboard.exists():
            continue
        cfg = sub / 'config.json'
        if not cfg.exists():
            continue
        try:
            config = json.loads(cfg.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, ValueError, UnicodeDecodeError, OSError):
            try:
                config = json.loads(cfg.read_text(encoding='utf-8-sig'))
            except (json.JSONDecodeError, ValueError, UnicodeDecodeError, OSError):
                continue
        config['path'] = str(sub.parent)
        try:
            generate_submission(config)
            regen += 1
        except (json.JSONDecodeError, ValueError, UnicodeDecodeError, OSError):
            pass

    print(f'Regenerated {regen} index.html files with dashboard links')


if __name__ == '__main__':
    main()
