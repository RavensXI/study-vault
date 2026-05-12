"""
Phase 4 hero images for OCR History (history-ocr).
117 lessons across 12 units.

Strategy: INDEX-ONLY — do NOT call Unsplash or download anything.
  1. Load hero_keywords from scripts/_content_history-ocr/{unit_slug}/L{N}.json
  2. Search the hero index with min_score=3
  3. If a match is found → set hero_image_url, alt, caption, position on Supabase lesson row
  4. If no match → leave hero NULL (Tom will backfill manually in QA)

After the lesson loop, also ensure every unit has image_url set:
  - The Postgres trigger auto-syncs unit.image_url when L1 gets a hero.
  - For units where L1 has no hero → pick the best-hero lesson in the unit.
  - For units where no lesson got a hero → pick any history R2 image from the index.

Re-runnable: already-set heroes are left as-is (skip if hero_image_url is already populated).
Override mode: pass --force to re-evaluate all lessons even if already set.

Usage:
    python scripts/_heroes_history-ocr.py
    python scripts/_heroes_history-ocr.py --force
    python scripts/_heroes_history-ocr.py --dry-run
"""

import json
import os
import sys

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.supabase_client import get_client
from lib.hero_index import search_heroes

SUBJECT_ID = "0ba3a850-1759-410f-97fc-347a78bd5e3a"
SUBJECT_SLUG = "history-ocr"
CONTENT_DIR = os.path.join(SCRIPT_DIR, "_content_history-ocr")
HERO_REUSE_MIN_SCORE = 3

# ── Lesson manifest in display order ────────────────────────────────────────
# (unit_slug, lesson_numbers...)
UNIT_LESSONS = [
    ("china-people-state-1950-1981",        list(range(1, 10))),   # 9 lessons
    ("english-reformation-1520-1550",       list(range(1, 11))),   # 10 lessons
    ("germany-people-state-1925-1955",      list(range(1, 10))),   # 9 lessons
    ("impact-empire-britain-1688-1730",     list(range(1, 11))),   # 10 lessons
    ("international-relations-1918-1975",   list(range(1, 13))),   # 12 lessons
    ("migration-to-britain-1000-2010",      list(range(1, 11))),   # 10 lessons
    ("personal-rule-restoration-1629-1660", list(range(1, 11))),   # 10 lessons
    ("power-monarchy-democracy-1000-2014",  list(range(1, 11))),   # 10 lessons
    ("south-africa-people-state-1960-1994", list(range(1, 10))),   # 9 lessons
    ("usa-people-state-1919-1948",          list(range(1, 10))),   # 9 lessons
    ("usa-people-state-1945-1974",          list(range(1, 10))),   # 9 lessons
    ("war-british-society-790-2010",        list(range(1, 11))),   # 10 lessons
]

LESSONS = [(unit, n) for unit, ns in UNIT_LESSONS for n in ns]


def load_json(unit_slug, lesson_number):
    # Try both naming conventions: L1.json and L01.json
    for name in (f"L{lesson_number}.json", f"L{lesson_number:02d}.json"):
        path = os.path.join(CONTENT_DIR, unit_slug, name)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError(f"No JSON for {unit_slug}/L{lesson_number} (tried L{lesson_number}.json and L{lesson_number:02d}.json)")


def find_hero_from_index(keywords):
    """Search the hero index. Returns the top match dict, or None."""
    query_str = " ".join(keywords)
    matches = search_heroes(query_str, min_score=HERO_REUSE_MIN_SCORE)
    if matches:
        return matches[0]
    return None


def make_alt(lesson_title, unit_slug):
    unit_label = unit_slug.replace("-", " ").title()
    return f"{lesson_title} — {unit_label} (OCR History)"


