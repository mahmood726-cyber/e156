"""Append 13 evidence reversal E156 papers to the workbook, then rebuild the library."""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from reversal_e156_data import REVERSAL_PAPERS


def count_words(text):
    return len(text.split())


def main():
    workbook_path = 'C:/E156/rewrite-workbook.txt'

    with open(workbook_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find current max entry number and total
    max_num = 0
    for m in re.finditer(r'\[(\d+)/\d+\]', text):
        n = int(m.group(1))
        if n > max_num:
            max_num = n

    # Find the current total from header
    total_m = re.search(r'Total projects:\s*(\d+)', text)
    old_total = int(total_m.group(1)) if total_m else max_num

    new_total = old_total + len(REVERSAL_PAPERS)

    # Update all existing [N/OLD] to [N/NEW]
    text = re.sub(rf'\[(\d+)/{old_total}\]', lambda m: f'[{m.group(1)}/{new_total}]', text)
    text = text.replace(f'Total projects: {old_total}', f'Total projects: {new_total}')

    # Build new entries
    next_num = max_num + 1
    new_entries = []

    for name, proj in REVERSAL_PAPERS.items():
        body = proj['body']
        rewrite = proj['rewrite']
        wc_body = count_words(body)
        wc_rewrite = count_words(rewrite)

        entry = f"""
======================================================================

[{next_num}/{new_total}] {name}
TITLE: {proj['title']}
TYPE: {proj['type']}  |  ESTIMAND: {proj['estimand']}
DATA: {proj['data']}
PATH: {proj['path']}

CURRENT BODY ({wc_body} words):
{body}

YOUR REWRITE (at most 156 words, 7 sentences):

{rewrite}
"""
        new_entries.append(entry)
        print(f'  [{next_num}/{new_total}] {name}: {wc_body}w body, {wc_rewrite}w rewrite')
        next_num += 1

    # Append
    text = text.rstrip() + '\n' + '\n'.join(new_entries) + '\n'

    with open(workbook_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f'\nAppended {len(REVERSAL_PAPERS)} reversal papers')
    print(f'Total entries now: {new_total}')

    # Rebuild library
    print('\nRebuilding library...')
    from build_library import build
    entries = build()
    print(f'Library rebuilt with {len(entries)} entries')


if __name__ == '__main__':
    main()
