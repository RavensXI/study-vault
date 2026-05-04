"""Strip the Podcasts category from PE OCR related_media.

The AQA podcasts were inherited via the AQA→OCR asset copy; they reference
AQA-specific narrative and shouldn't ship under OCR. Clearing them so Tom
can generate fresh OCR podcasts via NotebookLM.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

sid = sb.table("subjects").select("id").eq("slug", "physical-education-ocr").is_("school_id", "null").execute().data[0]["id"]
units = sb.table("units").select("id, slug").eq("subject_id", sid).execute().data

stripped = 0
already_clean = 0
for u in units:
    rows = (
        sb.table("lessons")
        .select("id, lesson_number, slug, related_media")
        .eq("unit_id", u["id"])
        .order("lesson_number")
        .execute()
        .data
    )
    for r in rows:
        rm = r.get("related_media") or []
        had_podcasts = any(c.get("category") == "Podcasts" for c in rm)
        if not had_podcasts:
            already_clean += 1
            continue
        new_rm = [c for c in rm if c.get("category") != "Podcasts"]
        sb.table("lessons").update({"related_media": new_rm}).eq("id", r["id"]).execute()
        print(f"  cleared L{r['lesson_number']:2d} {r['slug']}")
        stripped += 1

print(f"\n  Stripped: {stripped}, already clean: {already_clean}")
