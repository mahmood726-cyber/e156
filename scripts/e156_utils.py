"""Shared utilities for E156 scripts — scanning, path validation, constants."""

from pathlib import Path

WINDOWS_ALLOWED_ROOTS = [
    r"C:\Models", r"C:\Projects", r"C:\HTML apps", r"C:\E156",
    r"C:\Users\user",
    r"C:\AfricaRCT", r"C:\mahmood726-cyber.github.io",
    r"C:\FragilityAtlas", r"C:\AlMizan", r"C:\AdaptSim", r"C:\BiasForensics",
    r"C:\RMSTmeta", r"C:\ubcma", r"C:\BenfordMA", r"C:\MetaShift",
    r"C:\EvidenceHalfLife", r"C:\EvidenceQuality", r"C:\OutcomeReportingBias",
    r"C:\OverlapDetector", r"C:\PredictionGap", r"C:\MetaFolio",
    r"C:\MetaAudit", r"C:\MetaReproducer", r"C:\CausalSynth",
]


def windows_to_wsl(root: str) -> str:
    drive = root[0].lower()
    suffix = root[2:].replace("\\", "/")
    return f"/mnt/{drive}{suffix}"


ALLOWED_ROOTS = WINDOWS_ALLOWED_ROOTS + [windows_to_wsl(root) for root in WINDOWS_ALLOWED_ROOTS]
REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_RELEASES_ROOT = REPO_ROOT / "releases"

SYSTEM_DIRS = frozenset({
    "Windows", "Program Files", "Program Files (x86)", "ProgramData",
    "Users", "$Recycle.Bin", "System Volume Information", "Recovery",
    "PerfLogs", "Intel", "AMD", "Boot", "Drivers", "msys64", "cygwin64",
})


def find_all_submissions():
    """Find all e156-submission directories on C: drive."""
    submissions = []
    drive_roots = [Path("C:/"), Path("/mnt/c")]
    container_roots = [
        Path("C:/Models"),
        Path("C:/Projects"),
        Path("C:/HTML apps"),
        Path("C:/Users/user"),
        Path("/mnt/c/Models"),
        Path("/mnt/c/Projects"),
        Path("/mnt/c/HTML apps"),
        Path("/mnt/c/Users/user"),
    ]

    # Root-level project dirs
    for root in drive_roots:
        if not root.is_dir():
            continue
        for d in root.iterdir():
            try:
                is_dir = d.is_dir()
            except OSError:
                continue
            if not is_dir or d.name in SYSTEM_DIRS:
                continue
            sub = d / "e156-submission"
            try:
                is_submission = sub.is_dir()
            except OSError:
                continue
            if is_submission:
                submissions.append(sub)

    # Recurse into container dirs
    for root in container_roots:
        if root.is_dir():
            for d in root.glob("*/e156-submission"):
                if d.is_dir():
                    submissions.append(d)

    if LOCAL_RELEASES_ROOT.is_dir():
        for d in LOCAL_RELEASES_ROOT.glob("*/e156-submission"):
            if d.is_dir():
                submissions.append(d)

    return sorted(set(submissions))


def validate_path(project_path):
    """Check that a project path is within allowed roots."""
    resolved = str(Path(project_path).resolve())
    return any(resolved.startswith(r) for r in ALLOWED_ROOTS)
