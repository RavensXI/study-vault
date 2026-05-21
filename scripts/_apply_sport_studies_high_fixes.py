"""Apply 4 HIGH fact-check fixes for Sport Studies + regen narration.

Affects 3 lessons (L6 Hillsborough context, L7 WADA categories, L8 Paris
date + budget — two HIGH findings in the same lesson).
"""
import os, sys, time
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
from lib.narration import extract_narration_chunks, generate_audio_rest, get_mp3_duration, get_voice_for_lesson, AZURE_KEY

SUBJECT_SLUG = "cambridge-nationals-sport-studies"
UNIT_SLUG = "contemporary-issues-in-sport"

FIXES = [
    {
        "lesson_number": 6,
        "label": "L6 Hillsborough — add context that toll rose to 97 after 96-named campaign",
        "find": "Following the Hillsborough disaster in 1989 &mdash; where 97 Liverpool supporters lost their lives in a crowd crush &mdash;",
        "replace": "Following the Hillsborough disaster in April 1989 &mdash; a crowd crush at Sheffield Wednesday&rsquo;s ground that ultimately claimed 97 Liverpool supporters (95 died at the scene, a 96th in 1993, and a 97th in 2021; the campaign was historically known as Justice for the 96) &mdash;",
    },
    {
        "lesson_number": 7,
        "label": "L7 WADA categories — replace wrong 9-cat list with correct WADA 10-substance + methods + sport-specific",
        "find": "&mdash; which names every banned substance and method. The nine categories on the Prohibited List include: anabolic agents, peptide hormones, beta blockers, stimulants, diuretics, narcotics, cannabinoids, glucocorticoids, and alcohol (in certain sports).",
        "replace": "&mdash; which names every banned substance and method. The list groups substances into ten categories (S0&ndash;S9): non-approved substances, anabolic agents, peptide hormones and growth factors, beta-2 agonists, hormone and metabolic modulators, diuretics and masking agents, stimulants, narcotics, cannabinoids, and glucocorticoids. Three further categories (M1&ndash;M3) cover prohibited methods (such as blood doping and gene doping). Beta-blockers and alcohol are listed separately as banned only in particular sports &mdash; archery and shooting for beta-blockers; archery and motorsport for alcohol.",
    },
    {
        "lesson_number": 8,
        "label": "L8 Paris date — 1900 -> 1924 (Paris hosted in 1900, 1924, 2024; the 100-year gap is from 1924)",
        "find": "the same city is unlikely to host again in your lifetime (Paris last hosted the summer Olympics in 1900; it returned in 2024 after 100 years).",
        "replace": "the same city is unlikely to host again in your lifetime (Paris previously hosted the summer Olympics in 1900 and 1924, returning in 2024 after a hundred-year gap from its last hosting).",
    },
    {
        "lesson_number": 8,
        "label": "L8 Paris 2024 budget — 3.6/8.8bn replaced with verified 4.48bn organising / 6.6bn total",
        "find": "The Paris 2024 Games budget grew from an initial estimate of around 3.6 billion euros to approximately 8.8 billion euros by the time the Games opened.",
        "replace": "The Paris 2024 organising committee budget reached around &euro;4.48 billion, while total French state spending including infrastructure and security came to roughly &euro;6.6 billion according to the French Court of Auditors&rsquo; 2025 report.",
    },
]


def resolve_lesson(sb, lesson_number):
    subj = sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG).is_("school_id", "null").execute().data[0]
    unit = sb.table("units").select("id").eq("subject_id", subj["id"]).eq("slug", UNIT_SLUG).execute().data[0]
    L = sb.table("lessons").select("id, content_html, exam_tip_html, conclusion_html").eq("unit_id", unit["id"]).eq("lesson_number", lesson_number).execute().data[0]
    return L


def renarrate(sb, r2, lesson_number, lesson_id):
    voice_name, voice_label = get_voice_for_lesson(lesson_number)
    L = sb.table("lessons").select("content_html, exam_tip_html, conclusion_html").eq("id", lesson_id).execute().data[0]
    combined = (L.get("content_html") or "") + (L.get("exam_tip_html") or "") + (L.get("conclusion_html") or "")
    chunks = extract_narration_chunks(combined)
    print(f"  re-narrating L{lesson_number:02d} ({voice_label}, {len(chunks)} chunks)")
    manifest = []
    t0 = time.time()
    for nid, text in chunks:
        r2_key = f"{SUBJECT_SLUG}/{UNIT_SLUG}/narration_lesson-{lesson_number:02d}_{nid}.mp3"
        mp3 = generate_audio_rest(text, voice_name)
        if mp3 is None:
            print(f"    FAILED {nid}")
            continue
        d = get_mp3_duration(mp3)
        upload_bytes_to_r2(r2, AUDIO_BUCKET, r2_key, mp3, "audio/mpeg")
        manifest.append({"id": nid, "src": f"{AUDIO_PUBLIC_URL}/{r2_key}", "duration": d})
    sb.table("lessons").update({"narration_manifest": manifest}).eq("id", lesson_id).execute()
    print(f"    {len(manifest)} chunks in {time.time()-t0:.1f}s")


def main():
    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY not set")
        sys.exit(1)
    sb = get_client()
    r2 = get_r2_client()

    # Cache lessons we touch
    cache = {}
    for f in FIXES:
        n = f["lesson_number"]
        if n not in cache:
            cache[n] = resolve_lesson(sb, n)
        L = cache[n]
        h = L["content_html"]
        c = h.count(f["find"])
        print(f"\n  [L{n:02d}] {f['label']}")
        if c == 0:
            print(f"    SKIP — find string not present")
            continue
        L["content_html"] = h.replace(f["find"], f["replace"])
        sb.table("lessons").update({"content_html": L["content_html"]}).eq("id", L["id"]).execute()
        print(f"    PATCHED ({c} occurrence)")

    print(f"\n\n=== Re-narrating {len(cache)} affected lessons ===")
    for n, L in cache.items():
        print(f"\n  L{n:02d}")
        renarrate(sb, r2, n, L["id"])

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
