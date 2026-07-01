"""Re-narrate ONE lesson by id (for one-off content fixes outside the pipeline job flow).
Extracts narration chunks from the lesson's current content_html, generates Azure TTS
(voice by lesson parity), uploads to R2 with the standard key scheme, and REPLACES the
lesson's narration_manifest so it exactly matches the current content (dropping any stale
orphan clips).

  python scripts/_narrate_single_lesson.py <lesson_id> [--dry-run]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client
from lib.narration import extract_narration_chunks, generate_audio_rest, get_mp3_duration, get_voice_for_lesson

LID = sys.argv[1] if len(sys.argv) > 1 else '92399074-94ca-40c0-a880-5c0363ef510c'
DRY = "--dry-run" in sys.argv

sb = get_client()
row = sb.table("lessons").select(
    "content_html,lesson_number,units!inner(slug,subjects!inner(slug))"
).eq("id", LID).single().execute().data
html = row["content_html"]
num = row["lesson_number"]
unit_slug = row["units"]["slug"]
subject_slug = row["units"]["subjects"]["slug"]
voice, label = get_voice_for_lesson(num)

chunks = extract_narration_chunks(html)
print(f"lesson {subject_slug}/{unit_slug} L{num:02d} | voice {label} | {len(chunks)} chunks")
for nid, text in chunks:
    disp = text if len(text) < 90 else text[:90] + "…"
    print(f"  {nid}: {disp}")

if DRY:
    total_chars = sum(len(t) for _, t in chunks)
    print(f"\n[DRY RUN] {len(chunks)} chunks, {total_chars} chars, est ${total_chars*16/1_000_000:.3f}. No audio generated.")
    sys.exit(0)

from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL
r2 = get_r2_client()
manifest = []
for nid, text in chunks:
    key = f"{subject_slug}/{unit_slug}/narration_lesson-{num:02d}_{nid}.mp3"
    mp3 = generate_audio_rest(text, voice)
    if not mp3:
        print(f"  FAILED {nid}"); continue
    dur = get_mp3_duration(mp3)
    upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
    manifest.append({"id": nid, "src": f"{AUDIO_PUBLIC_URL}/{key}", "duration": dur})
    print(f"  {nid}: {len(mp3)//1024} KB, {dur:.1f}s -> uploaded")

sb.table("lessons").update({"narration_manifest": manifest}).eq("id", LID).execute()
print(f"\nnarration_manifest replaced: {len(manifest)} clips (was 25, stale orphans dropped)")
