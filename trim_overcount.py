"""Trim the 12 entries that are 1-7 words over 156."""
import sys, re
sys.path.insert(0, 'C:/E156/scripts')
from validate_e156 import split_sentences

WORKBOOK = 'C:/E156/rewrite-workbook.txt'

def count_words(t): return len(t.split())

# Trimming rules: remove filler words/phrases one at a time
TRIM_RULES = [
    # (pattern, replacement, description)
    (r'\bin total\b', '', 'remove "in total"'),
    (r'\bat this time\b', '', 'remove "at this time"'),
    (r'\b[Aa]lso\s', ' ', 'remove "also"'),
    (r'\bthen\s', ' ', 'remove "then"'),
    (r'\b[Ff]urther\s', ' ', 'remove "further"'),
    (r'\b[Hh]owever,?\s', '', 'remove "however"'),
    (r'\bfully\s', '', 'remove "fully"'),
    (r'\bcurrently\s', '', 'remove "currently"'),
    (r'\bgenerally\s', '', 'remove "generally"'),
    (r'\bfundamental\s', '', 'remove "fundamental"'),
    (r'\bsubstantially\s', '', 'remove "substantially"'),
    (r'\bsignificantly\s', '', 'remove "significantly"'),
    (r'\bapproximately\s', '~', 'shorten "approximately"'),
    (r'\bspecifically\s', '', 'remove "specifically"'),
    (r'\badditionally,?\s', '', 'remove "additionally"'),
    (r'\bvery\s', '', 'remove "very"'),
    (r'\bof these\b', '', 'remove "of these"'),
    (r'\bthat is\b', '', 'remove "that is"'),
    (r'\bwe found that\b', '', 'remove "we found that"'),
    (r'\bof the\b', 'of', 'shorten "of the" to "of"'),
    (r'\bfor the\b', 'for', 'shorten "for the" to "for"'),
    (r'\bin the\b', 'in', 'shorten "in the" to "in"'),
    (r'\bwhich is\b', '', 'remove "which is"'),
    (r'\bthat are\b', '', 'remove "that are"'),
    (r'\ball of\b', 'all', 'shorten "all of"'),
    (r'\beach of\b', 'each', 'shorten "each of"'),
]

with open(WORKBOOK, 'r', encoding='utf-8') as f:
    text = f.read()

# Find all entries
pattern = r'(\[\d+/\d+\]\s+(\S+).*?YOUR REWRITE \(at most 156 words, 7 sentences\):\n)(.*?)(\n*={50,}|\Z)'
matches = list(re.finditer(pattern, text, re.DOTALL))

changes = []
for m in matches:
    name = m.group(2)
    body = m.group(3).strip()
    if not body or body == '[No E156 body generated yet]':
        continue

    wc = count_words(body)
    sc = len(split_sentences(body))

    if wc <= 156:
        continue

    if sc != 7:
        continue  # Only trim 7-sentence entries

    # Try trimming
    trimmed = body
    for pat, repl, desc in TRIM_RULES:
        if count_words(trimmed) <= 156:
            break
        new = re.sub(pat, repl, trimmed, count=1)
        new = re.sub(r'  +', ' ', new).strip()
        # Make sure we didn't break sentences
        if len(split_sentences(new)) == 7:
            trimmed = new

    new_wc = count_words(trimmed)
    if new_wc <= 156 and trimmed != body:
        changes.append((m.start(3), m.end(3), body, trimmed, name, wc, new_wc))
        print(f'  TRIMMED: {name:35s} {wc}w -> {new_wc}w')
    else:
        over = count_words(trimmed) - 156
        print(f'  STUCK:   {name:35s} {count_words(trimmed)}w (still {over} over)')

# Apply changes in reverse order to preserve positions
for start, end, old, new, name, old_wc, new_wc in reversed(changes):
    text = text[:start] + '\n' + new + '\n' + text[end:]

with open(WORKBOOK, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'\nTrimmed {len(changes)} entries')
