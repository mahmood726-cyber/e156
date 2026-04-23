# sentinel:skip-file  (P1-unpopulated-placeholder: Python f-string {{ }} = literal { } in generated output)
"""
v3: NYT editorial portfolio with Research / Course / About sections.
Quranic storytelling. Tiered projects. Course integration. No clinical noise.
"""

import json, os, subprocess, sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from e156_utils import find_all_submissions

GH_USER = os.environ.get("E156_GH_USER", "mahmood726-cyber")
BASE = f"https://{GH_USER}.github.io"
COURSE_REPO = "fatiha-course-github-v2"
COURSE_BASE = f"{BASE}/{COURSE_REPO}"

COURSE_MODULES = {
    "Start here": [
        ("meta-analysis-topic-selection-course", "1. Choosing Your Topic", "Gap analysis, feasibility, registration, scope"),
        ("synthesis-course", "2. Evidence Synthesis Foundations", "The complete introduction — from question to conclusion"),
        ("meta-analysis-methods-course", "3. Meta-Analysis Methods", "Random effects, heterogeneity, subgroups, prediction intervals"),
        ("risk-of-bias-mastery-course", "4. Risk of Bias Mastery", "RoB 2, ROBINS-I, domain-level judgments"),
        ("grade-certainty-course", "5. GRADE Certainty", "Rating evidence from high to very low — domains, tables, decisions"),
        ("publication-bias-detective", "6. Publication Bias", "Funnel plots, trim-and-fill, selection models, sensitivity"),
        ("meta-analysis-writing-course", "7. Writing the Paper", "From PRISMA to submission — methods, results, discussion"),
    ],
    "Intermediate": [
        ("dta-course-when-the-test-lies-v4", "Diagnostic Test Accuracy", "Bivariate models, HSROC, QUADAS"),
        ("ipd-meta-analysis-course", "IPD Meta-Analysis", "Individual participant data — one-stage, two-stage"),
        ("advanced-meta-analysis-course", "Advanced Methods", "Network MA, dose-response, multiverse, Bayesian"),
        ("living-reviews-course", "Living Reviews", "Cumulative updates, stopping rules, trial sequential analysis"),
        ("umbrella-reviews-course", "Umbrella Reviews", "Reviews of reviews — overlap, credibility, classification"),
        ("observational-evidence-course", "Observational Evidence", "ROBINS-E, target trials, confounding, transportability"),
    ],
    "Advanced": [
        ("prognostic-reviews-course", "Prognostic Reviews", "Prediction models, calibration, PROBAST, validation"),
        ("hta-oman-course", "HTA for Decision-Makers", "Cost-effectiveness, ICER, budget impact"),
        ("qualitative-evidence-synthesis-course", "Qualitative Synthesis", "Meta-ethnography, thematic synthesis, CERQual"),
        ("rapid-reviews-course", "Rapid Reviews", "Abbreviated methods, trade-offs, reporting"),
        ("ai-meta-analysis-course", "AI in Meta-Analysis", "LLMs, extraction, quality checks, disclosure"),
        ("meta-sprint-course", "MetaSprint Automation", "Pipelines and validated tools"),
        ("truthcert-course", "TruthCert & Reproducibility", "Proof-carrying numbers, versioned capsules"),
        ("becoming-methodologist", "Becoming a Methodologist", "Skills, publishing, collaboration, impact"),
    ],
}

LANGUAGES = [
    ("", "English"), ("fr", "French"), ("ar", "Arabic"), ("es", "Spanish"),
    ("de", "German"), ("it", "Italian"), ("pt", "Portuguese"), ("zh", "Chinese"),
    ("ja", "Japanese"), ("ko", "Korean"), ("ru", "Russian"), ("hi", "Hindi"),
]


