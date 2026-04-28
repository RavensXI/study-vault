"""Backfill any newly-QA'd History AQA hero images into the hero-image index.

Run after Tom has finished QA via /admin/images: any hero he swapped in via
Unsplash will be on the lessons row but may not be in data/hero-image-index.json.
This pulls all 210 history-aqa lessons, checks each hero_image_url against the
index, and adds missing entries with auto-generated tags.

Idempotent — re-running with no missing entries is a no-op.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.supabase_client import get_client

INDEX_PATH = ROOT / "data" / "hero-image-index.json"

STOP_WORDS = frozenset([
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of",
    "with", "by", "from", "is", "it", "its", "as", "be", "was", "are", "were",
    "been", "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "this", "that", "these",
    "those", "how", "what", "which", "who", "whom", "when", "where", "why",
    "your", "our", "their", "my", "his", "her", "we", "you", "they", "us",
    "them", "he", "she", "lesson", "lessons", "unit", "part", "paper", "using",
    "used", "between", "through", "into", "over", "after", "before", "during",
    "about", "each", "other", "than", "then", "some", "such", "only", "also",
    "just", "more", "most", "very", "well", "back", "much", "many", "own",
    "way", "long", "make", "like", "new", "first", "come", "know", "take",
    "get", "made", "find", "here", "thing", "world", "still", "need", "too",
    "any", "right", "not", "now", "old",
])


def gen_tags(*texts):
    text = " ".join(t or "" for t in texts).lower()
    words = re.sub(r"[^a-z0-9\s-]", " ", text).split()
    return sorted({w for w in words if len(w) > 2 and w not in STOP_WORDS})


def main():
    sb = get_client()
    sub = (
        sb.table("subjects")
        .select("id, slug, name")
        .eq("slug", "history-aqa")
        .is_("school_id", "null")
        .single()
        .execute()
        .data
    )
    units = (
        sb.table("units")
        .select("id, slug, name")
        .eq("subject_id", sub["id"])
        .order("sort_order")
        .execute()
        .data
    )
    units_by_id = {u["id"]: u for u in units}

    lessons = []
    for u in units:
        res = (
            sb.table("lessons")
            .select("id, slug, lesson_number, title, description, hero_image_url, unit_id")
            .eq("unit_id", u["id"])
            .order("lesson_number")
            .execute()
            .data
        )
        lessons.extend(res)

    print(f"Loaded {len(lessons)} history-aqa lessons across {len(units)} units")

    idx = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    indexed_urls = {e["hero_url"] for e in idx if e.get("hero_url")}
    print(f"Index has {len(idx)} entries before backfill")

    missing = []
    no_hero = []
    for L in lessons:
        url = L.get("hero_image_url")
        if not url:
            no_hero.append(L)
            continue
        if url not in indexed_urls:
            missing.append(L)

    if no_hero:
        print(f"WARNING: {len(no_hero)} lessons have no hero_image_url — skipping:")
        for L in no_hero[:5]:
            print(f"  {units_by_id[L['unit_id']]['slug']:35s} L{L['lesson_number']:>2} {L['title'][:60]}")

    if not missing:
        print("\nAll history-aqa hero images are already in the index. Nothing to do.")
        return

    print(f"\n{len(missing)} lessons have heroes not yet in the index. Backfilling...")
    added = 0
    for L in missing:
        unit = units_by_id[L["unit_id"]]
        entry = {
            "title": L.get("title") or "",
            "description": L.get("description") or "",
            "subject": sub["slug"],
            "subject_name": sub["name"],
            "unit": unit["slug"],
            "unit_name": unit["name"],
            "lesson_slug": L.get("slug") or "",
            "hero_url": L["hero_image_url"],
            "tags": gen_tags(
                L.get("title"),
                L.get("description"),
                unit.get("name"),
                sub.get("name"),
            ),
        }
        idx.append(entry)
        indexed_urls.add(L["hero_image_url"])
        added += 1
        print(f"  + {unit['slug']:35s} L{L['lesson_number']:>2} {L['title'][:50]}")

    INDEX_PATH.write_text(
        json.dumps(idx, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nIndex saved: {len(idx)} entries (+{added})")


if __name__ == "__main__":
    main()
