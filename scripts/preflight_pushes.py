"""Pre-flight the 94 push targets before we touch `gh repo create`.

For each target in resolution_plan.json push_from_local:
  - Confirm source_path still on disk
  - Check existing .git state (init/no-init, existing remote)
  - Estimate total bytes (warn for > 500 MB, likely needs LFS or split)
  - Count files (warn for > 5000, likely a build artifact graveyard)
  - Look for .gitignore recommendations (node_modules/, __pycache__/, *.pyc)

Writes audit_output/push_plan.json with per-target status.
"""
from __future__ import annotations
import json
import subprocess
from pathlib import Path

E156 = Path(__file__).resolve().parents[1]
PLAN_IN = E156 / "audit_output" / "resolution_plan.json"
PLAN_OUT = E156 / "audit_output" / "push_plan.json"

MAX_BYTES_WARN = 500 * 1024 * 1024  # 500 MB
MAX_FILES_WARN = 5000


def git_state(path: Path) -> dict:
    git_dir = path / ".git"
    info: dict = {"has_git": git_dir.is_dir()}
    if not info["has_git"]:
        return info
    try:
        out = subprocess.check_output(
            ["git", "-C", str(path), "remote", "-v"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
        info["remotes"] = out.splitlines() if out else []
    except subprocess.CalledProcessError:
        info["remotes"] = []
    try:
        out = subprocess.check_output(
            ["git", "-C", str(path), "branch", "--show-current"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
        info["branch"] = out or None
    except subprocess.CalledProcessError:
        info["branch"] = None
    try:
        out = subprocess.check_output(
            ["git", "-C", str(path), "log", "-1", "--oneline"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
        info["has_commits"] = bool(out)
        info["last_commit"] = out
    except subprocess.CalledProcessError:
        info["has_commits"] = False
        info["last_commit"] = None
    return info


def dir_stats(path: Path) -> dict:
    total_bytes = 0
    files = 0
    big_dirs = {"node_modules": 0, "__pycache__": 0, ".venv": 0, "dist": 0, "build": 0}
    try:
        for sub in path.rglob("*"):
            parts = sub.parts
            if ".git" in parts:
                continue
            for bd in big_dirs:
                if bd in parts:
                    big_dirs[bd] += 1
                    break
            if sub.is_file():
                files += 1
                try:
                    total_bytes += sub.stat().st_size
                except OSError:
                    pass
    except (PermissionError, OSError) as e:
        return {
            "error": str(e),
            "files": files,
            "bytes": total_bytes,
            "mb": round(total_bytes / (1024 * 1024), 1),
            "noise_dirs": {k: v for k, v in big_dirs.items() if v > 0},
        }
    return {
        "files": files,
        "bytes": total_bytes,
        "mb": round(total_bytes / (1024 * 1024), 1),
        "noise_dirs": {k: v for k, v in big_dirs.items() if v > 0},
    }


def main() -> int:
    plan = json.loads(PLAN_IN.read_text(encoding="utf-8"))
    out = []
    warnings = 0
    for g in plan["push_from_local"]:
        source = Path(g["source_path"])
        rec = {
            "target_repo": g["target_repo"],
            "entry_nums": g["entry_nums"],
            "source_path": str(source),
        }
        if not source.is_dir():
            rec["preflight"] = "FAIL_source_missing"
            warnings += 1
            out.append(rec)
            continue
        rec["git"] = git_state(source)
        rec["stats"] = dir_stats(source)
        flags = []
        if rec["git"]["has_git"] and rec["git"].get("remotes"):
            flags.append("has_remote_already")
        if rec["git"]["has_git"] and not rec["git"].get("has_commits"):
            flags.append("git_init_no_commits")
        if rec["stats"].get("bytes", 0) > MAX_BYTES_WARN:
            flags.append(f"big_dir_{rec['stats']['mb']}MB")
        if rec["stats"].get("files", 0) > MAX_FILES_WARN:
            flags.append(f"many_files_{rec['stats']['files']}")
        if rec["stats"].get("noise_dirs"):
            flags.append("noise_dirs_present")
        rec["flags"] = flags
        rec["preflight"] = "OK" if not flags else "REVIEW"
        if flags:
            warnings += 1
        out.append(rec)

    summary = {
        "total": len(out),
        "ok": sum(1 for r in out if r["preflight"] == "OK"),
        "review": sum(1 for r in out if r["preflight"] == "REVIEW"),
        "fail": sum(1 for r in out if r["preflight"].startswith("FAIL")),
    }
    PLAN_OUT.write_text(
        json.dumps({"summary": summary, "targets": out}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {PLAN_OUT}")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