def main():
    force = "--force" in sys.argv
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("[DRY-RUN MODE — no Supabase writes]")
    if force:
        print("[FORCE MODE — re-evaluating all lessons even if hero already set]")

    sb = get_client()

    # Build unit slug → unit_id map
    units_resp = sb.table("units").select("id,slug,name,image_url").eq("subject_id", SUBJECT_ID).execute()
    unit_map = {u["slug"]: u for u in units_resp.data}
    print(f"Units found in Supabase: {sorted(unit_map.keys())}\n")

    stats = {
        "set": 0,
        "skipped_already_set": 0,
        "no_match": 0,
        "error": 0,
    }
    no_hero_lessons = []           # (unit_slug, lesson_number, lesson_title)
    unit_heroes_set = {}           # unit_slug → list of (lesson_number, hero_url)

    for unit_slug, lesson_number in LESSONS:
        label = f"{unit_slug}/L{lesson_number:02d}"

        # Load JSON for keywords
        try:
            data = load_json(unit_slug, lesson_number)
        except FileNotFoundError:
            print(f"  [MISS] No JSON: {label}")
            stats["error"] += 1
            no_hero_lessons.append((unit_slug, lesson_number, "???"))
            continue

        keywords = data.get("hero_keywords") or []
        json_caption = data.get("hero_image_caption", "")

        # Get lesson row from Supabase
        if unit_slug not in unit_map:
            print(f"  [ERR] Unit not in Supabase: {unit_slug}")
            stats["error"] += 1
            continue

        unit_id = unit_map[unit_slug]["id"]
        lesson_resp = (
            sb.table("lessons")
            .select("id,title,lesson_number,hero_image_url")
            .eq("unit_id", unit_id)
            .eq("lesson_number", lesson_number)
            .execute()
        )

        if not lesson_resp.data:
            print(f"  [ERR] Lesson not found in Supabase: {label}")
            stats["error"] += 1
            continue

        lesson = lesson_resp.data[0]
        lesson_id = lesson["id"]
        lesson_title = lesson.get("title", "")

        # Skip if already set (unless force mode)
        if lesson.get("hero_image_url") and not force:
            print(f"  [SKIP] Already set: {label} — {lesson_title}")
            stats["skipped_already_set"] += 1
            if unit_slug not in unit_heroes_set:
                unit_heroes_set[unit_slug] = []
            unit_heroes_set[unit_slug].append((lesson_number, lesson["hero_image_url"]))
            continue

        print(f"\n{label}  [{lesson_title}]")
        print(f"  keywords: {keywords}")

        match = find_hero_from_index(keywords)

        if not match:
            print(f"  [NO MATCH] — leaving hero NULL")
            stats["no_match"] += 1
            no_hero_lessons.append((unit_slug, lesson_number, lesson_title))
            continue

        hero_url = match["hero_url"]
        print(f"  [REUSE] score={match['score']}  {hero_url[:80]}")

        # Build caption: prefer the content-author's editorial caption; fall back to index title
        final_caption = json_caption.strip() if json_caption else match.get("title", "")
        alt_text = make_alt(lesson_title, unit_slug)

        if not dry_run:
            sb.table("lessons").update({
                "hero_image_url": hero_url,
                "hero_image_alt": alt_text,
                "hero_image_caption": final_caption,
                "hero_image_position": "center center",
            }).eq("id", lesson_id).execute()

        stats["set"] += 1
        if unit_slug not in unit_heroes_set:
            unit_heroes_set[unit_slug] = []
        unit_heroes_set[unit_slug].append((lesson_number, hero_url))

    # ── Unit image_url back-fill ──────────────────────────────────────────────
    # The Postgres trigger syncs unit.image_url when L1 is updated.
    # We only need to manually patch units where L1 had no hero.
    print("\n" + "=" * 60)
    print("UNIT IMAGE BACK-FILL")
    print("=" * 60)

    for unit_slug, unit_data in unit_map.items():
        unit_id = unit_data["id"]
        current_unit_img = unit_data.get("image_url")

        lessons_with_hero = unit_heroes_set.get(unit_slug, [])

        # Check if L1 was among those set in this run
        l1_set = any(n == 1 for n, _ in lessons_with_hero)

        if l1_set:
            # Trigger will handle it automatically
            print(f"  {unit_slug}: L1 was set → trigger will auto-sync unit image")
            continue

        # L1 was not set in this run — check if it was already set in Supabase
        l1_resp = (
            sb.table("lessons")
            .select("hero_image_url")
            .eq("unit_id", unit_id)
            .eq("lesson_number", 1)
            .execute()
        )
        l1_hero = l1_resp.data[0].get("hero_image_url") if l1_resp.data else None

        if l1_hero:
            # L1 already had a hero → unit image should already be set by trigger
            print(f"  {unit_slug}: L1 already has hero → unit image should be synced")
            if not current_unit_img and not dry_run:
                sb.table("units").update({"image_url": l1_hero}).eq("id", unit_id).execute()
                print(f"    Patched unit image from L1 hero (trigger may not have fired yet)")
            continue

        # L1 has no hero — find any lesson in this unit that did get a hero
        if lessons_with_hero:
            # Pick the lowest lesson number with a hero (most "introductory")
            lessons_with_hero_sorted = sorted(lessons_with_hero, key=lambda x: x[0])
            best_n, best_url = lessons_with_hero_sorted[0]
            print(f"  {unit_slug}: L1 has no hero → using L{best_n} hero for unit image")
            if not dry_run:
                sb.table("units").update({"image_url": best_url}).eq("id", unit_id).execute()
            continue

        # No lesson in this unit got a hero in this run — check if any lessons have heroes in Supabase
        all_lessons_resp = (
            sb.table("lessons")
            .select("lesson_number,hero_image_url")
            .eq("unit_id", unit_id)
            .order("lesson_number")
            .execute()
        )
        existing_heroes = [(l["lesson_number"], l["hero_image_url"])
                           for l in all_lessons_resp.data if l.get("hero_image_url")]
        if existing_heroes:
            best_n, best_url = existing_heroes[0]
            print(f"  {unit_slug}: using existing L{best_n} hero for unit image")
            if not dry_run:
                sb.table("units").update({"image_url": best_url}).eq("id", unit_id).execute()
            continue

        # Absolute fallback: search the index broadly for any history R2 image
        print(f"  {unit_slug}: NO heroes at all → searching index for history fallback...")
        fallback_queries = [
            unit_slug.replace("-", " "),
            "history medieval England",
            "history war Britain society",
        ]
        fallback_url = None
        for fq in fallback_queries:
            fb_matches = search_heroes(fq, min_score=2)
            for fb in fb_matches:
                if "history" in fb["subject"] and "r2.dev" in fb["hero_url"]:
                    fallback_url = fb["hero_url"]
                    print(f"    Fallback: [{fb['score']}] {fb['title'][:50]} → {fallback_url[:70]}")
                    break
            if fallback_url:
                break

        if fallback_url and not dry_run:
            sb.table("units").update({"image_url": fallback_url}).eq("id", unit_id).execute()
        elif not fallback_url:
            print(f"    [WARN] Could not find any fallback for {unit_slug} — unit image_url remains NULL")

    # ── Final summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total = len(LESSONS)
    print(f"Total lessons:          {total}")
    print(f"Heroes set from index:  {stats['set']}")
    print(f"Already set (skipped):  {stats['skipped_already_set']}")
    print(f"No index match (NULL):  {stats['no_match']}")
    print(f"Errors:                 {stats['error']}")
    covered = stats["set"] + stats["skipped_already_set"]
    print(f"Total with heroes:      {covered}/{total}")

    if no_hero_lessons:
        print(f"\nLessons WITHOUT a hero ({len(no_hero_lessons)}) — Tom to backfill manually:")
        current_unit = None
        for unit_slug, lesson_number, title in sorted(no_hero_lessons, key=lambda x: (x[0], x[1])):
            if unit_slug != current_unit:
                print(f"\n  {unit_slug}:")
                current_unit = unit_slug
            print(f"    L{lesson_number:02d}  {title}")
    else:
        print("\nAll 117 lessons have heroes.")


if __name__ == "__main__":
    main()
