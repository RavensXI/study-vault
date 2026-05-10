"""Insert 4 new lesson shells into the existing it-ocr R050 unit.

Existing L1-L8 are untouched. New lessons land at lesson_number 9-12,
status='pending_review', empty content_html. Phase 3 content agent fills
them after.
"""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from lib.supabase_client import get_client


def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def main():
    sb = get_client()
    plan = json.loads(open("scripts/_plan_it-ocr_expansion.json", encoding="utf-8").read())
    unit_id = plan["unit_id"]
    subject_id = plan["subject_id"]

    # Sanity check: the unit and subject still exist + L1-L8 still present
    units = sb.table("units").select("id, slug").eq("id", unit_id).execute().data
    if not units:
        print(f"ERR: unit {unit_id} not found")
        return 1
    existing = sb.table("lessons").select("lesson_number, title").eq("unit_id", unit_id).order("lesson_number").execute().data
    print(f"Existing lessons in {units[0]['slug']}:")
    for r in existing:
        print(f"  L{r['lesson_number']}: {r['title']}")
    if len(existing) != 8:
        print(f"ERR: expected exactly 8 existing lessons, found {len(existing)}. Aborting.")
        return 1

    # Insert new shells
    inserted = []
    for new in plan["new_lessons"]:
        n = new["lesson_number"]
        title = new["title"]
        slug = slugify(title)
        # Check for collision
        clash = sb.table("lessons").select("id").eq("unit_id", unit_id).eq("lesson_number", n).execute().data
        if clash:
            print(f"ERR: lesson_number {n} already exists in unit. Aborting.")
            return 1
        row = {
            "unit_id": unit_id,
            "lesson_number": n,
            "title": title,
            "slug": slug,
            "status": "pending_review",
            "description": new["description"],
            "content_html": None,
        }
        result = sb.table("lessons").insert(row).execute()
        inserted.append(result.data[0])
        print(f"  inserted L{n} {title} -> {result.data[0]['id']}")

    # Verify
    after = sb.table("lessons").select("lesson_number, title, id").eq("unit_id", unit_id).order("lesson_number").execute().data
    print(f"\nUnit now has {len(after)} lessons:")
    for r in after:
        print(f"  L{r['lesson_number']}: {r['title']} ({r['id']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
