"""Dump a candidate reference lesson to file for review."""
import sys, json
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

sb = get_client()

slug, title = "religious-education", "Worship & Prayer"
subj = sb.table("subjects").select("id").eq("slug", slug).execute().data
sids = [s["id"] for s in subj]
units = sb.table("units").select("id").in_("subject_id", sids).execute().data
uids = [u["id"] for u in units]
l = sb.table("lessons").select("*").in_("unit_id", uids).eq("title", title).limit(1).execute().data[0]

# Save for review
with open("scripts/_reference_candidate_re_l01.json", "w", encoding="utf-8") as f:
    json.dump(l, f, indent=2, ensure_ascii=False)

print(f"Wrote scripts/_reference_candidate_re_l01.json")
print(f"content_html length: {len(l.get('content_html') or '')}")
print("\n--- First 2000 chars of content_html ---")
print((l.get("content_html") or "")[:2000])
print("\n--- First practice question ---")
print(json.dumps((l.get("practice_questions") or [{}])[0], indent=2, ensure_ascii=False))
