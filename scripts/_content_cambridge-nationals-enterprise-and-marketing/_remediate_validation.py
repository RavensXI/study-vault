"""Mechanical remediation pass over the 12 generated lesson JSONs.

Fixes the following validator findings without changing meaning:

  - HTML entities in practice_questions[].marks: decode &mdash; / &rsquo; /
    &lsquo; / &ldquo; / &rdquo; / &amp; / &pound; to their unicode chars
    (these fields are plain text — per feedback_question_fields_are_plain_text)

Does NOT auto-fix flashcard enumeration splits, single-word flashcard
answers, insufficient dfn glossary entries, or insufficient key-facts —
those need editorial judgement and are reported for manual edit.
"""
import json
import re
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
lessons_dir = here / "lessons"

ENTITY_MAP = {
    "&mdash;": "—",
    "&ndash;": "–",
    "&rsquo;": "’",
    "&lsquo;": "‘",
    "&ldquo;": "“",
    "&rdquo;": "”",
    "&amp;": "&",
    "&pound;": "£",
}

PLAINTEXT_FIELDS = (
    "practice_questions",
    "knowledge_checks",
    "flashcard_questions",
    "glossary_terms",
    "description",
)


def decode(s: str) -> str:
    if not isinstance(s, str):
        return s
    out = s
    for k, v in ENTITY_MAP.items():
        out = out.replace(k, v)
    return out


def walk(node):
    """Recursively replace entities in any string under a JSON node."""
    if isinstance(node, dict):
        return {k: walk(v) for k, v in node.items()}
    if isinstance(node, list):
        return [walk(v) for v in node]
    if isinstance(node, str):
        return decode(node)
    return node


changed_files = 0
changed_total = 0
for p in sorted(lessons_dir.glob("*.json")):
    data = json.loads(p.read_text(encoding="utf-8"))
    before = json.dumps(data, ensure_ascii=False)
    # Walk only the plain-text fields, not content_html/exam_tip_html/
    # conclusion_html where entities are allowed.
    for field in PLAINTEXT_FIELDS:
        if field in data:
            data[field] = walk(data[field])
    after = json.dumps(data, ensure_ascii=False)
    if before != after:
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        # Count how many entity replacements landed.
        n = sum(before.count(k) - after.count(k) for k in ENTITY_MAP)
        print(f"  decoded {n} entities in {p.name}")
        changed_files += 1
        changed_total += n

print()
print(f"=== Remediation pass complete ===")
print(f"  Files changed: {changed_files}")
print(f"  Total entity replacements: {changed_total}")
