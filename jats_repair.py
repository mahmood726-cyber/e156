#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jats_repair.py  -  PMC-readiness JATS galley repair for synthesis-medicine.org
Repairs all 114 published article XML galleys:
  1. Replace placeholder <issn> comment with clean empty element
  2. Replace placeholder <doi> comment with clean empty element (no DOIs assigned yet)
  3. Remove <contrib-id orcid> placeholder comments (keep element only if real ORCID)
  4. Add <aff> elements from OJS author_settings.affiliation
  5. Add <ref-list> from OJS citations table (raw_citation)
Backs up originals to BACKUP_DIR before any write.
Validates each output as well-formed XML.
"""

import os, sys, re, glob, json, shutil, subprocess, datetime
from xml.etree import ElementTree as ET

BACKUP_DIR = "/var/www/files_jats_backup_20260624"
FILES_ROOT  = "/var/www/files"
DB_USER     = "ojsuser"
DB_PASS     = "OjsPass123!"
DB_NAME     = "ojs"


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def db_rows(sql):
    """Run SQL, return list of tab-split string lists. NULLs become empty str."""
    cmd = [
        "mysql", "-u", DB_USER, f"-p{DB_PASS}",
        "--default-character-set=utf8mb4",
        "--batch", "--skip-column-names",
        DB_NAME, "-e", sql
    ]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"DB error: {r.stderr[:500]}")
    rows = []
    for line in r.stdout.splitlines():
        if line:
            rows.append([c if c != "\\N" else "" for c in line.split("\t")])
    return rows


# ---------------------------------------------------------------------------
# Load article inventory  (one row per submission -> latest published pub)
# ---------------------------------------------------------------------------

def load_articles():
    """Returns {submission_id(int): {fields}}."""
    sql = (
        "SELECT sub.submission_id, sub.context_id, "
        "       MAX(p.publication_id) AS pub_id "
        "FROM submissions sub "
        "JOIN publications p ON p.submission_id = sub.submission_id AND p.status = 3 "
        "GROUP BY sub.submission_id, sub.context_id"
    )
    arts = {}
    for row in db_rows(sql):
        sid, jid, pub_id = int(row[0]), int(row[1]), row[2]
        arts[sid] = {"journal_id": jid, "pub_id": pub_id}

    # Get XML file path for each submission (one path per submission)
    xml_sql = (
        "SELECT sf.submission_id, MAX(f.path) AS xml_path "
        "FROM submission_files sf "
        "JOIN files f ON f.file_id = sf.file_id "
        "WHERE f.path LIKE '%.xml' "
        "GROUP BY sf.submission_id"
    )
    for row in db_rows(xml_sql):
        sid = int(row[0])
        if sid in arts:
            arts[sid]["xml_path"] = row[1]

    return arts


# ---------------------------------------------------------------------------
# Load journal metadata
# ---------------------------------------------------------------------------

def load_journals():
    """Returns {journal_id(int): {fields}}."""
    sql = (
        "SELECT j.journal_id, j.path AS slug, "
        "  MAX(CASE WHEN js.setting_name='onlineIssn' THEN js.setting_value END) AS online_issn, "
        "  MAX(CASE WHEN js.setting_name='printIssn'  THEN js.setting_value END) AS print_issn, "
        "  MAX(CASE WHEN js.setting_name='doiPrefix'  THEN js.setting_value END) AS doi_prefix, "
        "  MAX(CASE WHEN js.setting_name='name' AND js.locale='en' THEN js.setting_value END) AS name "
        "FROM journals j "
        "LEFT JOIN journal_settings js ON js.journal_id = j.journal_id "
        "GROUP BY j.journal_id, j.path"
    )
    journals = {}
    for row in db_rows(sql):
        journals[int(row[0])] = {
            "slug": row[1], "online_issn": row[2],
            "print_issn": row[3], "doi_prefix": row[4], "name": row[5]
        }
    return journals


# ---------------------------------------------------------------------------
# Load authors (publication_id -> list of author dicts)
# ---------------------------------------------------------------------------

def load_authors():
    """Returns {pub_id(str): [author_dict, ...]}."""
    sql = (
        "SELECT a.publication_id, a.author_id, a.seq, "
        "  MAX(CASE WHEN ase.setting_name='givenName'   THEN ase.setting_value END) AS given, "
        "  MAX(CASE WHEN ase.setting_name='familyName'  THEN ase.setting_value END) AS family, "
        "  MAX(CASE WHEN ase.setting_name='affiliation' THEN ase.setting_value END) AS affiliation, "
        "  MAX(CASE WHEN ase.setting_name='orcid'       THEN ase.setting_value END) AS orcid "
        "FROM authors a "
        "LEFT JOIN author_settings ase ON ase.author_id = a.author_id "
        "GROUP BY a.publication_id, a.author_id, a.seq "
        "ORDER BY a.publication_id, a.seq"
    )
    authors = {}
    for row in db_rows(sql):
        pub_id = row[0]
        if pub_id not in authors:
            authors[pub_id] = []
        authors[pub_id].append({
            "author_id": row[1], "seq": row[2],
            "given": row[3], "family": row[4],
            "affiliation": row[5], "orcid": row[6]
        })
    return authors


# ---------------------------------------------------------------------------
# Load citations (publication_id -> [raw_citation, ...])
# ---------------------------------------------------------------------------

def load_citations():
    """Returns {pub_id(str): [raw_str, ...]}."""
    sql = (
        "SELECT c.publication_id, c.seq, c.raw_citation "
        "FROM citations c "
        "ORDER BY c.publication_id, c.seq"
    )
    cites = {}
    for row in db_rows(sql):
        pub_id = row[0]
        if pub_id not in cites:
            cites[pub_id] = []
        cites[pub_id].append(row[2])
    return cites


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

def xe(s):
    """XML-escape a string."""
    if not s:
        return ""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&apos;"))


def validate_wf(xml_str):
    """Check well-formedness. Strip DOCTYPE/XMLdecl (ET can't parse external DTD)."""
    try:
        s = re.sub(r'<\?xml[^?]*\?>', '', xml_str, count=1)
        s = re.sub(r'<!DOCTYPE\s[^[>]*(?:\[[^\]]*\])?\s*>', '', s, count=1, flags=re.DOTALL)
        ET.fromstring(s.strip().encode("utf-8"))
        return True, ""
    except ET.ParseError as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# JATS repair logic
# ---------------------------------------------------------------------------

def repair(xml_str, pub_id, journal, auth_list, cite_list):
    """
    Apply all repairs to xml_str.
    Returns (repaired_str, stats_dict).
    """
    s = {}  # stats

    # 1. Clean ISSN placeholder  -> empty element
    xml_str = re.sub(
        r'<issn\s+pub-type="epub">\s*<!--[\s\S]*?-->\s*</issn>',
        '<issn pub-type="epub"/>',
        xml_str, flags=re.DOTALL
    )

    # 2. Clean DOI placeholder -> empty element (no DOIs assigned yet)
    xml_str = re.sub(
        r'<article-id\s+pub-id-type="doi">\s*<!--[\s\S]*?-->\s*</article-id>',
        '<article-id pub-id-type="doi"/>',
        xml_str, flags=re.DOTALL
    )

    # 3. Strip ORCID placeholder comments (keep real ORCIDs if any author has one)
    xml_str = re.sub(
        r'<contrib-id\s+contrib-id-type="orcid">\s*<!--[\s\S]*?-->\s*</contrib-id>',
        '',
        xml_str, flags=re.DOTALL
    )
    # Re-insert real ORCID elements for authors that have them
    for a in auth_list:
        orcid = (a.get("orcid") or "").strip()
        if orcid and orcid.startswith("http"):
            family = xe((a.get("family") or "").strip())
            given  = xe((a.get("given")  or "").strip())
            # Insert after matching <surname>...</surname> in a <contrib> block
            orcid_el = (f'<contrib-id contrib-id-type="orcid"'
                        f' authenticated="true">{xe(orcid)}</contrib-id>\n          ')
            # Find the contrib block for this author by surname
            def inject_orcid(m):
                block = m.group(0)
                sn = re.search(r'<surname>([^<]*)</surname>', block)
                if sn and sn.group(1).strip() == (a.get("family") or "").strip():
                    if 'contrib-id-type="orcid"' not in block:
                        block = block.replace('<name>', orcid_el + '<name>', 1)
                return block
            xml_str = re.sub(
                r'<contrib\s+contrib-type="author">[\s\S]*?</contrib>',
                inject_orcid, xml_str, flags=re.DOTALL
            )

    # 4. Build <aff> elements and insert after </contrib-group>
    unique_affs = {}   # aff_text -> aff_id
    author_aff  = {}   # family_name -> aff_id
    ctr = 0
    for a in auth_list:
        aff = (a.get("affiliation") or "").strip()
        family = (a.get("family") or "").strip()
        if aff:
            if aff not in unique_affs:
                ctr += 1
                unique_affs[aff] = f"aff{ctr}"
            author_aff[family] = unique_affs[aff]

    s["n_affs"] = ctr
    s["has_affs"] = ctr > 0

    if unique_affs:
        aff_xml = "\n".join(
            f'    <aff id="{aid}">{xe(txt)}</aff>'
            for txt, aid in unique_affs.items()
        )
        xml_str = xml_str.replace('</contrib-group>',
                                  f'</contrib-group>\n{aff_xml}', 1)

    # 5. Build <ref-list> and insert before </back>
    s["n_refs"] = len(cite_list)
    s["has_refs"] = len(cite_list) > 0

    if cite_list:
        ref_items = []
        for i, raw in enumerate(cite_list, 1):
            raw = raw.strip()
            # Clean leading section-title bleed or numbering
            raw = re.sub(r'^References\s*', '', raw, flags=re.IGNORECASE).strip()
            raw = re.sub(r'^[\[\(]?\d+[\]\)\.:\s]+', '', raw).strip()
            if raw:
                ref_items.append(
                    f'      <ref id="ref{i}">\n'
                    f'        <label>{i}</label>\n'
                    f'        <mixed-citation>{xe(raw)}</mixed-citation>\n'
                    f'      </ref>'
                )
        if ref_items:
            ref_list = (
                '    <ref-list>\n'
                '      <title>References</title>\n'
                + '\n'.join(ref_items) + '\n'
                '    </ref-list>'
            )
            if '</back>' in xml_str:
                xml_str = xml_str.replace('</back>', ref_list + '\n  </back>', 1)
            else:
                xml_str = xml_str.replace('</article>',
                                          f'  <back>\n{ref_list}\n  </back>\n</article>', 1)

    return xml_str, s


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] JATS repair starting")
    os.makedirs(BACKUP_DIR, exist_ok=True)

    print("  Loading DB data...")
    articles = load_articles()
    journals = load_journals()
    authors  = load_authors()
    cites    = load_citations()
    print(f"  {len(articles)} articles, {len(journals)} journals, "
          f"{len(authors)} pub-auth records, {len(cites)} pub-cite records")

    total = valid = invalid = 0
    with_affs = without_affs = with_refs = without_refs = 0
    errors = []
    no_aff_ids  = []
    no_ref_ids  = []
    no_xml_ids  = []

    for sid in sorted(articles):
        art = articles[sid]
        if "xml_path" not in art:
            no_xml_ids.append(sid)
            continue

        total += 1
        xml_abs  = os.path.join(FILES_ROOT, art["xml_path"])
        pub_id   = art["pub_id"]
        jid      = art["journal_id"]
        journal  = journals.get(jid, {})
        auth_list = authors.get(pub_id, [])
        cite_list = cites.get(pub_id, [])

        if not os.path.exists(xml_abs):
            errors.append(f"MISSING FILE sid={sid}: {xml_abs}")
            continue

        # Backup (idempotent)
        bk = os.path.join(BACKUP_DIR, f"{sid}_{os.path.basename(xml_abs)}")
        if not os.path.exists(bk):
            shutil.copy2(xml_abs, bk)

        with open(xml_abs, encoding="utf-8", errors="replace") as f:
            original = f.read()

        try:
            repaired, st = repair(original, pub_id, journal, auth_list, cite_list)
        except Exception as e:
            errors.append(f"REPAIR ERROR sid={sid}: {e}")
            continue

        ok, err = validate_wf(repaired)
        if not ok:
            errors.append(f"INVALID XML sid={sid}: {err}")
            invalid += 1
            continue

        with open(xml_abs, "w", encoding="utf-8") as f:
            f.write(repaired)
        valid += 1

        if st["has_affs"]:
            with_affs += 1
        else:
            without_affs += 1
            no_aff_ids.append(sid)
        if st["has_refs"]:
            with_refs += 1
        else:
            without_refs += 1
            no_ref_ids.append(sid)

    # Report
    print("\n=== JATS REPAIR COMPLETE ===")
    print(f"  Total processed:            {total}")
    print(f"  Repaired & valid:           {valid}")
    print(f"  Invalid after repair:       {invalid}")
    print(f"  No XML file in DB:          {len(no_xml_ids)}")
    print(f"")
    print(f"  With real affiliations:     {with_affs}")
    print(f"  Without affiliations:       {without_affs}  (authors must supply)")
    print(f"  With ref-list:              {with_refs}")
    print(f"  Without refs (0 in DB):     {without_refs}  (editorial curation needed)")
    print(f"")

    if no_aff_ids:
        print(f"  Missing-aff submission IDs ({len(no_aff_ids)}):")
        print(f"    {no_aff_ids}")
    if no_ref_ids:
        print(f"  Zero-ref submission IDs ({len(no_ref_ids)}):")
        print(f"    {no_ref_ids}")
    if errors:
        print(f"\n  ERRORS ({len(errors)}):")
        for e in errors:
            print(f"    {e}")

    report = {
        "total": total, "valid": valid, "invalid": invalid,
        "with_affs": with_affs, "without_affs": without_affs,
        "with_refs": with_refs, "without_refs": without_refs,
        "no_aff_ids": no_aff_ids, "no_ref_ids": no_ref_ids,
        "errors": errors
    }
    rp = "/tmp/jats_repair_report.json"
    with open(rp, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n  JSON report: {rp}")
    return report


if __name__ == "__main__":
    main()
