"""Copy revision-technique guides from PE OCR to Food Prep Eduqas with neutral name swap."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

src_sid = sb.table("subjects").select("id").eq("slug", "physical-education-ocr").is_("school_id", "null").execute().data[0]["id"]
dst_sid = sb.table("subjects").select("id").eq("slug", "sociology-aqa").is_("school_id", "null").execute().data[0]["id"]

# Only revision-technique guides; skip exam-technique (mark bands differ between subjects)
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

    html = g["content_html"] or ""
    # Neutral subject-name swap. PE OCR guides reference "OCR Physical Education" / "Physical Education".
    # Food Prep is a Path A subject so write neutrally — "GCSE Sociology".
    html = re.sub(r"\bOCR Physical Education\b", "GCSE Sociology", html)
    html = re.sub(r"\bPhysical Education\b", "Sociology", html)
    # Update inter-guide nav links
    html = html.replace("/guide/physical-education-ocr/", "/guide/sociology-aqa/")
    title = re.sub(r"\bPhysical Education\b", "Sociology", g["title"] or "")

    sb.table("guide_pages").insert({
        "subject_id": dst_sid,
        "slug": g["slug"],
        "guide_type": g["guide_type"],
        "title": title,
        "sort_order": g["sort_order"],
        "content_html": html,
    }).execute()
    print(f"  inserted: {g['slug']:40s} | {title}")
    inserted += 1

print(f"\n  Inserted: {inserted}, skipped: {skipped}")
