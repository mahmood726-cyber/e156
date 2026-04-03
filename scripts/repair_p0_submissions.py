"""
Repair partial e156-submission folders and bootstrap missing ones for the
current P0 audit backlog.
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from add_protocols_and_disclosure import process as add_protocol_and_disclosure
from finalize_all import DATE, process_submission
from generate_submission import generate_submission

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "e156-submission",
    "releases",
    "renv",
    "build",
    "dist",
    "site-packages",
    "MLM501.Rcheck",
    "bapmr.Rcheck",
    "pwcvR2.Rcheck",
}

DOC_EXTS = {".md", ".rmd", ".qmd", ".txt", ".cff"}
CODE_EXTS = {".py", ".r", ".js", ".ts", ".tsx", ".jsx", ".html", ".css"}
ASSET_EXTS = {".png", ".svg", ".jpg", ".jpeg", ".gif", ".pdf", ".html"}

PROJECT_SPECS = {
    "/mnt/c/AfricaRCT": {
        "title": "AfricaRCT Observatory: Reproducibility Capsule for African Trial-Methods Audits",
        "code_override": "https://github.com/mahmood726-cyber/africa-rct",
    },
    "/mnt/c/CausalSynth": {
        "title": "CausalSynth: Reproducibility Capsule for Cross-Design Evidence Triangulation",
        "code_override": "https://github.com/mahmood726-cyber/CausalSynth",
    },
    "/mnt/c/MetaAudit": {
        "title": "MetaAudit: Reproducibility Capsule for Automated Meta-Analytic Quality Audits",
        "code_override": "https://github.com/mahmood726-cyber/metaaudit",
    },
    "/mnt/c/MetaReproducer": {
        "title": "MetaReproducer: Reproducibility Capsule for Cochrane Reproduction Audits",
        "code_override": "https://github.com/mahmood726-cyber/metareproducer",
    },
    "/mnt/c/Projects/Paper2.111025": {
        "title": "Precision-Weighted Cross-Validation: Reproducibility Capsule for Meta-Regression R-Squared Evaluation",
        "code_override": "https://github.com/mahmood726-cyber/pwcvR2",
    },
    "/mnt/c/Projects/chat2": {
        "title": "CBAMM-Chat2: Reproducibility Capsule for Automated Meta-Overfitting Validation",
        "code_override": "https://github.com/cbamm-dev/cbamm",
    },
    "/mnt/c/Projects/cardio-ctgov-living-meta-portfolio": {
        "title": "Cardio CT.gov Living Meta Portfolio: Reproducibility Capsule for Registry-First Cardiovascular Surveillance",
        "code_override": "https://github.com/mahmood726-cyber/cardio-ctgov-living-meta-portfolio",
    },
    "/mnt/c/Projects/chatpaper": {
        "title": "MA4 vs HKSJ: Reproducibility Capsule for Robustness-Metric Comparison",
        "code_override": "/mnt/c/Projects/chatpaper",
    },
    "/mnt/c/Projects/claude2": {
        "title": "Weighted vs Unweighted CV in Meta-Regression: Reproducibility Capsule",
        "code_override": "https://github.com/cbamm-dev/claude2",
    },
    "/mnt/c/Projects/clauderepo": {
        "title": "clauderepo: Reproducibility Capsule for an Advanced Meta-Analysis Compendium",
        "code_override": "https://github.com/mahmood726-cyber/clauderepo",
    },
    "/mnt/c/Projects/everything-claude-code": {
        "title": "Everything Claude Code: Reproducibility Capsule for a Claude Plugin Stack",
        "code_override": "https://github.com/affaan-m/everything-claude-code",
    },
    "/mnt/c/Projects/esc-acs-living-meta": {
        "title": "ESC ACS Living Meta: Reproducibility Capsule for Guideline-Aware Cardiovascular Surveillance",
        "code_override": "https://github.com/mahmood726-cyber/esc-acs-living-meta",
    },
    "/mnt/c/Projects/my-python-project": {
        "title": "my-python-project: Reproducibility Capsule for a Python Evidence-Synthesis Scaffold",
        "code_override": "/mnt/c/Projects/my-python-project",
    },
    "/mnt/c/Projects/nmapaper111025": {
        "title": "nmatransport: Reproducibility Capsule for Transported Network Meta-Analysis",
        "code_override": "https://github.com/mahmood726-cyber/nmatransport",
    },
    "/mnt/c/mahmood726-cyber.github.io": {
        "title": "Evidence Synthesis Portfolio Site: Reproducibility Capsule",
        "code_override": "https://github.com/mahmood726-cyber/mahmood726-cyber.github.io",
    },
}

LEGACY_PAPER_JSON_PROJECTS = [
    Path("/mnt/c/Models/DPMA"),
    Path("/mnt/c/Models/ROBMA"),
]


def iter_files(project_dir: Path):
    for path in project_dir.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(project_dir)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        yield path


def is_test_file(path: Path) -> bool:
    lowered = path.name.lower()
    parts = {part.lower() for part in path.parts}
    return (
        lowered.startswith("test")
        or lowered.endswith("_test.py")
        or lowered.endswith(".test.js")
        or lowered.endswith("_test.r")
        or "tests" in parts
        or "test" in parts
    )


def count_dependencies(project_dir: Path) -> int:
    total = 0

    requirements = project_dir / "requirements.txt"
    if requirements.exists():
        total += sum(
            1
            for line in requirements.read_text(encoding="utf-8", errors="ignore").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )

    pyproject = project_dir / "pyproject.toml"
    if pyproject.exists():
        try:
            import tomllib

            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            total += len(data.get("project", {}).get("dependencies", []))
            for group in data.get("project", {}).get("optional-dependencies", {}).values():
                total += len(group)
        except Exception:
            pass

    package_json = project_dir / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            for key in ("dependencies", "devDependencies", "peerDependencies"):
                total += len(data.get(key, {}))
        except Exception:
            pass

    description = project_dir / "DESCRIPTION"
    if description.exists():
        lines = description.read_text(encoding="utf-8", errors="ignore").splitlines()
        capture = None
        fields = {"Depends", "Imports", "Suggests", "LinkingTo"}
        for line in lines:
            if re.match(r"^[A-Za-z][A-Za-z0-9]+:", line):
                field = line.split(":", 1)[0]
                capture = field if field in fields else None
                content = line.split(":", 1)[1] if capture else ""
            elif capture and (line.startswith(" ") or line.startswith("\t")):
                content = line
            else:
                content = ""
                capture = None
            if capture and content:
                pkgs = [
                    item.strip()
                    for item in content.replace("\t", " ").split(",")
                    if item.strip() and item.strip().upper() != "R"
                ]
                total += len(pkgs)

    return total


def inventory(project_dir: Path) -> dict:
    source_files = 0
    test_files = 0
    doc_files = 0
    asset_files = 0
    entry_files = 0

    for path in iter_files(project_dir):
        suffix = path.suffix.lower()
        rel = path.relative_to(project_dir)
        name = path.name.lower()

        if is_test_file(rel):
            test_files += 1
        elif suffix in CODE_EXTS:
            source_files += 1

        if suffix in DOC_EXTS or name in {"readme", "readme.md", "protocol.md"}:
            doc_files += 1

        if suffix in ASSET_EXTS:
            asset_files += 1

        if re.search(r"(run|main|index|app|dashboard|pipeline|generate|setup|build)", path.stem.lower()):
            entry_files += 1

    dep_count = count_dependencies(project_dir)
    surfaces = [source_files, test_files, doc_files, asset_files]
    surface_range = f"{min(surfaces)}-{max(surfaces)}"
    total_surface = max(sum(surfaces), 1)
    doc_proportion = f"{doc_files / total_surface:.2f}"

    return {
        "source_files": source_files,
        "test_files": test_files,
        "doc_files": doc_files,
        "asset_files": asset_files,
        "entry_files": entry_files,
        "dep_count": dep_count,
        "surface_range": surface_range,
        "doc_proportion": doc_proportion,
    }


def sanitize_slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def legacy_config(project_dir: Path) -> dict:
    submission_dir = project_dir / "e156-submission"
    legacy = json.loads((submission_dir / "paper.json").read_text(encoding="utf-8"))
    note = legacy.get("outsideNote", {})
    body = legacy.get("body", "")
    sentences = legacy.get("sentences", [])
    title = legacy.get("title", project_dir.name)
    return {
        "title": title,
        "slug": sanitize_slug(project_dir.name),
        "date": note.get("date", DATE),
        "path": str(project_dir),
        "type": note.get("type", "methods"),
        "primary_estimand": note.get("primary_estimand", "summary effect"),
        "certainty": note.get("certainty", "moderate"),
        "summary": body.split(". ", 1)[0].strip(),
        "body": body,
        "sentences": sentences,
        "notes": {
            "app": note.get("app", f"{project_dir.name} v1.0"),
            "data": note.get("data", f"Repository artifacts in {project_dir}"),
            "code": note.get("code", str(project_dir)),
            "doi": note.get("doi", ""),
            "version": note.get("version", "1.0"),
            "date": note.get("date", DATE),
            "certainty": note.get("certainty", "moderate"),
            "validation": note.get("validationStatus", "DRAFT"),
            "protocol": note.get("protocol", ""),
            "source_article": note.get("source_article", ""),
        },
    }


def generic_sentences(counts: dict) -> list[str]:
    return [
        "Can a reproducibility capsule turn an evidence-synthesis repository into a reviewer-auditable submission without restaging the workflow?",
        (
            "We audited the shipped project using "
            f"{counts['source_files']} source files, {counts['test_files']} test files, "
            f"{counts['doc_files']} manuscript or guide files, and {counts['asset_files']} "
            "dashboard or figure assets committed locally."
        ),
        "The capsule packages a micro-paper, a machine-readable config, an interactive reader, and a protocol so the repository can be inspected across reviewers.",
        (
            "Across the inventory, the repository yields a documentation proportion of "
            f"{counts['doc_proportion']}, with file-count range {counts['surface_range']} "
            f"across core surfaces, while exposing {counts['entry_files']} entry points and "
            f"{counts['dep_count']} declared dependencies."
        ),
        "Git metadata, file counts, and copied assets provide a stable local audit trail even when engine outputs remain outside the submission bundle.",
        "This packaging step converts a diffuse codebase into a citable, inspectable micro-publication suitable for rapid editorial triage and downstream peer review.",
        "The capsule does not verify scientific correctness itself; it standardizes what reviewers receive first, and deeper validation still depends on tests and manuscripts.",
    ]


def generic_config(project_dir: Path, spec: dict) -> dict:
    counts = inventory(project_dir)
    sentences = generic_sentences(counts)
    body = " ".join(sentences)
    summary = (
        f"Reviewer-facing capsule built from {counts['source_files']} source files, "
        f"{counts['test_files']} tests, and {counts['asset_files']} copied assets."
    )
    code_value = spec.get("code_override", str(project_dir))
    return {
        "title": spec["title"],
        "slug": sanitize_slug(project_dir.name),
        "date": DATE,
        "path": str(project_dir),
        "type": "methods",
        "primary_estimand": "documentation proportion",
        "certainty": "moderate",
        "summary": summary,
        "body": body,
        "sentences": [{"role": role, "text": text} for role, text in zip(
            ["Question", "Dataset", "Method", "Primary result", "Robustness", "Interpretation", "Boundary"],
            sentences,
        )],
        "notes": {
            "app": f"{project_dir.name} E156 Capsule v1.0",
            "data": (
                "Repository inventory with "
                f"{counts['source_files']} source files, {counts['test_files']} test files, "
                f"{counts['doc_files']} documents, and {counts['asset_files']} assets."
            ),
            "code": code_value,
            "doi": "",
            "version": "1.0",
            "date": DATE,
            "certainty": "moderate",
            "validation": "DRAFT",
            "protocol": "",
            "source_article": "",
        },
    }


def materialize(config: dict) -> Path:
    submission_dir = Path(config["path"]) / "e156-submission"
    generate_submission(config)
    if not submission_dir.exists():
        raise RuntimeError(f"Submission generation did not create {submission_dir}")
    process_submission(submission_dir)
    add_protocol_and_disclosure(submission_dir)
    return submission_dir


def main() -> None:
    if "--no-github" not in sys.argv:
        sys.argv.append("--no-github")

    built = []
    failures = []

    for project_dir in LEGACY_PAPER_JSON_PROJECTS:
        try:
            submission_dir = materialize(legacy_config(project_dir))
            built.append({"project": str(project_dir), "submission_dir": str(submission_dir), "mode": "legacy_repair"})
            print(f"built {project_dir}", flush=True)
        except Exception as exc:
            failures.append({"project": str(project_dir), "mode": "legacy_repair", "error": str(exc)})
            print(f"failed {project_dir}: {exc}", flush=True)

    for project_path, spec in PROJECT_SPECS.items():
        project_dir = Path(project_path)
        try:
            submission_dir = materialize(generic_config(project_dir, spec))
            built.append({"project": str(project_dir), "submission_dir": str(submission_dir), "mode": "bootstrap"})
            print(f"built {project_dir}", flush=True)
        except Exception as exc:
            failures.append({"project": str(project_dir), "mode": "bootstrap", "error": str(exc)})
            print(f"failed {project_dir}: {exc}", flush=True)

    print(json.dumps({"built": built, "failures": failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
