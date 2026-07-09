#!/usr/bin/env python
"""
Deterministic verification for the v2 of View/40
(Inequities in clinical-trial distribution for neglected tropical diseases).

Recomputes, from the AACT April-12-2026 snapshot, the count of African-site trials
for NTDs (WHO-Roadmap classic African-endemic set) and the three comparators the
v1 used (HIV/AIDS, cancer, cardiovascular), plus the burden-adjusted NTD-vs-HIV
ratio that is the paper's valid core argument. Deterministic, read-only.

Definitions:
  African-site trial : >=1 facility in an African country (AU + territories).
  condition match    : conditions.downcase_name contains any group keyword.
  NTD (core)         : classic African-endemic NTDs; dengue/chikungunya/rabies/
                       snakebite are EXCLUDED from the core count (large, largely
                       non-African) and shown separately as an inclusive band.
"""
import os, re, sys

SNAP="2026-04-12"
CANDS=[os.environ.get("AACT_DIR",""),
       rf"F:\AACT-storage\AACT\{SNAP}", rf"C:\AACT-storage\AACT\{SNAP}"]
AACT=next((c for c in CANDS if c and os.path.isfile(os.path.join(c,"studies.txt"))),None)
if not AACT: sys.exit("FAIL-CLOSED: no AACT snapshot; set $AACT_DIR")

AFRICA={"Algeria","Angola","Benin","Botswana","Burkina Faso","Burundi","Cabo Verde",
 "Cameroon","Central African Republic","Chad","Comoros","Congo",
 "Congo, The Democratic Republic of the","Democratic Republic of the Congo",
 "Cote D'Ivoire","Côte D'Ivoire","Djibouti","Egypt","Equatorial Guinea","Eritrea",
 "Eswatini","Swaziland","Ethiopia","Gabon","Gambia","Ghana","Guinea","Guinea-Bissau",
 "Kenya","Lesotho","Liberia","Libya","Madagascar","Malawi","Mali","Mauritania",
 "Mauritius","Morocco","Mozambique","Namibia","Niger","Nigeria","Rwanda",
 "Sao Tome and Principe","Senegal","Seychelles","Sierra Leone","Somalia",
 "South Africa","South Sudan","Sudan","Tanzania","Togo","Tunisia","Uganda","Zambia",
 "Zimbabwe","Western Sahara","Réunion","Reunion","Mayotte"}

CHILD=re.compile(rb"^\d+\|NCT\d{8}\|"); F2=re.compile(rb"^\d+\|(NCT\d{8})\|")

def africa_ncts():
    s=set(); buf=None
    def flush(b):
        m=F2.match(b)
        if not m: return
        p=b.rstrip(b"\n").split(b"|")
        if len(p)>7 and p[7].strip().decode(errors="replace") in AFRICA:
            s.add(m.group(1).decode())
    with open(os.path.join(AACT,"facilities.txt"),"rb") as fh:
        fh.readline()
        for ln in fh:
            if CHILD.match(ln):
                if buf is not None: flush(buf)
                buf=ln
            elif buf is not None: buf+=ln
        if buf is not None: flush(buf)
    return s

def all_ncts():
    s=set()
    with open(os.path.join(AACT,"studies.txt"),"rb") as fh:
        fh.readline()
        for ln in fh:
            if re.match(rb"^NCT\d{8}\|",ln): s.add(ln[:11].decode())
    return s