def h(s):
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def classify(p):
    name = p["name"].lower()
    body = p.get("body", "").lower()
    # Exclude clinical/personal
    if any(x in name for x in ["clinic", "private-website", "portfolio-site", "childnajia", "waternajia", "stories"]):
        return None, None
    # Category
    if any(x in name for x in ["course", "fatiha"]):
        return "Course", "archive"
    if any(x in name for x in ["html", "truthcert", "nma", "dta-pro", "hta", "dose", "pairwise"]):
        cat = "Browser App"
    elif "r package" in body or name in ("cres","gwam","fatiha_project","new_heterogeneity_model",
            "ipd_qma","grma_paper","lfa","501mlm","mlm501","mlmresearch","multilevelerror","rmstnma","metaoverfit"):
        cat = "R Package"
    elif any(x in name for x in ["sprint","extract","dataextract","cochranedataextract"]):
        cat = "Pipeline"
    elif any(x in name for x in ["pairwise70","dta70","repo100","repo300"]):
        cat = "Dataset"
    elif p.get("has_app"):
        cat = "Browser App"
    else:
        cat = "Method"

    flagships = {"FragilityAtlas","BiasForensics","HTA","Truthcert1_work","DTA_Pro_Review",
                 "IPD-Meta-Pro","MetaRep","ComponentNMA","Asa","CardioOracle",
                 "NNTMapper","RMSTmeta","AdaptSim","AlMizan"}
    if p["name"] in flagships:
        tier = "flagship"
    elif p.get("fig_count",0) >= 3 or (p.get("has_app") and p.get("fig_count",0) >= 1):
        tier = "published"
    elif p.get("has_app"):
        tier = "tool"
    else:
        tier = "archive"
    return cat, tier


def load_projects():
    subs = find_all_submissions()
    mapping = json.loads((SCRIPT_DIR/"repo_mapping.json").read_text(encoding="utf-8")) if (SCRIPT_DIR/"repo_mapping.json").exists() else {}
    projects = []
    for sub in subs:
        cfg = sub / "config.json"
        if not cfg.exists(): continue
        try: c = json.loads(cfg.read_text(encoding="utf-8"))
        except: continue
        name = sub.parent.name
        repo = mapping.get(str(sub.parent), name.lower().replace(" ","-").replace("_","-"))
        sents = c.get("sentences",[])
        assets_dir = sub / "assets"
        has_app = False; fig_count = 0; first_fig = ""; app_name = ""
        if assets_dir.is_dir():
            for f in sorted(assets_dir.iterdir()):
                if f.suffix == ".html" and f.name not in ("index.html","dashboard.html"):
                    has_app = True
                    if not app_name: app_name = f.name
                elif f.suffix in (".png",".jpg",".svg"):
                    fig_count += 1
                    if not first_fig: first_fig = f.name
        p = {"name":name,"repo":repo,"title":c.get("title",name),"type":c.get("type","methods"),
             "estimand":c.get("primary_estimand",""),"body":c.get("body",""),
             "s1":sents[0].get("text","") if sents and isinstance(sents[0],dict) else "",
             "s4":sents[3].get("text","") if len(sents)>3 and isinstance(sents[3],dict) else "",
             "s6":sents[5].get("text","") if len(sents)>5 and isinstance(sents[5],dict) else "",
             "has_app":has_app,"fig_count":fig_count,"first_fig":first_fig,"app_name":app_name,
             "code":c.get("notes",{}).get("code","")}
        cat, tier = classify(p)
        if cat is None: continue  # Excluded
        p["cat"] = cat; p["tier"] = tier
        projects.append(p)
    return projects


