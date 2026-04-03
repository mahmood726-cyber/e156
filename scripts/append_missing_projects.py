"""Append the 29 missing projects to the rewrite workbook."""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from missing_projects_data import MISSING_PROJECTS


def count_words(text):
    return len(text.split())


def main():
    workbook_path = 'C:/E156/rewrite-workbook.txt'

    with open(workbook_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find current max entry number
    max_num = 302
    for m in re.finditer(r'\[(\d+)/302\]', text):
        n = int(m.group(1))
        if n > max_num:
            max_num = n

    # Update total count
    total = max_num + len(MISSING_PROJECTS)

    # First, update all existing [N/302] to [N/TOTAL]
    text = re.sub(r'\[(\d+)/302\]', lambda m: f'[{m.group(1)}/{total}]', text)
    text = text.replace('Total projects: 302', f'Total projects: {total}')

    # Build new entries
    new_entries = []
    next_num = max_num + 1

    for name, proj in sorted(MISSING_PROJECTS.items()):
        body = proj['body']
        rewrite = proj['rewrite']
        wc = count_words(body)
        rw_wc = count_words(rewrite)

        entry = f"""
======================================================================

[{next_num}/{total}] {name}
TITLE: {proj['title']}
TYPE: {proj['type']}  |  ESTIMAND: {proj['estimand']}
DATA: {proj['data']}
PATH: {proj['path']}

CURRENT BODY ({wc} words):
{body}

YOUR REWRITE (at most 156 words, 7 sentences):

{rewrite}
"""
        new_entries.append(entry)
        print(f'  [{next_num}/{total}] {name}: {wc}w body, {rw_wc}w rewrite')
        next_num += 1

    # Append to end
    text = text.rstrip() + '\n' + '\n'.join(new_entries) + '\n'

    with open(workbook_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f'\nAppended {len(MISSING_PROJECTS)} new entries')
    print(f'Total entries now: {total}')

    # Verify
    with open(workbook_path, 'r', encoding='utf-8') as f:
        final = f.read()
    entry_count = len(re.findall(r'\[\d+/\d+\]', final))
    filled = 0
    blank = 0
    for sec in re.split(r'={50,}', final):
        m2 = re.search(r'\[\d+/\d+\]', sec)
        if not m2:
            continue
        rw = re.search(r'YOUR REWRITE[^\n]*:\s*\n(.*)', sec, re.DOTALL)
        if rw and len(rw.group(1).strip()) > 10:
            filled += 1
        else:
            blank += 1

    print(f'Verification: {entry_count} entries, {filled} filled, {blank} blank')


if __name__ == '__main__':
    main()
