"""Decode HTML entities in plain-text fields across lesson JSONs.

Plain-text fields per CONTENT_PROMPT.md:
- description
- hero_image_caption
- practice_questions[].text, .type, .marks
- knowledge_checks[].q, .options[], .left[], .right[]
- flashcard_questions[].q, .a
- glossary_terms[].term, .definition

HTML-rendered fields (preserve entities, do not decode):
- content_html, exam_tip_html, conclusion_html
- glossary <dfn data-def="..."> attribute (rendered as HTML)

Usage: python scripts/_fix_entities_in_text_fields.py <subject-slug>
"""
import html
import json
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python scripts/_fix_entities_in_text_fields.py <subject-slug>")
    sys.exit(1)

slug = sys.argv[1]
scripts_dir = Path(__file__).resolve().parent
lessons_dir = scripts_dir / f"_content_{slug}" / "lessons"

PLAIN_TEXT_PATHS = {
    # top-level
    "description": "str",
    "hero_image_caption": "str",
    # arrays
    "practice_questions": "pq_array",
    "knowledge_checks": "kc_array",
    "flashcard_questions": "fc_array",
    "glossary_terms": "gloss_array",
}

# Fields within each array element that are plain-text
PQ_TEXT_FIELDS = {"text", "type", "marks", "question"}
KC_TEXT_FIELDS = {"q", "explanation"}  # options/left/right handled as lists
FC_TEXT_FIELDS = {"q", "a"}
GLOSS_TEXT_FIELDS = {"term", "definition"}


def decode_if_changed(v):
    if not isinstance(v, str):
        return v, False
    d = html.unescape(v)
    return d, d != v


def fix_str_dict(d, text_fields, changed_ref):
    for k, v in list(d.items()):
        if k in text_fields:
            new, ch = decode_if_changed(v)
            if ch:
                d[k] = new
                changed_ref[0] = True


def fix_str_list(lst, changed_ref):
    """For string list fields (options[], left[], right[])."""
    for i, v in enumerate(lst):
        if isinstance(v, str):
            new, ch = decode_if_changed(v)
            if ch:
                lst[i] = new
                changed_ref[0] = True


def fix_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("﻿"):
        raw = raw[1:]
    data = json.loads(raw)
    changed = [False]

    # Top-level scalar plain-text fields
    for k in ("description", "hero_image_caption"):
        if isinstance(data.get(k), str):
            new, ch = decode_if_changed(data[k])
            if ch:
                data[k] = new
                changed[0] = True

    # Practice questions
    for q in data.get("practice_questions", []) or []:
        if isinstance(q, dict):
            fix_str_dict(q, PQ_TEXT_FIELDS, changed)
            # mark_scheme can be a string OR a dict with rubric fields — handle string
            if isinstance(q.get("mark_scheme"), str):
                new, ch = decode_if_changed(q["mark_scheme"])
                if ch:
                    q["mark_scheme"] = new
                    changed[0] = True

    # Knowledge checks
    for kc in data.get("knowledge_checks", []) or []:
        if isinstance(kc, dict):
            fix_str_dict(kc, KC_TEXT_FIELDS, changed)
            if isinstance(kc.get("options"), list):
                fix_str_list(kc["options"], changed)
            if isinstance(kc.get("left"), list):
                fix_str_list(kc["left"], changed)
            if isinstance(kc.get("right"), list):
                fix_str_list(kc["right"], changed)
            # fill type — `answer` is plain text
            if isinstance(kc.get("answer"), str):
                new, ch = decode_if_changed(kc["answer"])
                if ch:
                    kc["answer"] = new
                    changed[0] = True

    # Flashcards
    for fc in data.get("flashcard_questions", []) or []:
        if isinstance(fc, dict):
            fix_str_dict(fc, FC_TEXT_FIELDS, changed)

    # Glossary
    for g in data.get("glossary_terms", []) or []:
        if isinstance(g, dict):
            fix_str_dict(g, GLOSS_TEXT_FIELDS, changed)

    # hero_keywords (string list)
    if isinstance(data.get("hero_keywords"), list):
        fix_str_list(data["hero_keywords"], changed)

    if changed[0]:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return changed[0]


def main():
    if not lessons_dir.exists():
        print(f"ERROR: {lessons_dir} not found")
        sys.exit(1)
    files = sorted(lessons_dir.glob("*.json"))
    fixed = 0
    for f in files:
        try:
            if fix_file(f):
                print(f"  fixed: {f.name}")
                fixed += 1
        except Exception as e:
            print(f"  ERROR {f.name}: {e}")
    print(f"\nDecoded entities in {fixed}/{len(files)} files for {slug}")


if __name__ == "__main__":
    main()
