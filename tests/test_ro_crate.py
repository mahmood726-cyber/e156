"""Tests for the RO-Crate capsule packaging (Track C)."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT, ROOT / "scripts"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

rc = importlib.import_module("assurance.ro_crate")


def _by_id(crate: dict) -> dict:
    return {e["@id"]: e for e in crate["@graph"]}


def test_has_context_and_graph():
    crate = rc.build_ro_crate(name="Demo", description="d", files=["a.md"])
    assert crate["@context"] == rc.RO_CRATE_CONTEXT
    assert isinstance(crate["@graph"], list)


def test_metadata_descriptor_conforms():
    crate = rc.build_ro_crate(name="Demo", description="d", files=["a.md"])
    desc = _by_id(crate)["ro-crate-metadata.json"]
    assert desc["@type"] == "CreativeWork"
    assert desc["conformsTo"]["@id"] == rc.RO_CRATE_CONFORMS
    assert desc["about"]["@id"] == "./"


def test_root_dataset_lists_all_files():
    files = ["students.html", "e156-submission/assurance.json", "x_REVIEW.html"]
    crate = rc.build_ro_crate(name="Demo", description="d", files=files)
    root = _by_id(crate)["./"]
    assert root["@type"] == "Dataset"
    assert root["name"] == "Demo"
    part_ids = {p["@id"] for p in root["hasPart"]}
    assert part_ids == set(files)
    entities = _by_id(crate)
    for f in files:
        assert entities[f]["@type"] == "File"


def test_doi_and_tier_recorded():
    crate = rc.build_ro_crate(
        name="Demo", description="d", files=["a.md"],
        doi="10.5281/zenodo.123", assurance_tier="silver",
    )
    root = _by_id(crate)["./"]
    assert root["identifier"] == "10.5281/zenodo.123"
    props = {p["name"]: p["value"] for p in root["additionalProperty"]}
    assert props["e156-assurance-tier"] == "silver"


def test_author_entity_linked():
    crate = rc.build_ro_crate(name="Demo", description="d", files=["a.md"], author="Mahmood Ahmad")
    root = _by_id(crate)["./"]
    assert root["author"]["@id"] == "#author"
    assert _by_id(crate)["#author"]["name"] == "Mahmood Ahmad"


def test_cli_writes_crate(tmp_path):
    (tmp_path / "README.md").write_text("hi\n", encoding="utf-8")
    rc.main(["--repo", str(tmp_path)])
    out = tmp_path / "ro-crate-metadata.json"
    assert out.is_file()
    import json
    crate = json.loads(out.read_text(encoding="utf-8"))
    assert crate["@context"] == rc.RO_CRATE_CONTEXT
