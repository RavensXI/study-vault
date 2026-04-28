"""Decode HTML entities to actual unicode in History AQA practice/KC/flashcard fields.

Practice questions, knowledge checks, and flashcards render via textContent and
escape-then-innerHTML paths — both treat HTML entities as literal text. Agents
generated content with `&mdash;`, `&rsquo;`, etc. expecting browser parsing,
which never happens for these JSON fields. Convert to unicode.

content_html is HTML so entities stay valid there — leave alone.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client


# HTML entity → unicode replacements. `&amp;` MUST be last so we don't
# accidentally re-decode something like `&amp;mdash;` mid-pass.
REPLACEMENTS = [
    ("&mdash;", "—"),
    ("&ndash;", "–"),
    ("&lsquo;", "‘"),
    ("&rsquo;", "’"),
    ("&ldquo;", "“"),
    ("&rdquo;", "”"),
    ("&hellip;", "…"),
    ("&nbsp;", " "),
    ("&lt;", "<"),
    ("&gt;", ">"),
    ("&#39;", "'"),
    ("&#x27;", "'"),
    ("&amp;", "&"),
]

FIELDS_TO_FIX = ["practice_questions", "knowledge_checks", "flashcard_questions", "glossary_terms"]


def decode_string(s: str) -> tuple[str, int]:
    n = 0
    for entity, char in REPLACEMENTS:
        if entity in s:
            n += s.count(entity)
            s = s.replace(entity, char)
    return s, n


def walk_decode(obj):
    """Recursively decode entity strings in dicts and lists. Returns (obj, n_replacements)."""
    if isinstance(obj, dict):
        total = 0
        for k, v in list(obj.items()):
            new_v, n = walk_decode(v)
            obj[k] = new_v
            total += n
        return obj, total
    elif isinstance(obj, list):
        total = 0
        for i, v in enumerate(obj):
            new_v, n = walk_decode(v)
            obj[i] = new_v
            total += n
        return obj, total
    elif isinstance(obj, str):
        return decode_string(obj)
    return obj, 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Push fixes to Supabase")
    args = parser.parse_args()

    sb = get_client()
    sub = (
        sb.table("subjects")
        .select("id")
        .eq("slug", "history-aqa")
        .is_("school_id", "null")
        .single()
        .execute()
        .data
    )
    units = sb.table("units").select("id").eq("subject_id", sub["id"]).execute().data
    unit_ids = [u["id"] for u in units]

    all_lessons = []
    for uid in unit_ids:
        res = (
            sb.table("lessons")
            .select("id, title, " + ", ".join(FIELDS_TO_FIX))
            .eq("unit_id", uid)
            .execute()
            .data
        )
        all_lessons.extend(res)

    print(f"Inspecting {len(all_lessons)} lessons across {len(FIELDS_TO_FIX)} fields\n")

    field_replacements = {f: 0 for f in FIELDS_TO_FIX}
    field_lessons_changed = {f: 0 for f in FIELDS_TO_FIX}
    updates_to_apply = []

    for L in all_lessons:
        update = {}
        for fname in FIELDS_TO_FIX:
            original = L.get(fname)
            if original is None:
                continue
            # Deep-copy via JSON round-trip to avoid mutating input
            payload = json.loads(json.dumps(original))
            payload, n = walk_decode(payload)
            if n > 0:
                update[fname] = payload
                field_replacements[fname] += n
                field_lessons_changed[fname] += 1
        if update:
            updates_to_apply.append((L["id"], L["title"], update))

    print(f"Replacements per field:")
    for f in FIELDS_TO_FIX:
        print(f"  {f:<25} {field_replacements[f]:>5} replacements across {field_lessons_changed[f]} lessons")
    print(f"\nTotal lessons needing updates: {len(updates_to_apply)}")

    if not args.apply:
        print("\nDry run. Re-run with --apply to push to Supabase.")
        # Show one sample
        if updates_to_apply:
            lid, ltitle, upd = updates_to_apply[0]
            print(f"\nSample changes for '{ltitle}':")
            for f in upd:
                print(f"  {f}: first item after fix —")
                first = upd[f][0] if upd[f] else None
                if isinstance(first, dict):
                    for k, v in first.items():
                        if isinstance(v, str):
                            print(f"    {k}: {v[:160]!r}")
        return

    print("\nApplying fixes…")
    pushed = 0
    for lid, _, upd in updates_to_apply:
        sb.table("lessons").update(upd).eq("id", lid).execute()
        pushed += 1
    print(f"Updated {pushed} lessons.")


if __name__ == "__main__":
    main()
