"""
Write content for it-ocr expansion lessons L9-L12 to Supabase.
Updates existing shell rows by known lesson IDs.
Status stays pending_review (already set at insert time).
"""
import sys, os, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from lib.supabase_client import get_client

LESSONS = [
    {
        "lesson_id": "babbf45b-3d9e-4318-a943-685285fb1f0c",
        "lesson_number": 9,
        "json_file": "scripts/_content_it-ocr/it-in-the-digital-world/L9.json",
    },
    {
        "lesson_id": "354e675f-7fa4-4c3b-b2df-34af32694fd0",
        "lesson_number": 10,
        "json_file": "scripts/_content_it-ocr/it-in-the-digital-world/L10.json",
    },
    {
        "lesson_id": "4dc82838-0a74-4f4b-94a8-d65a63a208b3",
        "lesson_number": 11,
        "json_file": "scripts/_content_it-ocr/it-in-the-digital-world/L11.json",
    },
    {
        "lesson_id": "2c006ee9-82d0-492a-943d-bef1e8730845",
        "lesson_number": 12,
        "json_file": "scripts/_content_it-ocr/it-in-the-digital-world/L12.json",
    },
]

CONTENT_KEYS = [
    "description",
    "content_html",
    "exam_tip_html",
    "conclusion_html",
    "practice_questions",
    "knowledge_checks",
    "flashcard_questions",
    "glossary_terms",
    "hero_image_caption",
]


def main():
    sb = get_client()
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for entry in LESSONS:
        path = os.path.join(base, entry["json_file"])
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        # Verify the lesson row exists
        row = sb.table("lessons").select("id, title, lesson_number, status").eq("id", entry["lesson_id"]).single().execute().data
        if not row:
            print(f"ERR: lesson {entry['lesson_id']} not found in Supabase")
            return 1
        print(f"L{entry['lesson_number']}: found '{row['title']}' (status={row['status']})")

        # Build update payload — only content keys
        payload = {k: data[k] for k in CONTENT_KEYS if k in data}

        result = sb.table("lessons").update(payload).eq("id", entry["lesson_id"]).execute()
        if result.data:
            print(f"  -> updated OK ({len(payload)} fields written)")
        else:
            print(f"  -> ERR: {result}")
            return 1

    print("\nAll 4 lessons updated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
