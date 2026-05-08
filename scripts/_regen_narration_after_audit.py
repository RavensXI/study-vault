"""Regenerate narration MP3s for the 26 lessons whose content_html changed
during the poem audit (3 full regens + 23 surgical fixes).

Walks each lesson, extracts narration chunks via lib.narration, generates
fresh MP3s via Azure TTS, uploads to R2, updates manifest in Supabase.
"""
import os
import sys
from pathlib import Path

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

LESSON_IDS = [
    "0769b2c1-32b0-405e-9a26-3d073fb42f3b",
    "0e4206cb-013c-4d14-a555-3760a96c0b9d",
    "175d5a2f-60ea-4fdc-9897-72ed6417b50c",
    "23564a46-0a26-4e0f-a5ea-96d850a0683d",
    "2b9901df-aa06-4169-87f5-1bfaf199d583",
    "337d64f7-6a4e-4896-8422-feac38123809",
    "47b7f5e1-9ed6-49a9-92a1-bcf81bb686fd",
    "4fb42f8b-e4c2-47ff-9468-d771ac307748",
    "52f7c2a5-285a-4df9-ab02-9f09b93aa361",
    "5d00f939-f7b6-4c71-8346-125758700059",
    "681ee296-a685-4427-afa7-edc642737065",
    "705185df-1eb7-4748-90d9-b1b32c60187c",
    "73dc71b5-ff23-4971-b403-bface667a402",
    "800fe93e-d68d-41a7-81a6-ff17fe5a715c",
    "86689ccf-2ffb-4d6a-9dc7-c1579371e050",
    "8cfb8271-de6d-479d-85ec-6a7612a62143",
    "9de8bdfe-ed46-4093-a26a-c45e56155be5",
    "afc96b91-baea-46fd-87f3-2e81ea7be23e",
    "b6562ab2-0b6d-49ac-8cbe-1e38f632b5a0",
    "be0ab045-6828-4d1e-8452-df6bd5779f21",
    "cade3aa6-1bb2-4f55-908d-d37426e876a8",
    "d5821e85-e717-484a-9ba5-4c917cf64c75",
    "d904aa40-afe9-4066-9414-2b1ac053b921",
    "e80168e3-1eb6-4ff0-8e16-624a2511a13e",
    "efb4be31-f7b3-404f-aca8-e5280651b9df",
    "fa8bcfab-c09a-4046-b5a4-d0e051b222cf",
]


def main():
    sb = get_client()
    r2 = get_r2_client()

    ok = fail = 0
    for i, lid in enumerate(LESSON_IDS, 1):
        l = sb.table("lessons").select(
            "id, lesson_number, title, content_html, exam_tip_html, conclusion_html, "
            "narration_manifest, unit_id"
        ).eq("id", lid).single().execute().data

        # Look up subject + unit slug for R2 path
        unit = sb.table("units").select("slug, subject_id").eq("id", l["unit_id"]).single().execute().data
        subject = sb.table("subjects").select("slug").eq("id", unit["subject_id"]).single().execute().data
        subject_slug = subject["slug"]
        unit_slug = unit["slug"]

        combined = (l.get("content_html") or "") + (l.get("exam_tip_html") or "") + (l.get("conclusion_html") or "")
        chunks = extract_narration_chunks(combined)
        if not chunks:
            print(f"[{i:2d}/{len(LESSON_IDS)}] SKIP {subject_slug}/{unit_slug}/L{l['lesson_number']:02d}: no chunks")
            continue

        voice_name, voice_label = get_voice_for_lesson(l["lesson_number"])
        print(f"[{i:2d}/{len(LESSON_IDS)}] GEN  {subject_slug}/{unit_slug}/L{l['lesson_number']:02d}: {len(chunks)} chunks ({voice_label})")

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