def build(projects):
    flagships = [p for p in projects if p["tier"]=="flagship"]
    published = [p for p in projects if p["tier"]=="published"]
    tools = [p for p in projects if p["tier"]=="tool"]
    archive = [p for p in projects if p["tier"]=="archive"]
    total = len(projects)
    apps = sum(1 for p in projects if p["has_app"])
    vis = sum(1 for p in projects if p["fig_count"]>0 or p["has_app"])
    cats = {}
    for p in projects:
        if p["cat"] != "Course": cats[p["cat"]] = cats.get(p["cat"],0)+1
    now = datetime.now().strftime("%B %Y")

    def card(p, flagship=False):
        pu = f'{BASE}/{p["repo"]}/e156-submission/'
        au = f'{BASE}/{p["repo"]}/e156-submission/assets/{p["app_name"]}' if p["app_name"] else ""
        gu = f'https://github.com/{GH_USER}/{p["repo"]}'
        r = h(p["s4"][:130]) if p["s4"] else h(p["s6"][:130])
        cc = p["cat"].lower().replace(" ","-")
        if flagship:
            fu = f'{BASE}/{p["repo"]}/e156-submission/assets/{p["first_fig"]}' if p["first_fig"] else ""
            fig = f'<img src="{h(fu)}" alt="{h(p["title"][:40])}" class="card-fig" loading="lazy" onerror="this.style.display=\'none\'">' if fu else ""
            q = h(p["s1"][:100])
            return f'''<article class="card card-flag" data-cat="{h(p["cat"])}">
  {fig}<div class="card-body">
  <div class="card-eyebrow"><span class="cat-dot {cc}"></span>{h(p["cat"])}</div>
  <h3><a href="{h(pu)}">{h(p["title"][:80])}</a></h3>
  <p class="card-q">{q}</p><p class="card-r">{r}</p>
  <div class="card-links"><a href="{h(pu)}">Paper <span class="draft-tag">DRAFT</span></a>{"<a href='"+h(au)+"' class='al' rel='noopener'>App</a>" if au else ""}<a href="{h(gu)}" class="gl" rel="noopener">Code</a></div>
  </div></article>'''
        return f'''<a href="{h(pu)}" class="card card-sm" data-cat="{h(p["cat"])}">
  <div class="card-eyebrow"><span class="cat-dot {cc}"></span>{h(p["cat"])}</div>
  <h4>{h(p["title"][:65])}</h4><p class="card-meta">{h(p["estimand"][:50])}</p></a>'''

    fl_h = "\n".join(card(p,True) for p in flagships[:10])
    pu_h = "\n".join(card(p,True) for p in published[:20])
    to_h = "\n".join(card(p) for p in tools)
    ar_h = "\n".join(card(p) for p in archive if p["cat"]!="Course")

    cn = ""
    for c in ["Browser App","R Package","Method","Pipeline","Dataset"]:
        if c in cats:
            cn += f'<button class="cat-btn" data-cat="{h(c)}" aria-pressed="false"><span class="cat-dot {c.lower().replace(" ","-")}"></span>{h(c)} <span class="cc">{cats[c]}</span></button>\n'

    # Course modules — tiered layout
    cm = ""
    total_modules = sum(len(mods) for mods in COURSE_MODULES.values())
    tier_icons = {"Start here": "&#9654;", "Intermediate": "&#9650;", "Advanced": "&#9733;"}
    for tier_name, mods in COURSE_MODULES.items():
        icon = tier_icons.get(tier_name, "")
        cm += f'<h3 class="course-tier"><span class="tier-arrow">{icon}</span> {h(tier_name)} ({len(mods)} modules)</h3>\n'
        cm += '<div class="course-grid">\n'
        for slug, title, desc in mods:
            url = f"{COURSE_BASE}/{slug}.html"
            cm += f'''<a href="{h(url)}" class="course-card" aria-label="{h(title)} — opens course module">
  <h4>{h(title)}</h4><p>{h(desc)}</p>
  <span class="course-langs">EN FR AR ES DE +7 more</span></a>\n'''
        cm += '</div>\n'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mahmood Ahmad — Evidence Synthesis Research</title>
