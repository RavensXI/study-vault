"""Mechanical remediation for Eduqas History lesson JSONs.

Fixes the deterministic validator failures:
  1. HTML entities in plain-text fields (html.unescape) — description,
     hero_image_caption, practice_questions[text/type/marks],
     knowledge_checks[q], flashcard_questions[q/a], glossary_terms[term/definition].
     (content_html / exam_tip_html / conclusion_html are LEFT ALONE — entities allowed there.)
  2. Missing hero_image_caption — generated from _lesson_slug.
  3. description length > 120 — trimmed at a sentence/clause boundary.
  4. Banned "Award N marks for" — reworded to "N marks awarded for" (all string fields).
  5. Banned AO codes (AO1-4 with optional .n) — reworded to plain skill language (all string fields).

Content-quality issues (flashcard enumerations/single-word/duplicates, word count,
insufficient key-fact/collapsible/dfn) are NOT handled here — those go to remediation agents.
"""
import html
import json
import re
from pathlib import Path

LESSONS_DIR = Path(__file__).resolve().parent / "lessons"

PLAIN_TEXT_TOP = ["description", "hero_image_caption"]
NESTED = {
    "practice_questions": ["text", "type", "marks"],
    "knowledge_checks": ["q"],
    "flashcard_questions": ["q", "a"],
    "glossary_terms": ["term", "definition"],
}

ENTITY_PATTERN = re.compile(r'&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);')
AWARD_PATTERN = re.compile(r'Award\s+(\d+)\s+(marks?)\s+for', re.IGNORECASE)
AO_MAP = {
    "AO1": "recall and understanding",
    "AO2": "explanation and analysis",
    "AO3": "source analysis",
    "AO4": "interpretation analysis",
}
AO_PATTERN = re.compile(r'\bAO([1-4])(\.[0-9]?)?')


def fix_award(s):
    return AWARD_PATTERN.sub(lambda m: f"{m.group(1)} {m.group(2)} awarded for", s)


def fix_ao(s):
    # Replace AO1-4 (with optional .n) by plain language, dropping the trailing dot-number.
    return AO_PATTERN.sub(lambda m: AO_MAP[f"AO{m.group(1)}"], s)


def fix_file(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    notes = []

    # 1. Entity decode on plain-text fields
    for f in PLAIN_TEXT_TOP:
        v = data.get(f)
        if isinstance(v, str) and ENTITY_PATTERN.search(v):
            data[f] = html.unescape(v)
            notes.append(f"entity:{f}")
    for arr_name, sub_fields in NESTED.items():
        arr = data.get(arr_name)
        if not isinstance(arr, list):
            continue
        for item in arr:
            if not isinstance(item, dict):
                continue
            for sf in sub_fields:
                v = item.get(sf)
                if isinstance(v, str) and ENTITY_PATTERN.search(v):
                    item[sf] = html.unescape(v)
                    notes.append(f"entity:{arr_name}.{sf}")

    # 2. Missing hero_image_caption
    if not data.get("hero_image_caption"):
        title = (data.get("_lesson_slug", "lesson") or "lesson").replace("-", " ").strip()
        title = title[:1].upper() + title[1:]
        data["hero_image_caption"] = f"{title} — illustrative image."
        notes.append("hero_caption")

    # 3. description trim > 120
    desc = data.get("description", "")
    if isinstance(desc, str) and len(desc) > 120:
        trimmed = desc[:118]
        cut = max(trimmed.rfind("."), trimmed.rfind(";"), trimmed.rfind(","))
        if cut > 60:
            trimmed = trimmed[:cut].rstrip(",;") + "."
        else:
            trimmed = trimmed.rstrip() + "."
        data["description"] = trimmed
        notes.append("desc_trim")

    # 4 & 5. Banned "Award N marks for" + AO codes across ALL string fields
    def walk(node):
        if isinstance(node, dict):
            return {k: walk(v) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(v) for v in node]
        if isinstance(node, str):
            s = node
            if AWARD_PATTERN.search(s):
                s = fix_award(s)
                notes.append("award_phrase")
            if AO_PATTERN.search(s):
                s = fix_ao(s)
                notes.append("ao_code")
            return s
        return node

    data = walk(data)

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return notes


def main():
    total = 0
    touched = 0
    summary = {}
    for p in sorted(LESSONS_DIR.glob("*.json")):
        total += 1
        notes = fix_file(p)
        if notes:
            touched += 1
            for n in notes:
                key = n.split(":")[0]
                summary[key] = summary.get(key, 0) + 1
    print(f"Processed {total} files, modified {touched}.")
    print("Fix counts:")
    for k, v in sorted(summary.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
