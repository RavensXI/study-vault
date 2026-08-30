"""
FULL re-narration of english-literature-ocr / unseen-poetry (L1-L6).

The unit was rebuilt, style-swept and fact-checked (Aug 2026). The old
narration_manifest on every lesson is STALE — it covers only a subset of
the old id set (e.g. 17 of 30 ids on L1) and the surviving MP3s narrate
DELETED text. This is a from-scratch regeneration: every data-narration-id
chunk in the current content is (re)generated and (re)uploaded, overwriting
any R2 key that coincides and adding new keys where the id is new.

Voice assignment (CLAUDE.md convention):
  Odd lesson_number  -> Ollie (en-GB-OllieMultilingualNeural)
  Even lesson_number -> Ada   (en-GB-AdaMultilingualNeural)

R2 audio key:
  english-literature-ocr/unseen-poetry/narration_lesson-{NN}_{nid}.mp3

Usage:
  python scripts/_narrate_englit-ocr_unseen-poetry.py --dry-run
  python scripts/_narrate_englit-ocr_unseen-poetry.py
  python scripts/_narrate_englit-ocr_unseen-poetry.py --lesson 3
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

SUBJECT_SLUG = "english-literature-ocr"
UNIT_SLUG = "unseen-poetry"


def process_lesson(sb, r2_client, unit_id, lesson_number, dry_run=False):
    voice_name, voice_label = get_voice_for_lesson(lesson_number)
    print(f"\n  Lesson {lesson_number:02d} ({voice_label})")
    print(f"  {'=' * 54}")

    lesson_start = time.time()

    result = (
        sb.table("lessons")
        .select("id, lesson_number, title, content_html, exam_tip_html, conclusion_html, narration_manifest")
        .eq("unit_id", unit_id)
        .eq("lesson_number", lesson_number)
        .single()
        .execute()
    )
    lesson = result.data
    lesson_id = lesson["id"]
    print(f"  Title: {lesson['title']}")

    old_manifest = lesson.get("narration_manifest") or []
    old_ids = [e["id"] for e in old_manifest]
    print(f"  Old manifest: {len(old_ids)} ids")

    combined_html = (
        (lesson.get("content_html") or "")
        + (lesson.get("exam_tip_html") or "")
        + (lesson.get("conclusion_html") or "")
    )
    if not combined_html.strip():
        print("  ERROR: no content_html")
        return None

    chunks = extract_narration_chunks(combined_html)
    if not chunks:
        print("  ERROR: no data-narration-id elements found")
        return None
    print(f"  Found {len(chunks)} narration chunks: {chunks[0][0]}..{chunks[-1][0]}")

    new_ids = set(nid for nid, _ in chunks)
    stale_ids = [i for i in old_ids if i not in new_ids]

    if dry_run:
        total_chars = sum(len(text) for _, text in chunks)
        print(f"  [DRY RUN] would generate {len(chunks)} clips, ~{total_chars:,} chars")
        if stale_ids:
            print(f"  [DRY RUN] would delete {len(stale_ids)} stale R2 keys: {stale_ids}")
        return {
            "lesson_number": lesson_number, "voice": voice_label, "generated": 0,
            "chars": total_chars, "overwritten": 0, "added": 0, "deleted": [],
            "manifest": None,
        }

    manifest = []
    total_chars = 0
    generated = 0
    overwritten = 0
    added = 0
    total_duration = 0.0
    old_id_set = set(old_ids)

    for nid, text in chunks:
        r2_key = f"{SUBJECT_SLUG}/{UNIT_SLUG}/narration_lesson-{lesson_number:02d}_{nid}.mp3"
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
        generated += 1
        if nid in old_id_set:
            overwritten += 1
        else:
            added += 1
        print(f"           -> {len(mp3_bytes)/1024:.0f} KB, {duration:.1f}s, uploaded")

    if not manifest:
        print("  ERROR: no clips generated")
        return None

    if len(manifest) != len(chunks):
        print(f"  WARNING: only {len(manifest)}/{len(chunks)} clips generated - NOT updating manifest "
              f"(would leave gaps). Re-run to retry failed ids.")
        return {
            "lesson_number": lesson_number, "voice": voice_label, "generated": generated,
            "chars": total_chars, "overwritten": overwritten, "added": added,
            "deleted": [], "manifest": None, "incomplete": True,
        }

    deleted = []
    for sid in stale_ids:
        r2_key = f"{SUBJECT_SLUG}/{UNIT_SLUG}/narration_lesson-{lesson_number:02d}_{sid}.mp3"
        try:
            r2_client.delete_object(Bucket=AUDIO_BUCKET, Key=r2_key)
            deleted.append(r2_key)
            print(f"  Deleted stale R2 key: {r2_key}")
        except Exception as e:
            print(f"  WARNING: failed to delete {r2_key}: {e}")

    sb.table("lessons").update({"narration_manifest": manifest}).eq("id", lesson_id).execute()
    elapsed = time.time() - lesson_start
    print(f"  Manifest updated ({len(manifest)} entries: {overwritten} overwritten, {added} new, "
          f"{total_duration:.1f}s audio, {elapsed:.1f}s)")

    return {
        "lesson_number": lesson_number, "voice": voice_label, "generated": generated,
        "chars": total_chars, "overwritten": overwritten, "added": added,
        "deleted": deleted, "manifest": manifest,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--lesson", type=int, default=None)
    args = parser.parse_args()

    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY not set")
        sys.exit(1)

    print("English Literature OCR / Unseen Poetry - FULL Re-narration")
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

    units_result = (
        sb.table("units").select("id, slug")
        .eq("subject_id", subject_id).eq("slug", UNIT_SLUG).execute()
    )
    if not units_result.data:
        print(f"ERROR: unit '{UNIT_SLUG}' not found")
        sys.exit(1)
    unit_id = units_result.data[0]["id"]

    lesson_numbers = [args.lesson] if args.lesson else [1, 2, 3, 4, 5, 6]

    print(f"Lessons to re-narrate: {lesson_numbers}")
    r2_client = None if args.dry_run else get_r2_client()

    total_start = time.time()
    results = []

    for lesson_num in lesson_numbers:
        try:
            r = process_lesson(sb, r2_client, unit_id, lesson_num, dry_run=args.dry_run)
            if r:
                results.append(r)
        except Exception as e:
            print(f"  ERROR: {e}")

    total_elapsed = time.time() - total_start
    total_clips = sum(r["generated"] for r in results)
    total_chars = sum(r["chars"] for r in results)
    total_overwritten = sum(r["overwritten"] for r in results)
    total_added = sum(r["added"] for r in results)
    total_deleted = sum(len(r["deleted"]) for r in results)

    print(f"\n{'=' * 55}")
    print(f"TOTAL: {total_clips} clips ({total_overwritten} overwritten, {total_added} new), "
          f"{total_deleted} stale keys deleted, {total_chars:,} chars, {total_elapsed:.1f}s")
    if total_chars > 0:
        cost = total_chars * 16 / 1_000_000
        print(f"Estimated Azure cost: ${cost:.2f}")

    incomplete = [r["lesson_number"] for r in results if r.get("incomplete")]
    if incomplete:
        print(f"INCOMPLETE lessons (manifest NOT updated): {incomplete}")
        sys.exit(2)


if __name__ == "__main__":
    main()
