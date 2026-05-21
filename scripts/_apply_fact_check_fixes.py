"""Apply the 6 HIGH fact-check fixes from the 2026-05-21 audit + regen narration.

Each fix is a literal string replace on content_html, then the lesson row
is patched back to Supabase. After all fixes land, narration is regenerated
for each affected lesson (whole-lesson regen — simpler than per-chunk).
"""
import os
import sys
import time
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
    AZURE_KEY,
)

# ============================================================ Fix manifest

FIXES = [
    {
        "subject_slug": "geology-eduqas",
        "lesson_id": "c9bd790a",  # resolved at runtime
        "lesson_id_full": None,
        "unit_slug": "geological-time-and-life",
        "lesson_number": 5,
        "label": "Chicxulub crater diameter 180 → 200 km",
        "find": "(approximately 180 km in diameter)",
        "replace": "(approximately 200 km in diameter)",
    },
    {
        "subject_slug": "geology-eduqas",
        "lesson_id_full": "d181de9f-624d-42ab-bc2f-cd9d53b1dcb8",
        "unit_slug": "hazards-resources-and-investigative-geology",
        "lesson_number": 6,
        "label": "St Francis Dam — multi-factor failure description",
        "find": "the dam had been built on a fault zone and across a contact between two incompatible rock types that differentially weakened under reservoir loading.",
        "replace": "the dam had been built on a thrust fault zone, with weak Sespe conglomerate on one abutment that swelled when saturated and unstable schist on the other.",
    },
    {
        "subject_slug": "design-technology-eduqas",
        "lesson_id_full": "a4417a7c-e4e3-4254-9589-6b1e2a67489f",
        "unit_slug": "designing-and-making-principles",
        "lesson_number": 2,
        "label": "Dyson G-Force — designed 1983, launched 1986",
        "find": "the G-Force cyclonic vacuum cleaner was launched in 1983 in Japan",
        "replace": "the G-Force cyclonic vacuum cleaner was designed in 1983 and launched in Japan in 1986",
    },
    {
        "subject_slug": "design-technology-eduqas",
        "lesson_id_full": "8a364adc-f796-4a78-8439-4c5e387bd81a",
        "unit_slug": "designing-and-making-principles",
        "lesson_number": 5,
        "label": "Toy safety — replace fabricated 45mm rule with EN 71-1 cylinder",
        "find": "choking-hazard rules (no component smaller than 45 mm in any direction for products intended for children under 3)",
        "replace": "choking-hazard rules under the EU Toy Safety Directive and EN 71-1 (the small parts test uses a cylinder 57.1 mm tall by 31.7 mm in diameter — any component that fits entirely inside this cylinder is classified as a choking hazard and must not appear in toys intended for children under 3)",
    },
    {
        "subject_slug": "physical-education-edexcel",
        "lesson_id_full": "e2892fe8-ecdc-45c0-adb1-fc0be1e5cd10",
        "unit_slug": "fitness-and-body-systems",
        "lesson_number": 13,
        "label": "Harvard Step Test — clarify school-adapted variant",
        "find": "The Harvard Step Test requires the participant to step up and down on a 30 cm bench for 5 minutes at a set pace. One minute after stopping, the heart rate is measured.",
        "replace": "The Harvard Step Test (school-adapted GCSE version, sometimes called the Three-Minute Step Test) uses a 30 cm bench — the original protocol uses 50 cm for men and 40 cm for women. The participant steps up and down for 5 minutes at a set pace. In the standard protocol the recovery pulse is measured in three 30-second windows (at 1:00–1:30, 2:00–2:30 and 3:00–3:30 after stopping); the GCSE-adapted version often takes a single reading from 1 minute post-exercise.",
    },
    {
        "subject_slug": "physical-education-edexcel",
        "lesson_id_full": "e2892fe8-ecdc-45c0-adb1-fc0be1e5cd10",
        "unit_slug": "fitness-and-body-systems",
        "lesson_number": 13,
        "label": "Illinois Agility — cone spacing 5m → 3.3m for weaving cones",
        "find": "sprints up and back along a course of cones placed 5 metres apart, weaving between cones in the middle section.",
        "replace": "sprints up and back along a 10 m by 5 m rectangular course, weaving between four central cones spaced 3.3 metres apart.",
    },
]