<meta name="description" content="{total} open-access meta-analysis tools, {total_modules} course modules, and E156 micro-papers.">
<style>
:root{{--bg:#FDFCFA;--tx:#1a1a1a;--t2:#555;--t3:#999;--ac:#7A5A10;--bl:#2E6B8A;--gn:#28a745;
--pu:#7D3C98;--rd:#CB4335;--cd:#fff;--bd:#E8E4DC;--hv:#F5F2EB;
--sf:Georgia,'Times New Roman',serif;--sn:system-ui,-apple-system,'Segoe UI',sans-serif}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{font-family:var(--sn);background:var(--bg);color:var(--tx);line-height:1.6}}
.skip{{position:absolute;top:-50px;left:0;background:var(--cd);padding:8px 16px;font-size:.8rem;z-index:999;border:1px solid var(--bd);border-radius:4px}}.skip:focus{{top:8px;left:8px}}

/* Masthead */
.mast{{max-width:1100px;margin:0 auto;padding:10px 2rem;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--bd);font-size:.8rem;color:var(--t2)}}
.mast-brand{{font-family:var(--sf);font-weight:700;color:var(--tx);font-size:1rem}}
.mast-tag{{font-family:var(--sf);font-style:italic;font-size:.72rem;color:var(--t3);margin-left:.5rem;font-weight:400}}
.mast a{{color:var(--t2);text-decoration:none}}.mast a:hover{{color:var(--ac)}}
.mast-nav{{display:flex;gap:1.5rem;font-weight:600;font-size:.82rem}}
.mast-nav a{{padding:2px 0;border-bottom:2px solid transparent}}.mast-nav a:hover,.mast-nav a.active{{border-color:var(--ac);color:var(--tx)}}

/* Hero */
.hero{{max-width:780px;margin:0 auto;padding:4rem 2rem 3rem;text-align:center}}
.hero-lab{{font-size:.55rem;font-weight:700;letter-spacing:.35em;text-transform:uppercase;color:var(--ac);margin-bottom:1rem}}
.hero h1{{font-family:var(--sf);font-size:clamp(2rem,5vw,3.2rem);line-height:1.1;letter-spacing:-.03em;margin-bottom:1rem}}
.hero .deck{{font-family:var(--sf);font-size:1.05rem;color:var(--t2);line-height:1.8;max-width:55ch;margin:0 auto 2rem}}
.hero .deck em{{color:var(--ac);font-style:normal}}
.stats{{display:flex;gap:2rem;justify-content:center;flex-wrap:wrap}}
.stat{{text-align:center}}.stat-n{{font-family:var(--sf);font-size:2.2rem;font-weight:700}}.stat-l{{font-size:.55rem;letter-spacing:.15em;text-transform:uppercase;color:var(--t3)}}

/* Sections */
.sec{{max-width:1100px;margin:0 auto;padding:3rem 2rem}}
.rule{{border:none;border-top:1px solid var(--bd);margin:0 2rem}}
.sec-hd{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.5rem;flex-wrap:wrap;gap:.5rem}}
.sec-lab{{font-family:var(--sf);font-size:1.3rem;font-weight:700}}
.sec-ct{{font-size:.7rem;color:var(--t3)}}
.sec-intro{{font-family:var(--sf);color:var(--t2);max-width:60ch;font-size:.9rem;line-height:1.7;padding-bottom:1.5rem;margin-bottom:1.5rem;border-bottom:1px solid var(--bd)}}

