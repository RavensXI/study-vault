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
    if len(fc) != 5:
        violations.append(f"flashcard_questions count {len(fc)}, want 5")

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
