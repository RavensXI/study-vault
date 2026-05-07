"""Copy revision-technique guides from sociology-aqa to sociology-eduqas.

The sociology-aqa guides already use generic 'GCSE Sociology' phrasing
(per Path A neutral phrasing) — only the inter-guide nav links need
updating. No subject-name swap needed.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

src_sid = sb.table("subjects").select("id").eq("slug", "sociology-aqa").is_("school_id", "null").execute().data[0]["id"]
dst_sid = sb.table("subjects").select("id").eq("slug", "sociology-eduqas").is_("school_id", "null").execute().data[0]["id"]

src_guides = sb.table("guide_pages").select("*").eq("subject_id", src_sid).eq("guide_type", "revision-technique").execute().data
existing_dst = {g["slug"] for g in sb.table("guide_pages").select("slug").eq("subject_id", dst_sid).execute().data}

print(f"Source revision-technique guides: {len(src_guides)}")

inserted = 0
skipped = 0
for g in src_guides:
    if g["slug"] in existing_dst:
        print(f"  SKIP existing: {g['slug']}")
        skipped += 1
        continue

    html = (g["content_html"] or "").replace("/guide/sociology-aqa/", "/guide/sociology-eduqas/")
    sb.table("guide_pages").insert({
        "subject_id": dst_sid,
        "slug": g["slug"],
        "guide_type": g["guide_type"],
        "title": g["title"],
        "sort_order": g["sort_order"],
        "content_html": html,
    }).execute()
    print(f"  inserted: {g['slug']:40s} | {g['title']}")
    inserted += 1

print(f"\n  Inserted: {inserted}, skipped: {skipped}")
