"""
Create push.sh helper scripts in each project directory for easy updates.
Also creates a live status dashboard at mahmood726-cyber.github.io.
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


def local_windows_path(path_str):
    if os.name == "nt":
        return Path(path_str)
    drive = path_str[0].lower()
    suffix = path_str[2:].replace("\\", "/").lstrip("/")
    return Path(f"/mnt/{drive}/{suffix}")


def repo_name_for(project_dir, config):
    repo_url = str(config.get("repo_url", "")).rstrip("/")
    if repo_url:
        return repo_url.rsplit("/", 1)[-1]
    slug = str(config.get("slug", "")).strip()
    if slug:
        return slug
    return project_dir.name.lower().replace(" ", "-").replace("_", "-")


def create_push_script(project_dir, repo_name):
    """Create push.sh in each project for easy updating."""
    script = f'''#!/bin/bash
# Quick push — run after updating paper.md or any files
# Usage: bash push.sh "commit message"

MSG="${{1:-Update E156 submission}}"

git add -A
git commit -m "$MSG"
git push origin master 2>/dev/null || git push origin main 2>/dev/null

echo ""
echo "Pushed to GitHub. View at:"
echo "  https://github.com/{GH_USER}/{repo_name}"
echo "  https://{GH_USER}.github.io/{repo_name}/"
echo "  https://{GH_USER}.github.io/{repo_name}/e156-submission/"
'''
    (project_dir / "push.sh").write_text(script, encoding="utf-8", newline="\n")


def create_live_dashboard():
    """Create a live status dashboard showing all projects and their state."""
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
        title = c.get("title", name)
        repo_name = repo_name_for(sub.parent, c)
        proj_type = c.get("type", "methods")
        body = c.get("body", "")
        wc = len(body.split())
        notes = c.get("notes", {})
        refs = c.get("references", [])
        has_app = any(f.suffix == ".html" for f in (sub / "assets").iterdir()) if (sub / "assets").is_dir() else False
        has_figs = any(f.suffix in (".png", ".svg", ".jpg") for f in (sub / "assets").iterdir()) if (sub / "assets").is_dir() else False

        # Status determination
        if wc == 156 and len(refs) >= 2:
            status = "ready"
            status_label = "Ready for Review"
        elif wc == 156:
            status = "draft"
            status_label = "Draft"
        else:
            status = "wip"
            status_label = f"WIP ({wc}w)"

        projects.append({
            "name": name, "repo": repo_name, "title": title,
            "type": proj_type, "status": status, "status_label": status_label,
            "wc": wc, "has_app": has_app, "has_figs": has_figs,
            "code": notes.get("code", ""),
        })

    projects.sort(key=lambda p: ({"ready": 0, "draft": 1, "wip": 2}[p["status"]], p["type"], p["name"]))

    esc = lambda s: str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")

    # Status counts
    ready = sum(1 for p in projects if p["status"] == "ready")
    draft = sum(1 for p in projects if p["status"] == "draft")
    wip = sum(1 for p in projects if p["status"] == "wip")
    with_apps = sum(1 for p in projects if p["has_app"])

    # Build project rows
    rows = ""
    for p in projects:
        status_class = p["status"]
        app_badge = '<span class="badge app">App</span>' if p["has_app"] else ""
        fig_badge = '<span class="badge fig">Figs</span>' if p["has_figs"] else ""
        rows += f'''<tr class="{status_class}">
  <td><a href="https://{GH_USER}.github.io/{p['repo']}/e156-submission/">{esc(p['title'][:65])}</a></td>
  <td>{esc(p['type'])}</td>
  <td><span class="status {status_class}">{esc(p['status_label'])}</span></td>
  <td>{p['wc']}</td>
  <td>{app_badge}{fig_badge}</td>
  <td><a href="https://github.com/{GH_USER}/{p['repo']}" class="gh-link">GitHub</a></td>
</tr>\n'''

    dashboard = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Evidence Synthesis — Live Dashboard</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:system-ui,-apple-system,sans-serif;background:#f8f9fa;color:#1a1a1a;line-height:1.5}}
.page{{max-width:1200px;margin:0 auto;padding:2rem 1.5rem}}
.hero{{text-align:center;padding:1.5rem 0 2rem;margin-bottom:1.5rem}}
.hero h1{{font-family:Georgia,serif;font-size:1.8rem;margin-bottom:.3rem}}
.hero .sub{{font-size:.85rem;color:#666}}
.stats{{display:flex;gap:1rem;justify-content:center;margin:1.5rem 0;flex-wrap:wrap}}
.stat-card{{background:#fff;border:1px solid #e0e0e0;border-radius:8px;padding:1rem 1.5rem;text-align:center;min-width:120px}}
.stat-num{{font-size:1.8rem;font-weight:700}}
.stat-num.green{{color:#28a745}}
.stat-num.amber{{color:#d68910}}
.stat-num.blue{{color:#2E86C1}}
.stat-label{{font-size:.7rem;color:#888;text-transform:uppercase;letter-spacing:.1em}}
.search{{width:100%;max-width:500px;margin:0 auto 1.5rem;display:block;padding:10px 16px;border:1px solid #ddd;border-radius:6px;font-size:.9rem}}
.search:focus{{outline:2px solid #2E86C1;border-color:transparent}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e0e0e0;border-radius:8px;overflow:hidden}}
th{{background:#f1f3f5;padding:10px 12px;text-align:left;font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:#666;border-bottom:2px solid #e0e0e0}}
td{{padding:8px 12px;border-bottom:1px solid #f0f0f0;font-size:.85rem}}
td a{{color:#2E6B8A;text-decoration:none}}
td a:hover{{text-decoration:underline}}
tr:hover{{background:#f8f9ff}}
.status{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.7rem;font-weight:600}}
.status.ready{{background:#d4edda;color:#155724}}
.status.draft{{background:#fff3cd;color:#856404}}
.status.wip{{background:#f8d7da;color:#721c24}}
.badge{{display:inline-block;padding:1px 5px;border-radius:3px;font-size:.6rem;font-weight:700;margin-right:3px}}
.badge.app{{background:#2E86C1;color:#fff}}
.badge.fig{{background:#28a745;color:#fff}}
.gh-link{{font-size:.75rem;color:#888}}
.footer{{text-align:center;margin-top:2rem;font-size:.7rem;color:#aaa}}
@media(max-width:768px){{td:nth-child(4),th:nth-child(4),td:nth-child(5),th:nth-child(5){{display:none}}.page{{padding:1rem}}}}
</style>
</head>
<body>
<div class="page">
  <header class="hero">
    <h1>Evidence Synthesis Portfolio</h1>
    <div class="sub">Mahmood Ahmad &middot; Tahir Heart Institute &middot; Live Project Dashboard</div>
  </header>

  <div class="stats">
    <div class="stat-card"><div class="stat-num green">{ready}</div><div class="stat-label">Ready</div></div>
    <div class="stat-card"><div class="stat-num amber">{draft}</div><div class="stat-label">Draft</div></div>
    <div class="stat-card"><div class="stat-num" style="color:#c0392b">{wip}</div><div class="stat-label">In Progress</div></div>
    <div class="stat-card"><div class="stat-num blue">{with_apps}</div><div class="stat-label">Apps</div></div>
    <div class="stat-card"><div class="stat-num">{len(projects)}</div><div class="stat-label">Total</div></div>
  </div>

  <input type="search" class="search" placeholder="Filter projects..." id="filter" aria-label="Filter projects">

  <table id="table">
    <thead>
      <tr><th>Project</th><th>Type</th><th>Status</th><th>Words</th><th>Assets</th><th>Code</th></tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>

  <div class="footer">Updated {projects[0].get("code","")[:0]}2026 &middot; E156 Micro-Paper Format &middot; All work in progress</div>
</div>
<script>
document.getElementById("filter").addEventListener("input",function(){{
  const q=this.value.toLowerCase();
  document.querySelectorAll("#table tbody tr").forEach(r=>{{
    r.style.display=r.textContent.toLowerCase().includes(q)?"":"none";
  }});
}});
</script>
</body>
</html>'''

    return dashboard


def main():
    submissions = find_all_submissions()
    print(f"Found {len(submissions)} submissions\n")

    # Create push.sh in each project
    created = 0
    for sub in submissions:
        project_dir = sub.parent
        cfg = sub / "config.json"
        config = {}
        if cfg.exists():
            try:
                config = json.loads(cfg.read_text(encoding="utf-8"))
            except Exception:
                config = {}
        repo_name = repo_name_for(project_dir, config)
        create_push_script(project_dir, repo_name)
        created += 1

    print(f"Created {created} push.sh scripts\n")

    # Create live dashboard
    dashboard_html = create_live_dashboard()
    portfolio_dir = local_windows_path(rf"C:\{GH_USER}.github.io")
    portfolio_dir.mkdir(exist_ok=True)
    (portfolio_dir / "dashboard.html").write_text(dashboard_html, encoding="utf-8")
    (portfolio_dir / "index.html").write_text(dashboard_html, encoding="utf-8")
    print(f"Dashboard saved to {portfolio_dir}/index.html")

    # Push portfolio
    subprocess.run(["git", "-C", str(portfolio_dir), "add", "-A"], capture_output=True, timeout=10)
    subprocess.run(["git", "-C", str(portfolio_dir), "commit", "-m", "Update live dashboard"],
                  capture_output=True, timeout=10)
    r = subprocess.run(["git", "-C", str(portfolio_dir), "push", "origin", "master"],
                      capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        print(f"Dashboard live at: https://{GH_USER}.github.io/")
    else:
        subprocess.run(["git", "-C", str(portfolio_dir), "push", "origin", "main"],
                      capture_output=True, timeout=30)
        print(f"Dashboard pushed (main branch)")


if __name__ == "__main__":
    main()
