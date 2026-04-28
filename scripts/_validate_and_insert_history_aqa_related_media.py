"""Validate generated related_media JSONs and merge-safe insert into Supabase.

For each lesson JSON in scripts/_content_history-aqa/related_media/lessons/:
1. Schema check — flat list of category dicts, required minima.
2. URL spot-check — YouTube oembed for every YT link (catches dead videos that
   curl HEAD would miss). JustWatch / BBC Bitesize / generic URLs assumed
   verified by the agent (the prompt mandates it).
3. Merge with current Supabase row — preserve any existing "Lesson Podcast"
   entry under Podcasts (the podcast pipeline injects this concurrently;
   we must not clobber it).
4. With --insert flag, push the merged result. Without, dry-run.

Filename convention: {unit-slug}_{NN}.json

Usage:
  python scripts/_validate_and_insert_history_aqa_related_media.py
  python scripts/_validate_and_insert_history_aqa_related_media.py --insert
  python scripts/_validate_and_insert_history_aqa_related_media.py --filter germany
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.supabase_client import get_client

LESSONS_DIR = ROOT / "scripts" / "_content_history-aqa" / "related_media" / "lessons"


REQUIRED_CATEGORIES = {
    # at least one item from each of these top-level groups
    "Podcasts": ["Podcasts", "Podcast"],
    "Videos & Channels": ["Videos & Channels", "Videos and Channels", "Videos", "Video & Channels", "Video"],
    "Movies/TV/Docs": ["Movies", "TV Shows", "Movies & TV", "Documentaries", "Movies, TV & Documentaries", "Movies & Documentaries"],
    "Study Tools": ["Study Tools", "Study Tool"],
}


def youtube_id(url: str) -> str | None:
    if "youtube.com" in url or "youtu.be" in url:
        try:
            parsed = urllib.parse.urlparse(url)
            if "youtu.be" in parsed.netloc:
                return parsed.path.lstrip("/").split("/")[0] or None
            qs = urllib.parse.parse_qs(parsed.query)
            if "v" in qs:
                return qs["v"][0]
            # /watch/{id} or /shorts/{id}
            m = re.search(r"/(?:watch|shorts|embed)/([\w-]{11})", parsed.path)
            if m:
                return m.group(1)
        except Exception:
            pass
    return None


def oembed_check(url: str) -> tuple[bool, str]:
    """Return (ok, msg). Verifies a YouTube watch/short URL via oembed."""
    yid = youtube_id(url)
    if not yid:
        # Channel/playlist URLs: skip
        if "youtube.com/@" in url or "youtube.com/channel/" in url or "youtube.com/playlist" in url:
            return True, "channel/playlist (skipped)"
        return False, "could not extract YouTube id"
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={yid}&format=json"
    try:
        req = urllib.request.Request(oembed_url, headers={"User-Agent": "StudyVault/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                return True, "ok"
            return False, f"oembed status {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"oembed HTTP {e.code}"
    except Exception as e:
        return False, f"oembed error: {e}"


def category_match(actual: str, candidates: list[str]) -> bool:
    a = (actual or "").strip().lower()
    return any(a == c.lower() for c in candidates)


def validate_schema(media: list, lesson_label: str) -> list[str]:
    issues = []
    if not isinstance(media, list):
        issues.append("not a list")
        return issues
    total_items = 0
    found = {k: False for k in REQUIRED_CATEGORIES}
    for cat in media:
        if not isinstance(cat, dict):
            issues.append("category entry is not a dict")
            continue
        cat_name = cat.get("category", "")
        items = cat.get("items")
        if items is None:
            issues.append(f"category '{cat_name}' has no items field (or null)")
            continue
        if not isinstance(items, list):
            issues.append(f"category '{cat_name}' items is not a list")
            continue
        total_items += len(items)
        for group, candidates in REQUIRED_CATEGORIES.items():
            if category_match(cat_name, candidates) and items:
                found[group] = True
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                issues.append(f"category '{cat_name}' item[{i}] not a dict")
                continue
            for k in ("url", "title", "description"):
                if not item.get(k):
                    issues.append(f"category '{cat_name}' item[{i}] missing {k}")
    if total_items < 6:
        issues.append(f"only {total_items} total items (need >=6)")
    for group, ok in found.items():
        if not ok:
            issues.append(f"missing required category group: {group}")
    return issues


def validate_youtube_urls(media: list) -> list[tuple[str, str]]:
    """Returns [(url, error_msg), ...] for any YouTube URL that fails oembed."""
    yt_urls = []
    for cat in media or []:
        if not isinstance(cat, dict):
            continue
        for item in cat.get("items") or []:
            url = (item or {}).get("url") or ""
            if "youtube.com" in url or "youtu.be" in url:
                yt_urls.append(url)
    failures = []
    if not yt_urls:
        return failures
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(oembed_check, u): u for u in yt_urls}
        for fut in as_completed(futures):
            url = futures[fut]
            ok, msg = fut.result()
            if not ok:
                failures.append((url, msg))
    return failures


def parse_filename(name: str):
    if not name.endswith(".json"):
        return None, None
    stem = name[:-5]
    m = re.match(r"^(.+)_(\d{1,3})$", stem)
    if not m:
        return None, None
    return m.group(1), int(m.group(2))


def merge_preserving_lesson_podcast(new_media: list, current_media: list) -> list:
    """Insert any existing Lesson Podcast entry into new_media's Podcasts category."""
    lesson_podcast = None
    for cat in current_media or []:
        if not isinstance(cat, dict):
            continue
        if (cat.get("category") or "").lower() in ("podcasts", "podcast"):
            for item in cat.get("items") or []:
                if isinstance(item, dict) and (item.get("title") or "").strip().lower() == "lesson podcast":
                    lesson_podcast = item
                    break
        if lesson_podcast:
            break
    if not lesson_podcast:
        return new_media

    # Find or create Podcasts category in new_media and prepend
    for cat in new_media:
        if (cat.get("category") or "").lower() in ("podcasts", "podcast"):
            existing_items = cat.get("items") or []
            # Avoid duplicating if agent included a Lesson Podcast
            if not any(isinstance(it, dict) and (it.get("title") or "").lower() == "lesson podcast" for it in existing_items):
                cat["items"] = [lesson_podcast] + existing_items
            return new_media
    new_media.insert(0, {
        "category": "Podcasts",
        "emoji": "&#127911;",
        "items": [lesson_podcast],
    })
    return new_media


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--insert", action="store_true", help="Push merged related_media to Supabase")
    parser.add_argument("--filter", help="Only process filenames containing this substring")
    parser.add_argument("--skip-yt", action="store_true", help="Skip YouTube oembed validation (fast path)")
    args = parser.parse_args()

    sb = get_client() if args.insert else None
    sub_id = None
    if sb:
        sub = (
            sb.table("subjects")
            .select("id")
            .eq("slug", "history-aqa")
            .is_("school_id", "null")
            .single()
            .execute()
            .data
        )
        sub_id = sub["id"]

    if not LESSONS_DIR.exists():
        print(f"No generated related_media found at {LESSONS_DIR}")
        return

    files = sorted(LESSONS_DIR.glob("*.json"))
    if args.filter:
        files = [f for f in files if args.filter in f.name]
    if not files:
        print("No matching JSON files.")
        return

    pass_count = 0
    fail_count = 0
    failures = []
    inserted = 0

    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            failures.append((f.name, [f"JSON parse error: {e}"]))
            fail_count += 1
            continue

        issues = validate_schema(data, f.name)
        if issues:
            failures.append((f.name, issues))
            fail_count += 1
            continue

        if not args.skip_yt:
            yt_failures = validate_youtube_urls(data)
            if yt_failures:
                failures.append((f.name, [f"dead YT: {url} ({msg})" for url, msg in yt_failures]))
                fail_count += 1
                continue

        pass_count += 1

        if args.insert:
            unit_slug, lesson_number = parse_filename(f.name)
            if not unit_slug:
                failures.append((f.name, ["bad filename"]))
                fail_count += 1
                pass_count -= 1
                continue
            try:
                unit = (
                    sb.table("units")
                    .select("id")
                    .eq("subject_id", sub_id)
                    .eq("slug", unit_slug)
                    .single()
                    .execute()
                    .data
                )
                lesson_row = (
                    sb.table("lessons")
                    .select("id, related_media")
                    .eq("unit_id", unit["id"])
                    .eq("lesson_number", lesson_number)
                    .single()
                    .execute()
                    .data
                )
            except Exception as e:
                failures.append((f.name, [f"DB lookup failed: {e}"]))
                fail_count += 1
                pass_count -= 1
                continue
            merged = merge_preserving_lesson_podcast(data, lesson_row.get("related_media") or [])
            sb.table("lessons").update({"related_media": merged}).eq("id", lesson_row["id"]).execute()
            inserted += 1

    print(f"\n{'='*60}")
    print(f"Validated: {pass_count} pass, {fail_count} fail (of {len(files)})")
    if args.insert:
        print(f"Inserted (merge-safe): {inserted}")
    print(f"{'='*60}\n")
    if failures:
        print("FAILURES:")
        for name, issues in failures:
            print(f"\n  {name}:")
            for i in issues[:6]:
                print(f"    - {i}")
            if len(issues) > 6:
                print(f"    ... and {len(issues) - 6} more")


if __name__ == "__main__":
    main()
