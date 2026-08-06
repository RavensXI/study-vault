# -*- coding: utf-8 -*-
"""Azure narration for the five 2027 historic-environment site lessons.

Run ONLY after the fact-check findings are applied (fact-check before
narration — pipeline rule). Voice by house convention: Ollie odd lessons,
Ada even. R2 keys follow each subject's existing convention:
  history-aqa/{unit_slug}/narration_lesson-{NN}_{nid}.mp3
  history/{unit_slug}/narration_lesson-{NN}_{nid}.mp3   (Unity)

Usage:
    python scripts/history-sites/narrate_site_lessons.py --dry-run
    python scripts/history-sites/narrate_site_lessons.py
    python scripts/history-sites/narrate_site_lessons.py --force   # re-narrate
"""
import argparse
import os
import sys
import time

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL
from lib.narration import (
    extract_narration_chunks,
    generate_audio_rest,
    get_mp3_duration,
    get_voice_for_lesson,
    AZURE_KEY,
)

# (subject slug, generic?, unit-name fragment, lesson number)
TARGETS_2027 = [
    ("history-aqa", True, "Norman England", 13),
    ("history-aqa", True, "Medieval England", 12),
    ("history-aqa", True, "Elizabethan England", 13),
    ("history-aqa", True, "Restoration England", 13),
    ("history", False, "Elizabethan England", 16),
]
TARGETS_2028 = [
    ("history-aqa", True, "Norman England", 14),
    ("history-aqa", True, "Medieval England", 13),
    ("history-aqa", True, "Elizabethan England", 14),
    ("history-aqa", True, "Restoration England", 14),
    ("history", False, "Elizabethan England", 17),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="re-narrate even if a manifest exists (post-fix re-runs)")
    ap.add_argument("--set", choices=["2027", "2028"], default="2027")
    args = ap.parse_args()

    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY not set")
        sys.exit(1)

    sb = get_client()
    r2 = None if args.dry_run else get_r2_client()
    total_clips, total_chars = 0, 0

    targets = TARGETS_2028 if args.set == "2028" else TARGETS_2027
    for slug, generic, frag, num in targets:
        subs = sb.table("subjects").select("id,school_id").eq("slug", slug).execute().data
        sub = [s for s in subs if (s["school_id"] is None) == generic][0]
        unit = [u for u in sb.table("units").select("id,slug,name").eq(
            "subject_id", sub["id"]).execute().data if frag in u["name"]][0]
        lesson = sb.table("lessons").select(
            "id,title,content_html,exam_tip_html,conclusion_html,narration_manifest"
        ).eq("unit_id", unit["id"]).eq("lesson_number", num).single().execute().data

        voice_name, voice_label = get_voice_for_lesson(num)
        print("\n%s / %s / L%d  (%s)" % (slug, unit["slug"], num, voice_label))
        print("  %s" % lesson["title"])

        if lesson.get("narration_manifest") and not args.force:
            print("  SKIP: manifest exists (%d clips) — use --force to re-narrate"
                  % len(lesson["narration_manifest"]))
            continue

        combined = ((lesson.get("content_html") or "")
                    + (lesson.get("exam_tip_html") or "")
                    + (lesson.get("conclusion_html") or ""))
        chunks = extract_narration_chunks(combined)
        if not chunks:
            print("  ERROR: no narration chunks found")
            continue
        chars = sum(len(t) for _, t in chunks)
        print("  %d chunks, %s chars" % (len(chunks), format(chars, ",")))
        total_chars += chars
        if args.dry_run:
            continue

        manifest = []
        for nid, text in chunks:
            key = "%s/%s/narration_lesson-%02d_%s.mp3" % (slug, unit["slug"], num, nid)
            mp3 = generate_audio_rest(text, voice_name)
            if mp3 is None:
                print("    FAILED %s" % nid)
                continue
            upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
            manifest.append({"id": nid, "src": "%s/%s" % (AUDIO_PUBLIC_URL, key),
                             "duration": get_mp3_duration(mp3)})
        if len(manifest) != len(chunks):
            print("  ERROR: %d/%d clips generated — manifest NOT written"
                  % (len(manifest), len(chunks)))
            continue
        sb.table("lessons").update({"narration_manifest": manifest}).eq(
            "id", lesson["id"]).execute()
        total_clips += len(manifest)
        print("  manifest written (%d clips)" % len(manifest))

    print("\nTOTAL: %d clips, %s chars (~$%.2f Azure)"
          % (total_clips, format(total_chars, ","), total_chars * 16 / 1_000_000))


if __name__ == "__main__":
    main()
