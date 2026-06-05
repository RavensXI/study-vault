"""Reusable hero setter for Cambridge National builds.
Usage: python _cambnat_heroes.py <subject_slug> <unit_slug> <content_dir>
Reads <content_dir>/_hero_keywords.json. Tries Unsplash (direct URL); on rate-limit
(403) or no result, falls back to the local hero index. Sets hero on each lesson.
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client
from lib.unsplash import search_unsplash, trigger_unsplash_download
from lib.hero_index import search_heroes

subject_slug, unit_slug, content_dir = sys.argv[1], sys.argv[2], sys.argv[3]
sb = get_client()
sid = sb.table("subjects").select("id,name").eq("slug", subject_slug).is_("school_id", "null").single().execute().data
subject_name = sid["name"]; sid = sid["id"]
uid = sb.table("units").select("id").eq("subject_id", sid).eq("slug", unit_slug).single().execute().data["id"]
side = json.load(open(os.path.join(content_dir, "_hero_keywords.json"), encoding="utf-8"))

unsplash_dead = False
reused = downloaded = 0
for slug, meta in side.items():
    url = None; ph = ""; src = None
    if not unsplash_dead:
        for q in meta["hero_keywords"]:
            try:
                r = search_unsplash(q, per_page=6)
            except Exception as e:
                if "403" in str(e):
                    unsplash_dead = True
                    print("  Unsplash rate-limited; switching to index reuse")
                    break
                continue
            if r:
                url = r[0]["url"]; ph = r[0].get("photographer", ""); src = "unsplash"
                try: trigger_unsplash_download(r[0].get("_download_location", ""))
                except Exception: pass
                break
            time.sleep(0.4)
    if not url:
        m = search_heroes(" ".join(meta["hero_keywords"]), min_score=3)
        if m:
            url = m[0]["hero_url"]; src = "index"
    cap = meta["hero_image_caption"]
    caption = (cap.rstrip(".") + f" (Photo: {ph} / Unsplash)") if (src == "unsplash" and ph) else cap
    sb.table("lessons").update({
        "hero_image_url": url, "hero_image_alt": meta["title"] + " — " + subject_name,
        "hero_image_caption": caption, "hero_image_position": "center center"
    }).eq("unit_id", uid).eq("lesson_number", meta["lesson_number"]).execute()
    if src == "unsplash": downloaded += 1
    elif src == "index": reused += 1
    print(f"  L{meta['lesson_number']:02d} {slug}: {src or 'NONE'}")
print(f"{subject_slug}: {downloaded} unsplash + {reused} index = {downloaded+reused}/{len(side)} heroes")
