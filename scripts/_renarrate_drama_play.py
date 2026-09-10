"""Re-generate Azure TTS narration for ONE rebuilt AQA Drama set-play unit.

The three set-play units rebuilt in September 2026 (a-taste-of-honey,
the-empress, things-i-know-to-be-true) kept their lesson rows, so they arrive
here carrying a stale narration_manifest for content that no longer exists.
Unlike the build-time narration scripts this one therefore OVERWRITES rather
than skipping, and it prunes any manifest entry left over from a longer
previous lesson.

Voice assignment (CLAUDE.md convention):
  Odd lesson_number  -> Ollie (en-GB-OllieMultilingualNeural)
  Even lesson_number -> Ada   (en-GB-AdaMultilingualNeural)

R2 audio key (unchanged from the original build, so the same object is
replaced rather than orphaned):
  drama-aqa/{unit_slug}/narration_lesson-{NN}_{nid}.mp3

Usage:
  python scripts/_renarrate_drama_play.py the-empress --dry-run
  python scripts/_renarrate_drama_play.py the-empress
  python scripts/_renarrate_drama_play.py the-empress --lesson 3
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
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL
from lib.narration import (
    extract_narration_chunks,
    generate_audio_rest,
    get_mp3_duration,
    get_voice_for_lesson,
    AZURE_KEY,
)

SUBJECT_SLUG = "drama-aqa"
UNITS = ["a-taste-of-honey", "the-empress", "things-i-know-to-be-true"]


def process_lesson(sb, r2_client, unit_slug, unit_id, lesson_number, dry_run=False):
    voice_name, voice_label = get_voice_for_lesson(lesson_number)
    print(f"\n  {unit_slug} / Lesson {lesson_number:02d} ({voice_label})")
    print(f"  {'=' * 54}")

    lesson_start = time.time()
    lesson = (
        sb.table("lessons")
        .select("id, lesson_number, title, content_html, exam_tip_html, "
                "conclusion_html, narration_manifest")
        .eq("unit_id", unit_id)
        .eq("lesson_number", lesson_number)
        .single()
        .execute()
    ).data
    lesson_id = lesson["id"]
    print(f"  Title: {lesson['title']}")

    old = lesson.get("narration_manifest") or []
    if old:
        print(f"  Existing manifest: {len(old)} clips (will be replaced)")

    combined_html = (
        (lesson.get("content_html") or "")
        + (lesson.get("exam_tip_html") or "")
        + (lesson.get("conclusion_html") or "")
    )
    if not combined_html.strip():
        print("  SKIP: no content_html")
        return 0, 0, 0.0

    chunks = extract_narration_chunks(combined_html)
    if not chunks:
        print("  ERROR: no data-narration-id elements found")
        return 0, 0, 0.0
    ids = [nid for nid, _ in chunks]
    nums = sorted(int(n[1:]) for n in ids)
    if nums != list(range(1, len(nums) + 1)):
        print(f"  ERROR: narration ids are not contiguous from n1: {ids}")
        return 0, 0, 0.0
    print(f"  Found {len(chunks)} narration chunks, contiguous n1..n{len(chunks)}")

    if dry_run:
        total_chars = sum(len(text) for _, text in chunks)
        print(f"  [DRY RUN] would generate {len(chunks)} clips, ~{total_chars:,} chars")
        return 0, total_chars, 0.0

    manifest = []
    total_chars = 0
    total_duration = 0.0

    for nid, text in chunks:
        r2_key = f"{SUBJECT_SLUG}/{unit_slug}/narration_lesson-{lesson_number:02d}_{nid}.mp3"
        public_url = f"{AUDIO_PUBLIC_URL}/{r2_key}"
        total_chars += len(text)
        display = (text[:70] + "...") if len(text) > 70 else text
        display = display.encode("ascii", errors="replace").decode("ascii")
        print(f"    {nid}: {display}")

        mp3_bytes = generate_audio_rest(text, voice_name)
        if mp3_bytes is None:
            print(f"    FAILED for {nid}")
            continue
        duration = get_mp3_duration(mp3_bytes)
        total_duration += duration
        upload_bytes_to_r2(r2_client, AUDIO_BUCKET, r2_key, mp3_bytes, "audio/mpeg")
        manifest.append({"id": nid, "src": public_url, "duration": duration})
        print(f"           -> {len(mp3_bytes)/1024:.0f} KB, {duration:.1f}s, uploaded")

    if len(manifest) != len(chunks):
        print(f"  ERROR: only {len(manifest)}/{len(chunks)} clips generated — manifest NOT written")
        return 0, total_chars, 0.0

    sb.table("lessons").update({"narration_manifest": manifest}).eq("id", lesson_id).execute()
    elapsed = time.time() - lesson_start
    stale = max(0, len(old) - len(manifest))
    print(f"  Manifest replaced ({len(manifest)} entries, {total_duration:.1f}s audio, "
          f"{elapsed:.1f}s){f', {stale} stale entries dropped' if stale else ''}")
    return len(manifest), total_chars, elapsed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("unit", choices=UNITS)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--lesson", type=int, default=None)
    args = parser.parse_args()

    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY not set")
        sys.exit(1)

    print(f"Drama AQA - re-narration - {args.unit}")
    print("=" * 55)

    sb = get_client()
    subjects = (
        sb.table("subjects").select("id, slug")
        .eq("slug", SUBJECT_SLUG).is_("school_id", "null").execute()
    )
    if not subjects.data:
        print(f"ERROR: subject '{SUBJECT_SLUG}' not found")
        sys.exit(1)
    subject_id = subjects.data[0]["id"]

    units = (
        sb.table("units").select("id, slug")
        .eq("subject_id", subject_id).eq("slug", args.unit).execute()
    ).data
    if not units:
        print(f"ERROR: unit '{args.unit}' not found")
        sys.exit(1)
    unit_id = units[0]["id"]

    query = (sb.table("lessons").select("lesson_number")
             .eq("unit_id", unit_id).order("lesson_number"))
    if args.lesson:
        query = query.eq("lesson_number", args.lesson)
    lesson_numbers = [r["lesson_number"] for r in query.execute().data]
    print(f"Lessons to narrate: {len(lesson_numbers)}")

    r2_client = None if args.dry_run else get_r2_client()
    total_start = time.time()
    total_clips = 0
    total_chars = 0
    for n in lesson_numbers:
        try:
            clips, chars, _ = process_lesson(sb, r2_client, args.unit, unit_id, n,
                                             dry_run=args.dry_run)
            total_clips += clips
            total_chars += chars
        except Exception as e:
            print(f"  ERROR on lesson {n}: {e}")

    print(f"\n{'=' * 55}")
    print(f"TOTAL: {total_clips} clips, {total_chars:,} chars, "
          f"{time.time() - total_start:.1f}s")
    if total_chars:
        print(f"Estimated Azure cost: ${total_chars * 16 / 1_000_000:.2f}")


if __name__ == "__main__":
    main()
