"""Phase-3 S: analysis_rerun check (Gold-tier enabler, opt-in per project).

Each project can opt into the analysis-rerun check by dropping two files
in its repo root:

  <project>/rerun.sh                    — the script to execute
  <project>/rerun.baseline.sha256       — expected sha256 of rerun stdout

When `derive_analysis_rerun()` is called for that project, it:
  1. Runs `bash rerun.sh` with a 600 s timeout.
  2. Hashes the stdout (sha256).
  3. Compares to the contents of rerun.baseline.sha256 (whitespace-stripped).
  4. Returns `pass | warn | fail | not-run`.

The project then satisfies one of the Gold-tier preconditions (the other
is `external_review`, which is still manual).

Phase 3 status: shipped + wired into build_assurance_jsons.py. No project
currently has the opt-in files — the check returns `not-run` for all 1700+
entries until operators start writing them. Adding the files is the
documented Gold-tier upgrade path.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


RERUN_SCRIPT_NAME = "rerun.sh"
BASELINE_SHA_NAME = "rerun.baseline.sha256"
TIMEOUT_SECONDS = 600


def derive_analysis_rerun(local_path: Path | None) -> str:
    """Returns one of: pass | warn | fail | not-run.

    not-run  — no rerun.sh in the project root
    pass     — rerun.sh exits 0 AND stdout sha256 matches baseline
    warn     — rerun.sh exits 0 but stdout sha256 differs from baseline
               (or no baseline file present yet)
    fail     — rerun.sh exits non-zero, or times out, or can't be invoked
    """
    if local_path is None or not local_path.is_dir():
        return "not-run"
    script = local_path / RERUN_SCRIPT_NAME
    if not script.is_file():
        return "not-run"

    # Pick a bash shell. On Windows, use Git for Windows' bash; on POSIX, plain bash.
    bash = "bash"
    if sys.platform == "win32":
        candidates = [
            r"C:\Program Files\Git\bin\bash.exe",
            r"C:\Program Files\Git\usr\bin\bash.exe",
        ]
        for c in candidates:
            if Path(c).is_file():
                bash = c
                break

    try:
        proc = subprocess.run(
            [bash, str(script)],
            cwd=str(local_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_SECONDS,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return "fail"

    if proc.returncode != 0:
        return "fail"

    stdout = proc.stdout or ""
    actual_sha = hashlib.sha256(stdout.encode("utf-8", errors="replace")).hexdigest()

    baseline_file = local_path / BASELINE_SHA_NAME
    if not baseline_file.is_file():
        # Successful run but no recorded baseline — operator hasn't
        # locked the expected output yet. WARN so they know to write it.
        return "warn"
    try:
        expected = baseline_file.read_text(encoding="utf-8").strip().lower()
    except OSError:
        return "warn"

    return "pass" if actual_sha.lower() == expected else "warn"


if __name__ == "__main__":
    # CLI: python rerun_analysis.py <project_path>
    if len(sys.argv) < 2:
        print("usage: rerun_analysis.py <project_path>", file=sys.stderr)
        sys.exit(2)
    result = derive_analysis_rerun(Path(sys.argv[1]))
    print(result)
    sys.exit(0 if result == "pass" else 1)
