"""Track 3 — remap the 17 Finrenone-cluster papers to per-therapy dashboards.

The 17 papers all point at `https://mahmood726-cyber.github.io/finrenone/`
(generic). The repo `rapidmeta-finerenone` actually contains per-therapy
HTML dashboards like SGLT2_HF_REVIEW.html, PCSK9_REVIEW.html, etc. This
script rewrites each paper's Dashboard URL in the workbook to its specific
per-therapy HTML file.

Mapping (paper num -> therapy review file):
  #57   Finerenone             -> FINERENONE_REVIEW.html
  #415  FinerenoneLivingMA     -> FINERENONE_REVIEW.html
  #416  GLP1CVOT               -> GLP1_CVOT_REVIEW.html
  #417  SGLT2HF                -> SGLT2_HF_REVIEW.html
  #418  SGLT2CKD               -> SGLT2_CKD_REVIEW.html
  #419  BempedoicAcid          -> BEMPEDOIC_ACID_REVIEW.html
  #420  PCSK9                  -> PCSK9_REVIEW.html
  #421  IVIronHF               -> IV_IRON_HF_REVIEW.html
  #422  AblationAF             -> ABLATION_AF_REVIEW.html
  #423  RivaroxabanVasc        -> RIVAROXABAN_VASC_REVIEW.html
  #424  ColchicineCVD          -> COLCHICINE_CVD_REVIEW.html
  #425  SotaterceptPAH         -> (no match — keep generic, flag)
  #430  LipidHub               -> LIPID_HUB_REVIEW.html
  #439  MavacamtenHCM          -> MAVACAMTEN_HCM_REVIEW.html
  #441  IntensiveBP            -> INTENSIVE_BP_REVIEW.html
  #442  IncretinHFpEF          -> INCRETIN_HFpEF_REVIEW.html
  #443  DOACCancerVTE          -> DOAC_CANCER_VTE_REVIEW.html

Writes audit_output/dashboard_remap_log.json.
"""
from __future__ import annotations
import io
import json
import re
import shutil
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
WORKBOOK_BAK = E156 / "rewrite-workbook.txt.bak.phase-c"
LOG = E156 / "audit_output" / "dashboard_remap_log.json"

SEP = "=" * 70
ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)

# {paper_num: review_html_filename}
FINRENONE_MAP = {
    57:  "FINERENONE_REVIEW.html",
    415: "FINERENONE_REVIEW.html",
    416: "GLP1_CVOT_REVIEW.html",
    417: "SGLT2_HF_REVIEW.html",
    418: "SGLT2_CKD_REVIEW.html",
    419: "BEMPEDOIC_ACID_REVIEW.html",
    420: "PCSK9_REVIEW.html",
    421: "IV_IRON_HF_REVIEW.html",
    422: "ABLATION_AF_REVIEW.html",
    423: "RIVAROXABAN_VASC_REVIEW.html",
    424: "COLCHICINE_CVD_REVIEW.html",
    # 425 no match — left out, keep current URL, flag in log
    430: "LIPID_HUB_REVIEW.html",
    439: "MAVACAMTEN_HCM_REVIEW.html",
    441: "INTENSIVE_BP_REVIEW.html",
    442: "INCRETIN_HFpEF_REVIEW.html",
    443: "DOAC_CANCER_VTE_REVIEW.html",
}

BASE_NEW = "https://mahmood726-cyber.github.io/rapidmeta-finerenone"


def main() -> int:
    shutil.copy2(WORKBOOK, WORKBOOK_BAK)
    text = WORKBOOK.read_text(encoding="utf-8")
    blocks = text.split(SEP)

    # num -> first block index
    block_of: dict[int, int] = {}
    for idx, block in enumerate(blocks):
        m = ENTRY_HEAD_RE.search(block)
        if m:
            num = int(m.group(1))
            if num not in block_of:
                block_of[num] = idx

    log = {"remaps": [], "flagged_no_match": []}
    for num, filename in FINRENONE_MAP.items():
        if num not in block_of:
            log["flagged_no_match"].append({"num": num, "reason": "block_not_found"})
            continue
        idx = block_of[num]
        block = blocks[idx]
        # Match any existing Dashboard URL and replace it
        dashboard_re = re.compile(r"(Dashboard:\s+)(\S+)")
        m = dashboard_re.search(block)
        if not m:
            log["flagged_no_match"].append({"num": num, "reason": "no_dashboard_line"})
            continue
        old_url = m.group(2)
        new_url = f"{BASE_NEW}/{filename}"
        if old_url == new_url:
            log["remaps"].append({"num": num, "status": "already_correct", "url": new_url})
            continue
        new_block = dashboard_re.sub(lambda m0: m0.group(1) + new_url, block, count=1)
        blocks[idx] = new_block
        log["remaps"].append({
            "num": num, "status": "remapped",
            "from": old_url, "to": new_url,
        })

    # Flag unmapped entries from the Finrenone cluster
    for num in (425,):
        log["flagged_no_match"].append({
            "num": num,
            "reason": "no review HTML for SotaterceptPAH in rapidmeta-finerenone — "
                      "dashboard URL left as-is; build a SOTATERCEPT_PAH_REVIEW.html "
                      "in rapidmeta-finerenone and add to FINRENONE_MAP",
        })

    WORKBOOK.write_text(SEP.join(blocks), encoding="utf-8")
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Remapped: {sum(1 for r in log['remaps'] if r.get('status') == 'remapped')}")
    print(f"Already correct: {sum(1 for r in log['remaps'] if r.get('status') == 'already_correct')}")
    print(f"Flagged (no match): {len(log['flagged_no_match'])}")
    print(f"Workbook backup: {WORKBOOK_BAK}")
    print(f"Log: {LOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
