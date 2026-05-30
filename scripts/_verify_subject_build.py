"""Verify a subject build is shippable.

Runs the checks that have caught real issues on past builds:
  - all units have image_url
  - quote_ticker_html exists and is wrapped in the proper structure
  - guide_pages exist for revision-technique
  - every lesson has description, hero_image_url, related_media
  - related_media meets per-category minimums
  - every YouTube ID in related_media is alive (verified via oembed,
    NOT curl HEAD — YT returns 200 for deleted videos)
  - free-tier policy: no Gemini diagram figures, no youtube_video_id
    on article lessons
  - fieldwork-keyword lessons begin with a <div class="lesson-notice">
    block (the school-fieldwork-is-different reminder)
  - every local /images/ asset referenced by index.html exists on disk
    (catches broken homepage cards — see _verify_homepage_images.py)

Exit code 0 = ship-ready, 1 = issues found.

Usage:
  python scripts/_verify_subject_build.py geography-edexcel-b
  python scripts/_verify_subject_build.py geography-eduqas --school unity
  python scripts/_verify_subject_build.py geography-edexcel-b --skip-yt   (faster)
"""

import argparse
import os
import re
import sys
import time
import urllib.error
import urllib.request

from supabase import create_client

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _verify_homepage_images import find_missing_images

YT_RE = re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([\w\-]{11})")
DIAGRAM_RE = re.compile(r'<figure[^>]*class="[^"]*\b(?:diagram|lesson-diagram)\b', re.IGNORECASE)
NOTICE_RE = re.compile(r'<div\s+class="lesson-notice"', re.IGNORECASE)
QUOTE_WRAPPER_RE = re.compile(
    r'<div[^>]*class="quote-ticker"[^>]*>\s*<div[^>]*class="quote-ticker-track"',
    re.IGNORECASE,
)
FIELDWORK_KEYWORDS = ("fieldwork", "enquiry", "investigation")

# Required related_media coverage. Subject-agnostic minimums.
MIN_TOTAL_ITEMS = 6
REQUIRED_CATEGORY_GROUPS = [
    # at least one item from each group must be present
    ("Podcasts",),
    ("Videos & Channels",),
    ("Movies", "TV Shows", "Documentaries"),
    ("Study Tools",),
]