GROUPS={
 # NOTE: "noma" removed as a bare keyword -- it is a substring of melaNOMA/
 # carciNOMA/lymphoma and false-matches thousands of cancer trials. "trachoma"
 # kept but excludes "trachomatis" (genital chlamydia) to avoid STI over-match.
 "ntd_core":(["schistosomiasis","bilharzia","lymphatic filariasis","filariasis",
   "onchocerciasis","river blindness","leishmaniasis","kala-azar","trypanosomiasis",
   "sleeping sickness","chagas","soil-transmitted helminth","ascariasis","hookworm",
   "trichuriasis","strongyloidiasis","leprosy","trachoma","buruli ulcer",
   "dracunculiasis","guinea worm","yaws","echinococcosis","cysticercosis",
   "taeniasis","scabies","mycetoma","podoconiosis","fascioliasis"],["trachomatis"]),
 "ntd_incl":(["schistosomiasis","bilharzia","lymphatic filariasis","filariasis",
   "onchocerciasis","river blindness","leishmaniasis","kala-azar","trypanosomiasis",
   "sleeping sickness","chagas","soil-transmitted helminth","ascariasis","hookworm",
   "trichuriasis","strongyloidiasis","leprosy","trachoma","buruli ulcer",
   "dracunculiasis","guinea worm","yaws","echinococcosis","cysticercosis","taeniasis",
   "scabies","mycetoma","podoconiosis","fascioliasis","dengue","chikungunya",
   "rabies","snakebite","snake bite","snake envenom"],["trachomatis"]),
 "hiv":(["hiv","human immunodeficiency virus","aids"],["hearing aids","band aids","aids-related lymphoma test"]),
 "cancer":(["cancer","carcinoma","neoplasm","tumor","tumour","malignan","sarcoma",
   "lymphoma","leukemia","leukaemia","melanoma","myeloma"],[]),
 "cvd":(["cardiovascular","coronary","myocardial","heart failure","hypertension",
   "stroke","atrial fibrillation","ischemic heart","ischaemic heart","angina"],[]),
}

def build_index(groups):
    kw={g:[k.encode() for k in inc] for g,(inc,exc) in groups.items()}
    ex={g:[k.encode() for k in exc] for g,(inc,exc) in groups.items()}
    hits={g:set() for g in groups}
    with open(os.path.join(AACT,"conditions.txt"),"rb") as fh:
        fh.readline()
        for ln in fh:
            m=F2.match(ln)
            if not m: continue
            parts=ln.rstrip(b"\n").split(b"|")
            if len(parts)<4: continue
            dn=parts[3].lower(); nct=m.group(1).decode()
            for g in groups:
                if any(e in dn for e in ex[g]): continue
                if any(k in dn for k in kw[g]): hits[g].add(nct)
    return hits

print("Loading African sites…", file=sys.stderr); afr=africa_ncts()
alln=all_ncts()
print("Indexing conditions…", file=sys.stderr); hits=build_index(GROUPS)

print("="*60)
print("NTD trial inequity — AACT verification |", AACT)
print("="*60)
print(f"African-site trials (denominator): {len(afr):,}  (v1 used 24,771)")
print("-"*60)
print(f"{'group':<12}{'africa':>9}{'% of African':>14}")
for g in GROUPS:
    a=len(hits[g]&afr)
    print(f"{g:<12}{a:>9,}{100.0*a/len(afr):>13.2f}%")

print("-"*60)
# burden-adjusted NTD-vs-HIV (paper's core argument), using African-site trials.
ntd=len(hits["ntd_core"]&afr); hiv=len(hits["hiv"]&afr)
# GBD 2019 African DALYs (order-of-magnitude, AS-CITED, flag for primary check):
#   these are illustrative; the paper's "~25% of NTD burden / 57M DALYs" is
#   global-scope and needs primary GBD verification -> reported AS-CITED only.
print("Burden-adjusted NTD-vs-HIV (trials per African-site count):")
print(f"  NTD-core African trials = {ntd};  HIV African trials = {hiv}")
print(f"  HIV:NTD trial ratio = {hiv/ntd:.1f}x  (HIV has ~{hiv/ntd:.0f}x more African trials)")
print("  NOTE: burden ratios (25% NTD burden; 57M DALYs) are v1 secondary-source")
print("  figures -> reported AS-CITED pending primary GBD 2019 table extraction.")
