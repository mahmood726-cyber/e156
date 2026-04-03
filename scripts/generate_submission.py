"""
E156 Submission Folder Generator
==================================
Creates e156-submission/ folders inside project directories with:
  - index.html   (interactive reader from Codex template)
  - paper.md     (markdown body + outside notes)
  - paper.json   (structured JSON)

Usage:
    python scripts/generate_submission.py config.json
    python scripts/generate_submission.py --batch manifest.json

Config format (single project):
{
    "title": "Paper Title",
    "slug": "paper-slug",
    "author": "M. Mahmood",
    "date": "2026-03-26",
    "path": "C:\\\\path\\\\to\\\\project",
    "type": "pairwise",
    "primary_estimand": "Risk ratio",
    "certainty": "moderate",
    "validation": "DRAFT",
    "summary": "One-sentence summary for the hero section.",
    "body": "Full 156-word body as a single string.",
    "sentences": [
        {"role": "Question", "text": "S1..."},
        {"role": "Dataset", "text": "S2..."},
        {"role": "Method", "text": "S3..."},
        {"role": "Primary result", "text": "S4..."},
        {"role": "Robustness", "text": "S5..."},
        {"role": "Interpretation", "text": "S6..."},
        {"role": "Boundary", "text": "S7..."}
    ],
    "notes": {
        "app": "Tool Name v1.0",
        "data": "Dataset description",
        "code": "Repository URL or local path",
        "doi": "",
        "version": "1.0",
        "date": "2026-03-26",
        "certainty": "moderate",
        "validation": "DRAFT",
        "protocol": "",
        "source_article": ""
    },
    "study_count": null,
    "participant_count": null,
    "studies": [],
    "primary_plot": {}
}
"""

import json
import html as html_mod
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR.parent / "templates"
TEMPLATE_PATH = TEMPLATE_DIR / "e156_editorial_template.html"

# Import validator
sys.path.insert(0, str(SCRIPT_DIR))
try:
    from e156_utils import validate_path
    from validate_e156 import validate
