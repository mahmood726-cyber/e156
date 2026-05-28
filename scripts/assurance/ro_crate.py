"""e156 Assurance — RO-Crate packaging (Track C).

Make the capsule a machine-readable research object instead of a bespoke
folder. RO-Crate (https://www.researchobject.org/ro-crate/, v1.1) is the
adopted JSON-LD / schema.org standard, so an e156 capsule that ships a
`ro-crate-metadata.json` becomes Findable/Accessible/Interoperable/Reusable
(FAIR) and indexable by existing tooling — the credibility step the standard
needs to be usable by people other than the author.

`build_ro_crate(...)` is a pure function (testable, no I/O). The CLI populates
it best-effort from a repo's e156-submission/config.json + assurance.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

RO_CRATE_CONTEXT = "https://w3id.org/ro/crate/1.1/context"
RO_CRATE_CONFORMS = "https://w3id.org/ro/crate/1.1"
DEFAULT_LICENSE = "https://creativecommons.org/licenses/by/4.0/"


def build_ro_crate(
    *,
    name: str,
    description: str,
    files: Iterable[str],
    date_published: Optional[str] = None,
    doi: Optional[str] = None,
    license_id: Optional[str] = DEFAULT_LICENSE,
    author: Optional[str] = None,
    assurance_tier: Optional[str] = None,
) -> dict:
    """Return a valid RO-Crate 1.1 metadata document (JSON-LD)."""
    files = list(files)
    date_published = date_published or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    graph: list[dict] = [
        {
            "@id": "ro-crate-metadata.json",
            "@type": "CreativeWork",
            "conformsTo": {"@id": RO_CRATE_CONFORMS},
            "about": {"@id": "./"},
        }
    ]

    root: dict = {
        "@id": "./",
        "@type": "Dataset",
        "name": name,
        "description": description,
        "datePublished": date_published,
        "hasPart": [{"@id": f} for f in files],
    }
    if doi:
        root["identifier"] = doi
    if license_id:
        root["license"] = {"@id": license_id}
    if author:
        root["author"] = {"@id": "#author"}
    if assurance_tier:
        root["additionalProperty"] = [{
            "@type": "PropertyValue",
            "name": "e156-assurance-tier",
            "value": assurance_tier,
        }]
    graph.append(root)

    if author:
        graph.append({"@id": "#author", "@type": "Person", "name": author})
    if license_id:
        graph.append({"@id": license_id, "@type": "CreativeWork", "name": "license"})
    for f in files:
        graph.append({"@id": f, "@type": "File", "name": f})

    return {"@context": RO_CRATE_CONTEXT, "@graph": graph}


def _existing_capsule_files(repo: Path) -> list[str]:
    """Best-effort: list the capsule artifacts that exist in the repo."""
    candidates = [
        "students.html", "doi-cache.json",
        "e156-submission/paper.md", "e156-submission/assurance.json",
        "e156-submission/config.json", "E156-PROTOCOL.md", "README.md",
    ]
    out = []
    for rel in candidates:
        if (repo / rel).is_file():
            out.append(rel)
    for p in sorted(repo.glob("*_REVIEW.html")):
        out.append(p.name)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Emit ro-crate-metadata.json for an e156 capsule.")
    ap.add_argument("--repo", default=".", help="Repo root (default: cwd)")
    ap.add_argument("--out", help="Output path (default: <repo>/ro-crate-metadata.json)")
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        sys.stderr.write(f"not a directory: {repo}\n")
        return 2

    name = repo.name
    description = f"e156 evidence capsule: {repo.name}"
    doi = None
    author = None
    cfg = repo / "e156-submission" / "config.json"
    if cfg.is_file():
        try:
            c = json.loads(cfg.read_text(encoding="utf-8"))
            name = c.get("title", name)
            doi = c.get("doi") or doi
            author = c.get("corresponding_author") or c.get("author") or author
        except (OSError, json.JSONDecodeError):
            pass

    tier = None
    badge = repo / "e156-submission" / "assurance.json"
    if badge.is_file():
        try:
            tier = json.loads(badge.read_text(encoding="utf-8")).get("tier")
        except (OSError, json.JSONDecodeError):
            pass

    crate = build_ro_crate(
        name=name, description=description,
        files=_existing_capsule_files(repo),
        doi=doi, author=author, assurance_tier=tier,
    )
    out = Path(args.out) if args.out else repo / "ro-crate-metadata.json"
    out.write_text(json.dumps(crate, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(crate['@graph'])} entities)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
