"""Fix remaining failing entries: merge to 7 sentences AND trim to ≤156 words."""
import sys, re
sys.path.insert(0, 'C:/E156/scripts')
from validate_e156 import split_sentences

WORKBOOK = 'C:/E156/rewrite-workbook.txt'

def count_words(t): return len(t.split())

def merge_pair(s1, s2):
    """Merge two sentences into one."""
    s1 = s1.rstrip()
    s2_first = s2.split()[0].lower() if s2.split() else ''

    joiners = {'this', 'it', 'the', 'these', 'those', 'our', 'we', 'its',
               'there', 'that', 'each', 'all', 'both', 'no', 'only', 'a', 'an',
               'using', 'across', 'among', 'for', 'in', 'of', 'from'}

    if s1.endswith('.'):
        s1_base = s1[:-1]
        s2_lower = s2[0].lower() + s2[1:]
        if s2_first in joiners:
            return s1_base + ', ' + s2_lower
        elif s2_first in {'and', 'but', 'or', 'while', 'with', 'yet'}:
            return s1_base + ' ' + s2_lower
        else:
            return s1_base + '; ' + s2_lower
    elif s1.endswith('?'):
        s2_lower = s2[0].lower() + s2[1:]
        return s1[:-1] + ', and ' + s2_lower
    else:
        return s1 + ' ' + s2

def trim_words(text, target=156):
    """Remove filler words to get under target."""
    fillers = [
        (r'\bin total\b', ''),
        (r'\bat this time\b', ''),
        (r' also ', ' '),
        (r' then ', ' '),
        (r' further ', ' '),
        (r' fully ', ' '),
        (r' currently ', ' '),
        (r' very ', ' '),
        (r'However, ', ''),
        (r'however, ', ''),
        (r'Furthermore, ', ''),
        (r'Additionally, ', ''),
        (r' fundamental ', ' '),
        (r' substantially ', ' '),
        (r' significantly ', ' '),
        (r' specifically ', ' '),
        (r' generally ', ' '),
        (r' approximately ', ' ~'),
        (r' particular ', ' '),
        (r' of these ', ' '),
        (r'We found that ', ''),
        (r'we found that ', ''),
        (r'It was found that ', ''),
        (r' which is ', ' '),
        (r' that are ', ' '),
        (r' of the ', ' of '),
        (r' all of ', ' all '),
        (r' each of ', ' each '),
        (r' available ', ' '),
        (r' published ', ' '),
        (r' potential ', ' '),
    ]
    result = text
    for pat, repl in fillers:
        if count_words(result) <= target:
            break
        new = re.sub(pat, repl, result, count=1)
        new = re.sub(r'  +', ' ', new).strip()
        if len(split_sentences(new)) == len(split_sentences(result)):
            result = new
    return result

def fix_entry(body):
    """Full fix: merge to 7 sentences, trim to ≤156 words."""
    sents = split_sentences(body)
    wc = count_words(body)

    if len(sents) == 7 and wc <= 156:
        return None  # Already OK

    # First: merge to 7 if needed
    while len(sents) > 7:
        # Find shortest adjacent pair (avoid S1 and last)
        best_i = None
        best_cost = float('inf')
        for i in range(len(sents) - 1):
            cost = count_words(sents[i]) + count_words(sents[i+1])
            if i == 0: cost += 10
            if i + 1 == len(sents) - 1: cost += 5
            if cost < best_cost:
                best_cost = cost
                best_i = i
        sents[best_i] = merge_pair(sents[best_i], sents[best_i + 1])
        del sents[best_i + 1]

    if len(sents) < 7:
        return None  # Can't split

    result = ' '.join(s.strip() for s in sents)
    result = re.sub(r'  +', ' ', result).strip()

    # Trim if over 156
    if count_words(result) > 156:
        result = trim_words(result, 156)

    # Final validation
    final_sents = split_sentences(result)
    final_wc = count_words(result)

    if len(final_sents) == 7 and final_wc <= 156:
        return result
    return None

# Main
with open(WORKBOOK, 'r', encoding='utf-8') as f:
    text = f.read()

# Process each entry
entry_pattern = re.compile(
    r'(\[\d+/\d+\]\s+(\S+).*?YOUR REWRITE \(at most 156 words, 7 sentences\):\n)(.*?)(\n={50,}|\Z)',
    re.DOTALL
)

fixed = 0
stuck = 0
replacements = []

for m in entry_pattern.finditer(text):
    name = m.group(2)
    body = m.group(3).strip()
    if not body or body == '[No E156 body generated yet]':
        continue

    sents = split_sentences(body)
    wc = count_words(body)

    if len(sents) == 7 and wc <= 156:
        continue  # OK

    fixed_body = fix_entry(body)
    if fixed_body:
        replacements.append((m.start(3), m.end(3), name, body, fixed_body, wc, len(sents)))
        new_wc = count_words(fixed_body)
        new_sc = len(split_sentences(fixed_body))
        print(f'  FIXED: {name:40s} {len(sents)}s/{wc}w -> {new_sc}s/{new_wc}w')
        fixed += 1
    else:
        print(f'  STUCK: {name:40s} {len(sents)}s/{wc}w')
        stuck += 1

# Apply in reverse order
for start, end, name, old, new, old_wc, old_sc in reversed(replacements):
    text = text[:start] + '\n' + new + '\n' + text[end:]

with open(WORKBOOK, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'\nFixed {fixed}, stuck {stuck}')
