import json
from pathlib import Path, PurePath


def test_submission_config_is_repo_relative_and_titled():
    config_path = Path(__file__).parent.parent / "e156-submission" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    assert config["title"].startswith("E156:")
    assert not PurePath(config["path"]).is_absolute()
    assert config["path"] == ".."


def test_build_library_defaults_are_repo_relative():
    import build_library

    root = Path(build_library.ROOT).resolve()

    assert root == Path(__file__).parent.parent.resolve()
    assert Path(build_library.WORKBOOK_PATH).resolve() == root / "rewrite-workbook.txt"
    assert Path(build_library.TEMPLATE_PATH).resolve() == root / "templates" / "library-template.html"
    assert Path(build_library.OUTPUT_PATH).resolve() == root / "e156-library.html"
