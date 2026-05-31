"""Insert Classical Civilisation AQA revision-technique guides from local files into guide_pages.

Reads scripts/_content_classical-civilisation-ocr/guides/*.json — each {slug, title,
content_html, sort_order} — and upserts a revision-technique guide row for the
classical-civilisation-ocr subject. Idempotent: updates by (subject_id, slug) if present.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()
GUIDE_DIR = Path("scripts/_content_classical-civilisation-ocr/guides")

sid = sb.table("subjects").select("id").eq("slug", "classical-civilisation-ocr").is_("school_id", "null").single().execute().data["id"]
existing = {g["slug"]: g["id"] for g in sb.table("guide_pages").select("id, slug").eq("subject_id", sid).execute().data}

n = 0
for f in sorted(GUIDE_DIR.glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    payload = {
        "subject_id": sid,
        "guide_type": "revision-technique",
        "slug": d["slug"],
        "title": d["title"],
        "content_html": d["content_html"],
        "sort_order": d.get("sort_order", 0),
    }
    if d["slug"] in existing:
        sb.table("guide_pages").update(payload).eq("id", existing[d["slug"]]).execute()
        print(f"  updated: {d['slug']}")
    else:
        sb.table("guide_pages").insert(payload).execute()
        print(f"  inserted: {d['slug']}")
    n += 1

total = sb.table("guide_pages").select("slug").eq("subject_id", sid).execute().data
print(f"\n  Processed {n} guides. Total guide_pages on classical-civilisation-ocr: {len(total)}")