/* Category nav */
.cnav{{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:1rem}}
.cat-btn{{padding:4px 10px;border:1px solid var(--bd);border-radius:16px;background:var(--cd);font-size:.68rem;cursor:pointer;display:flex;align-items:center;gap:4px;color:var(--t2);transition:all .12s}}
.cat-btn:hover,.cat-btn.active{{border-color:var(--ac);color:var(--tx);background:var(--hv)}}
.cc{{color:var(--t3)}}.cat-dot{{width:7px;height:7px;border-radius:50%;display:inline-block}}
.cat-dot.browser-app{{background:var(--bl)}}.cat-dot.r-package{{background:var(--gn)}}.cat-dot.method{{background:var(--pu)}}
.cat-dot.pipeline{{background:var(--rd)}}.cat-dot.dataset{{background:#E67E22}}

/* Search */
.srch{{width:100%;max-width:380px;padding:7px 12px;border:1px solid var(--bd);border-radius:5px;font-size:.82rem;background:var(--cd);margin-bottom:1.2rem}}.srch:focus{{outline:2px solid var(--ac);border-color:transparent}}

/* Cards */
.gf{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1rem}}
.gs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.7rem}}
.card{{border:1px solid var(--bd);border-radius:8px;padding:1.1rem 1.3rem;background:var(--cd);transition:border-color .12s,box-shadow .12s}}
.card:hover{{border-color:var(--ac);box-shadow:0 2px 10px rgba(0,0,0,.03)}}
.card-flag{{border-top:3px solid var(--ac);overflow:hidden;padding:0}}
.card-flag .card-body{{padding:1.1rem 1.3rem}}
.card-fig{{width:100%;height:150px;object-fit:cover;display:block;border-bottom:1px solid var(--bd)}}
.card-sm{{display:block;text-decoration:none;color:var(--tx);padding:.8rem 1rem}}
.card-eyebrow{{font-size:.55rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--t3);margin-bottom:.4rem;display:flex;align-items:center;gap:4px}}
.card h3{{font-family:var(--sf);font-size:1rem;line-height:1.3;margin-bottom:.3rem}}
.card h3 a{{color:var(--tx);text-decoration:none}}.card h3 a:hover{{color:var(--ac)}}
.card h4{{font-family:var(--sf);font-size:.85rem;line-height:1.3;margin-bottom:.2rem}}
.card-q{{font-family:var(--sf);font-size:.75rem;color:var(--t3);font-style:italic;line-height:1.5;margin-bottom:.3rem}}
.card-r{{font-size:.78rem;color:var(--t2);line-height:1.6;margin-bottom:.6rem}}
.card-meta{{font-size:.7rem;color:var(--t3)}}
.card-links{{display:flex;gap:.7rem;font-size:.72rem;font-weight:600}}
.card-links a{{color:var(--bl);text-decoration:none}}.card-links a:hover{{text-decoration:underline}}
.card-links .al{{color:var(--gn)}}.card-links .gl{{color:var(--t3)}}

/* Course */
.course-banner{{max-width:1100px;margin:0 auto;padding:2.5rem 2rem;background:linear-gradient(135deg,#f7f5f0,#ede9e0);border-top:3px solid var(--ac);border-bottom:1px solid var(--bd)}}
.course-banner h2{{font-family:var(--sf);font-size:1.4rem;margin-bottom:.3rem}}
.course-banner .cb-sub{{font-size:.9rem;color:var(--t2);margin-bottom:1.5rem;font-family:var(--sf)}}
.course-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:.8rem}}
.course-card{{display:block;padding:.9rem 1.1rem;background:var(--cd);border:1px solid var(--bd);border-radius:8px;text-decoration:none;color:var(--tx);transition:border-color .12s}}
.course-card:hover{{border-color:var(--ac)}}
.course-card h4{{font-family:var(--sf);font-size:.88rem;margin-bottom:.2rem}}
.course-card p{{font-size:.75rem;color:var(--t2);line-height:1.5;margin-bottom:.3rem}}
.course-langs{{font-size:.6rem;color:var(--t3);font-weight:600;letter-spacing:.05em}}
h3.course-tier{{font-size:.6rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--ac);margin:1.2rem 0 .6rem;padding-bottom:.3rem;border-bottom:1px solid var(--bd)}}
h3.course-tier:first-child{{margin-top:0}}
h3.course-tier .tier-arrow{{color:var(--gn);margin-right:.3rem}}

