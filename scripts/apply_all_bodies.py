"""
Apply zero-body data to the workbook - fills in all entries that have
'[No E156 body generated yet]' or capsule template bodies.
Uses the comprehensive data from zero_body_data.py.
"""

import re
import sys
import os

# Import the data
sys.path.insert(0, os.path.dirname(__file__))
from zero_body_data import ZERO_BODY_DATA


def count_words(text):
    return len(text.split())


def main():
    workbook_path = 'C:/E156/rewrite-workbook.txt'

    with open(workbook_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sections = re.split(r'(={50,})', text)

    generated = 0
    capsule_fixed = 0
    skipped = []

    for i, sec in enumerate(sections):
        if re.match(r'={50,}', sec):
            continue

        m = re.search(r'\[(\d+)/302\]\s+(.+)', sec)
        if not m:
            continue

        num, name = int(m.group(1)), m.group(2).strip()
        path_m = re.search(r'PATH:\s*(.+)', sec)
        path = path_m.group(1).strip() if path_m else ''

        has_zero = 'CURRENT BODY (0 words)' in sec or '[No E156 body generated yet]' in sec
        has_capsule = ('reproducibility capsule' in sec.lower() and 'documentation proportion' in sec.lower())

        rw_match = re.search(r'YOUR REWRITE[^\n]*:\s*\n(.*)', sec, re.DOTALL)
        has_rewrite = rw_match and len(rw_match.group(1).strip()) > 10

        if not has_zero and not (has_capsule and not has_rewrite):
            continue

        # Look up in our data
        if name not in ZERO_BODY_DATA:
            skipped.append((num, name))
            continue

        proj = ZERO_BODY_DATA[name]
        body = proj['body']
        rewrite = proj['rewrite']
        wc = count_words(body)

        if has_zero:
            # Replace zero body
            sec = re.sub(
                r'TITLE:\s*.+',
                f'TITLE: {proj["title"]}',
                sec,
                count=1
            )
            sec = re.sub(
                r'TYPE:\s*methods\s*\|\s*ESTIMAND:\s*TBD',
                f'TYPE: {proj.get("type", "methods")}  |  ESTIMAND: {proj.get("estimand", "TBD")}',
                sec
            )
            sec = re.sub(
                r'DATA:\s*TBD',
                f'DATA: {proj.get("data", "TBD")}',
                sec
            )
            sec = re.sub(
                r'CURRENT BODY \(0 words\):\n\[No E156 body generated yet\]',
                f'CURRENT BODY ({wc} words):\n{body}',
                sec
            )
            # Add rewrite
            rw_m = re.search(r'(YOUR REWRITE[^\n]*:\s*\n)', sec)
            if rw_m:
                insert_pos = rw_m.end()
                sec = sec[:insert_pos] + '\n' + rewrite + '\n' + sec[insert_pos:]

            sections[i] = sec
            generated += 1
            print(f'  [{num}] {name}: BODY+REWRITE ({wc} words)')

        elif has_capsule and not has_rewrite:
            # Replace capsule body
            body_match = re.search(r'(CURRENT BODY \(\d+ words\):\n)(.*?)(?=YOUR REWRITE)', sec, re.DOTALL)
            if body_match:
                sec = sec[:body_match.start()] + f'CURRENT BODY ({wc} words):\n{body}\n\n' + sec[body_match.end():]
            # Replace metadata
            sec = re.sub(
                r'TITLE:\s*.+',
                f'TITLE: {proj["title"]}',
                sec,
                count=1
            )
            # Add rewrite
            rw_m = re.search(r'(YOUR REWRITE[^\n]*:\s*\n)', sec)
            if rw_m:
                insert_pos = rw_m.end()
                sec = sec[:insert_pos] + '\n' + rewrite + '\n' + sec[insert_pos:]

            sections[i] = sec
            capsule_fixed += 1
            print(f'  [{num}] {name}: CAPSULE FIXED ({wc} words)')

    # Write output
    output = ''.join(sections)
    with open(workbook_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f'\nZero-body entries filled: {generated}')
    print(f'Capsule entries fixed: {capsule_fixed}')
    print(f'Skipped (no data): {len(skipped)}')
    if skipped:
        print('Skipped entries:')
        for num, name in skipped:
            print(f'  [{num}] {name}')


if __name__ == '__main__':
    main()
