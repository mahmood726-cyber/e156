"""
PMC-readiness audit — synthesis-medicine.org — all five journals.
Incorporates JATS spot-check findings (no <aff>, no <ref-list>, no ISSN/DOI in any file).
"""

import io

JOURNALS = {1: "Synthesis", 2: "Insight", 3: "Gnosis", 4: "Sapience", 5: "Hikmah"}

# ── Load raw inventory ──────────────────────────────────────────────────────
articles = {}
with open("ojs_audit_raw.tsv", encoding="utf-8") as f:
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 10:
            continue
        jid, slug, sid, title, section, authors, has_abs, refs, jats, pdf = p[:10]
        articles[int(sid)] = {
            "jid": int(jid),
            "journal": JOURNALS.get(int(jid), f"J{jid}"),
            "sid": int(sid),
            "title": title,
            "section": section,
            "authors": int(authors),
            "has_abstract": int(has_abs),
            "refs": int(refs),
            "has_jats_file": int(jats),   # skeleton exists for all 114
            "has_pdf": int(pdf),
        }

with open("ojs_affiliations.tsv", encoding="utf-8") as f:
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) < 3:
            continue
        sid, has_aff, abs_len = int(p[0]), int(p[1]), int(p[2])
        if sid in articles:
            articles[sid]["aff_in_db"] = has_aff
            articles[sid]["abstract_chars"] = abs_len

# ── Section classification ──────────────────────────────────────────────────
LETTER_SECTIONS = {"E156 Research Letter", "Research Letter", "E468 Short Report"}
FULL_SECTIONS   = {"Research Article", "Short Meta-Analysis", "Methods Note",
                   "Tool Paper", "Case Report", "Articles"}

STUB_TITLES = {
    "WaterNajia", "Health and Disease Burden", "COVID-19 Displacement",
    "Decolonising Research", "Community led Research",
    "SGLT2 Inhibitors and Heart Failure", "Global RCT Equity: Africa vs. Europe",
    "HIV Trial Saturation Index", "Altruism Efficiency & Health Expenditure",
    "Sample Size Adequacy Audit",
}

def classify(a):
    """
    Grade content quality assuming universal JATS skeleton fixes (ISSN, DOI,
    <aff>, <ref-list>) are applied.  Grades reflect work BEYOND those fixes.

    A — content-complete; only needs JATS/infrastructure fill-in
    B — content largely there; needs >=1 of: refs added, aff data entered, minor edit
    C — content gaps that require substantive editorial work
    """
    is_letter = a["section"] in LETTER_SECTIONS or "E156" in a["section"]
    is_full   = a["section"] in FULL_SECTIONS

    gaps = []

    # Universal JATS gaps (noted but not used to grade, affect all 114)
    jats_gaps = ["no <aff> in JATS", "no <ref-list> in JATS",
                 "no ISSN in JATS (application pending)", "no DOI assigned"]

    # Content gaps for grading
    if not a["has_abstract"] or a.get("abstract_chars", 0) < 80:
        gaps.append("no/stub abstract")

    if a["refs"] == 0:
        gaps.append("0 refs in DB (nothing to add to JATS)")
    elif a["refs"] < 3 and not is_full:
        gaps.append(f"{a['refs']} ref(s) — borderline")

    if not a.get("aff_in_db", 0):
        gaps.append("affiliations absent from OJS — must be sourced")

    if a["title"] in STUB_TITLES or len(a["title"].strip()) < 15:
        gaps.append("stub/informal title (editorial revision needed)")

    if a["authors"] >= 15 and is_letter:
        gaps.append(f"{a['authors']}-author single-para letter (authorship review)")

    # Tier logic
    hard_gaps = [g for g in gaps if "stub" in g or "0 refs" in g or "revision" in g]

    if is_full and not gaps:
        grade = "A"
    elif is_full and not hard_gaps and len(gaps) <= 2:
        grade = "B"
    elif is_letter and not hard_gaps and a["refs"] >= 3 and a.get("aff_in_db", 0):
        grade = "B"   # short-format letter, content OK, just needs infra fill-in
    elif is_letter and not hard_gaps and len(gaps) <= 1:
        grade = "B"   # single fixable gap
    else:
        grade = "C"

    return grade, gaps, jats_gaps

