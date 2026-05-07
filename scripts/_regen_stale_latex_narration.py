"""One-off: regenerate narration for lessons with LaTeX in content_html.

These lessons were narrated before scripts/lib/narration.py:latex_to_spoken
landed (commit 21b8c51, 2026-03-31), so the MP3s contain raw LaTeX
delimiters being read as 'backslash open paren' by Azure TTS. Regen with
the current code converts \(H_2O\) to 'H sub 2 O' etc.

Targets: science-aqa / science-ocr / science-edexcel / separate-sciences
(other free-tier subjects with LaTeX were built post-fix and are fine).
"""
import os
import sys

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
)

TARGET_SUBJECTS = [
    "science-aqa",
    "science-ocr",
    "science-edexcel",
    "separate-sciences",
]

EXCLUDE_LESSON_IDS = {
    "bf094a53-2a2e-4812-b33c-aa59fd9f7313",  # science-aqa chemistry-paper-1 L1 — already regen'd
}


def main():
    sb = get_client()
    r2 = get_r2_client()

    targets = []
    for slug in TARGET_SUBJECTS:
        sub_q = sb.table("subjects").select("id, slug").eq("slug", slug).is_("school_id", "null").execute().data
        if not sub_q:
            print(f"  no subject: {slug}")
            continue
        sub = sub_q[0]
        units = sb.table("units").select("id, slug").eq("subject_id", sub["id"]).execute().data
        for u in units:
            rows = sb.table("lessons").select(
                "id, lesson_number, title, content_html, exam_tip_html, conclusion_html, narration_manifest"
            ).eq("unit_id", u["id"]).order("lesson_number").execute().data
            for r in rows:
                if r["id"] in EXCLUDE_LESSON_IDS:
                    continue
                ch = r.get("content_html") or ""
                if "\\(" not in ch:
                    continue
                if not r.get("narration_manifest"):
                    continue
                targets.append({
                    "id": r["id"],
                    "subject_slug": sub["slug"],
                    "unit_slug": u["slug"],
                    "lesson_number": r["lesson_number"],
                    "title": r["title"],
                    "content_html": ch,
                    "exam_tip_html": r.get("exam_tip_html") or "",
                    "conclusion_html": r.get("conclusion_html") or "",
                })

    print(f"\nTargets: {len(targets)} lessons across {len(TARGET_SUBJECTS)} subjects\n")

    ok = fail = 0
    for i, l in enumerate(targets, 1):
        label = f"{l['subject_slug']}/{l['unit_slug']}/L{l['lesson_number']:02d}"
        combined = l["content_html"] + l["exam_tip_html"] + l["conclusion_html"]
        chunks = extract_narration_chunks(combined)
        if not chunks:
            print(f"[{i}/{len(targets)}] SKIP {label}: no chunks")
            continue
        voice_name, voice_label = get_voice_for_lesson(l["lesson_number"])
        print(f"[{i}/{len(targets)}] GEN  {label}: {len(chunks)} chunks ({voice_label})")

        manifest = []
        had_fail = False
        for nid, text in chunks:
            r2_key = (
                f"{l['subject_slug']}/{l['unit_slug']}/"
                f"narration_lesson-{l['lesson_number']:02d}_{nid}.mp3"
            )
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
            sb.table("lessons").update({"narration_manifest": manifest}).eq("id", l["id"]).execute()

    print(f"\nDone: {ok} ok, {fail} with failures")


if __name__ == "__main__":
    main()
