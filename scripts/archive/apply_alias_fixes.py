"""Phase A: apply workbook URL alias fixes (no GitHub calls).

For each alias target in audit_output/push_plan.json (has_remote_already):
  - Parse the local dir's git remote to get the *actual* GitHub repo name.
  - If owner != mahmood726-cyber, defer — this is someone else's clone.
  - Otherwise, in the workbook rewrite Code: and Protocol: URLs from
    mahmood726-cyber/<workbook_name> → mahmood726-cyber/<actual_name>
    across every entry num that points at this target.

Also un-hide entries resolved by audit_output/resolution_plan.json's
exists_on_github list (e.g. #339 Fatiha-Course).

Updates:
  - rewrite-workbook.txt
  - audit_output/hide_repo_404.json  (removes fixed entry nums)
  - audit_output/alias_fix_log.json  (per-target audit trail)
  - audit_output/repo_404_triage_deferred.json  (cross-owner + local_missing)
"""
from __future__ import annotations
import json
import re
import shutil
import subprocess
import sys
import io
from pathlib import Path

# Ensure UTF-8 stdout on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
WORKBOOK_BAK = E156 / "rewrite-workbook.txt.bak.phase-a"
PLAN = E156 / "audit_output" / "resolution_plan.json"
PUSH_PLAN = E156 / "audit_output" / "push_plan.json"
HIDE_LIST = E156 / "audit_output" / "hide_repo_404.json"
LOG_OUT = E156 / "audit_output" / "alias_fix_log.json"
DEFER_OUT = E156 / "audit_output" / "repo_404_triage_deferred.json"

GITHUB_USER = "mahmood726-cyber"
SEP = "=" * 70
ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)

# Remote URL parser: accepts both https and ssh forms
REMOTE_RE = re.compile(
    r"(?:https://github\.com/|git@github\.com:)([^/]+)/([^/\s]+?)(?:\.git)?\s"
)


def parse_remote(remotes: list[str]) -> tuple[str | None, str | None]:
    for line in remotes:
        if "(fetch)" not in line:
            continue
        m = REMOTE_RE.search(line + " ")
        if m:
            return m.group(1), m.group(2)
    return None, None