for a in articles.values():
    a["grade"], a["gaps"], a["jats_gaps"] = classify(a)

# ── Build report ─────────────────────────────────────────────────────────────
out = io.StringIO()
def pr(*args, **kw):
    print(*args, **kw, file=out)

all_arts = sorted(articles.values(), key=lambda x: (x["jid"], x["sid"]))
A = [a for a in all_arts if a["grade"] == "A"]
B = [a for a in all_arts if a["grade"] == "B"]
C = [a for a in all_arts if a["grade"] == "C"]

pr("=" * 80)
pr("PMC-READINESS AUDIT  —  synthesis-medicine.org  —  Five Journals")
pr("Assessed: 2026-06-23   Total published: 114")
pr("=" * 80)
pr()

pr("UNIVERSAL PREREQUISITES (block ALL 114 articles from PMC deposit)")
pr("-" * 80)
pr("  1. No registered ISSN for any of the five journals.")
pr("     (Synthesis has a DOI prefix 10.66040 but DOI assignment is disabled.)")
pr("  2. No DOI assigned to any article (doi_id = NULL across all 114 publications).")
pr("  3. JATS XML files exist for every article but are skeleton-only:")
pr("       - No <aff> tags in any file (even where OJS DB has affiliation text)")
pr("       - No <ref-list> in any file (even where OJS DB has citation records)")
pr("       - <issn> and <article-id pub-id-type=\"doi\"> are comment placeholders")
pr()
pr("  These are journal-infrastructure fixes, not per-article edits.")
pr("  Grades below assume those three fixes are applied uniformly.")
pr()

pr("OVERALL CONTENT GRADES  (post-infrastructure-fix readiness)")
pr("-" * 80)
pr(f"  A  Content-complete — needs only JATS/infra fill-in:   {len(A):3}")
pr(f"  B  Close — needs light editorial work beyond infra:    {len(B):3}")
pr(f"  C  Not PMC-quality — substantive gaps remain:         {len(C):3}")
pr(f"     TOTAL                                               {len(all_arts):3}")
pr()

pr("PER-JOURNAL BREAKDOWN")
pr("-" * 80)
pr(f"  {'Journal':<12} {'Total':>5} {'A':>4} {'B':>4} {'C':>4}  Notes")
for jid, jname in JOURNALS.items():
    j = [a for a in all_arts if a["jid"] == jid]
    ja = sum(1 for a in j if a["grade"] == "A")
    jb = sum(1 for a in j if a["grade"] == "B")
    jc = sum(1 for a in j if a["grade"] == "C")
    note = ""
    if jid == 1:  note = "100 articles; mostly E156 Research Letters"
    if jid == 2:  note = "6 articles; mixed"
    if jid == 3:  note = "4 articles; tool/methods papers"
    if jid == 4:  note = "3 articles; browser tool papers"
    if jid == 5:  note = "1 article"
    pr(f"  {jname:<12} {len(j):>5} {ja:>4} {jb:>4} {jc:>4}  {note}")
pr()

pr("TIER A — Content-complete (7 articles; needs infra fill-in only)")
pr("-" * 80)
pr(f"  {'ID':>4}  {'Journal':<10}  {'Section':<22}  {'Refs':>4}  {'Aff':>3}  Title")
for a in A:
    pr(f"  {a['sid']:>4}  {a['journal']:<10}  {a['section']:<22}  {a['refs']:>4}  "
       f"{a.get('aff_in_db',0):>3}  {a['title'][:65]}")
pr()

pr("TIER B — Close / fixable  (light work beyond infrastructure)")
pr("-" * 80)
pr(f"  {'ID':>4}  {'Journal':<10}  {'Section':<22}  {'Refs':>4}  {'Aff':>3}  Gap(s)")
pr(f"  {'—'*4}  {'—'*10}  {'—'*22}  {'—'*4}  {'—'*3}  {'—'*40}")
for a in B:
    gap_str = "; ".join(a["gaps"]) if a["gaps"] else "(none beyond infra)"
    pr(f"  {a['sid']:>4}  {a['journal']:<10}  {a['section'][:22]:<22}  "
       f"{a['refs']:>4}  {a.get('aff_in_db',0):>3}  {gap_str}")
