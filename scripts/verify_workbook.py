"""Final verification of the complete rewrite workbook."""
import re

def count_words(text):
    return len(text.split())

def count_sentences_approx(text):
    text = text.replace('e.g.', 'eg').replace('i.e.', 'ie').replace('vs.', 'vs').replace('et al.', 'etal')
    sents = re.split(r'(?<=[.?!])\s+(?=[A-Z])', text)
    return len([s for s in sents if s.strip()])

with open('C:/E156/rewrite-workbook.txt', 'r', encoding='utf-8') as f:
    text = f.read()

sections = re.split(r'={50,}', text)

total = 0
filled_rewrite = 0
blank_rewrite = 0
has_body = 0
zero_body = 0
capsule_body = 0

word_counts = []
over_156 = []
under_100 = []
sentence_issues = []

for sec in sections:
    m = re.search(r'\[(\d+)/\d+\]\s+(.+)', sec)
    if not m:
        continue
    num, name = int(m.group(1)), m.group(2).strip()
    total += 1

    # Check body
    if 'CURRENT BODY (0 words)' in sec or '[No E156 body generated yet]' in sec:
        zero_body += 1
    elif 'reproducibility capsule' in sec.lower() and 'documentation proportion' in sec.lower():
        # Check if rewrite replaced it
        rw = re.search(r'YOUR REWRITE[^\n]*:\s*\n(.*)', sec, re.DOTALL)
        if rw and len(rw.group(1).strip()) > 10 and 'reproducibility capsule' not in rw.group(1).lower():
            has_body += 1
        else:
            capsule_body += 1
    else:
        has_body += 1

    # Check rewrite
    rw = re.search(r'YOUR REWRITE[^\n]*:\s*\n(.*)', sec, re.DOTALL)
    if rw and len(rw.group(1).strip()) > 10:
        filled_rewrite += 1
        rewrite = rw.group(1).strip()
        wc = count_words(rewrite)
        word_counts.append(wc)
        if wc > 170:
            over_156.append((num, name, wc))
        if wc < 90:
            under_100.append((num, name, wc))
    else:
        blank_rewrite += 1

# Summary
print("=" * 60)
print("REWRITE WORKBOOK VERIFICATION")
print("=" * 60)
print(f"\nTotal entries: {total}")
print(f"\nBODY STATUS:")
print(f"  Has real body: {has_body}")
print(f"  Zero body (empty): {zero_body}")
print(f"  Capsule template (unreplaced): {capsule_body}")
print(f"\nREWRITE STATUS:")
print(f"  Filled: {filled_rewrite}")
print(f"  Blank: {blank_rewrite}")

if word_counts:
    print(f"\nWORD COUNTS:")
    print(f"  Min: {min(word_counts)}")
    print(f"  Max: {max(word_counts)}")
    print(f"  Mean: {sum(word_counts)/len(word_counts):.0f}")
    print(f"  Median: {sorted(word_counts)[len(word_counts)//2]}")

if over_156:
    print(f"\n  Over 170 words ({len(over_156)}):")
    for n, nm, wc in over_156[:10]:
        print(f"    [{n}] {nm}: {wc}")

if under_100:
    print(f"\n  Under 90 words ({len(under_100)}):")
    for n, nm, wc in under_100[:10]:
        print(f"    [{n}] {nm}: {wc}")

# Check for duplicate names
names = []
for sec in sections:
    m = re.search(r'\[\d+/\d+\]\s+(.+)', sec)
    if m:
        names.append(m.group(1).strip())

from collections import Counter
dupes = [(n, c) for n, c in Counter(names).items() if c > 1]
print(f"\nDUPLICATES: {len(dupes)}")
for n, c in dupes:
    print(f"  '{n}' appears {c} times")

# Check total matches header
header_match = re.search(r'Total projects:\s*(\d+)', text)
if header_match:
    header_total = int(header_match.group(1))
    print(f"\nHeader says: {header_total}, Actual: {total}")
    if header_total != total:
        print("  ** MISMATCH! **")

print(f"\n{'PASS' if blank_rewrite == 0 and zero_body == 0 else 'NEEDS WORK'}")
print(f"File size: {len(text):,} bytes")
