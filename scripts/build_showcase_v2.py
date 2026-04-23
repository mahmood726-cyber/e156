# sentinel:skip-file  (P1-unpopulated-placeholder: Python f-string {{ }} = literal { } in generated output)
"""
World-class NYT-style evidence synthesis portfolio.
Tiered: Flagship (6) > Published (30) > Tools (50+) > Archive.
Category navigation. Light mode. Editorial typography.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from e156_utils import find_all_submissions

GH_USER = os.environ.get("E156_GH_USER", "mahmood726-cyber")
BASE = f"https://{GH_USER}.github.io"


def h(s):
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def classify_project(p):
    """Assign a human-readable category and tier."""
    name = p["name"].lower()
    title = p["title"].lower()
    body = p.get("body", "").lower()
    t = p.get("type", "methods").lower()

    # Category (what it IS)
    if any(x in name for x in ["html", "truthcert", "nma", "dta-pro", "hta", "dose", "pairwise"]):
        cat = "Browser App"
    elif "r package" in body or name in ("cres", "gwam", "fatiha_project", "new_heterogeneity_model",
                                          "ipd_qma", "grma_paper", "lfa", "501mlm", "mlm501",
                                          "mlmresearch", "multilevelerror", "rmstnma", "metaoverfit"):
        cat = "R Package"
    elif any(x in name for x in ["sprint", "extract", "dataextract", "cochranedataextract"]):
        cat = "Pipeline"
    elif any(x in name for x in ["course", "fatiha-course"]):
        cat = "Course"
    elif any(x in name for x in ["pairwise70", "dta70", "repo100", "repo300"]):
        cat = "Dataset"
    elif any(x in name for x in ["clinic", "private-website", "portfolio"]):
        cat = "Clinical"
    elif p["has_app"]:
        cat = "Browser App"
    else:
        cat = "Method"

    # Tier based on richness
    fig_count = p.get("fig_count", 0)
    has_app = p.get("has_app", False)

    # Flagship: has figures AND app AND substantial content
    flagship_names = {
        "FragilityAtlas", "BiasForensics", "HTA", "Truthcert1_work", "DTA_Pro_Review",
        "IPD-Meta-Pro", "MetaRep", "ComponentNMA", "Asa", "CardioOracle",
        "NNTMapper", "RMSTmeta", "AdaptSim", "AlMizan"
    }
    if p["name"] in flagship_names:
        tier = "flagship"
    elif fig_count >= 3 or (has_app and fig_count >= 1):
        tier = "published"
    elif has_app:
        tier = "tool"
    else:
        tier = "archive"

    return cat, tier


def load_projects():
    subs = find_all_submissions()
    mapping_path = SCRIPT_DIR / "repo_mapping.json"
    repo_map = json.loads(mapping_path.read_text(encoding="utf-8")) if mapping_path.exists() else {}

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
        repo = repo_map.get(str(sub.parent), name.lower().replace(" ", "-").replace("_", "-"))
        body = c.get("body", "")
        sents = c.get("sentences", [])
        s1 = sents[0].get("text", "") if sents and isinstance(sents[0], dict) else ""
        s4 = sents[3].get("text", "") if len(sents) > 3 and isinstance(sents[3], dict) else ""
        s6 = sents[5].get("text", "") if len(sents) > 5 and isinstance(sents[5], dict) else ""
        notes = c.get("notes", {})

        assets_dir = sub / "assets"
        has_app = False
        fig_count = 0
        first_fig = ""
        app_name = ""
        if assets_dir.is_dir():
            for f in sorted(assets_dir.iterdir()):
                if f.suffix == ".html" and f.name not in ("index.html", "dashboard.html"):
                    has_app = True
                    if not app_name:
                        app_name = f.name
                elif f.suffix in (".png", ".jpg", ".svg"):
                    fig_count += 1
                    if not first_fig:
                        first_fig = f.name

        p = {
            "name": name, "repo": repo, "title": c.get("title", name),
            "type": c.get("type", "methods"),
            "estimand": c.get("primary_estimand", ""),
            "body": body, "s1": s1, "s4": s4, "s6": s6,
            "has_app": has_app, "fig_count": fig_count,
            "first_fig": first_fig, "app_name": app_name,
            "code": notes.get("code", ""),
        }
        p["cat"], p["tier"] = classify_project(p)
        projects.append(p)

    return projects


def build_site(projects):
    flagships = [p for p in projects if p["tier"] == "flagship"]
    published = [p for p in projects if p["tier"] == "published"]
    tools = [p for p in projects if p["tier"] == "tool"]
    archive = [p for p in projects if p["tier"] == "archive"]

    total = len(projects)
    apps = sum(1 for p in projects if p["has_app"])
    figs = sum(1 for p in projects if p["fig_count"] > 0 or p["has_app"])

    # Category counts for nav
    cats = {}
    for p in projects:
        cats[p["cat"]] = cats.get(p["cat"], 0) + 1
    cat_order = ["Browser App", "R Package", "Method", "Pipeline", "Dataset", "Course", "Clinical"]

    now = datetime.now().strftime("%B %Y")

    def card(p, size="normal"):
        paper_url = f'{BASE}/{p["repo"]}/e156-submission/'
        app_url = f'{BASE}/{p["repo"]}/e156-submission/assets/{p["app_name"]}' if p["app_name"] else ""
        gh_url = f'https://github.com/{GH_USER}/{p["repo"]}'
        result = h(p["s4"][:130]) if p["s4"] else h(p["s6"][:130])
        cat_class = p["cat"].lower().replace(" ", "-")

        if size == "flagship":
            fig_url = f'{BASE}/{p["repo"]}/e156-submission/assets/{p["first_fig"]}' if p["first_fig"] else ""
            fig_html = f'<img src="{h(fig_url)}" alt="{h(p["title"][:40])}" class="card-fig" loading="lazy" onerror="this.style.display=\'none\'">' if fig_url else ""
            question = h(p["s1"][:100]) if p["s1"] else ""
            return f'''<article class="card card-flag" data-cat="{h(p['cat'])}">
      {fig_html}
      <div class="card-body">
        <div class="card-eyebrow"><span class="cat-dot {cat_class}"></span>{h(p['cat'])}</div>
        <h3><a href="{h(paper_url)}">{h(p['title'][:80])}</a></h3>
        <p class="card-question">{question}</p>
        <p class="card-result">{result}</p>
        <div class="card-links">
          <a href="{h(paper_url)}">Paper</a>
          {"<a href='" + h(app_url) + "' class='app-link' rel='noopener'>App</a>" if app_url else ""}
          <a href="{h(gh_url)}" class="gh" rel="noopener">Code</a>
        </div>
      </div>
    </article>'''
        else:
            return f'''<a href="{h(paper_url)}" class="card card-sm" data-cat="{h(p['cat'])}">
      <div class="card-eyebrow"><span class="cat-dot {cat_class}"></span>{h(p['cat'])}</div>
      <h4>{h(p['title'][:65])}</h4>
      <p class="card-meta">{h(p['estimand'][:50])}</p>
    </a>'''

    flagship_html = "\n".join(card(p, "flagship") for p in flagships[:8])
    published_html = "\n".join(card(p, "flagship") for p in published[:20])
    tools_html = "\n".join(card(p) for p in tools)
    archive_html = "\n".join(card(p) for p in archive)

    cat_nav = ""
    for c in cat_order:
        if c in cats:
            cls = c.lower().replace(" ", "-")
            cat_nav += f'<button class="cat-btn" data-cat="{h(c)}"><span class="cat-dot {cls}"></span>{h(c)} <span class="cat-count">{cats[c]}</span></button>\n'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mahmood Ahmad — Evidence Synthesis Research</title>
<meta name="description" content="{total} open-access meta-analysis tools and E156 micro-papers by Mahmood Ahmad, Tahir Heart Institute.">
<style>
:root{{
  --bg:#FDFCFA;--text:#1a1a1a;--text2:#666;--text3:#999;
  --accent:#7A5A10;--blue:#2E6B8A;--green:#28a745;--purple:#7D3C98;--red:#CB4335;
  --card:#fff;--border:#E8E4DC;--hover:#F5F2EB;
  --serif:Georgia,'Times New Roman',serif;
  --sans:system-ui,-apple-system,'Segoe UI',sans-serif
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--sans);background:var(--bg);color:var(--text);line-height:1.6}}

/* ── Skip link ─────────────────────────────── */
.skip-link{{position:absolute;top:-50px;left:0;background:var(--card);padding:8px 16px;font-size:.8rem;z-index:999;border:1px solid var(--border);border-radius:4px}}
.skip-link:focus{{top:8px;left:8px}}

/* ── Masthead ──────────────────────────────── */
.masthead{{max-width:1100px;margin:0 auto;padding:12px 2rem;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border);font-size:.8rem;color:var(--text2)}}
.masthead-brand{{font-family:var(--serif);font-weight:700;color:var(--text);font-size:1rem;letter-spacing:-.02em}}
.masthead a{{color:var(--text2);text-decoration:none}}
.masthead a:hover{{color:var(--accent)}}

/* ── Hero ──────────────────────────────────── */
.hero{{max-width:780px;margin:0 auto;padding:5rem 2rem 3rem;text-align:center}}
.hero-label{{font-size:.6rem;font-weight:700;letter-spacing:.3em;text-transform:uppercase;color:var(--accent);margin-bottom:1rem}}
.hero h1{{font-family:var(--serif);font-size:clamp(2.2rem,5vw,3.5rem);line-height:1.1;letter-spacing:-.03em;margin-bottom:1rem}}
.hero .deck{{font-family:var(--serif);font-size:1.15rem;color:var(--text2);line-height:1.7;max-width:55ch;margin:0 auto 2rem}}
.hero .deck em{{color:var(--accent);font-style:normal}}
.stats-row{{display:flex;gap:2rem;justify-content:center;flex-wrap:wrap}}
.stat{{text-align:center}}
.stat-num{{font-family:var(--serif);font-size:2.5rem;font-weight:700;line-height:1}}
.stat-label{{font-size:.6rem;letter-spacing:.15em;text-transform:uppercase;color:var(--text3);margin-top:2px}}

/* ── Section ───────────────────────────────── */
.section{{max-width:1100px;margin:0 auto;padding:3rem 2rem}}
.section-rule{{border:none;border-top:1px solid var(--border);margin:0 2rem}}
.section-head{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:1.5rem;flex-wrap:wrap;gap:.5rem}}
.section-label{{font-family:var(--serif);font-size:1.4rem;font-weight:700}}
.section-count{{font-size:.75rem;color:var(--text3)}}
.section-intro{{font-family:var(--serif);color:var(--text2);max-width:60ch;margin-bottom:2rem;font-size:.95rem;line-height:1.7;padding:1rem 0;border-bottom:1px solid var(--border)}}

/* ── Category nav ──────────────────────────── */
.cat-nav{{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1.5rem;align-items:center}}
.cat-btn{{padding:5px 12px;border:1px solid var(--border);border-radius:20px;background:var(--card);font-size:.72rem;cursor:pointer;display:flex;align-items:center;gap:5px;transition:all .15s;color:var(--text2)}}
.cat-btn:hover,.cat-btn.active{{border-color:var(--accent);color:var(--text);background:var(--hover)}}
.cat-count{{color:var(--text3)}}
.cat-dot{{width:8px;height:8px;border-radius:50%;display:inline-block}}
.cat-dot.browser-app{{background:var(--blue)}}
.cat-dot.r-package{{background:var(--green)}}
.cat-dot.method{{background:var(--purple)}}
.cat-dot.pipeline{{background:var(--red)}}
.cat-dot.dataset{{background:#E67E22}}
.cat-dot.course{{background:#148F77}}
.cat-dot.clinical{{background:#85929E}}

/* ── Search ────────────────────────────────── */
.search-wrap{{margin-bottom:1.5rem}}
.search{{width:100%;max-width:400px;padding:8px 14px;border:1px solid var(--border);border-radius:6px;font-size:.85rem;background:var(--card)}}
.search:focus{{outline:2px solid var(--accent);border-color:transparent}}

/* ── Cards ─────────────────────────────────── */
.grid-flag{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.2rem}}
.grid-sm{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:.8rem}}

.card{{border:1px solid var(--border);border-radius:8px;padding:1.2rem 1.4rem;background:var(--card);transition:border-color .15s,box-shadow .15s}}
.card:hover{{border-color:var(--accent);box-shadow:0 2px 12px rgba(0,0,0,.04)}}
.card-flag{{border-top:3px solid var(--accent);overflow:hidden}}
.card-fig{{width:100%;height:160px;object-fit:cover;display:block;border-bottom:1px solid var(--border);margin:-1.2rem -1.4rem 1rem;width:calc(100% + 2.8rem)}}
.card-body{{}}
.card-question{{font-family:var(--serif);font-size:.8rem;color:var(--text3);font-style:italic;margin-bottom:.4rem;line-height:1.5}}
.card-sm{{display:block;text-decoration:none;color:var(--text);padding:1rem 1.2rem}}
.card-eyebrow{{font-size:.6rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--text3);margin-bottom:.5rem;display:flex;align-items:center;gap:5px}}
.card h3{{font-family:var(--serif);font-size:1.05rem;line-height:1.3;margin-bottom:.4rem}}
.card h3 a{{color:var(--text);text-decoration:none}}
.card h3 a:hover{{color:var(--accent)}}
.card h4{{font-family:var(--serif);font-size:.88rem;line-height:1.3;margin-bottom:.3rem}}
.card-result{{font-size:.82rem;color:var(--text2);line-height:1.6;margin-bottom:.8rem}}
.card-meta{{font-size:.75rem;color:var(--text3)}}
.card-links{{display:flex;gap:.8rem;font-size:.75rem;font-weight:600}}
.card-links a{{color:var(--blue);text-decoration:none}}
.card-links a:hover{{text-decoration:underline}}
.card-links .app-link{{color:var(--green)}}
.card-links .gh{{color:var(--text3)}}

/* ── About ─────────────────────────────────── */
.about{{max-width:680px;margin:0 auto;padding:3rem 2rem}}
.about h2{{font-family:var(--serif);font-size:1.3rem;margin-bottom:1rem}}
.about p{{font-size:.9rem;color:var(--text2);line-height:1.8;margin-bottom:1rem}}
.about a{{color:var(--blue)}}

/* ── Footer ────────────────────────────────── */
.footer{{max-width:1100px;margin:0 auto;padding:2rem;border-top:1px solid var(--border);font-size:.7rem;color:var(--text3);display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem}}
.footer a{{color:var(--accent);text-decoration:none}}
.footer-closing{{font-family:var(--serif);font-style:italic;color:var(--text2)}}

/* ── Toggle ────────────────────────────────── */
.toggle-btn{{padding:6px 12px;border:1px solid var(--border);border-radius:4px;background:var(--card);font-size:.72rem;cursor:pointer;color:var(--text2)}}
.toggle-btn:hover{{background:var(--hover)}}

/* ── Responsive ────────────────────────────── */
@media(max-width:768px){{
  .hero h1{{font-size:2rem}}
  .stats-row{{gap:1rem}}
  .stat-num{{font-size:1.8rem}}
  .grid-flag,.grid-sm{{grid-template-columns:1fr}}
  .section{{padding:2rem 1rem}}
  .masthead{{flex-direction:column;gap:.3rem;text-align:center}}
}}
@media print{{
  .cat-nav,.search-wrap,.toggle-btn,.card-links .gh{{display:none}}
  body{{background:#fff}}
}}
</style>
</head>
<body>

<a href="#all" class="skip-link">Skip to all projects</a>
<nav class="masthead" role="navigation" aria-label="Main navigation">
  <div class="masthead-brand">Mahmood Ahmad</div>
  <div>Tahir Heart Institute &middot; <a href="mailto:mahmood.ahmad2@nhs.net">Contact</a> &middot; <a href="https://github.com/{GH_USER}" rel="noopener">GitHub</a></div>
</nav>

<header class="hero">
  <div class="hero-label">Open-Access Evidence Synthesis</div>
  <h1>What if every conclusion in medicine could be verified in ninety seconds?</h1>
  <p class="deck">Most meta-analyses produce thousands of pages that few read and fewer challenge. We asked a different question: <em>what is the minimum truthful unit?</em> The answer is 156 words — seven sentences, one paragraph, no place to hide. {total} projects. Each with a micro-paper, an interactive app you can try right now, and code you can verify yourself. Not because transparency is fashionable, but because <em>the evidence demands it.</em></p>
  <div class="stats-row">
    <div class="stat"><div class="stat-num">{total}</div><div class="stat-label">Projects</div></div>
    <div class="stat"><div class="stat-num">{apps}</div><div class="stat-label">Interactive Apps</div></div>
    <div class="stat"><div class="stat-num">{figs}</div><div class="stat-label">Visualizations</div></div>
  </div>
</header>

<hr class="section-rule">

<section class="section">
  <div class="section-head">
    <div class="section-label">The evidence speaks first</div>
    <div class="section-count">{len(flagships)} flagship projects</div>
  </div>
  <p class="section-intro">Before the method. Before the software. Before the publication — there is a finding. These projects led with a number, then built everything around proving it right.</p>
  <div class="grid-flag">{flagship_html}</div>
</section>

<hr class="section-rule">

<section class="section">
  <div class="section-head">
    <div class="section-label">Then came the tools</div>
    <div class="section-count">{len(published)} validated instruments</div>
  </div>
  <p class="section-intro">A finding without a tool is a claim. A tool without validation is a promise. These projects are both — tested against R, validated on real data, open for anyone to challenge.</p>
  <div class="grid-flag">{published_html}</div>
</section>

<hr class="section-rule">

<section class="about">
  <h2>Why 156 words?</h2>
  <p>Because a paragraph is the smallest unit that can carry a complete argument. Seven sentences. One question, one dataset, one method, one result, one robustness check, one interpretation, one limitation. Nothing hidden. Nothing inflated.</p>
  <p>I am a cardiologist. I read meta-analyses that change how we treat patients. Most of them are buried in papers so long that the finding — the actual number that matters — is lost somewhere on page twelve. I wanted something different: a format where every word is load-bearing, where the limitation is mandatory, and where a reader can evaluate the entire claim in ninety seconds.</p>
  <p>That is what you are looking at. {total} projects. Each one distilled to its essential truth. The apps work. The code is open. The numbers are verifiable. This is not a finished body of work — it is a body of work that refuses to wait for permission to be visible.</p>
</section>

<hr class="section-rule">

<section class="section" id="all">
  <div class="section-head">
    <div class="section-label">And the work continues</div>
    <div class="section-count">{len(tools) + len(archive)} projects in progress</div>
  </div>

  <div class="cat-nav" id="catNav">
    <button class="cat-btn active" data-cat="all" aria-pressed="true">All <span class="cat-count">{len(tools)+len(archive)}</span></button>
    {cat_nav}
  </div>

  <div class="search-wrap">
    <input type="search" class="search" id="search" placeholder="Search {total} tools, datasets, and methods..." aria-label="Search projects">
  </div>

  <div class="grid-sm" id="grid">
    {tools_html}
    {archive_html}
  </div>
</section>

<footer class="footer">
  <div>&copy; {datetime.now().year} Mahmood Ahmad &middot; Tahir Heart Institute &middot; <a href="https://github.com/{GH_USER}">GitHub</a></div>
  <div class="footer-closing">Every conclusion in medicine can be verified in ninety seconds. &middot; {now}</div>
</footer>

<script>
const grid=document.getElementById("grid");
const cards=Array.from(grid.querySelectorAll(".card-sm"));
const search=document.getElementById("search");
const catBtns=document.querySelectorAll(".cat-btn");
let activeCat="all";

function filter(){{
  const q=search.value.toLowerCase();
  cards.forEach(c=>{{
    const matchCat=activeCat==="all"||c.dataset.cat===activeCat;
    const matchQ=!q||c.textContent.toLowerCase().includes(q);
    c.style.display=(matchCat&&matchQ)?"":"none";
  }});
}}

search.addEventListener("input",filter);
catBtns.forEach(btn=>{{
  btn.addEventListener("click",()=>{{
    catBtns.forEach(b=>{{b.classList.remove("active");b.setAttribute("aria-pressed","false")}});
    btn.classList.add("active");btn.setAttribute("aria-pressed","true");
    activeCat=btn.dataset.cat;
    filter();
  }});
}});
</script>
</body>
</html>'''

    return html


def main():
    projects = load_projects()
    print(f"Loaded {len(projects)} projects")

    cats = {}
    tiers = {}
    for p in projects:
        cats[p["cat"]] = cats.get(p["cat"], 0) + 1
        tiers[p["tier"]] = tiers.get(p["tier"], 0) + 1
    print(f"Categories: {cats}")
    print(f"Tiers: {tiers}")

    html = build_site(projects)
    out = Path(f"C:/{GH_USER}.github.io")
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
    print(f"Dashboard: {len(html):,} bytes")

    subprocess.run(["git", "-C", str(out), "add", "-A"], capture_output=True, timeout=10)
    subprocess.run(["git", "-C", str(out), "commit", "-m", "v2: NYT editorial redesign with tiers + categories"],
                  capture_output=True, timeout=10)
    subprocess.run(["git", "-C", str(out), "push", "origin", "master"], capture_output=True, timeout=30)
    print(f"Live at: {BASE}/")


if __name__ == "__main__":
    main()
