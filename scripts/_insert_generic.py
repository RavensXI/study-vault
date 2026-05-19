"""Generic insert script — takes a subject slug as argument.

Patches lesson rows in Supabase from JSON files in scripts/_content_{slug}/lessons/*.json.
Each JSON file must have a `_lesson_id` field pointing to its target row.

Usage:
  python scripts/_insert_generic.py <subject-slug>
  python scripts/_insert_generic.py <subject-slug> --dry-run
"""
import argparse
import glob
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

import requests

ARTICLE_KEYS = [
    "description", "content_html", "exam_tip_html", "conclusion_html",
    "practice_questions", "knowledge_checks", "flashcard_questions",
    "glossary_terms", "hero_image_caption",
]

URL = os.environ["SUPABASE_URL"]
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}


def load_json(path: str) -> dict:
    raw = open(path, "rb").read()
    if raw[:3] == b"\xef\xbb\xbf":
        raw = raw[3:]
    return json.loads(raw.decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="Subject slug (e.g. electronics-eduqas)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    slug = args.slug

    scripts_dir = Path(__file__).resolve().parent
    lessons_dir = scripts_dir / f"_content_{slug}" / "lessons"
    if not lessons_dir.exists():
        print(f"ERROR: {lessons_dir} not found")
        sys.exit(1)

    # Fetch subject_id
    r = requests.get(
        f"{URL}/rest/v1/subjects",
        headers=H,
        params={"slug": f"eq.{slug}", "school_id": "is.null", "select": "id"},
    )
    if not r.ok or not r.json():
        print(f"ERROR: subject '{slug}' not found in Supabase")
        sys.exit(1)
    sid = r.json()[0]["id"]
    print(f"Subject id: {sid}")

    units = requests.get(
        f"{URL}/rest/v1/units",
        headers=H,
        params={"subject_id": f"eq.{sid}", "select": "id,slug"},
    ).json()
    unit_ids = ",".join(u["id"] for u in units)
    lessons = requests.get(
        f"{URL}/rest/v1/lessons",
        headers=H,
        params={"unit_id": f"in.({unit_ids})", "select": "id,slug,content_html", "limit": "500"},
    ).json()
    print(f"Shells: {len(lessons)} lesson rows across {len(units)} units")

    paths = sorted(glob.glob(str(lessons_dir / "*.json")))
    print(f"Found {len(paths)} content JSONs\n")

    ok = 0
    fail = 0
    skip = 0
    for p in paths:
        slug_base = os.path.splitext(os.path.basename(p))[0]
        try:
            data = load_json(p)
        except Exception as e:
            print(f"  [PARSE-FAIL] {slug_base}: {e}")
            fail += 1
            continue

        lid = data.get("_lesson_id")
        if not lid:
            print(f"  [SKIP] {slug_base} — no _lesson_id")
            skip += 1
            continue

        payload = {k: data[k] for k in ARTICLE_KEYS if k in data}
        if not payload:
            print(f"  [SKIP] {slug_base} — no content fields")
            skip += 1
            continue

        if args.dry_run:
            print(f"  [DRY] {slug_base[:55]:55s} -> {lid[:8]}  ({len(payload)} fields)")
            ok += 1
        else:
            resp = requests.patch(
                f"{URL}/rest/v1/lessons",
                headers=H,
                params={"id": f"eq.{lid}"},
                json=payload,
            )
            if resp.status_code >= 300:
                print(f"  [FAIL] {slug_base}: {resp.status_code} {resp.text[:160]}")
                fail += 1
            else:
                print(f"  [OK]   {slug_base[:55]:55s} -> {lid[:8]}")
                ok += 1

    print()
    print(f"=== Insert summary for {slug} ===")
    print(f"  OK   : {ok}")
    print(f"  FAIL : {fail}")
    print(f"  SKIP : {skip}")
    print(f"  Files: {len(paths)}  /  Shells in DB: {len(lessons)}")


if __name__ == "__main__":
    main()
