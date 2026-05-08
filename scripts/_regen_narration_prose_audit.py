"""Regenerate narration MP3s for the 134 lessons whose content_html
changed during the prose/drama audit fix pipeline (37 regens + 7 section
rewrites + ~91 surgical fixes).
"""
import json
import os
import sys

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
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
)


def main():
    sb = get_client()
    r2 = get_r2_client()
    with open("scripts/_regen_prose/_all_affected_ids.json") as f:
        lesson_ids = json.load(f)

    print(f"Regenerating narration for {len(lesson_ids)} lessons")

    ok = fail = 0
    for i, lid in enumerate(lesson_ids, 1):
        rows = sb.table("lessons").select(
            "id, lesson_number, title, content_html, exam_tip_html, conclusion_html, "
            "narration_manifest, unit_id"
        ).eq("id", lid).execute().data
        if not rows:
            print(f"[{i:3d}/{len(lesson_ids)}] MISS lesson {lid}")
            continue
        l = rows[0]
        unit = sb.table("units").select("slug, subject_id").eq("id", l["unit_id"]).single().execute().data
        subject = sb.table("subjects").select("slug").eq("id", unit["subject_id"]).single().execute().data
        subject_slug = subject["slug"]
        unit_slug = unit["slug"]

        combined = (l.get("content_html") or "") + (l.get("exam_tip_html") or "") + (l.get("conclusion_html") or "")
        chunks = extract_narration_chunks(combined)
        if not chunks:
            print(f"[{i:3d}/{len(lesson_ids)}] SKIP {subject_slug}/{unit_slug}/L{l['lesson_number']:02d}: no chunks")
            continue

        voice_name, voice_label = get_voice_for_lesson(l["lesson_number"])
        print(f"[{i:3d}/{len(lesson_ids)}] {subject_slug}/{unit_slug}/L{l['lesson_number']:02d}: {len(chunks)} chunks ({voice_label})")

        manifest = []
        had_fail = False
        for nid, text in chunks:
            r2_key = f"{subject_slug}/{unit_slug}/narration_lesson-{l['lesson_number']:02d}_{nid}.mp3"
            public_url = f"{AUDIO_PUBLIC_URL}/{r2_key}"
            mp3 = generate_audio_rest(text, voice_name)
            if mp3 is None:
                print(f"     FAIL {nid}: {text[:80]}")
                had_fail = True
                continue
            dur = get_mp3_duration(mp3)
            upload_bytes_to_r2(r2, AUDIO_BUCKET, r2_key, mp3, "audio/mpeg")
            manifest.append({"id": nid, "src": public_url, "duration": dur})

        if had_fail:
            fail += 1
        else:
            ok += 1
            sb.table("lessons").update({"narration_manifest": manifest}).eq("id", lid).execute()

    print(f"\nok={ok} fail={fail}")


if __name__ == "__main__":
    main()
