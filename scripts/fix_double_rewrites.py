"""Fix entries where the rewrite section has duplicate content (body + rewrite concatenated)."""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from zero_body_data import ZERO_BODY_DATA


def count_words(text):
    return len(text.split())


def main():
    workbook_path = 'C:/E156/rewrite-workbook.txt'

    with open(workbook_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sections = re.split(r'(={50,})', text)
    fixed = 0

    for i, sec in enumerate(sections):
        if re.match(r'={50,}', sec):
            continue

        m = re.search(r'\[(\d+)/\d+\]\s+(.+)', sec)
        if not m:
            continue
        num, name = int(m.group(1)), m.group(2).strip()

        # Check rewrite word count
        rw = re.search(r'YOUR REWRITE[^\n]*:\s*\n(.*)', sec, re.DOTALL)
        if not rw:
            continue
        rewrite_text = rw.group(1).strip()
        wc = count_words(rewrite_text)

        if wc <= 170:
            continue

        # This entry has inflated rewrite - fix it
        # If we have data for it, use the correct rewrite
        if name in ZERO_BODY_DATA:
            correct_rewrite = ZERO_BODY_DATA[name]['rewrite']
        else:
            # Take just the first ~156 words worth of sentences
            # Split on sentence boundaries and take first 7
            temp = rewrite_text.replace('e.g.', 'e_g_').replace('i.e.', 'i_e_')
            sents = re.split(r'(?<=[.?!])\s+(?=[A-Z])', temp)
            sents = [s.replace('e_g_', 'e.g.').replace('i_e_', 'i.e.') for s in sents]
            # Take first 7 sentences
            if len(sents) > 7:
                correct_rewrite = ' '.join(sents[:7])
            else:
                correct_rewrite = ' '.join(sents)

        # Ensure under 156 words
        words = correct_rewrite.split()
        if len(words) > 156:
            # Trim to last sentence ending before 156 words
            text_156 = ' '.join(words[:156])
            last_period = text_156.rfind('.')
            if last_period > len(text_156) * 0.6:
                correct_rewrite = text_156[:last_period + 1]

        # Replace in section
        rw_header = re.search(r'(YOUR REWRITE[^\n]*:\s*\n)', sec)
        if rw_header:
            sec = sec[:rw_header.end()] + '\n' + correct_rewrite + '\n'
            sections[i] = sec
            new_wc = count_words(correct_rewrite)
            print(f'  [{num}] {name}: {wc}w -> {new_wc}w')
            fixed += 1

    output = ''.join(sections)
    with open(workbook_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f'\nFixed {fixed} entries')


if __name__ == '__main__':
    main()
