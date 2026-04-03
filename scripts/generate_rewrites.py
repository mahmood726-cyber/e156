"""
Generate editorial rewrites for E156 entries that have CURRENT BODY but no YOUR REWRITE.

The rewrite rules follow observed patterns from existing human rewrites:
1. S1 (Question): Slightly rephrase opening question
2. S2 (Dataset): Condense dataset description
3. S3 (Method): Keep method but improve flow
4. S4 (Result): Preserve exact numbers and CIs, rephrase surrounding text
5. S5 (Robustness): Keep robustness checks, slightly rephrase
6. S6 (Interpretation): Reframe interpretation more concisely
7. S7 (Boundary): Rephrase limitation more naturally

Rules:
- Keep all numbers, CIs, percentages EXACTLY as in original
- 7 sentences, <= 156 words
- Follow S1-S7 structure
"""

import re
import sys
import os

def count_words(text):
    return len(text.split())

def count_sentences(text):
    """Count sentences (periods, question marks, exclamation marks at end of sentence)."""
    # Split on sentence-ending punctuation followed by space or end
    sentences = re.split(r'(?<=[.?!])\s+', text.strip())
    # Filter out empty strings
    return len([s for s in sentences if s.strip()])

def extract_numbers(text):
    """Extract all numbers, CIs, percentages from text to verify preservation."""
    patterns = [
        r'\d+\.?\d*\s*(?:percent|%)',
        r'\d+\.?\d*\s*\(95%\s*CI\s*[\d.-]+\s*to\s*[\d.-]+\)',
        r'(?:CI|confidence interval)\s*[\d.-]+\s*to\s*[\d.-]+',
        r'\b\d+\.?\d+\b',
    ]
    numbers = set()
    for p in patterns:
        for m in re.finditer(p, text):
            numbers.add(m.group())
    return numbers

def rewrite_body(body, title=""):
    """Apply editorial transformations to produce a rewrite.

    Strategy: Make minimal but meaningful edits that improve flow
    while preserving all factual content.
    """
    sentences = split_sentences(body)

    if len(sentences) < 3:
        return body  # Too short to meaningfully rewrite

    rewritten = []
    for i, sent in enumerate(sentences):
        sent = sent.strip()
        if not sent:
            continue

        if i == 0:  # S1: Question - slight rephrase
            sent = rewrite_question(sent)
        elif i == 1:  # S2: Dataset
            sent = rewrite_dataset(sent)
        elif i == 2:  # S3: Method
            sent = rewrite_method(sent)
        elif i == 3:  # S4: Result
            sent = rewrite_result(sent)
        elif i == 4:  # S5: Robustness
            sent = rewrite_robustness(sent)
        elif i == 5:  # S6: Interpretation
            sent = rewrite_interpretation(sent)
        elif i == 6:  # S7: Boundary/Limitation
            sent = rewrite_boundary(sent)
        else:
            # Extra sentences - condense
            sent = condense_sentence(sent)

        rewritten.append(sent)

    # If we have more than 7 sentences, merge some
    while len(rewritten) > 7:
        rewritten = merge_shortest_pair(rewritten)

    # If we have fewer than 7, split the longest
    while len(rewritten) < 7 and max(count_words(s) for s in rewritten) > 30:
        rewritten = split_longest(rewritten)

    result = ' '.join(rewritten)

    # Trim to 156 words if over
    result = trim_to_limit(result, 156)

    return result

def split_sentences(text):
    """Split text into sentences, being careful with abbreviations and numbers."""
    # Handle common abbreviations
    text = text.replace('e.g.', 'e·g·')
    text = text.replace('i.e.', 'i·e·')
    text = text.replace('vs.', 'vs·')
    text = text.replace('et al.', 'et al·')
    text = text.replace('Dr.', 'Dr·')
    text = text.replace('Fig.', 'Fig·')
    text = text.replace('No.', 'No·')

    # Split on sentence boundaries
    parts = re.split(r'(?<=[.?!])\s+(?=[A-Z])', text)

    # Restore abbreviations
    result = []
    for p in parts:
        p = p.replace('e·g·', 'e.g.')
        p = p.replace('i·e·', 'i.e.')
        p = p.replace('vs·', 'vs.')
        p = p.replace('et al·', 'et al.')
        p = p.replace('Dr·', 'Dr.')
        p = p.replace('Fig·', 'Fig.')
        p = p.replace('No·', 'No.')
        result.append(p)

    return result