except ImportError:
    def validate_path(project_path):
        return True

    def validate(text, strict_words=True):
        words = len(text.split())
        sents = len(re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', text.strip()))
        return {"word_count": words, "sentence_count": sents, "ok": words == 156 and sents == 7,
                "checks": [{"name": "word count", "ok": words == 156, "detail": f"{words} words"},
                           {"name": "sentence count", "ok": sents == 7, "detail": f"{sents} sentences"}]}


def build_article(config):
    """Build a full article dict from config, compatible with Codex template."""
    body = config.get("body", "")
    if not body and "sentences" in config:
        body = " ".join(s["text"] if isinstance(s, dict) else s for s in config["sentences"])

    notes = config.get("notes", {})
    validation_result = validate(body, strict_words=True)

    article = {
        "title": config.get("title", "Untitled E156"),
        "summary": config.get("summary", ""),
        "type": config.get("type", "methods"),
        "primary_estimand": config.get("primary_estimand", ""),
        "study_count": config.get("study_count"),
        "participant_count": config.get("participant_count"),
        "version": config.get("version", notes.get("version", "1.0")),
        "date": config.get("date", notes.get("date", "2026-03-26")),
        "certainty": config.get("certainty", notes.get("certainty", "")),
        "app": notes.get("app", ""),
        "data": notes.get("data", ""),
        "code": notes.get("code", ""),
        "doi": notes.get("doi", ""),
        "protocol": notes.get("protocol", ""),
        "source_article": notes.get("source_article", ""),
        "body": body,
        "validation": {
            "status": "pass" if validation_result["ok"] else "fail",
            "checks": validation_result["checks"],
        },
        "sentences": config.get("sentences", []),
        "primary_plot": config.get("primary_plot", {}),
        "studies": config.get("studies", []),
        "search_strategy": config.get("search_strategy", {}),
        "prisma": config.get("prisma", {}),
        "included_papers": config.get("included_papers", []),
        "analysis_modules": config.get("analysis_modules", []),
    }

    # Carry through extra fields
    for key in ("funding", "conflicts", "author", "affiliation", "email",
                "slug", "references", "_assets", "_disclosure"):
        if key in config:
            article[key] = config[key]

    return article, validation_result


def render_html(article, template_text):
    """Inject article JSON into the HTML template."""
    safe_json = json.dumps(article, indent=2, ensure_ascii=False)
    safe_json = re.sub(r"</script", r"<\\/script", safe_json, flags=re.IGNORECASE)
    html = template_text.replace("__E156_JSON__", safe_json)
    html = html.replace("__TITLE__", html_mod.escape(article.get("title", "E156")))
    return html


def generate_markdown(config, body, notes):
    """Generate paper.md."""
    title = config.get("title", "Untitled")
    author = config.get("author", "M. Mahmood")
    date_str = config.get("date", notes.get("date", "2026-03-26"))

    affiliation = config.get("affiliation", "")
    email = config.get("email", "")
    lines = [author]
    if affiliation:
        lines.append(affiliation)
    if email:
        lines.append(email)
    lines.extend(["", title, "", body, "", "Outside Notes", ""])

    note_fields = [
        ("Type", config.get("type", "")),
        ("Primary estimand", config.get("primary_estimand", "")),
        ("App", notes.get("app", "")),
        ("Data", notes.get("data", "")),
        ("Code", notes.get("code", "")),
        ("DOI", notes.get("doi", "")),
        ("Version", notes.get("version", config.get("version", ""))),
        ("Certainty", notes.get("certainty", config.get("certainty", ""))),
        ("Validation", notes.get("validation", "DRAFT")),
        ("Protocol", notes.get("protocol", "")),
        ("Source article", notes.get("source_article", "")),
    ]

    for label, value in note_fields:
        if value:
            lines.append(f"{label}: {value}")

    refs = config.get("references", [])
    if refs:
        lines.extend(["", "References", ""])
        for i, ref in enumerate(refs, 1):
            lines.append(f"{i}. {ref}")

    return "\n".join(lines) + "\n"


def hydrate_config_from_source(config, source_path):
    """Resolve relative config paths and recover body fields from an existing submission."""
    hydrated = dict(config)
    if not source_path:
        return hydrated

    source_path = Path(source_path).resolve()
    if source_path.name == "config.json" and source_path.parent.name == "e156-submission":
        project_dir = source_path.parent.parent
        if not hydrated.get("path") or str(hydrated.get("path")).strip() in {".", "./"}:
            hydrated["path"] = str(project_dir)

        paper_path = source_path.parent / "paper.json"
        if paper_path.exists():
            try:
                paper = json.loads(paper_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                paper = {}
            for field in ("title", "slug", "date", "type", "primary_estimand", "certainty", "summary", "body", "sentences"):
                if not hydrated.get(field) and paper.get(field):
                    hydrated[field] = paper[field]

    return hydrated


def generate_submission(config):
    """Create e156-submission/ folder inside the project directory."""
    project_path = config.get("path", "")
    if not project_path:
        print(f"  SKIP: no path for '{config.get('title', '?')}'")
        return False

    # Path validation
    resolved = str(Path(project_path).resolve())
    if not validate_path(project_path):
        print(f"  SKIP: path '{resolved}' outside allowed directories")
        return False

    # Build article
    article, validation_result = build_article(config)
    body = article["body"]
    notes = config.get("notes", {})
    wc = validation_result["word_count"]
    sc = validation_result["sentence_count"]

    # Output directory
    out_dir = Path(project_path) / "e156-submission"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Scan assets/ directory and inject into article for template
    assets_dir = out_dir / "assets"
    if assets_dir.is_dir():
        asset_files = sorted(f.name for f in assets_dir.iterdir() if f.is_file())
        article["_assets"] = asset_files
    else:
        article["_assets"] = []

    # Add AI disclosure
    article["_disclosure"] = config.get("_disclosure",
        "This work represents a compiler-generated evidence micro-publication. "
        "AI is used as a constrained synthesis engine operating on structured inputs "
        "and predefined rules, rather than as an autonomous author. All results and "
        "text were reviewed and verified by the author, who takes full responsibility "
        "for the content.")

    # 1. HTML — interactive reader
    if TEMPLATE_PATH.exists():
        template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
        html = render_html(article, template_text)
    else:
        # Fallback: minimal HTML (escaped)
        safe_title = html_mod.escape(article['title'])
        safe_body = html_mod.escape(body)
        safe_pre = html_mod.escape(json.dumps(article, indent=2))
        html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>E156 - {safe_title}</title></head>
<body><h1>{safe_title}</h1><p>{safe_body}</p>
<pre>{safe_pre}</pre></body></html>"""

    (out_dir / "index.html").write_text(html, encoding="utf-8")

    # 2. Markdown
    md = generate_markdown(config, body, notes)
    (out_dir / "paper.md").write_text(md, encoding="utf-8")

    # 3. JSON
    paper_json = {
        "title": article["title"],
        "slug": config.get("slug", re.sub(r"[^a-z0-9]+", "-", article["title"].lower())[:60].strip("-")),
        "author": config.get("author", "M. Mahmood"),
        "date": article["date"],
        "body": body,
        "word_count": wc,
        "sentence_count": sc,
        "sentences": article.get("sentences", []),
        "notes": notes,
        "type": article["type"],
        "primary_estimand": article["primary_estimand"],
        "validation": article["validation"],
        "schema": "e156-v0.2",
    }
    (out_dir / "paper.json").write_text(
        json.dumps(paper_json, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 4. Config backup (for re-generation)
    (out_dir / "config.json").write_text(
        json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    status = "PASS" if validation_result["ok"] else f"WARN({wc}w/{sc}s)"
    print(f"  {status}: {article['title']} -> {out_dir}")
    return validation_result["ok"]


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_submission.py <config.json>")
        print("       python generate_submission.py --batch <manifest.json>")
        sys.exit(1)

    batch_mode = "--batch" in sys.argv
    positional = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not positional:
        print("Error: no config file specified.")
        sys.exit(1)
    file_arg = positional[0]

    try:
        with open(file_arg, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON in {file_arg}: {e}")
        sys.exit(1)

    if batch_mode or "projects" in data:
        projects = data.get("projects", data if isinstance(data, list) else [data])
        ok = 0
        total = len(projects)
        for i, proj in enumerate(projects, 1):
            print(f"[{i}/{total}] {proj.get('title', '?')}...")
            if generate_submission(proj):
                ok += 1
        print(f"\n{'='*60}")
        print(f"Generated {total} submissions ({ok} valid, {total - ok} warnings)")
    else:
        generate_submission(hydrate_config_from_source(data, file_arg))


if __name__ == "__main__":
    main()
