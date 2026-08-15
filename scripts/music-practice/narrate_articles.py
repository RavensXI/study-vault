# -*- coding: utf-8 -*-
"""Azure narration for the music-aqa article lessons (post fact-check).

Eleven lessons across the four AoS article units. Voice by house convention
(Ollie odd, Ada even). R2: music-aqa/{unit_slug}/narration_lesson-{NN}_{nid}.mp3

Usage:
    python scripts/music-practice/narrate_articles.py --dry-run
    python scripts/music-practice/narrate_articles.py [--force]
"""
import argparse
import os
import sys

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
from lib.narration import (extract_narration_chunks, generate_audio_rest,
                           get_mp3_duration, get_voice_for_lesson, AZURE_KEY)

ARTICLE_UNITS = ["aos1-western-classical", "aos2-popular-music",
                 "aos3-traditional-music", "aos4-since-1910"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", help="unit-slug:lesson-number, e.g. aos1-western-classical:2")
    args = ap.parse_args()
    only = None
    if args.only:
        u, n = args.only.rsplit(":", 1)
        only = (u, int(n))
    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY not set")
        sys.exit(1)
    sb = get_client()
    r2 = None if args.dry_run else get_r2_client()
    sub = [x for x in sb.table("subjects").select("id,school_id").eq(
        "slug", "music-aqa").execute().data if not x["school_id"]][0]
    total_clips, total_chars = 0, 0
    for uslug in ARTICLE_UNITS:
        unit = [u for u in sb.table("units").select("id,slug").eq(
            "subject_id", sub["id"]).execute().data if u["slug"] == uslug][0]
        for lesson in sb.table("lessons").select(
                "id,lesson_number,title,content_html,exam_tip_html,"
                "conclusion_html,narration_manifest").eq(
                "unit_id", unit["id"]).order("lesson_number").execute().data:
            num = lesson["lesson_number"]
            if only and (uslug, num) != only:
                continue
            voice_name, voice_label = get_voice_for_lesson(num)
            print("\n%s / L%d (%s)  %s" % (uslug, num, voice_label,
                                           lesson["title"][:52]))
            if lesson.get("narration_manifest") and not args.force:
                print("  SKIP: manifest exists (%d clips)"
                      % len(lesson["narration_manifest"]))
                continue
            combined = ((lesson.get("content_html") or "")
                        + (lesson.get("exam_tip_html") or "")
                        + (lesson.get("conclusion_html") or ""))
            chunks = extract_narration_chunks(combined)
            if not chunks:
                print("  ERROR: no narration chunks")
                continue
            chars = sum(len(t) for _, t in chunks)
            total_chars += chars
            print("  %d chunks, %s chars" % (len(chunks), format(chars, ",")))
            if args.dry_run:
                continue
            manifest = []
            for nid, text in chunks:
                key = "music-aqa/%s/narration_lesson-%02d_%s.mp3" % (uslug, num, nid)
                mp3 = generate_audio_rest(text, voice_name)
                if mp3 is None:
                    print("    FAILED %s" % nid)
                    continue
                upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
                manifest.append({"id": nid,
                                 "src": "%s/%s" % (AUDIO_PUBLIC_URL, key),
                                 "duration": get_mp3_duration(mp3)})
            if len(manifest) != len(chunks):
                print("  ERROR: %d/%d generated - manifest NOT written"
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
