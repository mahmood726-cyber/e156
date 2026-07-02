"""
PMC-readiness audit for synthesis-medicine.org journals.
Reads ojs_audit_raw.tsv + ojs_affiliations.tsv and classifies articles into A/B/C.
"""

import csv, sys, io

JOURNALS = {1: "Synthesis", 2: "Insight", 3: "Gnosis", 4: "Sapience", 5: "Hikmah"}

# ── Load raw inventory ──────────────────────────────────────────────────────
# Cols: journal_id, slug, sub_id, title, section, author_count,
#       has_abstract, ref_count, has_jats_xml, has_pdf
articles = {}
with open("ojs_audit_raw.tsv", encoding="utf-8") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 10:
            continue
        jid, slug, sub_id, title, section, authors, has_abs, refs, jats, pdf = parts[:10]
        articles[int(sub_id)] = {
            "jid": int(jid),
            "journal": JOURNALS.get(int(jid), f"J{jid}"),
            "sub_id": int(sub_id),
            "title": title,
            "section": section,
            "authors": int(authors),
            "has_abstract": int(has_abs),
            "refs": int(refs),
            "has_jats": int(jats),
            "has_pdf": int(pdf),
        }

# ── Load affiliations + abstract lengths ────────────────────────────────────
# Cols: sub_id, has_affiliation, abstract_len_chars
with open("ojs_affiliations.tsv", encoding="utf-8") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        sub_id, has_aff, abs_len = int(parts[0]), int(parts[1]), int(parts[2])
        if sub_id in articles:
            articles[sub_id]["has_affiliation"] = has_aff
            articles[sub_id]["abstract_len"] = abs_len

# ── Stub-title heuristic ────────────────────────────────────────────────────
STUB_TITLES = {
    "WaterNajia", "Health and Disease Burden", "COVID-19 Displacement",
    "Decolonising Research", "Community led Research",
    "SGLT2 Inhibitors and Heart Failure", "Global RCT Equity: Africa vs. Europe",
    "HIV Trial Saturation Index", "Altruism Efficiency & Health Expenditure",
    "Sample Size Adequacy Audit",
}

# ── Classification ───────────────────────────────────────────────────────────
def classify(a):
    gaps = []
    is_e156 = "E156" in a["section"] or a["section"] in ("Research Letter",)

    if not a["has_jats"]:
        gaps.append("no JATS XML")
    if not a.get("has_affiliation", 0):
        gaps.append("no author affiliations")
    if not a["has_abstract"] or a.get("abstract_len", 0) < 100:
        gaps.append("no/stub abstract")
    if a["refs"] == 0:
        gaps.append("0 references")
    elif a["refs"] < 3:
        gaps.append(f"only {a['refs']} reference(s)")

    if a["title"] in STUB_TITLES or len(a["title"]) < 15:
        gaps.append("stub/informal title")

    # E156 by-design very short — PMC would class as letter; flagging as C
    # unless it has proper XML + metadata + refs
    if is_e156:
        gaps.append("E156 format (~156 words, single para)")

    # "one paragraph, many authors" signal
    if a["authors"] >= 15 and is_e156:
        gaps.append(f"{a['authors']}-author single-paragraph letter")

    # Decide tier
    blocking = [g for g in gaps if g in (
        "no JATS XML", "no/stub abstract", "no author affiliations",
        "0 references", "stub/informal title", "E156 format (~156 words, single para)"
    )]
    if len(blocking) == 0:
        grade = "A"
    elif len(blocking) <= 2 and "no JATS XML" not in blocking:
        grade = "B"
    else:
        grade = "C"

    return grade, gaps

for a in articles.values():
    a["grade"], a["gaps"] = classify(a)

# ── Summary ──────────────────────────────────────────────────────────────────
out = io.StringIO()

def pr(*args, **kw):
    print(*args, **kw, file=out)

