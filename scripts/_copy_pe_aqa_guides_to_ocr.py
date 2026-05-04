"""Copy revision-technique guides from PE AQA to PE OCR with board-name swaps."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

src_sid = sb.table("subjects").select("id").eq("slug", "physical-education-aqa").is_("school_id", "null").execute().data[0]["id"]
dst_sid = sb.table("subjects").select("id").eq("slug", "physical-education-ocr").is_("school_id", "null").execute().data[0]["id"]

src_guides = sb.table("guide_pages").select("*").eq("subject_id", src_sid).execute().data
existing_dst = {g["slug"] for g in sb.table("guide_pages").select("slug").eq("subject_id", dst_sid).execute().data}

print(f"Source guides: {len(src_guides)}")
print(f"Existing dst guides: {len(existing_dst)}")

inserted = 0
skipped = 0
for g in src_guides:
    if g["slug"] in existing_dst:
        print(f"  SKIP existing: {g['slug']}")
        skipped += 1
        continue

    # Board-name swaps in content_html and title
    html = g["content_html"] or ""
    html = re.sub(r"\bAQA\b", "OCR", html)
    html = re.sub(r"\b8582\b", "J587", html)
    title = re.sub(r"\bAQA\b", "OCR", g["title"] or "")

    payload = {
        "subject_id": dst_sid,
        "slug": g["slug"],
        "guide_type": g["guide_type"],
        "title": title,
        "sort_order": g["sort_order"],
        "content_html": html,
    }
    sb.table("guide_pages").insert(payload).execute()
    print(f"  inserted: {g['slug']:40s} | {title}")
    inserted += 1

print(f"\n  Inserted: {inserted}, skipped: {skipped}")
