"""
Activate the 9 Geography AQA optional-topic lessons (free tier, school_id NULL).
Inserts NEW lesson rows only into existing paper-1 / paper-2 units at
status='pending_review'. Refuses to overwrite any existing lesson_number.

p1_lesson-21..25 -> paper-1   (Cold Environments x2, Glacial x3)
p2_lesson-21..24 -> paper-2   (Food x2, Water x2)

hero_keywords (build hint, not a DB column) is written to a sidecar JSON for the
hero step.
"""
import json
import os
import sys

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.supabase_client import get_client

CONTENT_DIR = os.path.join(SCRIPT_DIR, "_content_geography-aqa")
SUBJECT_SLUG = "geography-aqa"

FILES = {
    "paper-1": ["p1_lesson-21", "p1_lesson-22", "p1_lesson-23", "p1_lesson-24", "p1_lesson-25"],
    "paper-2": ["p2_lesson-21", "p2_lesson-22", "p2_lesson-23", "p2_lesson-24"],
}

CONTENT_KEYS = [
    "lesson_number", "slug", "title", "description",
    "content_html", "exam_tip_html", "conclusion_html",
    "glossary_terms", "practice_questions", "knowledge_checks", "flashcard_questions",
    "hero_image_caption",
]


def main():
    dry = "--apply" not in sys.argv
    sb = get_client()
    subj = (
        sb.table("subjects").select("id,status")
        .eq("slug", SUBJECT_SLUG).is_("school_id", "null").single().execute().data
    )
    sid = subj["id"]
    print(f"subject {SUBJECT_SLUG} (status={subj['status']}) id={sid}")

    hero_sidecar = {}
    to_insert = []
    for uslug, files in FILES.items():
        uid = (
            sb.table("units").select("id").eq("subject_id", sid)
            .eq("slug", uslug).single().execute().data["id"]
        )
        existing = {r["lesson_number"] for r in
                    sb.table("lessons").select("lesson_number").eq("unit_id", uid).execute().data}
        for fname in files:
            d = json.load(open(os.path.join(CONTENT_DIR, fname + ".json"), encoding="utf-8"))
            ln = d["lesson_number"]
            if ln in existing:
                print(f"  !! REFUSING: {uslug} lesson {ln} already exists. Aborting.")
                sys.exit(1)
            row = {k: d[k] for k in CONTENT_KEYS if k in d}
            row["unit_id"] = uid
            row["tier"] = "both"
            row["status"] = "pending_review"
            to_insert.append((uslug, row))
            hero_sidecar[f"{uslug}/lesson-{ln:02d}"] = {
                "unit_slug": uslug, "lesson_number": ln,
                "title": d["title"], "hero_keywords": d.get("hero_keywords", []),
                "hero_image_caption": d.get("hero_image_caption", ""),
            }

    print(f"\n{len(to_insert)} lessons to insert at pending_review:")
    for uslug, row in to_insert:
        print(f"  {uslug} L{row['lesson_number']:02d}  {row['title']}")

    json.dump(hero_sidecar, open(os.path.join(CONTENT_DIR, "_hero_keywords.json"), "w",
              encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"\nwrote _hero_keywords.json ({len(hero_sidecar)} entries)")

    if dry:
        print("\n[DRY RUN] pass --apply to insert.")
        return

    for uslug, row in to_insert:
        res = sb.table("lessons").insert(row).execute()
        print(f"  inserted {uslug} L{row['lesson_number']:02d} -> id {res.data[0]['id']}")
    print("\nDONE.")


if __name__ == "__main__":
    main()
