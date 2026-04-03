"""
Enable GitHub Pages on all repos and create navigation index pages.
1. Enable Pages (main branch, root) on each repo
2. Create root index.html for each project linking to e156-submission/ and app
3. Create central portfolio at mahmood726-cyber.github.io
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from e156_utils import find_all_submissions

GH_USER = os.environ.get("E156_GH_USER", "mahmood726-cyber")


def get_all_repos():
    """Get all repos for the user."""
    result = subprocess.run(
        ["gh", "repo", "list", GH_USER, "-L", "300", "--json", "name,url,description"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        print(f"Error listing repos: {result.stderr}")
        return []
    return json.loads(result.stdout)


def enable_pages(repo_name):
    """Enable GitHub Pages on main branch, root path."""
    result = subprocess.run(
        ["gh", "api", f"repos/{GH_USER}/{repo_name}/pages",
         "-X", "POST",
         "-f", "source[branch]=master",
         "-f", "source[path]=/",
         "-f", "build_type=legacy"],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode == 0:
        return True
    if "already" in result.stderr.lower() or "409" in result.stderr:
        return True  # Already enabled
    # Try 'main' branch
    result2 = subprocess.run(
        ["gh", "api", f"repos/{GH_USER}/{repo_name}/pages",
         "-X", "POST",
         "-f", "source[branch]=main",
         "-f", "source[path]=/",
         "-f", "build_type=legacy"],
        capture_output=True, text=True, timeout=15
    )
    return result2.returncode == 0 or "already" in result2.stderr.lower()


def create_project_index(project_dir):
    """Create a root index.html for a project that links to its E156 content and app."""
    sub = project_dir / "e156-submission"
    if not sub.is_dir():
        return False

    cfg_path = sub / "config.json"
    if not cfg_path.exists():
        return False

    try:
        config = json.loads(cfg_path.read_text(encoding="utf-8"))
    except:
        return False

    title = config.get("title", project_dir.name)
    author = config.get("author", "Mahmood Ahmad")
    summary = config.get("summary", "")
    body = config.get("body", "")
    notes = config.get("notes", {})
    proj_type = config.get("type", "methods")

    # Find assets
    assets_dir = sub / "assets"
    html_apps = []
    figures = []
    if assets_dir.is_dir():
        for f in sorted(assets_dir.iterdir()):
            if f.suffix == ".html" and f.name != "index.html":
                html_apps.append(f.name)
            elif f.suffix in (".png", ".jpg", ".svg"):
                figures.append(f.name)

    # Build links section
    links_html = ""
    links_html += '<a href="e156-submission/index.html" class="card">E156 Micro-Paper (interactive reader)</a>\n'
    if html_apps:
        for app in html_apps[:3]:
            label = app.replace("-", " ").replace("_", " ").replace(".html", "").title()
            links_html += f'    <a href="e156-submission/assets/{app}" class="card app">{label} (interactive app)</a>\n'
    if (sub / "assets" / "dashboard.html").exists():
        links_html += '    <a href="e156-submission/assets/dashboard.html" class="card">Project Dashboard</a>\n'
    links_html += '    <a href="e156-submission/paper.md" class="card">Paper (markdown)</a>\n'
    links_html += '    <a href="e156-submission/protocol.md" class="card">Protocol (markdown)</a>\n'

    esc = lambda s: str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")

    index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Georgia,serif;background:#FDFCFA;color:#1a1a1a;line-height:1.7}}
.page{{max-width:700px;margin:0 auto;padding:3rem 1.5rem}}
.badge{{font-family:system-ui,sans-serif;font-size:.6rem;font-weight:700;letter-spacing:.25em;text-transform:uppercase;color:#7A5A10;margin-bottom:1rem}}
h1{{font-size:1.8rem;margin-bottom:.5rem}}
.meta{{font-family:system-ui,sans-serif;font-size:.85rem;color:#777;margin-bottom:1.5rem;padding-bottom:1rem;border-bottom:2px solid #E5E0D6}}
.summary{{font-size:1.05rem;margin-bottom:2rem;color:#444}}
.links{{display:grid;gap:.8rem;margin-bottom:2rem}}
.card{{display:block;padding:1rem 1.2rem;background:#fff;border:1px solid #E5E0D6;border-radius:8px;text-decoration:none;color:#1a1a1a;font-family:system-ui,sans-serif;font-size:.9rem;transition:border-color .2s,box-shadow .2s}}
.card:hover{{border-color:#7A5A10;box-shadow:0 2px 12px rgba(0,0,0,.06)}}
.card.app{{border-left:4px solid #2E86C1}}
.figs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-bottom:2rem}}
.figs img{{width:100%;border-radius:6px;border:1px solid #E5E0D6}}
.footer{{font-family:system-ui,sans-serif;font-size:.7rem;color:#aaa;padding-top:1rem;border-top:1px solid #E5E0D6}}
.footer a{{color:#2E6B8A}}
</style>
</head>
<body>
<div class="page">
  <div class="badge">E156 Project</div>
  <h1>{esc(title)}</h1>
  <div class="meta">{esc(author)} &middot; {esc(proj_type.title())} &middot; {esc(notes.get("date","2026"))}</div>
  <p class="summary">{esc(summary or body[:200]+"...")}</p>
  <div class="links">
    {links_html}
  </div>
  {"<h2 style='font-family:system-ui,sans-serif;font-size:.7rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#7A5A10;margin-bottom:.8rem'>Figures</h2><div class=figs>" + "".join(f'<img src="e156-submission/assets/{f}" alt="{esc(f)}" loading="lazy">' for f in figures[:6]) + "</div>" if figures else ""}
  <div class="footer">
    <a href="https://github.com/{GH_USER}/{project_dir.name.lower().replace(' ','-').replace('_','-')}">&larr; Source on GitHub</a>
    &middot; <a href="https://{GH_USER}.github.io/">All Projects</a>
  </div>
</div>
</body>
</html>'''

    # Only write if no index.html exists OR it's tiny/auto-generated
    root_index = project_dir / "index.html"
    if root_index.exists() and root_index.stat().st_size > 5000:
        # Don't overwrite a real app
        return False

    root_index.write_text(index_html, encoding="utf-8")
    return True


def create_portfolio_site():
    """Create the central portfolio site at mahmood726-cyber.github.io."""
    submissions = find_all_submissions()

    projects = []
    for sub in submissions:
        cfg = sub / "config.json"
        if not cfg.exists():
            continue
        try:
            c = json.loads(cfg.read_text(encoding="utf-8"))
        except:
            continue

        name = sub.parent.name
        repo_name = name.lower().replace(" ", "-").replace("_", "-")
        title = c.get("title", name)
        proj_type = c.get("type", "methods")
        estimand = c.get("primary_estimand", "")

        # Check for HTML app in assets
        has_app = False
        assets = sub / "assets"
        if assets.is_dir():
            has_app = any(f.suffix == ".html" for f in assets.iterdir())

        projects.append({
            "name": name,
            "repo": repo_name,
            "title": title,
            "type": proj_type,
            "estimand": estimand,
            "has_app": has_app,
        })

    # Sort by type then name
    projects.sort(key=lambda p: (p["type"], p["name"]))

    esc = lambda s: str(s or "").replace("&", "&amp;").replace("<", "&lt;")

    # Build project cards
    cards = ""
    current_type = ""
    for p in projects:
        if p["type"] != current_type:
            current_type = p["type"]
            cards += f'<h2 class="type-label">{esc(current_type.title())}</h2>\n'

        app_badge = '<span class="badge-app">Interactive App</span>' if p["has_app"] else ""
        cards += f'''<a href="https://{GH_USER}.github.io/{p["repo"]}/e156-submission/" class="proj-card">
  <div class="proj-title">{esc(p["title"][:80])}</div>
  <div class="proj-meta">{esc(p["estimand"][:60])} {app_badge}</div>
</a>\n'''

    portfolio_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mahmood Ahmad — Evidence Synthesis Portfolio</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Georgia,serif;background:#FDFCFA;color:#1a1a1a;line-height:1.7}}
.page{{max-width:900px;margin:0 auto;padding:3rem 1.5rem}}
.hero{{text-align:center;padding:2rem 0 2.5rem;border-bottom:3px double #E5E0D6;margin-bottom:2rem}}
.hero-badge{{font-family:system-ui,sans-serif;font-size:.6rem;font-weight:700;letter-spacing:.3em;text-transform:uppercase;color:#7A5A10;margin-bottom:.8rem}}
.hero h1{{font-size:2.2rem;margin-bottom:.5rem}}
.hero .sub{{font-family:system-ui,sans-serif;font-size:.95rem;color:#777}}
.hero .sub a{{color:#2E6B8A;text-decoration:none}}
.stats{{display:flex;gap:1.5rem;justify-content:center;margin-top:1.5rem;flex-wrap:wrap}}
.stat{{text-align:center}}
.stat-num{{font-size:2rem;font-weight:700;color:#7A5A10;font-family:system-ui,sans-serif}}
.stat-label{{font-family:system-ui,sans-serif;font-size:.7rem;color:#888;letter-spacing:.1em;text-transform:uppercase}}
.type-label{{font-family:system-ui,sans-serif;font-size:.65rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#7A5A10;margin:2rem 0 .8rem;padding-bottom:.4rem;border-bottom:1px solid #E5E0D6}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.8rem}}
.proj-card{{display:block;padding:1rem 1.2rem;background:#fff;border:1px solid #E5E0D6;border-radius:8px;text-decoration:none;color:#1a1a1a;transition:border-color .2s,box-shadow .2s}}
.proj-card:hover{{border-color:#7A5A10;box-shadow:0 2px 12px rgba(0,0,0,.06)}}
.proj-title{{font-size:.9rem;font-weight:600;margin-bottom:.3rem;line-height:1.3}}
.proj-meta{{font-family:system-ui,sans-serif;font-size:.75rem;color:#888}}
.badge-app{{display:inline-block;padding:2px 6px;background:#2E86C1;color:#fff;border-radius:3px;font-size:.6rem;font-weight:700;letter-spacing:.04em;margin-left:.3rem}}
.footer{{margin-top:3rem;padding-top:1.5rem;border-top:1px solid #E5E0D6;font-family:system-ui,sans-serif;font-size:.75rem;color:#aaa;text-align:center}}
.footer a{{color:#2E6B8A;text-decoration:none}}
@media(max-width:600px){{.page{{padding:1.5rem 1rem}}.hero h1{{font-size:1.5rem}}}}
</style>
</head>
<body>
<div class="page">
  <header class="hero">
    <div class="hero-badge">Evidence Synthesis Research</div>
    <h1>Mahmood Ahmad</h1>
    <div class="sub">Tahir Heart Institute &middot; <a href="mailto:mahmood.ahmad2@nhs.net">mahmood.ahmad2@nhs.net</a></div>
    <div class="stats">
      <div class="stat"><div class="stat-num">{len(projects)}</div><div class="stat-label">Projects</div></div>
      <div class="stat"><div class="stat-num">{sum(1 for p in projects if p['has_app'])}</div><div class="stat-label">Interactive Apps</div></div>
      <div class="stat"><div class="stat-num">{len(set(p['type'] for p in projects))}</div><div class="stat-label">Categories</div></div>
    </div>
  </header>

  <div class="grid">
    {cards}
  </div>

  <footer class="footer">
    <a href="https://github.com/{GH_USER}">GitHub</a> &middot;
    E156 Micro-Paper Format &middot; All work in progress
  </footer>
</div>
</body>
</html>'''

    return portfolio_html, len(projects)


def main():
    print("=== Enabling GitHub Pages ===\n")

    # Get all repos
    repos = get_all_repos()
    print(f"Found {len(repos)} repos on GitHub\n")

    # Enable Pages on each
    enabled = 0
    failed = []
    for r in repos:
        name = r["name"]
        if enable_pages(name):
            enabled += 1
        else:
            failed.append(name)

    print(f"Pages enabled: {enabled}/{len(repos)}")
    if failed:
        print(f"Failed: {failed[:10]}")

    # Create project index pages
    print("\n=== Creating project index pages ===\n")
    submissions = find_all_submissions()
    created = 0
    for sub in submissions:
        if create_project_index(sub.parent):
            created += 1
            print(f"  Created index: {sub.parent.name}")

    print(f"\nCreated {created} project index pages")

    # Create portfolio site
    print("\n=== Creating portfolio site ===\n")
    portfolio_html, proj_count = create_portfolio_site()

    # Save portfolio to a dedicated repo dir
    portfolio_dir = Path(f"C:/{GH_USER}.github.io")
    portfolio_dir.mkdir(exist_ok=True)
    (portfolio_dir / "index.html").write_text(portfolio_html, encoding="utf-8")
    print(f"Portfolio saved to {portfolio_dir}/index.html ({proj_count} projects)")

    # Create/push the portfolio repo
    if not (portfolio_dir / ".git").is_dir():
        subprocess.run(["git", "-C", str(portfolio_dir), "init"], capture_output=True, timeout=10)
    subprocess.run(["git", "-C", str(portfolio_dir), "add", "index.html"], capture_output=True, timeout=10)
    subprocess.run(["git", "-C", str(portfolio_dir), "commit", "-m", "Update portfolio"], capture_output=True, timeout=10)

    # Create repo if needed
    result = subprocess.run(
        ["gh", "repo", "create", f"{GH_USER}/{GH_USER}.github.io",
         "--public", "--source", str(portfolio_dir), "--push"],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode == 0:
        print(f"Portfolio live at: https://{GH_USER}.github.io/")
    elif "already exists" in result.stderr:
        subprocess.run(
            ["git", "-C", str(portfolio_dir), "remote", "set-url", "origin",
             f"https://github.com/{GH_USER}/{GH_USER}.github.io.git"],
            capture_output=True, timeout=10
        )
        subprocess.run(
            ["git", "-C", str(portfolio_dir), "push", "-u", "origin", "master", "--force"],
            capture_output=True, timeout=60
        )
        print(f"Portfolio updated at: https://{GH_USER}.github.io/")


if __name__ == "__main__":
    main()