def yt_alive(video_id, cache):
    """Return True if a YouTube video is reachable via oembed.

    HEAD requests return 200 even for deleted videos — only oembed gives
    a real 404. Cached per-run because the same ID often appears across
    many lessons.
    """
    if video_id in cache:
        return cache[video_id]
    url = (
        "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v="
        + video_id
        + "&format=json"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            cache[video_id] = r.status == 200
    except urllib.error.HTTPError:
        cache[video_id] = False
    except Exception:
        cache[video_id] = None  # network blip; treat as unknown, not dead
    time.sleep(0.05)
    return cache[video_id]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="subject slug, e.g. geography-edexcel-b")
    ap.add_argument(
        "--school",
        default=None,
        help="school slug (e.g. unity) or 'generic' for free-tier (default: generic)",
    )
    ap.add_argument(
        "--skip-yt", action="store_true", help="skip per-video oembed verification"
    )
    args = ap.parse_args()

    sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])

    q = sb.table("subjects").select(
        "id, slug, name, school_id, settings, exam_board"
    ).eq("slug", args.slug)
    if args.school and args.school != "generic":
        schools = sb.table("schools").select("id, slug").eq("slug", args.school).execute().data
        if not schools:
            print(f"School '{args.school}' not found", file=sys.stderr)
            sys.exit(2)
        q = q.eq("school_id", schools[0]["id"])
    else:
        q = q.is_("school_id", "null")
    rows = q.execute().data
    if not rows:
        print(f"Subject '{args.slug}' not found", file=sys.stderr)
        sys.exit(2)
    subject = rows[0]
    is_free_tier = subject.get("school_id") is None

    print(f"Verifying {subject['name']} ({subject['slug']}) — "
          f"{'free-tier' if is_free_tier else 'bespoke'}\n")

    issues = []
    warnings = []

    # ----- subject.settings -----
    settings = subject.get("settings") or {}
    if not isinstance(settings, dict):
        issues.append("subject.settings is not a dict (likely json.dumps'd) — "
                      "breaks quote ticker silently")
    qt = settings.get("quote_ticker_html") or ""
    if not qt:
        issues.append("subject.settings.quote_ticker_html missing")
    elif not QUOTE_WRAPPER_RE.search(qt):
        issues.append(
            'quote_ticker_html missing wrapper: must start with '
            '<div class="quote-ticker"><div class="quote-ticker-track">'
        )

    # ----- units -----
    units = sb.table("units").select(
        "id, slug, name, image_url, sort_order"
    ).eq("subject_id", subject["id"]).order("sort_order").execute().data
    if not units:
        issues.append("subject has no units")
    for u in units:
        if not (u.get("image_url") or "").strip():
            issues.append(f"unit '{u['slug']}' has no image_url")

    # ----- guide_pages -----
    gpq = sb.table("guide_pages").select("id, slug, guide_type").eq("subject_id", subject["id"])
    gps = gpq.execute().data
    rev = [g for g in gps if g.get("guide_type") == "revision-technique"]
    if len(rev) < 3:
        issues.append(f"only {len(rev)} revision-technique guide pages "
                      "(expect at least 3 — 1 hub + technique pages)")

    # ----- lessons -----
    unit_ids = [u["id"] for u in units]
    lessons = []
    for i in range(0, len(unit_ids), 50):
        res = sb.table("lessons").select(
            "id, title, lesson_number, description, hero_image_url, "
            "content_html, related_media, youtube_video_id, practice_data, unit_id"
        ).in_("unit_id", unit_ids[i:i + 50]).execute().data
        lessons.extend(res)
    print(f"Lessons: {len(lessons)}")

    yt_cache = {}
    yt_dead = []
    for l in lessons:
        ctx = f"L{l.get('lesson_number')}: {l.get('title')}"
        is_practice = bool(l.get("practice_data"))

        if not (l.get("description") or "").strip():
            issues.append(f"{ctx} — missing description")

        if not (l.get("hero_image_url") or "").strip():
            if is_practice:
                # Some practice subjects (e.g. Geography Skills) skip per-lesson
                # heroes and use the unit hero instead — convention varies.
                pass
            else:
                issues.append(f"{ctx} — missing hero_image_url")

        # Free-tier policy: no Gemini diagrams, no cinematic videos on article lessons
        ch = l.get("content_html") or ""
        if is_free_tier and DIAGRAM_RE.search(ch):
            issues.append(f"{ctx} — contains <figure class=\"diagram\"> "
                          "(free tier strips Gemini diagrams)")
        yt = (l.get("youtube_video_id") or "").strip()
        if is_free_tier and yt and yt != "practice-only" and ch and not is_practice:
            warnings.append(f"{ctx} — has youtube_video_id on free-tier article "
                            "(cinematic videos are Unity-only)")

        # Fieldwork-notice — applies to article lessons in subjects that
        # actually involve physical fieldwork (Geography, Biology, RS field
        # studies). The keyword 'investigation' overlaps with statistical
        # enquiries; skip subjects where the word doesn't carry a safeguarding
        # implication.
        FIELDWORK_SAFE_SUBJECTS = ("statistics-",)  # statistical investigations, not field trips
        is_fieldwork_subject = not any(args.slug.startswith(p) for p in FIELDWORK_SAFE_SUBJECTS)
        title_l = (l.get("title") or "").lower()
        if is_fieldwork_subject and not is_practice and any(k in title_l for k in FIELDWORK_KEYWORDS) and ch:
            head = ch[:400]
            if not NOTICE_RE.search(head):
                issues.append(f"{ctx} — fieldwork-keyword lesson without "
                              "<div class=\"lesson-notice\"> block at top of content_html")

        # related_media — required on article lessons. Practice subjects vary
        # (Geography Skills has none; English Language has full coverage).
        rm = l.get("related_media") or []
        if not rm:
            if is_practice:
                pass  # subject-specific convention; not flagged
            else:
                issues.append(f"{ctx} — related_media is empty")
            continue

        # Structural validity — each category must have items as a list, not null.
        # Catches the 'looks filled but items=null' shape that crashed lesson-loader
        # in Apr 2026 on Geography free-tier lessons. Always fails ship, on any
        # tier, even practice subjects.
        for ci, c in enumerate(rm):
            if not isinstance(c, dict):
                issues.append(f"{ctx} — related_media[{ci}] is not an object")
                continue
            if "items" in c and c["items"] is None:
                issues.append(f"{ctx} — related_media[{ci}] '{c.get('category','?')}' "
                              "has items=null (must be a list, even if empty)")
            elif "items" in c and not isinstance(c["items"], list):
                issues.append(f"{ctx} — related_media[{ci}] '{c.get('category','?')}' "
                              f"items must be a list, got {type(c['items']).__name__}")

        if is_practice:
            continue  # have media — that's enough; no coverage rules

        total_items = sum(
            len(c["items"]) for c in rm
            if isinstance(c, dict) and isinstance(c.get("items"), list)
        )
        if total_items < MIN_TOTAL_ITEMS:
            issues.append(f"{ctx} — only {total_items} related_media items "
                          f"(min {MIN_TOTAL_ITEMS})")

        cats_present = {(c.get("category") or "") for c in rm}
        for group in REQUIRED_CATEGORY_GROUPS:
            if not (cats_present & set(group)):
                issues.append(f"{ctx} — related_media missing any of: " + ", ".join(group))

        # YouTube oembed verification
        if not args.skip_yt:
            for cat in rm:
                for item in cat.get("items") or []:
                    url = item.get("url") or ""
                    m = YT_RE.search(url)
                    if not m:
                        continue
                    vid = m.group(1)
                    alive = yt_alive(vid, yt_cache)
                    if alive is False:
                        yt_dead.append((ctx, item.get("title", ""), url))

    if yt_dead:
        for ctx, title, url in yt_dead:
            issues.append(f"{ctx} — dead YouTube ref: {title} ({url})")

    # ----- homepage subject images exist (index.html references a local file) -----
    # Catches the Psychology/Sociology failure mode: a card/picker/meta entry
    # wired to /images/subject-{slug}.jpg with no committed file -> broken card.
    missing_imgs, _ = find_missing_images()
    for ref in missing_imgs:
        issues.append(f"homepage — index.html references {ref} but no such file exists in images/")

    # ----- report -----
    print()
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  ! {w}")
        print()
    if issues:
        print(f"FAIL — {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    print("PASS — subject is ship-ready.")


if __name__ == "__main__":
    main()
