"""Audit hero-image-index, backfill gaps, then match History AQA lessons.

Three phases:

1. AUDIT — find all hero_image_url values in Supabase lessons that are missing
   from data/hero-image-index.json, and re-tag any indexed entries that have
   empty `tags` fields. Saves the updated index.

2. MATCH — for each of the 210 History AQA lessons, score every index entry
   against the lesson's hero_keywords + title + description, picking the best
   image while constraining "no image repeated within a unit". Output a per-
   lesson JSON proposal file (no Supabase writes yet).

3. APPLY (with --apply flag only) — push the proposed image URLs to Supabase
   lesson rows.

Usage:
    python scripts/_audit_and_match_history_aqa_heroes.py             # phases 1+2 (no DB writes)
    python scripts/_audit_and_match_history_aqa_heroes.py --apply     # phases 1+2+3
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.supabase_client import get_client

INDEX_PATH = ROOT / "data" / "hero-image-index.json"
PROPOSALS_PATH = ROOT / "scripts" / "_content_history-aqa" / "_hero_proposals.json"

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Push proposed images to Supabase")
    args = parser.parse_args()

    sb = get_client()

    # ─────────────── Phase 1: AUDIT

    idx = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    idx_by_url = {e["hero_url"]: e for e in idx if e.get("hero_url")}

    # Re-tag entries with empty tags
    retag = 0
    for e in idx:
        if not e.get("tags"):
            e["tags"] = gen_tags(e.get("title"), e.get("description"), e.get("unit_name"), e.get("subject_name"))
            retag += 1
    print(f"Re-tagged {retag} index entries with empty tags")

    # Pull all in-use lessons (paginated)
    all_lessons = []
    page_size = 1000
    offset = 0
    while True:
        batch = (
            sb.table("lessons")
            .select("id, slug, title, description, hero_image_url, unit_id")
            .range(offset, offset + page_size - 1)
            .execute()
            .data
        )
        if not batch:
            break
        all_lessons.extend(batch)
        if len(batch) < page_size:
            break
        offset += page_size

    # Build unit/subject lookup
    units_by_id = {}
    units_data = sb.table("units").select("id, slug, name, subject_id").execute().data
    units_by_id = {u["id"]: u for u in units_data}
    subjects_by_id = {s["id"]: s for s in sb.table("subjects").select("id, slug, name").execute().data}

    in_use_urls = {L["hero_image_url"] for L in all_lessons if L.get("hero_image_url")}
    missing_urls = in_use_urls - set(idx_by_url.keys())
    print(f"Lessons total: {len(all_lessons)}; with heroes: {sum(1 for L in all_lessons if L.get('hero_image_url'))}; "
          f"unique hero URLs: {len(in_use_urls)}; missing from index: {len(missing_urls)}")

    backfilled = 0
    for L in all_lessons:
        url = L.get("hero_image_url")
        if not url or url not in missing_urls:
            continue
        unit = units_by_id.get(L.get("unit_id")) or {}
        subject = subjects_by_id.get(unit.get("subject_id")) or {}
        entry = {
            "title": L.get("title") or "",
            "description": L.get("description") or "",
            "subject": subject.get("slug") or "",
            "subject_name": subject.get("name") or "",
            "unit": unit.get("slug") or "",
            "unit_name": unit.get("name") or "",
            "lesson_slug": L.get("slug") or "",
            "hero_url": url,
            "tags": gen_tags(L.get("title"), L.get("description"), unit.get("name"), subject.get("name")),
        }
        idx.append(entry)
        idx_by_url[url] = entry
        missing_urls.discard(url)
        backfilled += 1
    print(f"Backfilled {backfilled} entries into index")

    INDEX_PATH.write_text(json.dumps(idx, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Index saved: {len(idx)} total entries")

    # ─────────────── Phase 2: MATCH

    history_subject = sb.table("subjects").select("id").eq("slug", "history-aqa").is_("school_id", "null").single().execute().data
    history_units = sb.table("units").select("id, slug, name, sort_order").eq("subject_id", history_subject["id"]).order("sort_order").execute().data

    # Pull plan to get per-lesson hero_keywords (saved JSON files)
    lessons_dir = ROOT / "scripts" / "_content_history-aqa" / "lessons"

    proposals = []
    skipped = 0
    by_unit_taken: dict[str, set[str]] = defaultdict(set)

    # Pre-compute index entries for matching: drop those already used in History AQA
    # (we don't want to re-pick history-aqa heroes from earlier matches if any)
    existing_history_aqa_urls = {
        L["hero_image_url"]
        for L in all_lessons
        if L.get("hero_image_url") and units_by_id.get(L.get("unit_id"), {}).get("subject_id") == history_subject["id"]
    }
    print(f"\nExisting history-aqa hero URLs (will be excluded from matching): {len(existing_history_aqa_urls)}")

    for unit in history_units:
        unit_lessons = (
            sb.table("lessons")
            .select("id, lesson_number, slug, title, description")
            .eq("unit_id", unit["id"])
            .order("lesson_number")
            .execute()
            .data
        )
        for L in unit_lessons:
            content_file = lessons_dir / f"{unit['slug']}_{L['lesson_number']:02d}.json"
            if not content_file.exists():
                skipped += 1
                continue
            content = json.loads(content_file.read_text(encoding="utf-8"))
            hero_keywords = content.get("hero_keywords") or []

            # Build query terms: hero_keywords + title + description
            query_text = " ".join(
                [str(k) for k in hero_keywords]
                + [L["title"] or "", L.get("description") or ""]
            ).lower()
            query_words = set(re.findall(r"\b[a-z][a-z0-9-]{2,}\b", query_text)) - STOP_WORDS

            # Score every index entry
            best = None  # (score, entry, signals)
            taken_in_unit = by_unit_taken[unit["slug"]]
            for entry in idx:
                if entry["hero_url"] in taken_in_unit:
                    continue
                if entry["hero_url"] in existing_history_aqa_urls:
                    continue
                tags = set(entry.get("tags") or [])
                title_words = set(re.findall(r"\b[a-z][a-z0-9-]{2,}\b", (entry.get("title") or "").lower())) - STOP_WORDS
                title_hits = len(query_words & title_words)
                tag_hits = len(query_words & tags)
                # Prefer images from non-History subjects to avoid Unity history reuse,
                # but allow Unity history images as a fallback (they're the closest topical match).
                cross_subject_bonus = 0
                if entry.get("subject") and entry["subject"] not in {"history", "history-aqa"}:
                    cross_subject_bonus = 0  # neutral — Unity history heroes are still good
                score = title_hits * 3 + tag_hits + cross_subject_bonus
                if score > 0 and (best is None or score > best[0]):
                    best = (score, entry, {"title_hits": title_hits, "tag_hits": tag_hits, "query_terms": sorted(query_words)[:8]})

            proposal = {
                "unit_slug": unit["slug"],
                "unit_name": unit["name"],
                "lesson_id": L["id"],
                "lesson_number": L["lesson_number"],
                "lesson_title": L["title"],
                "hero_keywords": hero_keywords,
                "hero_image_caption": content.get("hero_image_caption"),
                "match": None,
                "score": 0,
            }
            if best:
                score, entry, signals = best
                taken_in_unit.add(entry["hero_url"])
                proposal["match"] = {
                    "hero_url": entry["hero_url"],
                    "title": entry["title"],
                    "subject": entry.get("subject"),
                    "unit": entry.get("unit"),
                    "tags_sample": (entry.get("tags") or [])[:8],
                }
                proposal["score"] = score
                proposal["match_signals"] = signals
            proposals.append(proposal)

    PROPOSALS_PATH.write_text(json.dumps(proposals, indent=2, ensure_ascii=False), encoding="utf-8")
    matched = sum(1 for p in proposals if p["match"])
    print(f"\nProposed matches: {matched}/{len(proposals)} ({skipped} skipped — no content JSON)")
    print(f"Score distribution: 0={sum(1 for p in proposals if p['score']==0)} | 1-3={sum(1 for p in proposals if 1<=p['score']<=3)} | 4-6={sum(1 for p in proposals if 4<=p['score']<=6)} | 7+={sum(1 for p in proposals if p['score']>=7)}")
    print(f"Proposals saved to: {PROPOSALS_PATH}")
    print("\nLow/no-score lessons (will need Unsplash QA):")
    low = [p for p in proposals if p["score"] < 3][:20]
    for p in low:
        print(f"  [score {p['score']:>2}] {p['unit_slug']:40s} L{p['lesson_number']:>2} {p['lesson_title'][:60]}")
    if sum(1 for p in proposals if p['score'] < 3) > 20:
        print(f"  ... and {sum(1 for p in proposals if p['score'] < 3) - 20} more")

    # ─────────────── Phase 3: APPLY (only with --apply)

    if not args.apply:
        print("\nDry run. Re-run with --apply to push these to Supabase.")
        return

    print("\nApplying proposals to Supabase...")
    pushed = 0
    for p in proposals:
        if not p["match"]:
            continue
        sb.table("lessons").update(
            {
                "hero_image_url": p["match"]["hero_url"],
                "hero_image_alt": p["lesson_title"],
                "hero_image_caption": p.get("hero_image_caption"),
                "hero_image_position": "center",
            }
        ).eq("id", p["lesson_id"]).execute()
        pushed += 1
    print(f"Pushed {pushed} hero image assignments to Supabase.")


if __name__ == "__main__":
    main()
