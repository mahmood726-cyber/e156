#!/usr/bin/env python
"""
Reusable deterministic analysis for the Synthesis Africa-equity papers
(View IDs 40, 49, 53, 54, 55, 57, 61, 70, 78, 82, ...).

For each disease keyword group it reports, from the raw AACT April-12-2026
snapshot (no sampling):
  - global trials whose condition matches (distinct nct_id)
  - trials with at least one site in an African country (AU + territories)
  - African share (%)
  - interventional-only counterparts
Plus registry-wide context: total trials, total interventional, total with an
African site, and the African share of the whole registry.

Definitions (exact):
  African-site trial : >=1 row in facilities with country in AFRICA (54 AU
                       member states + Western Sahara).
  condition match    : conditions.downcase_name contains ANY keyword in the
                       group (case-insensitive substring), OR is excluded if it
                       matches an exclusion keyword.
  interventional     : studies.study_type == INTERVENTIONAL.

Deterministic, read-only, ~30 s. AACT root from $AACT_DIR or discovered; fail-closed.
"""
import os, re, sys
from collections import defaultdict

SNAP="2026-04-12"
CANDS=[os.environ.get("AACT_DIR",""),
       rf"F:\AACT-storage\AACT\{SNAP}", rf"C:\AACT-storage\AACT\{SNAP}",
       rf"D:\AACT-storage\AACT\{SNAP}", f"/f/AACT-storage/AACT/{SNAP}"]
AACT=next((c for c in CANDS if c and os.path.isfile(os.path.join(c,"studies.txt"))),None)
if not AACT: sys.exit("FAIL-CLOSED: no AACT snapshot; set $AACT_DIR")

AFRICA={  # AACT facilities.country spellings
 "Algeria","Angola","Benin","Botswana","Burkina Faso","Burundi","Cabo Verde",
 "Cameroon","Central African Republic","Chad","Comoros","Congo",
 "Congo, The Democratic Republic of the","Democratic Republic of the Congo",
 "Cote D'Ivoire","Côte D'Ivoire","Djibouti","Egypt","Equatorial Guinea",
 "Eritrea","Eswatini","Swaziland","Ethiopia","Gabon","Gambia","Ghana","Guinea",
 "Guinea-Bissau","Kenya","Lesotho","Liberia","Libya","Madagascar","Malawi",
 "Mali","Mauritania","Mauritius","Morocco","Mozambique","Namibia","Niger",
 "Nigeria","Rwanda","Sao Tome and Principe","Senegal","Seychelles",
 "Sierra Leone","Somalia","South Africa","South Sudan","Sudan","Tanzania",
 "Togo","Tunisia","Uganda","Zambia","Zimbabwe","Western Sahara","Réunion",
 "Reunion","Mayotte",
}

CHILD=re.compile(rb"^\d+\|NCT\d{8}\|")
STUDY=re.compile(rb"^NCT\d{8}\|")
F2=re.compile(rb"^\d+\|(NCT\d{8})\|")

def africa_ncts():
    s=set(); buf=None
    def flush(b):
        m=F2.match(b)
        if not m: return
        p=b.rstrip(b"\n").split(b"|")
        if len(p)>7:
            c=p[7].strip().decode(errors="replace")
            if c in AFRICA: s.add(m.group(1).decode())
    with open(os.path.join(AACT,"facilities.txt"),"rb") as fh:
        fh.readline()
        for ln in fh:
            if CHILD.match(ln):
                if buf is not None: flush(buf)
                buf=ln
            elif buf is not None: buf+=ln
        if buf is not None: flush(buf)
    return s