/* Draft label */
.draft-tag{{display:inline-block;padding:1px 6px;background:#fff3cd;color:#856404;border-radius:3px;font-size:.55rem;font-weight:700;letter-spacing:.06em;margin-left:.4rem;vertical-align:middle}}
.verified-tag{{display:inline-block;padding:1px 6px;background:#d4edda;color:#155724;border-radius:3px;font-size:.55rem;font-weight:700;letter-spacing:.06em;margin-left:.4rem;vertical-align:middle}}
.card-flag.verified{{border-top-color:var(--gn)}}

/* Timeline note */
.timeline{{font-family:var(--sf);font-size:.78rem;color:var(--t3);font-style:italic;text-align:center;padding:.8rem 2rem;max-width:700px;margin:0 auto}}

/* About */
.about{{max-width:680px;margin:0 auto;padding:3rem 2rem}}
.about h2{{font-family:var(--sf);font-size:1.2rem;margin-bottom:.8rem}}
.about p{{font-size:.88rem;color:var(--t2);line-height:1.8;margin-bottom:.8rem}}

/* Footer */
.ft{{max-width:1100px;margin:0 auto;padding:1.5rem 2rem;border-top:1px solid var(--bd);font-size:.68rem;color:var(--t3);display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem}}
.ft a{{color:var(--ac);text-decoration:none}}
.ft-close{{font-family:var(--sf);font-style:italic;color:var(--t2)}}

@media(max-width:768px){{.hero h1{{font-size:1.8rem}}.gf,.gs,.course-grid{{grid-template-columns:1fr}}.sec{{padding:2rem 1rem}}.mast{{flex-direction:column;gap:.5rem;text-align:center}}.mast-nav{{justify-content:center}}}}
@media print{{.cnav,.srch,.card-links .gl,.skip,.mast-nav{{display:none}}body{{background:#fff}}}}
</style>
</head>
<body>
<a href="#all" class="skip">Skip to all projects</a>

<nav class="mast" role="navigation" aria-label="Main">
  <div><span class="mast-brand">Mahmood Ahmad</span><span class="mast-tag">by the grace given, we seek to understand</span></div>
  <div class="mast-nav">
    <a href="#research" class="active">Research</a>
    <a href="#course">Course</a>
    <a href="#about">About</a>
    <a href="https://github.com/{GH_USER}" rel="noopener">GitHub</a>
  </div>
</nav>

<section role="region" aria-labelledby="research-heading" id="research">
<header class="hero">
  <div class="hero-lab" id="research-heading">Open-Access Evidence Synthesis</div>
  <h1>What if every conclusion in medicine could be verified in ninety seconds?</h1>
  <p class="deck">Most meta-analyses produce thousands of pages that few read and fewer challenge. We asked: <em>what is the minimum truthful unit?</em> The answer is 156 words. {total} projects. Each with a micro-paper, an app you can try now, and code you can verify. Not because transparency is fashionable — but because <em>the evidence demands it.</em></p>
  <div class="stats">
    <div class="stat"><div class="stat-n" aria-label="{total} projects">{total}</div><div class="stat-l">Projects</div></div>
    <div class="stat"><div class="stat-n" aria-label="{apps} interactive apps">{apps}</div><div class="stat-l">Interactive Apps</div></div>
    <div class="stat"><div class="stat-n" aria-label="{total_modules} course modules">{total_modules}</div><div class="stat-l">Course Modules</div></div>
  </div>
</header>

<hr class="rule">
<section class="sec">
  <div class="sec-hd"><div class="sec-lab">The evidence speaks first</div><div class="sec-ct">{len(flagships)} flagship projects</div></div>
  <p class="sec-intro">Before the method. Before the software. Before the publication — there is a finding. These projects led with a number, then built everything around proving it right.</p>
  <div class="gf">{fl_h}</div>
</section>

<hr class="rule">
<section class="sec">
  <div class="sec-hd"><div class="sec-lab">Then came the tools</div><div class="sec-ct">{len(published)} validated</div></div>
  <p class="sec-intro">A finding without a tool is a claim. A tool without validation is a promise. These are both — tested against R, validated on real data, open for anyone to challenge.</p>
  <div class="gf">{pu_h}</div>
</section>

</section><!-- /research region -->

<hr class="rule">
<p class="timeline">These projects span 2023–2026. Individual project timelines, commit histories, and validation dates are recorded in each GitHub repository.</p>

<hr class="rule">
<section class="course-banner" id="course" role="region" aria-labelledby="course-heading">
  <h2 id="course-heading">Learn evidence synthesis</h2>
  <p class="cb-sub">{total_modules} modules in {len(LANGUAGES)} languages — structured from first principles to advanced methods. Free. Open access. Interactive.</p>
  <div class="course-grid">{cm}</div>
</section>

<hr class="rule">
<section class="about" id="about" role="region" aria-labelledby="about-heading">
  <h2 id="about-heading">Why 156 words?</h2>
  <p>Because a paragraph is the smallest unit that can carry a complete argument. Seven sentences. One question, one dataset, one method, one result, one robustness check, one interpretation, one limitation. Nothing hidden. Nothing inflated.</p>
  <p>I am a cardiologist. I read meta-analyses that change how we treat patients. Most are buried in papers so long that the finding — the actual number that matters — is lost on page twelve. I wanted something different: a format where every word is load-bearing, the limitation is mandatory, and a reader can evaluate the claim in ninety seconds.</p>
  <p>{total} projects. Each distilled to its essential truth. The apps work. The code is open. The numbers are verifiable. Whatever understanding is reached here is not ours alone — it is given. This work exists because the capacity to reason, to measure, and to question was granted before any of us chose to use it.</p>
</section>

<hr class="rule">
<section class="sec" id="all">
  <div class="sec-hd"><div class="sec-lab">And the work continues</div><div class="sec-ct">{len(tools)+len(archive)} more</div></div>
  <div class="cnav">
    <button class="cat-btn active" data-cat="all" aria-pressed="true">All <span class="cc">{len(tools)+len(archive)}</span></button>
    {cn}
  </div>
  <input type="search" class="srch" id="srch" placeholder="Search {total} tools, datasets, and methods..." aria-label="Search projects">
  <div class="gs" id="grid">{to_h}{ar_h}</div>
</section>

<footer class="ft">
  <div>&copy; {datetime.now().year} Mahmood Ahmad &middot; Tahir Heart Institute &middot; <a href="mailto:mahmood.ahmad2@nhs.net">Contact</a></div>
  <div class="ft-close">By the grace given, we seek to understand. &middot; {now}</div>
</footer>

<script>
const g=document.getElementById("grid"),cs=Array.from(g.querySelectorAll(".card-sm")),s=document.getElementById("srch"),bs=document.querySelectorAll(".cat-btn");
let ac="all";
function f(){{const q=s.value.toLowerCase();cs.forEach(c=>{{c.style.display=(ac==="all"||c.dataset.cat===ac)&&(!q||c.textContent.toLowerCase().includes(q))?"":"none"}})}}
s.addEventListener("input",f);
bs.forEach(b=>{{b.addEventListener("click",()=>{{bs.forEach(x=>{{x.classList.remove("active");x.setAttribute("aria-pressed","false")}});b.classList.add("active");b.setAttribute("aria-pressed","true");ac=b.dataset.cat;f()}});}});
</script>
</body>
</html>'''


def main():
    projects = load_projects()
    print(f"Loaded {len(projects)} projects (excl. clinical/personal)")
    html = build(projects)
    out = Path(f"C:/{GH_USER}.github.io")
    (out/"index.html").write_text(html, encoding="utf-8")
    print(f"Dashboard: {len(html):,} bytes")
    subprocess.run(["git","-C",str(out),"add","-A"], capture_output=True, timeout=10)
    subprocess.run(["git","-C",str(out),"commit","-m","v3: Research+Course+About, Quranic storytelling, NYT editorial"],
                  capture_output=True, timeout=10)
    subprocess.run(["git","-C",str(out),"push","origin","master"], capture_output=True, timeout=30)
    print(f"Live at: {BASE}/")

if __name__ == "__main__":
    main()