def resolve_lesson_id(sb, subject_slug, unit_slug, lesson_number):
    """Return (lesson_id_full, content_html, current_manifest_present)."""
    subj = sb.table("subjects").select("id").eq("slug", subject_slug).is_("school_id", "null").execute().data[0]
    units = sb.table("units").select("id, slug").eq("subject_id", subj["id"]).eq("slug", unit_slug).execute().data
    unit_id = units[0]["id"]
    L = (
        sb.table("lessons")
        .select("id, content_html, narration_manifest")
        .eq("unit_id", unit_id)
        .eq("lesson_number", lesson_number)
        .execute()
        .data[0]
    )
    return L["id"], L.get("content_html") or "", L.get("narration_manifest") or []


def apply_text_fix(html, find, replace):
    """Literal find-and-replace. Returns (new_html, found_count)."""
    n = html.count(find)
    if n == 0:
        return html, 0
    return html.replace(find, replace), n


def renarrate_lesson(sb, r2, subject_slug, unit_slug, lesson_number, lesson_id):
    """Whole-lesson narration regen — overwrites all chunks on R2 + updates manifest."""
    voice_name, voice_label = get_voice_for_lesson(lesson_number)
    print(f"    re-narrating L{lesson_number:02d} ({voice_label})")
    row = (
        sb.table("lessons")
        .select("id, content_html, exam_tip_html, conclusion_html")
        .eq("id", lesson_id)
        .execute()
        .data[0]
    )
    combined = (
        (row.get("content_html") or "")
        + (row.get("exam_tip_html") or "")
        + (row.get("conclusion_html") or "")
    )
    chunks = extract_narration_chunks(combined)
    if not chunks:
        print(f"      WARN: no chunks; skip")
        return 0
    manifest = []
    t0 = time.time()
    for nid, text in chunks:
        r2_key = f"{subject_slug}/{unit_slug}/narration_lesson-{lesson_number:02d}_{nid}.mp3"
        public_url = f"{AUDIO_PUBLIC_URL}/{r2_key}"
        mp3 = generate_audio_rest(text, voice_name)
        if mp3 is None:
            print(f"      FAILED {nid}")
            continue
        d = get_mp3_duration(mp3)
        upload_bytes_to_r2(r2, AUDIO_BUCKET, r2_key, mp3, "audio/mpeg")
        manifest.append({"id": nid, "src": public_url, "duration": d})
    sb.table("lessons").update({"narration_manifest": manifest}).eq("id", lesson_id).execute()
    elapsed = time.time() - t0
    print(f"      {len(manifest)} chunks in {elapsed:.1f}s")
    return len(manifest)


def main():
    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY not set")
        sys.exit(1)

    sb = get_client()
    r2 = get_r2_client()

    # === Phase 1: text fixes ===
    lessons_changed = []  # list of (subject_slug, unit_slug, lesson_number, lesson_id)
    seen_lessons = set()  # (subject, unit, lesson_number)
    for f in FIXES:
        lesson_id, html, _ = resolve_lesson_id(
            sb, f["subject_slug"], f["unit_slug"], f["lesson_number"]
        )
        new_html, n = apply_text_fix(html, f["find"], f["replace"])
        print(f"\n  [{f['subject_slug']}/L{f['lesson_number']:02d}] {f['label']}")
        if n == 0:
            print(f"    SKIP — find string not present in current content_html")
            continue
        sb.table("lessons").update({"content_html": new_html}).eq("id", lesson_id).execute()
        print(f"    PATCHED — replaced {n} occurrence(s)")
        key = (f["subject_slug"], f["unit_slug"], f["lesson_number"])
        if key not in seen_lessons:
            seen_lessons.add(key)
            lessons_changed.append((f["subject_slug"], f["unit_slug"], f["lesson_number"], lesson_id))

    # === Phase 2: narration regen for each affected lesson ===
    print(f"\n\n=== Re-narrating {len(lessons_changed)} affected lessons ===")
    for subject_slug, unit_slug, lesson_number, lesson_id in lessons_changed:
        print(f"\n  {subject_slug} / {unit_slug} / L{lesson_number:02d}")
        renarrate_lesson(sb, r2, subject_slug, unit_slug, lesson_number, lesson_id)

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