pr()

pr("TIER C — Not PMC-quality  (substantive content gaps)")
pr("-" * 80)
pr(f"  {'ID':>4}  {'Journal':<10}  {'Sect':<22}  {'Auth':>4}  {'Refs':>4}  Primary gap")
pr(f"  {'—'*4}  {'—'*10}  {'—'*22}  {'—'*4}  {'—'*4}  {'—'*40}")
for a in C:
    primary = a["gaps"][0] if a["gaps"] else "(see JATS gaps)"
    pr(f"  {a['sid']:>4}  {a['journal']:<10}  {a['section'][:22]:<22}  "
       f"{a['authors']:>4}  {a['refs']:>4}  {primary}")
pr()

pr("KEY STATISTICS")
pr("-" * 80)
no_aff_db   = [a for a in all_arts if not a.get("aff_in_db", 0)]
zero_refs   = [a for a in all_arts if a["refs"] == 0]
solo        = [a for a in all_arts if a["authors"] == 1]
big_letters = [a for a in all_arts if a["authors"] >= 15 and "E156" in a["section"]]
letters     = [a for a in all_arts if a["section"] in LETTER_SECTIONS or "E156" in a["section"]]
full_papers = [a for a in all_arts if a["section"] in FULL_SECTIONS]

pr(f"  Total published:                              {len(all_arts)}")
pr(f"  Have JATS XML file (skeleton):                {len(all_arts)}  (100%)")
pr(f"  Have PDF galley:                              {sum(1 for a in all_arts if a['has_pdf'])}")
pr(f"  Authors have affiliations in OJS DB:          {len(all_arts)-len(no_aff_db)}")
pr(f"  Authors missing affiliations in OJS DB:       {len(no_aff_db)}")
pr(f"  Articles with 0 references in DB:             {len(zero_refs)}")
pr(f"  Articles with >=3 references in DB:           {sum(1 for a in all_arts if a['refs']>=3)}")
pr(f"  Solo-authored (1 author):                     {len(solo)}")
pr(f"  E156 letters with 15+ authors:                {len(big_letters)}")
pr(f"  E156/Research-Letter section:                 {len(letters)}")
pr(f"  Full-paper sections (Research Art/Methods/…): {len(full_papers)}")
pr()

pr("TIER C DETAIL — Articles with stub/informal titles:")
stub_arts = [a for a in C if "stub/informal title" in " ".join(a["gaps"])]
for a in stub_arts:
    pr(f"  #{a['sid']}: \"{a['title']}\"")
pr()

pr("TIER C — 15+ author single-paragraph letters:")
for a in big_letters:
    pr(f"  #{a['sid']} ({a['authors']} authors): {a['title'][:70]}")
pr()

pr("ROADMAP TO PMC (priority order)")
pr("-" * 80)
pr("  1. ISSN: apply for e-ISSNs for all 5 journals (ISSN International, free;")
pr("     wait ~3 weeks). Synthesis first — it has the largest article set.")
pr("  2. DOI: enable DOI plugin in OJS (prefix 10.66040 exists for Synthesis).")
pr("     Register DOIs for all existing articles via Crossref deposit.")
pr("     Other 4 journals need their own DOI prefixes.")
pr("  3. JATS repair (all 114 files): add <aff> per author, <ref-list> from")
pr("     the citations table, fill <issn> and <article-id pub-id-type=\"doi\">.")
pr("     This is automatable from OJS DB data.")
pr("  4. Affiliations (72 articles): 72 articles have no affiliation in OJS DB;")
pr("     these cannot be fixed from DB data alone — authors must supply them.")
pr("  5. References (31 zero-ref articles): these need editorial curation.")
pr("  6. Tier-C stub titles / content: 10 informal-title articles need editorial")
pr("     revision before PMC would index them.")
pr("  7. PMC journal application: once ISSN + DOIs are registered, apply via")
pr("     NLM's journal application portal. Expect 6-18 month review.")

result = out.getvalue()
print(result)
with open("pmc_audit_report.txt", "w", encoding="utf-8") as f:
    f.write(result)
print("[written to pmc_audit_report.txt]")
