# sentinel:skip-file  (P0-hardcoded-local-path: portfolio-management script with intentional external project paths)
"""Append new complete E156 projects to the rewrite workbook."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
E156_ROOT = SCRIPT_PATH.parent
WORKBOOK = E156_ROOT / "rewrite-workbook.txt"

STANDARD_WINDOWS_ROOTS = [
    r"C:\Projects",
    r"C:\Models",
    r"C:\HTML apps",
    r"C:\Users\user",
]

SKIP_TOP_LEVEL = {
    "$recycle.bin",
    "windows",
    "program files",
    "program files (x86)",
    "programdata",
    "users",
    "system volume information",
    "perflogs",
    "recovery",
    "e156",
}

LIMITATION_WORDS = [
    "limit",
    "cannot",
    "may not",
    "unclear",
    "uncertain",
    "caution",
    "scope",
    "boundary",
    "constrain",
    "restrict",
    "however",
    "does not",
    "only",
    "unable",
    "lack",
    "exclude",
    "depend",
    "assume",
    "not yet",
    "not address",
    "not extend",
    "not capture",
    "not replace",
    "not detect",
    "not account",
    "not support",
    "not verify",
    "remains",
    "caveat",
]


def normalize_windows_path(value: str) -> str:
    return re.sub(r"\\+", r"\\", value.strip().replace("/", "\\").rstrip("\\")).lower()


def windows_to_local_path(path_str: str) -> Path:
    path_str = path_str.replace("/", "\\")
    if os.name == "nt":
        return Path(path_str)
    match = re.match(r"^([A-Za-z]):\\(.*)$", path_str)
    if not match:
        return Path(path_str)
    drive = match.group(1).lower()
    remainder = match.group(2).replace("\\", "/")
    return Path(f"/mnt/{drive}/{remainder}")


def local_to_windows_path(path: Path) -> str:
    text = str(path)
    if os.name == "nt":
        return text.replace("/", "\\")
    if text == "/mnt/c":
        return "C:\\"
    if text.startswith("/mnt/c/"):
        return r"C:" + "\\" + text[len("/mnt/c/"):].replace("/", "\\")
    return text.replace("/", "\\")


def load_json_if_exists(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text.strip()) if part.strip()]


def valid_body(body: str) -> bool:
    if not body:
        return False
    words = len(body.split())
    sentences = split_sentences(body)
    if words < 100 or words > 156 or len(sentences) != 7:
        return False
    if len(sentences) >= 5 and not any(re.search(r"\d", sentences[index]) for index in range(2, 5)):
        return False
    if len(sentences) >= 7 and not any(word in sentences[6].lower() for word in LIMITATION_WORDS):
        return False
    return True


def has_mit_license(path: Path) -> bool:
    license_path = path / "LICENSE"
    if not license_path.exists():
        return False
    try:
        return "mit license" in license_path.read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        return False


def iter_candidate_projects() -> list[Path]:
    projects: list[Path] = []
    seen: set[Path] = set()

    for windows_root in STANDARD_WINDOWS_ROOTS:
        local_root = windows_to_local_path(windows_root)
        if not local_root.exists():
            continue
        try:
            children = sorted([child for child in local_root.iterdir() if child.is_dir()])
        except OSError:
            continue
        for child in children:
            if child not in seen:
                seen.add(child)
                projects.append(child)

    c_root = windows_to_local_path(r"C:\\")
    if c_root.exists():
        try:
            for child in sorted(c_root.iterdir()):
                try:
                    is_dir = child.is_dir()
                except OSError:
                    continue
                if not is_dir or child.name.lower() in SKIP_TOP_LEVEL:
                    continue
                if child in seen:
                    continue
                seen.add(child)
                projects.append(child)
        except OSError:
            pass

    return projects


def build_project_record(project_root: Path) -> dict[str, str] | None:
    e156_dir = project_root / "e156-submission"
    config_path = e156_dir / "config.json"
    paper_json_path = e156_dir / "paper.json"
    protocol_path = e156_dir / "protocol.md"
    dashboard_path = project_root / "index.html"
    alt_dashboard_path = e156_dir / "assets" / "dashboard.html"

    if not config_path.exists() or not paper_json_path.exists() or not protocol_path.exists():
        return None
    if not dashboard_path.exists() and not alt_dashboard_path.exists():
        return None
    if not has_mit_license(project_root):
        return None

    config = load_json_if_exists(config_path)
    paper = load_json_if_exists(paper_json_path)

    body = str(paper.get("body") or config.get("body") or "").strip()
    if not valid_body(body):
        return None

    notes = config.get("notes")
    note_data = ""
    if isinstance(notes, dict):
        note_data = str(notes.get("data", "")).strip()
    summary = str(paper.get("summary") or config.get("summary") or note_data).strip()

    return {
        "name": project_root.name,
        "title": str(paper.get("title") or config.get("title") or project_root.name).strip(),
        "type": str(paper.get("type") or config.get("type") or "methods").strip(),
        "estimand": str(paper.get("primary_estimand") or config.get("primary_estimand") or "See paper.json").strip(),
        "data": summary or "See paper.json summary",
        "path": local_to_windows_path(project_root),
        "body": body,
        "words": str(len(body.split())),
    }


def known_paths_from_workbook(text: str) -> set[str]:
    return {
        normalize_windows_path(match.group(1))
        for match in re.finditer(r"^PATH:\s*(.+)$", text, re.MULTILINE)
    }


def append_entries(text: str, records: list[dict[str, str]]) -> str:
    existing_count = len(re.findall(r"^\[\d+/\d+\]\s+.+$", text, re.MULTILINE))
    new_total = existing_count + len(records)
    updated = re.sub(r"Total projects:\s*\d+", f"Total projects: {new_total}", text)
    updated = re.sub(r"\[(\d+)/\d+\]", lambda match: f"[{match.group(1)}/{new_total}]", updated)

    entries: list[str] = []
    for offset, record in enumerate(records, start=1):
        index = existing_count + offset
        entry = (
            "======================================================================\n"
            f"[{index}/{new_total}] {record['name']}\n"
            f"TITLE: {record['title']}\n"
            f"TYPE: {record['type']}  |  ESTIMAND: {record['estimand']}\n"
            f"DATA: {record['data']}\n"
            f"PATH: {record['path']}\n\n"
            f"CURRENT BODY ({record['words']} words):\n"
            f"{record['body']}\n\n"
            "YOUR REWRITE (at most 156 words, 7 sentences):\n\n"
        )
        entries.append(entry)

    return updated.rstrip() + "\n\n" + "\n\n".join(entries) + "\n"


def main() -> None:
    if not WORKBOOK.exists():
        raise FileNotFoundError(f"Workbook not found: {WORKBOOK}")

    workbook_text = WORKBOOK.read_text(encoding="utf-8")
    known_paths = known_paths_from_workbook(workbook_text)

    new_records: list[dict[str, str]] = []
    for project_root in iter_candidate_projects():
        record = build_project_record(project_root)
        if not record:
            continue
        if normalize_windows_path(record["path"]) in known_paths:
            continue
        new_records.append(record)

    new_records.sort(key=lambda item: item["name"].lower())

    print(f"Existing workbook entries: {len(known_paths)}")
    print(f"New complete projects found: {len(new_records)}")
    for record in new_records:
        print(f"  + {record['path']}")

    if not new_records:
        print("Workbook already covers all complete projects.")
        return

    updated_text = append_entries(workbook_text, new_records)
    WORKBOOK.write_text(updated_text, encoding="utf-8")
    print(f"Workbook updated to {len(known_paths) + len(new_records)} total projects.")


if __name__ == "__main__":
    main()
