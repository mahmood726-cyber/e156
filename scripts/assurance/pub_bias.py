"""publication_bias check (advisory, opt-in per project).

A fifth, machine-derived assurance signal sourced from the **PubBiasSuite**
browser app (the ``pubbiassuite`` repo's ``pub-bias-suite.html``). PubBiasSuite runs
a 6+-method funnel-asymmetry / selection consensus (Egger, Begg, Peters,
PET-PEESE, Trim-Fill, 3PSM, p-curve, p-uniform*, WAAP-WLS, limit-MA) entirely
in client-side JavaScript and renders a 3-level Overall Verdict. Its engine is
NOT importable from Python, so this module does NOT re-derive the statistics
(re-implementing six estimators in Python would be a fresh correctness liability
— see advanced-stats.md). Instead it consumes PubBiasSuite's own output.

Opt-in: a capsule provides ONE of these in its repo root (produced once by
running the audited PubBiasSuite app on the capsule's effect/SE data):

  <repo>/pubbias.json          {"verdict": "<PubBiasSuite verdict text or
                                strong|some|little>"}   (preferred)
  <repo>/pubbias-verdict.txt    the raw #verdictText string, copy-pasted

Mapping (tier-gating: a 'warn' caps the badge at Bronze. publication bias is
informative, not a self-consistency failure, so it never emits 'fail' and so
never forces tier=none):

  "Strong evidence of publication bias"  -> warn  (label: strong)  caps Silver
  "Some evidence of publication bias"    -> warn  (label: some)    caps Silver
  "Little evidence of publication bias"  -> pass  (label: little)
  no artifact / unrecognised text        -> not-run

A selenium-gated headless extractor (`extract_verdict_headless`) is included
for a future fully-automated path: given the app HTML + a capsule's CSV it
loads the page, parses the data, clicks Run-All, and reads #verdictText. It is
NOT invoked by the assurance pipeline (keeps the pipeline browser-free and
dependency-free) and returns None when selenium/Chrome are unavailable.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# The three stable PubBiasSuite verdict literals (pub-bias-suite.html ~line
# 2149-2155). Matched as substrings so the trailing numeric detail is ignored.
_STRONG = "strong evidence of publication bias"
_SOME = "some evidence of publication bias"
_LITTLE = "little evidence of publication bias"

# Normalised single-word labels also accepted (so an author can write a short
# verdict instead of pasting the full sentence).
_WARN_LABELS = {"strong", "some", "moderate", "suspected", "confirmed"}
_PASS_LABELS = {"little", "low", "none", "clean", "robust"}

SIDECAR_JSON = "pubbias.json"
SIDECAR_TXT = "pubbias-verdict.txt"


def classify_verdict(text: str | None) -> tuple[str, str | None]:
    """Map a PubBiasSuite verdict string (or short label) to an assurance
    status. Returns (status, label) where status is one of
    pass | warn | not-run and label is strong|some|little|None.

    Pure and deterministic — the unit-tested core of this module.
    """
    if not text or not str(text).strip():
        return "not-run", None
    t = str(text).strip().lower()
    # Full-sentence verdicts first (most specific).
    if _STRONG in t:
        return "warn", "strong"
    if _SOME in t:
        return "warn", "some"
    if _LITTLE in t:
        return "pass", "little"
    # Short single-word labels.
    if t in _WARN_LABELS:
        return "warn", t
    if t in _PASS_LABELS:
        return "pass", t
    return "not-run", None


def _read_sidecar_verdict(repo: Path) -> str | None:
    """Return the verdict text from pubbias.json or pubbias-verdict.txt, or
    None if neither opt-in artifact is present/readable."""
    j = repo / SIDECAR_JSON
    if j.is_file():
        try:
            data = json.loads(j.read_text(encoding="utf-8"))
            v = data.get("verdict") if isinstance(data, dict) else None
            if v:
                return str(v)
        except (OSError, json.JSONDecodeError):
            pass
    txt = repo / SIDECAR_TXT
    if txt.is_file():
        try:
            s = txt.read_text(encoding="utf-8").strip()
            if s:
                return s
        except OSError:
            pass
    return None


def derive_pub_bias(local_path: Path | None) -> str:
    """Advisory publication_bias check. Returns pass | warn | not-run.

    not-run — no PubBiasSuite artifact in the repo root, or it can't be parsed
              into a recognised verdict.
    warn    — PubBiasSuite reported strong/some evidence of publication bias.
              (Tier-gating: caps the badge at Bronze.)
    pass    — PubBiasSuite reported little evidence of publication bias.

    Never returns 'fail': publication bias is informative, not a
    self-consistency failure, so it must not force tier=none.
    """
    if local_path is None or not local_path.is_dir():
        return "not-run"
    verdict = _read_sidecar_verdict(local_path)
    status, _label = classify_verdict(verdict)
    return status


# ---------------------------------------------------------------------------
# Future fully-automated path — selenium-gated, NOT called by the pipeline.
# ---------------------------------------------------------------------------

def selenium_available() -> bool:
    try:
        import selenium  # noqa: F401
        return True
    except ImportError:
        return False


def extract_verdict_headless(app_html: Path, csv_text: str, timeout: int = 60) -> str | None:
    """Load the PubBiasSuite app headless, feed it `csv_text` via #csvInput +
    #btnParseCsv, click #btnRunAll, and return the #verdictText string.

    Returns None if selenium/Chrome are unavailable or anything fails. Element
    IDs verified against pub-bias-suite.html: csvInput, btnParseCsv, btnRunAll,
    verdictText. This is the future auto-path; the assurance pipeline does not
    invoke it (it would put a browser in the default verify loop).
    """
    if not selenium_available() or not app_html.is_file():
        return None
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
    except ImportError:
        return None

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    driver = None
    try:
        driver = webdriver.Chrome(options=opts)
        driver.set_page_load_timeout(timeout)
        driver.get(app_html.resolve().as_uri())
        wait = WebDriverWait(driver, timeout)
        csv_el = wait.until(EC.presence_of_element_located((By.ID, "csvInput")))
        csv_el.clear()
        csv_el.send_keys(csv_text)
        driver.execute_script(
            "arguments[0].click()", driver.find_element(By.ID, "btnParseCsv"))
        driver.execute_script(
            "arguments[0].click()", driver.find_element(By.ID, "btnRunAll"))
        # The verdict lives on a tab panel that may be inactive (hidden) in
        # headless mode, so element.text returns ''. Read textContent via the
        # DOM, which is populated regardless of visibility.
        def _verdict(d):
            return (d.find_element(By.ID, "verdictText").get_attribute("textContent") or "")
        wait.until(lambda d: "evidence" in _verdict(d).lower())
        return _verdict(driver).strip()
    except Exception:
        return None
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: pub_bias.py <project_path>", file=sys.stderr)
        sys.exit(2)
    result = derive_pub_bias(Path(sys.argv[1]))
    print(result)
    sys.exit(0)
