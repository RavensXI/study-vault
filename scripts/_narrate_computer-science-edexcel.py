"""Generate narration MP3s for all Computer Science (Edexcel) lessons.

Usage:
    python scripts/_narrate_computer-science-edexcel.py
    python scripts/_narrate_computer-science-edexcel.py --dry-run
    python scripts/_narrate_computer-science-edexcel.py --resume   # skip lessons already narrated
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

SUBJECT_SLUG = "computer-science-edexcel"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--resume", action="store_true")
    args = p.parse_args()

    sb = get_client()
    r2 = get_r2_client()

    sub = sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG).is_("school_id", "null").single().execute().data
    subject_id = sub["id"]

    units = sb.table("units").select("id, slug, name, sort_order").eq(
        "subject_id", subject_id).order("sort_order").execute().data

    ok = fail = skip = 0
    total_chunks = 0
    total_duration = 0.0
    failed_chunks = []

    for unit in units:
        lessons = sb.table("lessons").select(
            "id, lesson_number, title, content_html, exam_tip_html, conclusion_html, narration_manifest"
        ).eq("unit_id", unit["id"]).order("lesson_number").execute().data

        for l in lessons:
            ctx = f"{unit['slug']}/L{l['lesson_number']:02d}"
            if args.resume and l.get("narration_manifest"):
                print(f"  SKIP {ctx}: manifest already present")
                skip += 1
                continue

            combined = (l.get("content_html") or "") + (l.get("exam_tip_html") or "") + (l.get("conclusion_html") or "")
            if not combined.strip():
                print(f"  SKIP {ctx}: empty body")
                skip += 1
                continue

            chunks = extract_narration_chunks(combined)
            if not chunks:
                print(f"  SKIP {ctx}: 0 chunks extracted")
                skip += 1
                continue

            voice_name, voice_label = get_voice_for_lesson(l["lesson_number"])
            print(f"  GEN  {ctx}: {len(chunks)} chunks ({voice_label}) — {l['title'][:50]}")
            if args.dry_run:
                total_chunks += len(chunks)
                continue

            manifest = []
            had_fail = False
            for nid, text in chunks:
                r2_key = f"{SUBJECT_SLUG}/{unit['slug']}/narration_lesson-{l['lesson_number']:02d}_{nid}.mp3"
                public_url = f"{AUDIO_PUBLIC_URL}/{r2_key}"
                mp3 = generate_audio_rest(text, voice_name)
                if mp3 is None:
                    print(f"       FAIL {nid}: {text[:60]}…")
                    had_fail = True
                    failed_chunks.append(f"{ctx}/{nid}: {text[:60]}")
                    continue
                dur = get_mp3_duration(mp3)
                upload_bytes_to_r2(r2, AUDIO_BUCKET, r2_key, mp3, "audio/mpeg")
                manifest.append({"id": nid, "src": public_url, "duration": dur})
                total_duration += dur
                total_chunks += 1

            if had_fail:
                fail += 1
            else:
                ok += 1
                sb.table("lessons").update({"narration_manifest": manifest}).eq("id", l["id"]).execute()

    total_minutes = total_duration / 60.0
    print(f"\n[DONE] ok={ok} fail={fail} skip={skip}")
    print(f"       chunks={total_chunks}  total_audio={total_minutes:.1f} min")
    if failed_chunks:
        print(f"\n[FAILED CHUNKS]")
        for fc in failed_chunks:
            print(f"  {fc}")


if __name__ == "__main__":
    main()