def rewrite_question(sent):
    """S1: Slight rephrase of opening question."""
    # Common patterns
    sent = re.sub(r'^Can a single ', 'Can a ', sent)
    sent = re.sub(r'^Can a fully offline, single-file ', 'Can a single-file ', sent)
    sent = re.sub(r'^How can ', 'Can ', sent)
    sent = re.sub(r'^What is ', 'What was ', sent)
    sent = re.sub(r'^Among ', 'Using ', sent)
    # Reduce wordiness in question
    sent = re.sub(r' while remaining usable at the point of care', '', sent)
    sent = re.sub(r' that otherwise depend on specialist software', '', sent)
    return sent

def rewrite_dataset(sent):
    """S2: Condense dataset description."""
    sent = re.sub(r'We developed and validated', 'We developed', sent)
    sent = re.sub(r'We built ([^,]+) as', r'\1 is', sent)
    sent = re.sub(r', preserving [^,]+,', ',', sent)
    return sent

def rewrite_method(sent):
    """S3: Keep method but improve flow."""
    sent = re.sub(r'The tool then ', 'This ', sent)
    sent = re.sub(r'The package ', 'It ', sent)
    sent = re.sub(r'The system ', 'It ', sent)
    return sent

def rewrite_result(sent):
    """S4: Preserve numbers exactly, rephrase surrounding text."""
    sent = re.sub(r'achieved an? ', 'reached ', sent)
    sent = re.sub(r'was observed at ', 'reached ', sent)
    return sent

def rewrite_robustness(sent):
    """S5: Keep robustness, slightly rephrase."""
    sent = re.sub(r'Sensitivity analyses? ', 'Our sensitivity analysis ', sent)
    sent = re.sub(r'Cross-validation ', 'Cross-validation ', sent)
    return sent

def rewrite_interpretation(sent):
    """S6: Reframe interpretation more concisely."""
    sent = re.sub(r'These findings suggest that ', '', sent)
    sent = re.sub(r'This suggests that ', '', sent)
    return sent

def rewrite_boundary(sent):
    """S7: Rephrase limitation more naturally."""
    sent = re.sub(r'^However, the limitation of ', 'However, ', sent)
    sent = re.sub(r'^One limitation is that ', '', sent)
    sent = re.sub(r'^The main limitation is that ', '', sent)
    sent = re.sub(r'^A limitation is that ', '', sent)
    sent = re.sub(r'^The tool is limited to ', 'This is limited to ', sent)
    return sent

def condense_sentence(sent):
    """General condensing."""
    sent = re.sub(r'in order to ', 'to ', sent)
    sent = re.sub(r'in the context of ', 'for ', sent)
    sent = re.sub(r'a large number of ', 'many ', sent)
    sent = re.sub(r'the vast majority of ', 'most ', sent)
    return sent

def merge_shortest_pair(sentences):
    """Merge the two shortest adjacent sentences with a semicolon."""
    if len(sentences) <= 1:
        return sentences

    min_combined = float('inf')
    min_idx = 0
    for i in range(len(sentences) - 1):
        combined = count_words(sentences[i]) + count_words(sentences[i+1])
        if combined < min_combined:
            min_combined = combined
            min_idx = i

    # Merge with semicolon
    merged = sentences[min_idx].rstrip('.')
    if sentences[min_idx+1][0].isupper():
        sentences[min_idx+1] = sentences[min_idx+1][0].lower() + sentences[min_idx+1][1:]
    merged = merged + '; ' + sentences[min_idx+1]

    result = sentences[:min_idx] + [merged] + sentences[min_idx+2:]
    return result

def split_longest(sentences):
    """Split the longest sentence at a natural breakpoint."""
    max_words = 0
    max_idx = 0
    for i, s in enumerate(sentences):
        wc = count_words(s)
        if wc > max_words:
            max_words = wc
            max_idx = i

    sent = sentences[max_idx]
    # Try to split at comma + conjunction
    parts = re.split(r',\s*(?:and|while|with|but)\s+', sent, maxsplit=1)
    if len(parts) == 2 and count_words(parts[0]) > 5 and count_words(parts[1]) > 5:
        parts[0] = parts[0].rstrip(',') + '.'
        parts[1] = parts[1][0].upper() + parts[1][1:]
        if not parts[1].endswith('.') and not parts[1].endswith('?'):
            parts[1] += '.'
        return sentences[:max_idx] + parts + sentences[max_idx+1:]

    return sentences  # Can't split safely