all_articles = sorted(articles.values(), key=lambda x: (x["jid"], x["sub_id"]))
A = [a for a in all_articles if a["grade"] == "A"]
B = [a for a in all_articles if a["grade"] == "B"]
C = [a for a in all_articles if a["grade"] == "C"]

pr("=" * 80)
pr("PMC-READINESS AUDIT  —  synthesis-medicine.org  —  All Five Journals")
pr("=" * 80)
pr()
pr(f"Total published articles: {len(all_articles)}")
pr(f"  A — PMC-ready:              {len(A)}")
pr(f"  B — Close / fixable:        {len(B)}")
pr(f"  C — Not PMC-quality:        {len(C)}")
pr()

# Per-journal breakdown
pr("PER-JOURNAL BREAKDOWN")
pr("-" * 50)
for jid, jname in JOURNALS.items():
    j_all = [a for a in all_articles if a["jid"] == jid]
    j_a = sum(1 for a in j_all if a["grade"] == "A")
    j_b = sum(1 for a in j_all if a["grade"] == "B")
    j_c = sum(1 for a in j_all if a["grade"] == "C")
    pr(f"  {jname:<12} ({len(j_all):3} articles)   A:{j_a}  B:{j_b}  C:{j_c}")
pr()

# B table
pr("TIER B — Close / Fixable")
pr("-" * 80)
pr(f"  {'ID':>5}  {'Journal':<12}  {'Refs':>4}  {'JATS':>4}  {'Aff':>3}  Gaps")
pr(f"  {'—'*5}  {'—'*12}  {'—'*4}  {'—'*4}  {'—'*3}  {'—'*40}")
for a in B:
    gap_str = "; ".join(g for g in a["gaps"] if "E156" not in g)
    pr(f"  {a['sub_id']:>5}  {a['journal']:<12}  {a['refs']:>4}  {a['has_jats']:>4}  {a.get('has_affiliation',0):>3}  {gap_str}")
pr()

# C table — show IDs and primary gap only (concise)
pr("TIER C — Not PMC-quality  (representative gaps only)")
pr("-" * 80)
pr(f"  {'ID':>5}  {'Journal':<12}  {'Section':<22}  {'Auth':>4}  {'Refs':>4}  {'JATS':>4}  Primary gap")
pr(f"  {'—'*5}  {'—'*12}  {'—'*22}  {'—'*4}  {'—'*4}  {'—'*4}  {'—'*40}")
for a in C:
    primary = next(
        (g for g in a["gaps"] if g in (
            "no JATS XML", "no author affiliations", "no/stub abstract",
            "0 references", "stub/informal title"
        )),
        a["gaps"][0] if a["gaps"] else ""
    )
    section_short = a["section"][:22]
    pr(f"  {a['sub_id']:>5}  {a['journal']:<12}  {section_short:<22}  {a['authors']:>4}  {a['refs']:>4}  {a['has_jats']:>4}  {primary}")

pr()
pr("KEY FINDINGS")
pr("-" * 80)
no_jats = [a for a in all_articles if not a["has_jats"]]
no_aff  = [a for a in all_articles if not a.get("has_affiliation",0)]
no_refs = [a for a in all_articles if a["refs"] == 0]
lone_auth = [a for a in all_articles if a["authors"] == 1]
big_team_letter = [a for a in all_articles if a["authors"] >= 15 and "E156" in a["section"]]

pr(f"  Articles with NO JATS XML galley:         {len(no_jats)}")
pr(f"  Articles with NO author affiliations:     {len(no_aff)}")
pr(f"  Articles with 0 references:               {len(no_refs)}")
pr(f"  Articles with solo author (=1):           {len(lone_auth)}")
pr(f"  E156 letters with 15+ authors:            {len(big_team_letter)}")

result = out.getvalue()
print(result, end="")

with open("pmc_audit_report.txt", "w", encoding="utf-8") as f:
    f.write(result)

print("\n[Report written to pmc_audit_report.txt]")
