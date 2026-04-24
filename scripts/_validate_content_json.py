"""
Validate a generated article-content JSON file against CONTENT_PROMPT.md rules.
Returns exit code 0 if clean, 1 with violations printed if dirty.

Run with UTF-8 output on Windows: prepend PYTHONIOENCODING=utf-8 or use the
reconfigure call below.

Usage:
  python scripts/_validate_content_json.py scripts/_gen_business/L01.json
  python scripts/_validate_content_json.py scripts/_gen_business/*.json
"""
import sys, json, re, os, glob
from pathlib import Path

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Banned patterns — fail the validation if any of these appear anywhere in content
BANNED_PATTERNS = [
    (re.compile(r"\bAQA\s+[0-9]{4}\b"), "spec code: AQA NNNN"),
    (re.compile(r"\bOCR\s+J[0-9]{3,}\b"), "spec code: OCR JNNN"),
    (re.compile(r"\bEdexcel\s+[0-9][A-Z]{2}[0-9]\b"), "spec code: Edexcel NXXN"),
    (re.compile(r"\bEduqas\s+C[0-9]{3}U\b"), "spec code: Eduqas CXXXU"),
    (re.compile(r"\bNCFE\s+603/[0-9]+"), "spec code: NCFE 603/..."),
    (re.compile(r"\bComponent\s+[0-9][a-z]?\b", re.IGNORECASE), "component code"),
    (re.compile(r"\bPaper\s+[0-9][A-Z]?\s+Section\b"), "paper section code"),
    (re.compile(r"\bLevel\s+[1-9]\b"), "Level N descriptor"),
    (re.compile(r"Nothing worthy of credit", re.IGNORECASE), "exam board rubric phrase"),
    (re.compile(r"Award\s+[0-9]+\s+marks\s+for", re.IGNORECASE), "mark-award rubric phrase"),
    (re.compile(r"\bAO[1-4]\.[0-9]?"), "AO code"),
]

# Required structural patterns in content_html
REQUIRED_PATTERNS = [
    (re.compile(r'class="key-fact"'), 2, "key-fact divs"),
    (re.compile(r'class="collapsible"'), 2, "collapsible divs"),
    (re.compile(r'class="term"'), 3, "dfn term glossary entries"),
    (re.compile(r'data-narration-id'), 10, "narration IDs (heuristic min)"),
]

# Flashcard-specific patterns (enforced per FLASHCARD_RULES.md)
FC_ENUM_PATTERN = re.compile(r',\s+\w+\s+(and|plus)\s+\w+', re.IGNORECASE)  # "X, Y and Z" lists
# Allow single-word answers if the question starts with any W-question or a
# common imperative (Name/Give/Define/State/List one). This catches "Who..." /
# "What colour..." / "What name..." / "When..." variants without over-matching.
FC_SINGLE_WORD_OK_Q = re.compile(r'^(what|who|when|where|which|why|how|name|give|define|state|list|in (which|what))\b', re.IGNORECASE)


def validate_flashcards(fc_list):
    """Enforce FLASHCARD_RULES.md hard rules. Returns list of violations."""
    violations = []
    if not isinstance(fc_list, list):
        return ["flashcard_questions is not a list"]

    answers_seen = []
    card_types_seen = set()

    for i, card in enumerate(fc_list):
        if not isinstance(card, dict):
            violations.append(f"FC[{i}]: not a dict")
            continue
        q = (card.get('q') or '').strip()
        a = (card.get('a') or '').strip()

        if not q or not a:
            violations.append(f"FC[{i}]: missing q or a")
            continue

        # Rule 7 — answer length
        a_words = len(re.findall(r"\S+", a))
        if a_words > 30:
            violations.append(f"FC[{i}] answer too long: {a_words} words (hard cap 30): '{a[:60]}...'")

        # Anti-fragment — question must be substantive. Allow short "What is X?"
        # / "Who is X?" patterns (3-4 words) since those are legitimate card forms.
        q_words = len(re.findall(r"\S+", q))
        # Real fragment markers: blank lines, underscores, ellipses, unescaped HTML
        is_fragment = bool(re.search(r'_{3,}|\.{3,}$|^\s*[a-z]', q)) or q.endswith('.')
        if q_words < 3 or (q_words < 5 and is_fragment):
            violations.append(f"FC[{i}] question too short/fragment: {q_words} words ('{q}'). Needs substantive question.")

        # Rule 2 — enumeration detection. Only flag if the answer is primarily a
        # list (short answer with "X, Y and Z" as the whole payload). Longer
        # definitions that happen to include illustrative lists are fine —
        # the card is testing the concept, not the list membership.
        if a_words <= 12 and FC_ENUM_PATTERN.search(a):
            violations.append(f"FC[{i}] answer has enumeration pattern: '{a[:60]}...'. Split into separate cards.")

        # Single-word answer only allowed if question pattern invites it
        if a_words == 1 and not (FC_SINGLE_WORD_OK_Q.search(q) or re.match(r'^\d', a)):
            violations.append(f"FC[{i}] single-word answer '{a}' — question '{q[:50]}' must start with 'What is/Who was/When/Name' etc., or answer must be a number/date.")

        # Rule — answer not a substring of question (card-restating-itself)
        if len(a) > 4 and a.lower() in q.lower():
            violations.append(f"FC[{i}] answer appears in question: q='{q[:50]}', a='{a}'")

        # Duplicate answer detection (Rule 4 — interference surrogate)
        a_norm = a.lower().strip('.,!? ')
        if a_norm in answers_seen:
            violations.append(f"FC[{i}] duplicate answer '{a}' — creates interference with earlier card")
        answers_seen.append(a_norm)

        # Track card type for diversity check
        if re.match(r'^(what is|what does)', q, re.IGNORECASE):
            card_types_seen.add('term_def')
        elif re.search(r'\bwhen\b|\bdate\b|\byear\b', q, re.IGNORECASE):
            card_types_seen.add('date')
        elif re.search(r'\bwho\b', q, re.IGNORECASE):
            card_types_seen.add('person')
        elif '___' in q or '_____' in q:
            card_types_seen.add('cloze')
        elif re.search(r'\bwhy\b|\bhow\b|\bwhat effect\b', q, re.IGNORECASE):
            card_types_seen.add('causal')
        else:
            card_types_seen.add('other')

    # Rule — at least 2 distinct card types (diversity)
    if len(fc_list) >= 8 and len(card_types_seen) < 2:
        violations.append(f"flashcards all one type ({card_types_seen}). Mix at least 2 types per FLASHCARD_RULES.md.")

    return violations


