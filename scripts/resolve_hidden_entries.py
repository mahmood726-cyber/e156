"""Resolve the 121 hidden entries by grouping on workbook Code: URL target.

For each num in audit_output/hide_repo_404.json:
  - Parse its workbook block
  - Extract Code URL (the authoritative GitHub target)
  - Extract PATH (the local source dir)

Then:
  - Group entries by target repo name
  - Cross-check each unique target against `gh repo list` (authoritative
    GitHub state right now — audit JSON may be stale)
  - Classify each target:
      exists_on_github   : URL-case / stale-audit — fix hide list only
      push_from_local    : local dir exists with files — push to create repo
      local_missing      : PATH unresolvable — stay hidden (deferred)
      workbook_no_code   : entry has no Code URL — stay hidden (deferred)

Writes audit_output/resolution_plan.json with the grouped plan.
"""
from __future__ import annotations
import json
import re
import subprocess
from pathlib import Path

E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
HIDE_LIST = E156 / "audit_output" / "hide_repo_404.json"
OUT = E156 / "audit_output" / "resolution_plan.json"

GITHUB_USER = "mahmood726-cyber"
ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)
SEP = "=" * 70


def parse_entry(block: str, num: int) -> dict | None:
    m = ENTRY_HEAD_RE.search(block)
    if not m or int(m.group(1)) != num:
        return None
    entry = {"num": num, "name": m.group(2).strip()}
    for line in block.splitlines():
        if line.startswith("PATH:"):
            entry["path"] = line[5:].strip()
    code_m = re.search(r"Code:\s+(\S+)", block)
    if code_m:
        entry["code_url"] = code_m.group(1)
        tail = code_m.group(1).rstrip("/").split("/")[-1]
        entry["target_repo"] = tail if tail else None
    return entry


def list_github_repos() -> set[str]:
    """Return lowercase set of repo names owned by GITHUB_USER.

    GitHub repo names are case-INSENSITIVE — compare lowercase.
    """
    out = subprocess.check_output(
        ["gh", "repo", "list", GITHUB_USER, "--limit", "500", "--json", "name"],
        text=True,
    )
    return {r["name"].lower() for r in json.loads(out)}


def local_dir_has_code(path_str: str) -> tuple[bool, int]:
    """Return (exists_and_nonempty, file_count_excluding_git)."""
    if not path_str:
        return (False, 0)
    p = Path(path_str)
    if not p.is_dir():
        return (False, 0)
    n = 0
    for sub in p.rglob("*"):
        if ".git" in sub.parts:
            continue
        if sub.is_file():
            n += 1
            if n > 5:
                return (True, n)
    return (n > 0, n)


def main() -> int:
    hide_nums = sorted(json.loads(HIDE_LIST.read_text(encoding="utf-8")))
    text = WORKBOOK.read_text(encoding="utf-8")
    blocks = text.split(SEP)

    # Map num → block(s). Some nums appear more than once in the workbook
    # (verified: #339 has a duplicate header). Keep the FIRST occurrence
    # only — that matches build_students_page.parse_entries behavior.
    num_to_entry: dict[int, dict] = {}
    for block in blocks:
        m = ENTRY_HEAD_RE.search(block)
        if not m:
            continue
        num = int(m.group(1))
        if num not in hide_nums or num in num_to_entry:
            continue
        parsed = parse_entry(block, num)
        if parsed:
            num_to_entry[num] = parsed

    missing_from_workbook = [n for n in hide_nums if n not in num_to_entry]

    # Group by target repo
    by_target: dict[str, list[dict]] = {}
    no_code: list[dict] = []
    for num, e in num_to_entry.items():
        target = e.get("target_repo")
        if not target:
            no_code.append(e)
            continue
        by_target.setdefault(target, []).append(e)

    # Check existence on GitHub
    gh_names = list_github_repos()

    exists: list[dict] = []
    push_needed: list[dict] = []
    local_missing: list[dict] = []

    for target, entries in sorted(by_target.items()):
        group = {
            "target_repo": target,
            "target_url": f"https://github.com/{GITHUB_USER}/{target}",
            "entry_nums": sorted(e["num"] for e in entries),
            "entry_names": [e["name"] for e in entries],
            "local_paths": sorted({e.get("path", "") for e in entries}),
        }
        if target.lower() in gh_names:
            # Repo exists on GitHub — the audit's 404 was wrong or stale.
            # Students would see a live repo. Just un-hide these entries.
            group["action"] = "unhide_only"
            exists.append(group)
            continue

        # Pick a local source dir. Prefer the first PATH that resolves.
        source_path = None
        file_count = 0
        for p in group["local_paths"]:
            ok, n = local_dir_has_code(p)
            if ok:
                source_path = p
                file_count = n
                break
        if source_path:
            group["action"] = "push_from_local"
            group["source_path"] = source_path
            group["file_count"] = file_count
            push_needed.append(group)
        else:
            group["action"] = "local_missing"
            group["checked_paths"] = group["local_paths"]
            local_missing.append(group)

    plan = {
        "generated": str(Path(__file__).name),
        "hide_list_total": len(hide_nums),
        "missing_from_workbook": missing_from_workbook,
        "no_code_url_entries": no_code,
        "summary": {
            "unique_targets": len(by_target),
            "exists_on_github": len(exists),
            "push_from_local": len(push_needed),
            "local_missing": len(local_missing),
            "no_code_url": len(no_code),
            "entries_covered_by_exists": sum(len(g["entry_nums"]) for g in exists),
            "entries_covered_by_push": sum(len(g["entry_nums"]) for g in push_needed),
            "entries_covered_by_local_missing": sum(len(g["entry_nums"]) for g in local_missing),
        },
        "exists_on_github": exists,
        "push_from_local": push_needed,
        "local_missing": local_missing,
    }

    OUT.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(json.dumps(plan["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
