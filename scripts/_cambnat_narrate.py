"""Reusable narrator for Cambridge National builds.
Usage: python _cambnat_narrate.py <subject_slug> <unit_slug>
Narrates every lesson in the unit that lacks a manifest. R2 key:
  <subject_slug>/<unit_slug>/narration_lesson-NN_nN.mp3   (number-keyed)
Voice: Ollie (odd) / Ada (even).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL
from lib.narration import (extract_narration_chunks, generate_audio_rest,
                           get_mp3_duration, get_voice_for_lesson, AZURE_KEY)

subject_slug, unit_slug = sys.argv[1], sys.argv[2]
assert AZURE_KEY, "AZURE_SPEECH_KEY not set"
sb = get_client(); r2 = get_r2_client()
sid = sb.table("subjects").select("id").eq("slug", subject_slug).is_("school_id", "null").single().execute().data["id"]
uid = sb.table("units").select("id").eq("subject_id", sid).eq("slug", unit_slug).single().execute().data["id"]
rows = sb.table("lessons").select("id,lesson_number,content_html,exam_tip_html,conclusion_html,narration_manifest").eq("unit_id", uid).order("lesson_number").execute().data
total = 0
for l in rows:
    if l.get("narration_manifest"):
        continue
    ln = l["lesson_number"]; voice, _ = get_voice_for_lesson(ln)
    html = (l.get("content_html") or "") + (l.get("exam_tip_html") or "") + (l.get("conclusion_html") or "")
    manifest = []
    for nid, text in extract_narration_chunks(html):
        key = f"{subject_slug}/{unit_slug}/narration_lesson-{ln:02d}_{nid}.mp3"
        mp3 = generate_audio_rest(text, voice)
        if mp3 is None:
            continue
        upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
        manifest.append({"id": nid, "src": f"{AUDIO_PUBLIC_URL}/{key}", "duration": get_mp3_duration(mp3)})
    sb.table("lessons").update({"narration_manifest": manifest}).eq("id", l["id"]).execute()
    total += len(manifest); print(f"  L{ln:02d}: {len(manifest)} clips")
print(f"{subject_slug}: {total} clips")