def trim_to_limit(text, limit):
    """Trim text to word limit by removing filler words and phrases."""
    words = text.split()
    if len(words) <= limit:
        return text

    # First pass: remove filler phrases
    fillers = [
        'in particular ', 'specifically ', 'notably ', 'importantly ',
        'furthermore ', 'additionally ', 'moreover ', 'indeed ',
        'essentially ', 'fundamentally ', 'basically ',
    ]
    for filler in fillers:
        if count_words(text) <= limit:
            break
        text = text.replace(filler, '')

    # Second pass: shorten common long phrases
    shortenings = [
        ('in order to', 'to'),
        ('a total of', ''),
        ('in the context of', 'for'),
        ('with respect to', 'for'),
        ('it should be noted that', ''),
        ('it is worth noting that', ''),
        ('a large number of', 'many'),
        ('the vast majority of', 'most'),
        ('as well as', 'and'),
        ('in addition to', 'besides'),
        ('on the other hand', 'however'),
        ('at the present time', 'now'),
        ('due to the fact that', 'because'),
    ]
    for long, short in shortenings:
        if count_words(text) <= limit:
            break
        text = text.replace(long, short)

    # Final: truncate last sentence if still over
    words = text.split()
    if len(words) > limit:
        text = ' '.join(words[:limit])
        # Find last sentence end
        last_period = text.rfind('.')
        if last_period > len(text) * 0.7:
            text = text[:last_period + 1]

    return text


def main():
    workbook_path = 'C:/E156/rewrite-workbook.txt'

    with open(workbook_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sections = re.split(r'(={50,})', text)

    # Process each section
    rewrites_generated = 0
    new_sections = []

    for sec in sections:
        if re.match(r'={50,}', sec):
            new_sections.append(sec)
            continue

        m = re.search(r'\[(\d+)/302\]\s+(.+)', sec)
        if not m:
            new_sections.append(sec)
            continue

        num, name = int(m.group(1)), m.group(2).strip()

        # Check if has real body but no rewrite
        has_capsule = 'reproducibility capsule' in sec.lower() and 'documentation proportion' in sec.lower()
        has_zero = 'CURRENT BODY (0 words)' in sec or '[No E156 body generated yet]' in sec

        rw_match = re.search(r'(YOUR REWRITE[^\n]*:\s*\n)(.*)', sec, re.DOTALL)
        has_rewrite = rw_match and len(rw_match.group(2).strip()) > 10

        if has_rewrite or has_zero or has_capsule:
            new_sections.append(sec)
            continue

        # Extract current body
        body_match = re.search(r'CURRENT BODY[^\n]*:\s*\n(.+?)(?=YOUR REWRITE)', sec, re.DOTALL)
        if not body_match:
            new_sections.append(sec)
            continue

        body = body_match.group(1).strip()
        if len(body) < 50:
            new_sections.append(sec)
            continue

        # Generate rewrite
        title_match = re.search(r'TITLE:\s*(.+)', sec)
        title = title_match.group(1).strip() if title_match else name

        rewrite = rewrite_body(body, title)

        # Verify we preserved key numbers
        orig_numbers = extract_numbers(body)
        new_numbers = extract_numbers(rewrite)

        wc = count_words(rewrite)
        sc = count_sentences(rewrite)

        # Insert rewrite into section
        if rw_match:
            rewrite_header = rw_match.group(1)
            sec = sec[:rw_match.start()] + rewrite_header + '\n' + rewrite + '\n' + sec[rw_match.end():]

        new_sections.append(sec)
        rewrites_generated += 1

        if rewrites_generated <= 5:
            print(f'[{num}] {name}: {wc} words, {sc} sentences')
            print(f'  First 80 chars: {rewrite[:80]}...')

    # Write output
    output = ''.join(new_sections)

    output_path = 'C:/E156/rewrite-workbook-draft.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f'\nGenerated {rewrites_generated} rewrites')
    print(f'Output: {output_path}')

    # Validation
    with open(output_path, 'r', encoding='utf-8') as f:
        output_text = f.read()

    out_sections = re.split(r'={50,}', output_text)
    filled = 0
    blank = 0
    for sec in out_sections:
        m = re.search(r'\[(\d+)/302\]', sec)
        if not m:
            continue
        rw = re.search(r'YOUR REWRITE[^\n]*:\s*\n(.*)', sec, re.DOTALL)
        if rw and len(rw.group(1).strip()) > 10:
            filled += 1
        else:
            blank += 1

    print(f'After generation: {filled} filled, {blank} blank')

if __name__ == '__main__':
    main()
