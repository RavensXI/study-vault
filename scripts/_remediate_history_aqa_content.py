"""Programmatic remediation of validator failures across History AQA content.

Fixes:
  A. `&mdash;` → `—` in practice_questions[*].type strings
  B. description > 110 chars → trim to ≤100 chars on word boundary
  C. `12 marks — Source Utility` → `12 marks — Source Evaluation`
  D. AQA-protected phrases:
     - "How far do you agree" (any case) → "Evaluate the claim that"
     - "Has X been the main factor" → "Was X the main factor"

Does NOT fix structural issues (missing collapsibles, missing dfns) — those need an agent.
"""
import json
import re
from pathlib import Path

d = Path("scripts/_content_history-aqa/lessons")

stats = {"a": 0, "b": 0, "c": 0, "d_hfdya": 0, "d_main_factor": 0}


def trim_description(desc: str) -> str:
    if len(desc) <= 110:
        return desc
    truncated = desc[:100].rsplit(" ", 1)[0].rstrip(",;:.")
    return truncated + "."


def normalize_type_strings(obj):
    """Replace HTML entities and the renamed Source Utility -> Source Evaluation."""
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k == "type" and isinstance(v, str):
                new = v
                if "&mdash;" in new:
                    new = new.replace("&mdash;", "—")
                    stats["a"] += 1
                if new == "12 marks — Source Utility":
                    new = "12 marks — Source Evaluation"
                    stats["c"] += 1
                if new == "8 marks — Source Utility":
                    new = "8 marks — Source Evaluation"
                    stats["c"] += 1
                obj[k] = new
            else:
                normalize_type_strings(v)
    elif isinstance(obj, list):
        for item in obj:
            normalize_type_strings(item)


def fix_aqa_phrases_in_text(text: str) -> str:
    """Replace AQA-protected rubric phrases with safe alternatives."""
    # "How far do you agree…?" → "Evaluate the claim that…"
    new = re.sub(
        r"How far do you agree(?:\s+with this statement)?(?:\s*\?)?",
        "Evaluate the claim that this is correct",
        text,
        flags=re.IGNORECASE,
    )
    diff_a = (text != new)
    text = new
    # "Has X been the main factor in" → "Was X the main factor in"
    new = re.sub(
        r"\bHas\s+([A-Z][\w\s]+?)\s+[Bb]een the [Mm]ain [Ff]actor",
        lambda m: f"Was {m.group(1)} the main factor",
        text,
    )
    diff_b = (text != new)
    return new, diff_a, diff_b


def walk_fix_text(obj):
    """Recursively fix AQA phrases in any string field."""
    a_total = 0
    b_total = 0
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if isinstance(v, str):
                new, da, db = fix_aqa_phrases_in_text(v)
                obj[k] = new
                if da: a_total += 1
                if db: b_total += 1
            else:
                aa, bb = walk_fix_text(v)
                a_total += aa
                b_total += bb
    elif isinstance(obj, list):
        for item in obj:
            aa, bb = walk_fix_text(item)
            a_total += aa
            b_total += bb
    return a_total, b_total


for f in sorted(d.glob("*.json")):
    obj = json.loads(f.read_text(encoding="utf-8"))
    before = json.dumps(obj, ensure_ascii=False)

    # B — description trim
    if "description" in obj and len(obj["description"]) > 110:
        obj["description"] = trim_description(obj["description"])
        stats["b"] += 1

    # A + C — type string normalisation
    normalize_type_strings(obj)

    # D — AQA phrase swaps
    a, b = walk_fix_text(obj)
    stats["d_hfdya"] += a
    stats["d_main_factor"] += b

    after = json.dumps(obj, ensure_ascii=False)
    if before != after:
        f.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Type-string entity fixes (&mdash;):    {stats['a']}")
print(f"Type-string Source Utility renames:    {stats['c']}")
print(f"Description trims:                     {stats['b']}")
print(f"'How far do you agree' replacements:   {stats['d_hfdya']}")
print(f"'Main factor' replacements:            {stats['d_main_factor']}")
