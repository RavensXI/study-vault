"""
Azure TTS narration for the 9 Geography AQA optional-topic lessons.
  paper-1 L21-L25, paper-2 L21-L24.

Voice: Ollie (odd lesson_number) / Ada (even). R2 audio key:
  geography/{unit_slug}/narration_lesson-{NN}_{nid}.mp3
Skips any lesson that already has a populated narration_manifest.
"""
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
    extract_narration_chunks, generate_audio_rest, get_mp3_duration,
    get_voice_for_lesson, AZURE_KEY,
)

SUBJECT_SLUG = "geography-aqa"
AUDIO_PREFIX = "geography"  # R2 audio lives under geography/ for this subject
TARGETS = {"paper-1": [21, 22, 23, 24, 25], "paper-2": [21, 22, 23, 24]}


def process_lesson(sb, r2, unit_slug, unit_id, ln):
    voice_name, voice_label = get_voice_for_lesson(ln)
    lesson = (sb.table("lessons")
              .select("id,title,content_html,exam_tip_html,conclusion_html,narration_manifest")
              .eq("unit_id", unit_id).eq("lesson_number", ln).single().execute().data)
    print(f"\n  {unit_slug} / L{ln:02d} ({voice_label}): {lesson['title']}")

    if lesson.get("narration_manifest") and len(lesson["narration_manifest"]) > 0:
        print(f"  SKIP: already has {len(lesson['narration_manifest'])} clips")
        return 0
    html = ((lesson.get("content_html") or "") + (lesson.get("exam_tip_html") or "")
            + (lesson.get("conclusion_html") or ""))
    chunks = extract_narration_chunks(html)
    if not chunks:
        print("  ERROR: no narration chunks")
        return 0
    print(f"  {len(chunks)} chunks")

    manifest = []
    for nid, text in chunks:
        r2_key = f"{AUDIO_PREFIX}/{unit_slug}/narration_lesson-{ln:02d}_{nid}.mp3"
        mp3 = generate_audio_rest(text, voice_name)
        if mp3 is None:
            print(f"    FAILED {nid}")
            continue
        dur = get_mp3_duration(mp3)
        upload_bytes_to_r2(r2, AUDIO_BUCKET, r2_key, mp3, "audio/mpeg")
        manifest.append({"id": nid, "src": f"{AUDIO_PUBLIC_URL}/{r2_key}", "duration": dur})
    if not manifest:
        print("  ERROR: nothing generated")
        return 0
    sb.table("lessons").update({"narration_manifest": manifest}).eq("id", lesson["id"]).execute()
    print(f"  OK: {len(manifest)} clips")
    return len(manifest)


def main():
    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY not set")
        sys.exit(1)
    sb = get_client()
    r2 = get_r2_client()
    sid = (sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG)
           .is_("school_id", "null").single().execute().data["id"])
    total = 0
    for unit_slug, nums in TARGETS.items():
        uid = (sb.table("units").select("id").eq("subject_id", sid)
               .eq("slug", unit_slug).single().execute().data["id"])
        for ln in nums:
            try:
                total += process_lesson(sb, r2, unit_slug, uid, ln)
            except Exception as e:
                print(f"  ERROR L{ln}: {e}")
    print(f"\nTOTAL clips generated: {total}")


if __name__ == "__main__":
    main()
