"""Auto-merge rewrites to exactly 7 sentences, ≤156 words, preserving user's voice."""
import sys, re
sys.path.insert(0, 'C:/E156/scripts')
from validate_e156 import split_sentences

WORKBOOK = 'C:/E156/rewrite-workbook.txt'

def count_words(t): return len(t.split())

def merge_to_seven(sentences):
    """Merge a list of >7 sentences down to exactly 7 by joining shortest adjacent pairs."""
    sents = list(sentences)
    while len(sents) > 7:
        # Find the shortest adjacent pair to merge
        best_idx = None
        best_len = float('inf')
        for i in range(len(sents) - 1):
            # Don't merge S1 (question) with S2 unless desperate
            # Don't merge across S4 (result) boundary if possible
            combined = count_words(sents[i]) + count_words(sents[i+1])
            # Prefer merging shorter pairs
            if combined < best_len:
                # Slight penalty for merging S1 (index 0) — preserve the question
                penalty = 10 if i == 0 else 0
                # Slight penalty for merging the last sentence (limitation)
                penalty += 5 if i+1 == len(sents)-1 else 0
                if combined + penalty < best_len:
                    best_len = combined + penalty
                    best_idx = i

        if best_idx is None:
            best_idx = len(sents) - 2

        # Merge sents[best_idx] and sents[best_idx+1]
        s1 = sents[best_idx].rstrip()
        s2 = sents[best_idx + 1]

        # Choose connector based on context
        # If s1 ends with period and s2 starts with a continuation word
        continuation_words = {'this', 'it', 'the', 'these', 'those', 'such',
                              'however', 'further', 'thus', 'our', 'we', 'its',
                              'there', 'that', 'each', 'all', 'both', 'using',
                              'across', 'among', 'between', 'for', 'in', 'a', 'an',
                              'no', 'only', 'of'}
        first_word = s2.split()[0].lower() if s2.split() else ''

        if s1.endswith('.'):
            s1_base = s1[:-1].rstrip()
            if first_word in continuation_words:
                # Join with comma + lowercase
                s2_lower = s2[0].lower() + s2[1:]
                merged = s1_base + ', ' + s2_lower
            elif first_word in {'and', 'but', 'or', 'while', 'with', 'yet'}:
                # Already has connector
                s2_lower = s2[0].lower() + s2[1:]
                merged = s1_base + ' ' + s2_lower
            else:
                # Join with semicolon
                s2_lower = s2[0].lower() + s2[1:]
                merged = s1_base + '; ' + s2_lower
        elif s1.endswith('?'):
            # Don't merge questions easily — use semicolon
            s2_lower = s2[0].lower() + s2[1:]
            merged = s1[:-1] + ', and ' + s2_lower
        else:
            # No terminal punctuation — just join
            merged = s1 + ' ' + s2

        sents[best_idx] = merged
        del sents[best_idx + 1]

    return sents


def trim_to_156(sentences, target=156):
    """If total words > target, trim filler words from longest sentences."""
    total = sum(count_words(s) for s in sentences)
    if total <= target:
        return sentences

    # Simple trimming: remove common filler phrases
    fillers = [
        (r'\balso\b', ''),
        (r'\bthen\b', ''),
        (r'\bin total\b', ''),
        (r'\bat this time\b', ''),
        (r'\bof these\b', ''),
        (r'\bhowever,?\s*', ''),
        (r'\bfurthermore,?\s*', ''),
        (r'\badditionally,?\s*', ''),
        (r'\bmoreover,?\s*', ''),
        (r'\bin turn\b', ''),
        (r'\bthat is\b', ''),
        (r'\bwe found that\b', 'we found'),
        (r'\bwas found to be\b', 'was'),
        (r'\bit was shown that\b', ''),
        (r'\ble-one-review-out\b', 'leave-one-out'),
    ]

    result = list(sentences)
    for pattern, repl in fillers:
        total = sum(count_words(s) for s in result)
        if total <= target:
            break
        for i in range(len(result)):
            if total <= target:
                break
            old = result[i]
            new = re.sub(pattern, repl, old, flags=re.IGNORECASE).strip()
            new = re.sub(r'  +', ' ', new)  # clean double spaces
            if new != old:
                result[i] = new
                total = sum(count_words(s) for s in result)

    return result


def fix_rewrite(body):
    """Fix a rewrite body to be exactly 7 sentences, ≤156 words."""
    if not body.strip():
        return None

    sents = split_sentences(body)
    wc = count_words(body)

    if len(sents) == 7 and wc <= 156:
        return None  # Already valid

    # Merge to 7 sentences
    if len(sents) > 7:
        sents = merge_to_seven(sents)
    elif len(sents) < 7:
        # Too few sentences — can't split automatically, skip
        return None

    # Trim if over 156
    sents = trim_to_156(sents)

    result = ' '.join(s.strip() for s in sents)
    # Clean up
    result = re.sub(r'  +', ' ', result)
    result = re.sub(r' ,', ',', result)
    result = re.sub(r',\s*,', ',', result)

    # Final check
    final_sents = split_sentences(result)
    final_wc = count_words(result)

    if len(final_sents) == 7 and final_wc <= 156:
        return result
    else:
        return None  # Couldn't fix automatically


# Main
with open(WORKBOOK, 'r', encoding='utf-8') as f:
    text = f.read()

# Parse entries
blocks = re.split(r'(={50,})', text)
fixed = 0
failed = 0
already_ok = 0

new_text = []
for i, block in enumerate(blocks):
    if '={50,}' in block or not re.search(r'\[\d+/\d+\]', block):
        new_text.append(block)
        continue

    # Find YOUR REWRITE section
    rewrite_match = re.search(
        r'(YOUR REWRITE \(at most 156 words, 7 sentences\):\n)(.*?)(\n*$)',
        block, re.DOTALL
    )

    if not rewrite_match:
        new_text.append(block)
        continue

    body = rewrite_match.group(2).strip()
    if not body or body == '[No E156 body generated yet]':
        new_text.append(block)
        continue

    sents = split_sentences(body)
    wc = count_words(body)

    if len(sents) == 7 and wc <= 156:
        already_ok += 1
        new_text.append(block)
        continue

    # Try to fix
    fixed_body = fix_rewrite(body)
    if fixed_body:
        # Replace the rewrite section
        prefix = block[:rewrite_match.start(2)]
        suffix = block[rewrite_match.end(2):]
        new_block = prefix + '\n' + fixed_body + '\n' + suffix
        new_text.append(new_block)
        fixed += 1

        # Get entry name for reporting
        nm = re.search(r'\[\d+/\d+\]\s+(\S+)', block)
        name = nm.group(1) if nm else '?'
        new_sents = split_sentences(fixed_body)
        new_wc = count_words(fixed_body)
        print(f'  FIXED: {name:35s} {len(sents)}s/{wc}w -> {len(new_sents)}s/{new_wc}w')
    else:
        failed += 1
        nm = re.search(r'\[\d+/\d+\]\s+(\S+)', block)
        name = nm.group(1) if nm else '?'
        print(f'  SKIP:  {name:35s} {len(sents)}s/{wc}w (could not auto-fix)')
        new_text.append(block)

result = ''.join(new_text)

with open(WORKBOOK, 'w', encoding='utf-8') as f:
    f.write(result)

print(f'\nDone: {fixed} fixed, {already_ok} already OK, {failed} could not auto-fix')
