"""Reshape related_media from flat per-item entries to grouped-by-category format
that lesson-loader.js + verifier expect.

Source shape (incorrect, written by recent agents):
  [ {"category": "Videos & Channels", "url": "...", "title": "...", ...},
    {"category": "Podcasts", "url": "...", ...},
    ... ]

Target shape (correct):
  [ {"category": "Videos & Channels", "emoji": "🎬", "items": [
        {"title": "...", "url": "...", "description": "..."}, ...]},
    {"category": "Podcasts", "emoji": "🎙️", "items": [...]},
    ... ]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

CATEGORY_EMOJI = {
    "Podcasts": "🎙️",
    "Videos & Channels": "🎬",
    "Movies": "🎬",
    "TV Shows": "📺",
    "Documentaries": "🎞️",
    "Articles & Reading": "📰",
    "Study Tools": "🧰",
}

ITEM_KEYS = ("title", "url", "description", "type", "channel", "host", "duration")

sid = sb.table("subjects").select("id").eq("slug", "food-preparation-and-nutrition-eduqas").is_("school_id", "null").execute().data[0]["id"]
units = sb.table("units").select("id").eq("subject_id", sid).execute().data

reshaped = 0
for u in units:
    rows = sb.table("lessons").select("id, lesson_number, slug, related_media").eq("unit_id", u["id"]).execute().data
    for r in rows:
        rm = r.get("related_media") or []
        if not rm:
            continue
        # Detect old-shape: each entry is a flat dict with category + url at the same level
        is_old_shape = all(
            isinstance(c, dict) and "category" in c and "items" not in c and "url" in c
            for c in rm
        )
        if not is_old_shape:
            continue

        # Group by category
        groups = {}
        order = []
        for entry in rm:
            cat = entry.get("category") or "Other"
            if cat not in groups:
                groups[cat] = []
                order.append(cat)
            item = {k: entry[k] for k in ITEM_KEYS if k in entry and entry[k] is not None}
            groups[cat].append(item)

        new_rm = [
            {
                "category": cat,
                "emoji": CATEGORY_EMOJI.get(cat, "🔗"),
                "items": groups[cat],
            }
            for cat in order
        ]

        sb.table("lessons").update({"related_media": new_rm}).eq("id", r["id"]).execute()
        reshaped += 1
        print(f"  reshaped L{r['lesson_number']:2d} {r['slug'][:50]:50s}  ({len(rm)} items -> {len(new_rm)} groups)")

print(f"\nReshaped: {reshaped} lessons")