def interventional_ncts():
    s=set(); buf=None; I_TYPE=30; N=71
    with open(os.path.join(AACT,"studies.txt"),"rb") as fh:
        fh.readline()
        for ln in fh:
            if STUDY.match(ln):
                if buf is not None:
                    p=buf.rstrip(b"\n").split(b"|")
                    if len(p)==N and p[I_TYPE].strip().decode().upper()=="INTERVENTIONAL":
                        s.add(p[0].decode())
                buf=ln
            elif buf is not None: buf+=ln
        if buf is not None:
            p=buf.rstrip(b"\n").split(b"|")
            if len(p)==N and p[I_TYPE].strip().decode().upper()=="INTERVENTIONAL":
                s.add(p[0].decode())
    return s

def all_study_ncts():
    s=set()
    with open(os.path.join(AACT,"studies.txt"),"rb") as fh:
        fh.readline()
        for ln in fh:
            if STUDY.match(ln): s.add(ln[:11].decode())
    return s

# condition index: keyword-group -> set(nct). Single streaming pass.
GROUPS={
 "sickle_cell":(["sickle cell","sickle-cell","drepanocyt"],[]),
 "epilepsy":(["epilepsy","epileptic","seizure disorder"],[]),
 "cervical_hpv":(["cervical cancer","cervical carcinoma","cervical intraepithelial",
                  "human papillomavirus","hpv","cervical dysplasia"],["oral hpv"]),
 "breast_cancer":(["breast cancer","breast carcinoma","breast neoplasm","breast tumor",
                   "breast tumour"],["male breast"]),
 "ntd":(["schistosomiasis","soil-transmitted helminth","lymphatic filariasis",
         "onchocerciasis","trachoma","leishmaniasis","chagas","human african trypanosomiasis",
         "sleeping sickness","buruli ulcer","dracunculiasis","guinea worm","yaws",
         "leprosy","dengue","rabies","echinococcosis","cysticercosis","scabies","noma",
         "mycetoma","chikungunya"],[]),
 "amr":(["antimicrobial resistance","antibiotic resistance","drug-resistant",
         "multidrug-resistant","carbapenem-resistant","methicillin-resistant",
         "extensively drug-resistant"],[]),
 "zoonotic":(["zoonotic","zoonosis","brucellosis","rift valley fever","lassa fever",
              "ebola","marburg","anthrax","q fever","leptospirosis","hantavirus",
              "nipah","monkeypox","mpox","avian influenza","rabies"],[]),
 "hiv":(["hiv","human immunodeficiency virus","aids"],["hearing aids","band aids"]),
}

def build_condition_index(groups):
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
            dn=parts[3].lower()
            nct=m.group(1).decode()
            for g in groups:
                if any(e in dn for e in ex[g]): continue
                if any(k in dn for k in kw[g]): hits[g].add(nct)
    return hits

print("Loading facilities (African sites)…", file=sys.stderr)
afr=africa_ncts()
print("Loading study types…", file=sys.stderr)
interv=interventional_ncts()
alln=all_study_ncts()
print("Indexing conditions…", file=sys.stderr)
hits=build_condition_index(GROUPS)

def row(name, s):
    g=len(s); a=len(s&afr)
    gi=len(s&interv); ai=len(s&afr&interv)
    sh=100.0*a/g if g else 0.0; shi=100.0*ai/gi if gi else 0.0
    print(f"{name:<16}{g:>9,}{a:>9,}{sh:>8.2f}{gi:>12,}{ai:>9,}{shi:>8.2f}")

print("="*74)
print("AFRICA-EQUITY — deterministic AACT verification |", AACT)
print("="*74)
print(f"Registry totals: all studies {len(alln):,} | interventional {len(interv):,} | "
      f"any African site {len(afr):,} ({100.0*len(afr)/len(alln):.2f}% of all; "
      f"{100.0*len(afr&interv)/len(interv):.2f}% of interventional)")
print("-"*74)
print(f"{'group':<16}{'global':>9}{'africa':>9}{'afr%':>8}{'glob_intv':>12}{'afr_intv':>9}{'afr%':>8}")
for g in GROUPS: row(g, hits[g])
print("="*74)
