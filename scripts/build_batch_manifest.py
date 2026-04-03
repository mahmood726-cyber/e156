"""Build a batch manifest for regenerating all discovered E156 submissions."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from e156_utils import find_all_submissions


DEFAULT_OUTPUT = SCRIPT_DIR / "_batch_all.json"


def load_config(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def hydrate_config(config: dict[str, object], submission_dir: Path) -> dict[str, object]:
    hydrated = dict(config)
    paper_path = submission_dir / "paper.json"
    paper: dict[str, object] = {}
    if paper_path.exists():
        try:
            paper = load_config(paper_path)
        except (OSError, json.JSONDecodeError):
            paper = {}

    for field in ("title", "slug", "date", "type", "primary_estimand", "certainty", "summary", "body", "sentences"):
        if not hydrated.get(field) and paper.get(field):
            hydrated[field] = paper[field]

    hydrated["path"] = str(submission_dir.parent)
    return hydrated


def main() -> None:
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT
    projects: list[dict[str, object]] = []

    for submission_dir in find_all_submissions():
        config_path = submission_dir / "config.json"
        if not config_path.exists():
            continue
        try:
            config = load_config(config_path)
        except (OSError, json.JSONDecodeError):
            continue
        projects.append(hydrate_config(config, submission_dir))

    output_path.write_text(
        json.dumps({"projects": projects}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {len(projects)} projects to {output_path}")


if __name__ == "__main__":
    main()
