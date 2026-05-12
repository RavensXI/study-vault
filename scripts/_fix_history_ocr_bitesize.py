"""Replace the hallucinated BBC Bitesize URL across history-ocr lessons.

The U9-U12 related-media agent shipped `https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb`
as a Study Tools recommendation — that slug doesn't exist on Bitesize and
returns 404 for every lesson it was added to (~30 lessons).

Real BBC Bitesize GCSE History hub: https://www.bbc.co.uk/bitesize/subjects/zk26n39
That's the right replacement — generic GCSE History hub from which students
can navigate to the topic they need.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from lib.supabase_client import get_client


BAD_URL = "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb"
GOOD_URL = "https://www.bbc.co.uk/bitesize/subjects/zk26n39"


def main():
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "history-ocr").execute().data[0]
    units = sb.table("units").select("id").eq("subject_id", sub["id"]).execute().data

    fixed = 0
    for u in units:
        rows = sb.table("lessons").select("id, title, related_media").eq("unit_id", u["id"]).execute().data
        for r in rows:
            rm = r.get("related_media") or []
            changed = False
            for cat in rm:
                if not isinstance(cat, dict):
                    continue
                for item in cat.get("items") or []:
                    if isinstance(item, dict) and item.get("url") == BAD_URL:
                        item["url"] = GOOD_URL
                        item["title"] = "BBC Bitesize — GCSE History hub"
                        item["description"] = "Topic-by-topic GCSE History coverage; useful for cross-checking facts on this period."
                        changed = True
            if changed:
                sb.table("lessons").update({"related_media": rm}).eq("id", r["id"]).execute()
                fixed += 1
                print(f"  fixed {r['title'][:60]}")

    print(f"\nTotal lessons updated: {fixed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
