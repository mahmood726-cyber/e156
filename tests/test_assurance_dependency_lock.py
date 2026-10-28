"""Fail-closed regression guard for the two E156 assurance dependency installs.

This is source-policy and mutation testing, not proof of a real signed release
or that a hosted runner successfully installed the selected wheels.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
LOCK = "requirements-assurance-ci.lock"
INSTALL = (
    "python -m pip install --force-reinstall --require-hashes "
    "--only-binary=:all: -r " + LOCK
)
WORKFLOWS = ("assurance-pr.yml", "assurance.yml")
# Deliberately repeated verified hashes: lock changes require reviewed test changes.
REQUIRED = (
    "pytest==9.1.1 --hash=sha256:37a86b45efb9a47a61a36449063e8e18d0cab3161329fc099eb21783169c4f0c",
    "iniconfig==2.3.1 --hash=sha256:9121e2c1fdb355232495be3194c8dfe87ccc2d5dee45947b78e68f499790d7a7",
    "packaging==26.3 --hash=sha256:d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c",
    "pluggy==1.7.0 --hash=sha256:7dd7b0d8832ba3cb632c306926ded123429211b83641b35dc5c41ad2d34f9bec",
    "pygments==2.21.0 --hash=sha256:2363c69b61c4a97c838da3b130dcd6468f4848992b21a82f2a63ec34377137d9",
    'colorama==0.4.6 ; sys_platform == "win32" --hash=sha256:4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6',
    "PyYAML==6.0.3 --hash=sha256:ba1cc08a7ccde2d2ec775841541641e4548226580ab850948cbfda66a1befcdc --hash=sha256:5fcd34e47f6e0b794d17de1b4ff496c00986e1c83f7ab2fb8fcfe9616ff7477b",
)


def lock_problems(source: str) -> list[str]:
    lines = tuple(line.strip() for line in source.splitlines()
                  if line.strip() and not line.lstrip().startswith("#"))
    return [] if lines == REQUIRED else ["assurance dependency lock changed outside reviewed wheel inventory"]


def install_problems(source: str) -> list[str]:
    try:
        data = yaml.safe_load(source)
    except yaml.YAMLError as exc:
        return [f"malformed workflow: {exc}"]
    jobs = data.get("jobs") if isinstance(data, dict) else None
    if not isinstance(jobs, dict) or len(jobs) != 1:
        return ["unexpected assurance job inventory"]
    job = next(iter(jobs.values()))
    if not isinstance(job, dict) or not isinstance(job.get("steps"), list):
        return ["missing assurance job steps"]
    installs: list[str] = []
    for step in job["steps"]:
        if not isinstance(step, dict):
            return ["malformed assurance step"]
        run = step.get("run")
        if not isinstance(run, str):
            continue
        # Normalize whitespace, not shell syntax: only the exact reviewed
        # one-line command is accepted as the unique pip-install step.
        if re.search(r"\bpip\s+install\b", run):
            installs.append(" ".join(run.split()))
    return [] if installs == [INSTALL] else ["unlocked, additional or missing assurance pip install"]


def test_assurance_lock_matches_reviewed_wheel_hashes():
    source = (ROOT / LOCK).read_text(encoding="utf-8")
    assert lock_problems(source) == []


@pytest.mark.parametrize("filename", WORKFLOWS)
def test_both_assurance_jobs_install_reviewed_hash_locked_wheels(filename):
    source = (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
    assert install_problems(source) == []


@pytest.mark.parametrize("filename", WORKFLOWS)
def test_lock_bypass_and_additional_install_are_refused(filename):
    source = (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
    assert source.count(INSTALL) == 1
    for weakened in (
        source.replace("--require-hashes ", ""),
        source.replace("--only-binary=:all: ", ""),
        source.replace("--force-reinstall ", ""),
        source.replace(LOCK, "requirements-unreviewed.txt"),
        source.replace(INSTALL, INSTALL + " && python -m pip install anotherpkg"),
        source.replace(INSTALL, "python -m pip install pytest==9.1.1 PyYAML==6.0.3"),
    ):
        assert weakened != source
        assert install_problems(weakened), "weakened workflow install was accepted"


def test_missing_or_tampered_lock_entries_are_refused():
    source = (ROOT / LOCK).read_text(encoding="utf-8")
    for line in REQUIRED:
        assert line in source
        assert lock_problems(source.replace(line, "", 1))
        assert lock_problems(source.replace(line, line.replace("sha256:", "sha256:0", 1), 1))
    assert lock_problems(source + "unreviewed==1.0 --hash=sha256:" + "0" * 64 + "\n")
