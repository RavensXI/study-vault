"""
Insert related_media for the 9 Geography AQA optional-topic lessons.
Reads scripts/_content_geography-aqa/related_media/{p1|p2}_lesson-NN.json
and updates the matching lesson row's related_media column.
"""
import json
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.supabase_client import get_client

RM_DIR = Path(SCRIPT_DIR) / "_content_geography-aqa" / "related_media"
SUBJECT_SLUG = "geography-aqa"
MAP = {"p1": "paper-1", "p2": "paper-2"}


def main():
    apply = "--apply" in sys.argv
    sb = get_client()
    sid = (sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG)
           .is_("school_id", "null").single().execute().data["id"])
    units = {u["slug"]: u["id"] for u in
             sb.table("units").select("id,slug").eq("subject_id", sid).execute().data}

    for f in sorted(RM_DIR.glob("*.json")):
        prefix, _, lpart = f.stem.partition("_")  # p1, lesson-21
        unit_slug = MAP[prefix]
        ln = int(lpart.split("-")[1])
        media = json.loads(f.read_text(encoding="utf-8"))
        ncat = len(media)
        nitems = sum(len(c.get("items", [])) for c in media)
        cats = [c.get("category") for c in media]
        print(f"{unit_slug} L{ln:02d}: {ncat} cats / {nitems} items  {cats}")
        if apply:
            res = (sb.table("lessons").update({"related_media": media})
                   .eq("unit_id", units[unit_slug]).eq("lesson_number", ln).execute())
            print(f"   updated {len(res.data)} row(s)")
    if not apply:
        print("\n[DRY RUN] pass --apply to write.")


if __name__ == "__main__":
    main()