def main() -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    push_plan = json.loads(PUSH_PLAN.read_text(encoding="utf-8"))

    hide_nums = set(json.loads(HIDE_LIST.read_text(encoding="utf-8")))
    original_hidden = len(hide_nums)

    # Build num → target map from resolution plan
    num_to_target: dict[int, str] = {}
    for g in plan["push_from_local"]:
        for n in g["entry_nums"]:
            num_to_target[n] = g["target_repo"]

    alias_apply: list[dict] = []
    cross_owner_defer: list[dict] = []

    for t in push_plan["targets"]:
        if "has_remote_already" not in t.get("flags", []):
            continue
        owner, actual = parse_remote(t["git"].get("remotes", []))
        if owner is None:
            cross_owner_defer.append({
                "target": t["target_repo"],
                "entry_nums": t["entry_nums"],
                "reason": "unparsable_remote",
                "remotes": t["git"].get("remotes"),
            })
            continue
        if owner != GITHUB_USER:
            cross_owner_defer.append({
                "target": t["target_repo"],
                "entry_nums": t["entry_nums"],
                "reason": f"remote_owner_is_{owner}",
                "remotes": t["git"].get("remotes"),
            })
            continue
        # Same owner, different name → alias fix
        alias_apply.append({
            "workbook_name": t["target_repo"],
            "actual_name": actual,
            "entry_nums": t["entry_nums"],
        })

    # Backup workbook once before any edits
    shutil.copy2(WORKBOOK, WORKBOOK_BAK)
    text = WORKBOOK.read_text(encoding="utf-8")

    # Apply fixes ONE ENTRY AT A TIME (scope replacement to that entry's block)
    blocks = text.split(SEP)
    num_fixes_applied = 0
    per_entry_log = []

    # Build a map num → set of (old_name, new_name) replacements to apply
    entry_fixes: dict[int, tuple[str, str]] = {}
    for a in alias_apply:
        for n in a["entry_nums"]:
            entry_fixes[n] = (a["workbook_name"], a["actual_name"])

    # Pre-compute which entry num is in which block (first occurrence wins)
    block_of: dict[int, int] = {}
    for idx, block in enumerate(blocks):
        m = ENTRY_HEAD_RE.search(block)
        if m:
            num = int(m.group(1))
            if num not in block_of:
                block_of[num] = idx

    for num, (old_name, new_name) in entry_fixes.items():
        if num not in block_of:
            per_entry_log.append({"num": num, "status": "block_not_found"})
            continue
        idx = block_of[num]
        block = blocks[idx]
        # Only rewrite the `Code:` and `Protocol:` URL lines. Leave
        # `Dashboard:` alone — it uses lowercase formatting and may point
        # to a correctly-enabled Pages site under the old slug. If Pages
        # is broken after the rename, the next audit will catch it.
        old_code = f"Code:      https://github.com/{GITHUB_USER}/{old_name}"
        new_code = f"Code:      https://github.com/{GITHUB_USER}/{new_name}"
        old_proto = f"Protocol:  https://github.com/{GITHUB_USER}/{old_name}/"
        new_proto = f"Protocol:  https://github.com/{GITHUB_USER}/{new_name}/"

        code_hit = block.count(old_code)
        proto_hit = block.count(old_proto)
        if code_hit == 0 and proto_hit == 0:
            per_entry_log.append({
                "num": num, "status": "no_match",
                "expected": old_code,
            })
            continue
        block = block.replace(old_code, new_code)
        block = block.replace(old_proto, new_proto)
        blocks[idx] = block
        num_fixes_applied += 1
        per_entry_log.append({
            "num": num, "status": "patched",
            "from": old_name, "to": new_name,
            "code_hits": code_hit, "proto_hits": proto_hit,
        })

    # Also un-hide the `exists_on_github` entries (audit was stale)
    exists_unhidden = []
    for g in plan["exists_on_github"]:
        for n in g["entry_nums"]:
            if n in hide_nums:
                hide_nums.discard(n)
                exists_unhidden.append({"num": n, "target": g["target_repo"]})

    # Un-hide all successfully patched alias entries
    alias_unhidden = []
    for entry in per_entry_log:
        if entry["status"] == "patched" and entry["num"] in hide_nums:
            hide_nums.discard(entry["num"])
            alias_unhidden.append(entry["num"])

    # Write updated workbook
    new_text = SEP.join(blocks)
    if new_text != text:
        WORKBOOK.write_text(new_text, encoding="utf-8")

    # Write updated hide list
    new_hide = sorted(hide_nums)
    HIDE_LIST.write_text(json.dumps(new_hide) + "\n", encoding="utf-8")

    # Write deferred list (cross-owner + local_missing from resolution plan)
    deferred = {
        "generated_by": "apply_alias_fixes.py",
        "cross_owner_aliases": cross_owner_defer,
        "local_missing": plan["local_missing"],
        "heavy_dirs_deferred_for_size_review": [],  # populated in Phase B
    }
    DEFER_OUT.write_text(
        json.dumps(deferred, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Write log
    log = {
        "alias_apply": alias_apply,
        "cross_owner_defer": cross_owner_defer,
        "entries_patched": num_fixes_applied,
        "alias_entries_unhidden": len(alias_unhidden),
        "exists_entries_unhidden": len(exists_unhidden),
        "hidden_before": original_hidden,
        "hidden_after": len(new_hide),
        "per_entry_log": per_entry_log,
        "exists_unhidden": exists_unhidden,
    }
    LOG_OUT.write_text(
        json.dumps(log, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Workbook backup: {WORKBOOK_BAK}")
    print(f"Aliases applied:          {len(alias_apply)} targets")
    print(f"  → Entries patched:      {num_fixes_applied}")
    print(f"  → Alias un-hidden:      {len(alias_unhidden)}")
    print(f"Cross-owner deferred:     {len(cross_owner_defer)} targets")
    print(f"Exists-on-GH un-hidden:   {len(exists_unhidden)}")
    print(f"Hide list: {original_hidden} -> {len(new_hide)} ({original_hidden - len(new_hide)} un-hidden)")
    no_match = [e for e in per_entry_log if e["status"] == "no_match"]
    if no_match:
        print(f"\nWARNING: {len(no_match)} entries had no Code-URL match (listed in log):")
        for e in no_match[:10]:
            print(f"  #{e['num']}: expected '{e['expected']}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