def validate_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    violations = []

    # Check required top-level keys
    required_keys = ['description', 'content_html', 'exam_tip_html', 'conclusion_html',
                     'practice_questions', 'knowledge_checks', 'flashcard_questions',
                     'glossary_terms', 'hero_keywords', 'hero_image_caption']
    for k in required_keys:
        if k not in data:
            violations.append(f"MISSING REQUIRED KEY: {k}")

    # Description length
    desc = data.get('description', '')
    if not (60 <= len(desc) <= 120):
        violations.append(f"description length {len(desc)} (want 60-100, 120 tolerated)")

    # Counts
    pq = data.get('practice_questions', [])
    if len(pq) != 6:
        violations.append(f"practice_questions count {len(pq)}, want 6")
    kc = data.get('knowledge_checks', [])
    if len(kc) != 5:
        violations.append(f"knowledge_checks count {len(kc)}, want 5")
    fc = data.get('flashcard_questions', [])
    # Post-retrofit: 8-15 cards per FLASHCARD_RULES.md. Tolerate down to 6
    # for lean lessons with agent justification, up to 18 for content-dense
    # subjects (Science).
    if len(fc) < 6 or len(fc) > 18:
        violations.append(f"flashcard_questions count {len(fc)}, want 8-15 (soft 6-18)")
    fc_violations = validate_flashcards(fc)
    violations.extend(fc_violations)

    # KC type distribution
    kc_types = [c.get('type') for c in kc]
    if kc_types.count('mcq') != 2:
        violations.append(f"knowledge_checks MCQ count {kc_types.count('mcq')}, want 2")
    if kc_types.count('fill') != 2:
        violations.append(f"knowledge_checks fill count {kc_types.count('fill')}, want 2")
    if kc_types.count('match') != 1:
        violations.append(f"knowledge_checks match count {kc_types.count('match')}, want 1")

    # Scan all text fields for banned patterns
    all_text_fields = ['description', 'content_html', 'exam_tip_html', 'conclusion_html', 'hero_image_caption']
    blob = ' '.join(str(data.get(f) or '') for f in all_text_fields)
    for pq_item in pq:
        blob += ' ' + str(pq_item.get('text', '')) + ' ' + str(pq_item.get('type', '')) + ' ' + str(pq_item.get('marks', ''))
    for kc_item in kc:
        blob += ' ' + str(kc_item.get('q', ''))

    for pattern, label in BANNED_PATTERNS:
        matches = pattern.findall(blob)
        if matches:
            violations.append(f"BANNED ({label}): {set(matches)}")

    # Structural minima in content_html
    content = data.get('content_html', '')
    for pattern, min_count, label in REQUIRED_PATTERNS:
        count = len(pattern.findall(content))
        if count < min_count:
            violations.append(f"insufficient {label}: found {count}, need ≥{min_count}")

    # Sequential narration IDs, no gaps
    narration_ids = re.findall(r'data-narration-id="n(\d+)"', content)
    narration_ids += re.findall(r'data-narration-id="n(\d+)"', data.get('exam_tip_html', '') + ' ' + data.get('conclusion_html', ''))
    if narration_ids:
        nums = sorted(set(int(n) for n in narration_ids))
        expected = list(range(1, max(nums) + 1))
        missing = [n for n in expected if n not in nums]
        if missing:
            violations.append(f"narration ID gaps: missing n{missing[:5]}... ({len(missing)} total)")

    # No <h1> in content_html
    if re.search(r'<h1\b', content):
        violations.append("<h1> tag present — should be absent (title rendered by template)")

    # Word count
    text_only = re.sub(r'<[^>]+>', ' ', content)
    word_count = len(text_only.split())
    if not (700 <= word_count <= 1700):
        violations.append(f"word count {word_count} (want 800-1500, tolerance 700-1700)")

    # Free-tier check: no DIAGRAM placeholder, no diagram_prompt
    if '<!-- DIAGRAM -->' in content:
        violations.append("<!-- DIAGRAM --> placeholder present (free-tier should omit)")
    if 'diagram_prompt' in data:
        violations.append("diagram_prompt present (free-tier should omit)")

    return violations


def main():
    paths = []
    for arg in sys.argv[1:]:
        if '*' in arg:
            paths.extend(glob.glob(arg))
        else:
            paths.append(arg)

    if not paths:
        print("Usage: _validate_content_json.py <json_path>...")
        sys.exit(2)

    any_fail = False
    for p in sorted(paths):
        try:
            violations = validate_file(p)
        except Exception as e:
            print(f"[PARSE ERROR] {p}: {e}")
            any_fail = True
            continue
        tag = "OK" if not violations else "FAIL"
        print(f"[{tag}] {p}")
        for v in violations:
            print(f"    - {v}")
        if violations:
            any_fail = True

    sys.exit(1 if any_fail else 0)


if __name__ == '__main__':
    main()
