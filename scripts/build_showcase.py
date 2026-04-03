"""
Build a world-class editorial portfolio dashboard.
Design: NYT meets Bloomberg meets Stripe.
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from e156_utils import find_all_submissions

GH_USER = os.environ.get("E156_GH_USER", "mahmood726-cyber")
BASE = f"https://{GH_USER}.github.io"


def h(s):
    """HTML-escape."""
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&#39;")


def load_projects():
    subs = find_all_submissions()

    # Load actual repo name mapping
    mapping_path = SCRIPT_DIR / "repo_mapping.json"
    repo_map = {}
    if mapping_path.exists():
        repo_map = json.loads(mapping_path.read_text(encoding="utf-8"))

    projects = []
    for sub in subs:
        cfg = sub / "config.json"
        if not cfg.exists():
            continue
        try:
            c = json.loads(cfg.read_text(encoding="utf-8"))
        except:
            continue

        name = sub.parent.name
        # Use actual repo name from git remote, not guessed from dir name
        repo = repo_map.get(str(sub.parent), name.lower().replace(" ", "-").replace("_", "-"))
        body = c.get("body", "")
        sents = c.get("sentences", [])
        s1 = sents[0].get("text", "") if sents and isinstance(sents[0], dict) else (sents[0] if sents else "")
        s4 = sents[3].get("text", "") if len(sents) > 3 and isinstance(sents[3], dict) else (sents[3] if len(sents) > 3 else "")
        s6 = sents[5].get("text", "") if len(sents) > 5 and isinstance(sents[5], dict) else (sents[5] if len(sents) > 5 else "")
        notes = c.get("notes", {})

        assets_dir = sub / "assets"
        has_app = False
        has_figs = False
        fig_count = 0
        first_fig = ""
        app_name = ""
        if assets_dir.is_dir():
            for f in sorted(assets_dir.iterdir()):
                if f.suffix == ".html" and f.name != "index.html":
                    has_app = True
                    if not app_name:
                        app_name = f.name
                elif f.suffix in (".png", ".jpg", ".svg"):
                    has_figs = True
                    fig_count += 1
                    if not first_fig:
                        first_fig = f.name

        projects.append({
            "name": name, "repo": repo,
            "title": c.get("title", name),
            "type": c.get("type", "methods"),
            "estimand": c.get("primary_estimand", ""),
            "body": body, "s1": s1, "s4": s4, "s6": s6,
            "has_app": has_app, "has_figs": has_figs,
            "fig_count": fig_count, "first_fig": first_fig,
            "app_name": app_name,
            "wc": len(body.split()),
            "code": notes.get("code", ""),
        })

    return projects


def build_dashboard(projects):
    # Sort: featured first (has figs + app), then by type
    featured = sorted(
        [p for p in projects if p["has_figs"] and p["has_app"] and p["s4"]],
        key=lambda p: p["fig_count"], reverse=True
    )[:6]

    # Type distribution for chart
    types = {}
    for p in projects:
        t = p["type"]
        types[t] = types.get(t, 0) + 1
    type_items = sorted(types.items(), key=lambda x: -x[1])

    # Stats
    total = len(projects)
    apps = sum(1 for p in projects if p["has_app"])
    figs = sum(1 for p in projects if p["has_figs"])
    exact_156 = sum(1 for p in projects if p["wc"] == 156)

    # Type chart SVG (horizontal bar)
    max_count = max(v for _, v in type_items) if type_items else 1
    type_bars = ""
    colors = ["#2E86C1", "#28B463", "#7D3C98", "#CB4335", "#D68910", "#148F77", "#85929E", "#E74C3C"]
    for i, (t, count) in enumerate(type_items[:8]):
        y = i * 36
        w = count / max_count * 320
        c = colors[i % len(colors)]
        type_bars += f'''<rect x="120" y="{y+2}" width="{w}" height="24" fill="{c}" rx="4" opacity="0.85"/>
    <text x="115" y="{y+18}" text-anchor="end" font-size="12" fill="#666">{h(t)}</text>
    <text x="{125+w}" y="{y+18}" font-size="12" font-weight="700" fill="#333">{count}</text>\n'''

    type_svg_h = len(type_items[:8]) * 36 + 10
    type_svg = f'<svg viewBox="0 0 500 {type_svg_h}" style="width:100%;max-width:500px">{type_bars}</svg>'

    # Featured cards
    featured_html = ""
    for i, p in enumerate(featured):
        fig_src = f"{BASE}/{p['repo']}/e156-submission/assets/{p['first_fig']}" if p["first_fig"] else ""
        app_url = f"{BASE}/{p['repo']}/e156-submission/assets/{p['app_name']}" if p["app_name"] else ""
        paper_url = f"{BASE}/{p['repo']}/e156-submission/"
        delay = i * 0.08

        featured_html += f'''<article class="feat" style="animation-delay:{delay}s">
      {"<img src='" + h(fig_src) + "' alt='" + h(p['title'][:40]) + "' loading='lazy' class='feat-img'>" if fig_src else "<div class='feat-img feat-placeholder'></div>"}
      <div class="feat-body">
        <div class="feat-type">{h(p['type'])}</div>
        <h3 class="feat-title">{h(p['title'][:75])}</h3>
        <p class="feat-result">{h(p['s4'][:140])}</p>
        <div class="feat-actions">
          <a href="{h(paper_url)}" class="btn btn-paper">Read Paper</a>
          {"<a href='" + h(app_url) + "' class='btn btn-app'>Try App</a>" if app_url else ""}
        </div>
      </div>
    </article>\n'''

    # All projects grid
    grid_html = ""
    all_sorted = sorted(projects, key=lambda p: (not p["has_app"], not p["has_figs"], p["type"], p["title"]))
    for p in all_sorted:
        paper_url = f"{BASE}/{p['repo']}/e156-submission/"
        app_url = f"{BASE}/{p['repo']}/e156-submission/assets/{p['app_name']}" if p["app_name"] else ""
        badges = ""
        if p["has_app"]:
            badges += '<span class="tag tag-app">App</span>'
        if p["has_figs"]:
            badges += f'<span class="tag tag-fig">{p["fig_count"]} fig{"s" if p["fig_count"]>1 else ""}</span>'

        grid_html += f'''<a href="{h(paper_url)}" class="proj" data-type="{h(p['type'])}" data-title="{h(p['title'].lower())}">
      <div class="proj-head">
        <span class="proj-type">{h(p['type'])}</span>
        {badges}
      </div>
      <h4 class="proj-title">{h(p['title'][:70])}</h4>
      <p class="proj-s4">{h(p['s4'][:100]) if p['s4'] else h(p['s6'][:100])}</p>
      {"<div class='proj-app'>Try interactive app &rarr;</div>" if app_url else ""}
    </a>\n'''

    now = datetime.now().strftime("%d %B %Y")

    dashboard = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mahmood Ahmad — Evidence Synthesis Research</title>
<meta name="description" content="{total} open-access meta-analysis tools, methods, and micro-papers. Interactive apps, datasets, and E156 publications.">
<style>
:root{{--bg:#0a0a0a;--card:#151515;--card2:#1a1a1a;--text:#e8e6e1;--text2:#888;--accent:#d4a843;--blue:#4a9ece;--green:#3dba6c;--purple:#9b6dcc;--border:#2a2a2a;--serif:Georgia,'Times New Roman',serif;--sans:system-ui,-apple-system,'Segoe UI',sans-serif}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--sans);background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased}}
a{{color:var(--blue);text-decoration:none}}

/* ── Hero ──────────────────────────────────────── */
.hero{{min-height:90vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:4rem 2rem;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 30% 20%,rgba(212,168,67,.08),transparent 50%),radial-gradient(ellipse at 70% 80%,rgba(74,158,206,.06),transparent 50%)}}
.hero-badge{{font-size:.65rem;font-weight:700;letter-spacing:.35em;text-transform:uppercase;color:var(--accent);margin-bottom:1.5rem;position:relative}}
.hero h1{{font-family:var(--serif);font-size:clamp(2.5rem,6vw,4.5rem);font-weight:700;line-height:1.05;letter-spacing:-.03em;margin-bottom:1rem;position:relative;max-width:14ch}}
.hero .sub{{font-size:1.1rem;color:var(--text2);margin-bottom:3rem;position:relative}}
.hero .sub a{{color:var(--accent)}}

/* ── Stats ribbon ──────────────────────────────── */
.stats{{display:flex;gap:0;justify-content:center;position:relative;flex-wrap:wrap}}
.stat{{padding:1.5rem 2.5rem;text-align:center;border-right:1px solid var(--border)}}
.stat:last-child{{border-right:none}}
.stat-num{{font-family:var(--serif);font-size:2.8rem;font-weight:700;line-height:1;color:var(--text)}}
.stat-num .accent{{color:var(--accent)}}
.stat-label{{font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;color:var(--text2);margin-top:.3rem}}

/* ── Scroll indicator ──────────────────────────── */
.scroll-hint{{position:absolute;bottom:2rem;left:50%;transform:translateX(-50%);font-size:.7rem;color:var(--text2);letter-spacing:.2em;text-transform:uppercase;animation:pulse 2s ease infinite}}
@keyframes pulse{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}

/* ── Section ───────────────────────────────────── */
.section{{padding:5rem 2rem;max-width:1200px;margin:0 auto}}
.section-label{{font-size:.6rem;font-weight:700;letter-spacing:.3em;text-transform:uppercase;color:var(--accent);margin-bottom:.5rem}}
.section-title{{font-family:var(--serif);font-size:1.8rem;margin-bottom:1rem}}
.section-desc{{color:var(--text2);font-size:.95rem;max-width:60ch;margin-bottom:2.5rem}}

/* ── Featured ──────────────────────────────────── */
.featured{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:1.5rem}}
.feat{{background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden;transition:transform .2s,border-color .2s;animation:rise .6s ease both}}
.feat:hover{{transform:translateY(-4px);border-color:var(--accent)}}
@keyframes rise{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
.feat-img{{width:100%;height:200px;object-fit:cover;display:block;border-bottom:1px solid var(--border)}}
.feat-placeholder{{background:linear-gradient(135deg,var(--card2),var(--border));height:200px}}
.feat-body{{padding:1.2rem 1.5rem 1.5rem}}
.feat-type{{font-size:.6rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);margin-bottom:.5rem}}
.feat-title{{font-family:var(--serif);font-size:1.1rem;line-height:1.3;margin-bottom:.6rem}}
.feat-result{{font-size:.82rem;color:var(--text2);line-height:1.6;margin-bottom:1rem}}
.feat-actions{{display:flex;gap:.5rem}}
.btn{{padding:8px 18px;border-radius:6px;font-size:.75rem;font-weight:600;transition:background .15s}}
.btn-paper{{background:var(--accent);color:#000}}
.btn-paper:hover{{background:#e0b64e}}
.btn-app{{background:var(--blue);color:#fff}}
.btn-app:hover{{background:#5cb3e0}}

/* ── Overview ──────────────────────────────────── */
.overview{{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start}}
.overview-text{{font-family:var(--serif);font-size:1.15rem;line-height:1.8;color:var(--text2)}}
.overview-text em{{color:var(--accent);font-style:normal;font-weight:600}}

/* ── Search + Grid ─────────────────────────────── */
.search-bar{{position:sticky;top:0;z-index:100;background:rgba(10,10,10,.9);backdrop-filter:blur(12px);padding:1rem 0;margin-bottom:1.5rem;display:flex;gap:.8rem;align-items:center;flex-wrap:wrap}}
.search-input{{flex:1;min-width:250px;padding:10px 16px;background:var(--card);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:.85rem}}
.search-input:focus{{outline:none;border-color:var(--accent)}}
.filter-btn{{padding:6px 14px;background:var(--card);border:1px solid var(--border);border-radius:6px;color:var(--text2);font-size:.7rem;font-weight:600;cursor:pointer;transition:all .15s}}
.filter-btn:hover,.filter-btn.active{{background:var(--accent);color:#000;border-color:var(--accent)}}

.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem}}
.proj{{display:block;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.2rem;transition:border-color .15s,transform .15s;text-decoration:none;color:var(--text)}}
.proj:hover{{border-color:var(--accent);transform:translateY(-2px)}}
.proj-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem}}
.proj-type{{font-size:.55rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--text2)}}
.tag{{font-size:.5rem;font-weight:700;padding:2px 6px;border-radius:3px}}
.tag-app{{background:var(--blue);color:#fff}}
.tag-fig{{background:var(--green);color:#fff}}
.proj-title{{font-family:var(--serif);font-size:.92rem;line-height:1.3;margin-bottom:.4rem}}
.proj-s4{{font-size:.75rem;color:var(--text2);line-height:1.5}}
.proj-app{{font-size:.7rem;color:var(--blue);margin-top:.6rem;font-weight:600}}

/* ── Footer ────────────────────────────────────── */
.footer{{text-align:center;padding:3rem 2rem;border-top:1px solid var(--border);font-size:.7rem;color:var(--text2)}}
.footer a{{color:var(--accent)}}

/* ── Responsive ────────────────────────────────── */
@media(max-width:768px){{
  .hero h1{{font-size:2rem}}
  .stats{{gap:0}}
  .stat{{padding:1rem 1.2rem}}
  .stat-num{{font-size:2rem}}
  .overview{{grid-template-columns:1fr}}
  .featured,.grid{{grid-template-columns:1fr}}
  .section{{padding:3rem 1rem}}
}}
@media(prefers-reduced-motion:reduce){{.feat,.scroll-hint{{animation:none}}}}
@media print{{body{{background:#fff;color:#000}}.hero{{min-height:auto;padding:2rem}}.hero::before{{display:none}}}}
</style>
</head>
<body>

<header class="hero">
  <div class="hero-badge">Evidence Synthesis Research Portfolio</div>
  <h1>Reproducible meta-analysis at scale</h1>
  <div class="sub">
    <a href="mailto:mahmood.ahmad2@nhs.net">Mahmood Ahmad</a> &middot; Tahir Heart Institute
  </div>
  <div class="stats">
    <div class="stat"><div class="stat-num">{total}</div><div class="stat-label">Projects</div></div>
    <div class="stat"><div class="stat-num"><span class="accent">{apps}</span></div><div class="stat-label">Interactive Apps</div></div>
    <div class="stat"><div class="stat-num">{figs}</div><div class="stat-label">With Figures</div></div>
    <div class="stat"><div class="stat-num">{exact_156}</div><div class="stat-label">E156 Papers</div></div>
  </div>
  <div class="scroll-hint">Scroll to explore &darr;</div>
</header>

<section class="section">
  <div class="section-label">Featured Work</div>
  <h2 class="section-title">Highlights</h2>
  <p class="section-desc">Each project produces a 156-word micro-paper, an interactive HTML companion, and a versioned evidence capsule. Click any card to read the paper or try the app.</p>
  <div class="featured">
    {featured_html}
  </div>
</section>

<section class="section">
  <div class="section-label">Portfolio Overview</div>
  <h2 class="section-title">The body of work</h2>
  <div class="overview">
    <div class="overview-text">
      This portfolio spans <em>{total} projects</em> in evidence synthesis methodology,
      from pairwise meta-analysis to network comparison, diagnostic test accuracy,
      health technology assessment, and novel methods like multiverse analysis and
      topological data analysis. Every project ships with an <em>E156 micro-paper</em>
      (exactly 156 words, 7 sentences), an interactive HTML companion for reviewers,
      and open-source code. <em>{apps} projects</em> include browser-based interactive apps
      that run with zero installation.
    </div>
    <div style="text-align:center">
      {type_svg}
    </div>
  </div>
</section>

<section class="section" id="projects">
  <div class="section-label">All Projects</div>
  <h2 class="section-title">{total} projects</h2>
  <div class="search-bar">
    <input type="search" class="search-input" id="search" placeholder="Search projects..." aria-label="Search projects">
    <button class="filter-btn active" data-filter="all">All</button>
    <button class="filter-btn" data-filter="app">Apps Only</button>
    <button class="filter-btn" data-filter="figs">With Figures</button>
  </div>
  <div class="grid" id="grid">
    {grid_html}
  </div>
</section>

<footer class="footer">
  <a href="https://github.com/{GH_USER}">GitHub</a> &middot;
  E156 Micro-Paper Format &middot; Updated {now} &middot; All work is open access
</footer>

<script>
const search=document.getElementById("search");
const grid=document.getElementById("grid");
const projs=Array.from(grid.querySelectorAll(".proj"));
const filters=document.querySelectorAll(".filter-btn");
let activeFilter="all";

function applyFilters(){{
  const q=search.value.toLowerCase();
  projs.forEach(p=>{{
    const matchesSearch=p.dataset.title.includes(q)||p.dataset.type.includes(q);
    let matchesFilter=true;
    if(activeFilter==="app") matchesFilter=p.querySelector(".tag-app")!==null;
    if(activeFilter==="figs") matchesFilter=p.querySelector(".tag-fig")!==null;
    p.style.display=(matchesSearch&&matchesFilter)?"":"none";
  }});
}}

search.addEventListener("input",applyFilters);
filters.forEach(btn=>{{
  btn.addEventListener("click",()=>{{
    filters.forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    activeFilter=btn.dataset.filter;
    applyFilters();
  }});
}});
</script>
</body>
</html>'''

    return dashboard


def main():
    projects = load_projects()
    print(f"Loaded {len(projects)} projects")

    html = build_dashboard(projects)
    out_dir = Path(f"C:/{GH_USER}.github.io")
    out_dir.mkdir(exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"Dashboard: {len(html)} bytes -> {out_dir / 'index.html'}")

    # Push
    subprocess.run(["git", "-C", str(out_dir), "add", "-A"], capture_output=True, timeout=10)
    subprocess.run(["git", "-C", str(out_dir), "commit", "-m", "Redesign: world-class editorial dashboard"],
                  capture_output=True, timeout=10)
    r = subprocess.run(["git", "-C", str(out_dir), "push", "origin", "master"],
                      capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        subprocess.run(["git", "-C", str(out_dir), "push", "origin", "main"],
                      capture_output=True, timeout=30)
    print(f"Live at: https://{GH_USER}.github.io/")


if __name__ == "__main__":
    main()
