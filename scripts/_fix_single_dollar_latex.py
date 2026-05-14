"""Fix lessons that use single-$ LaTeX delimiters (KaTeX auto-render only
catches \\(...\\) and $$...$$, so $X$ renders as raw text and TTS reads
'dollar text Energy change...').

For each affected lesson:
  1. Rewrite $X$ -> \\(X\\) in content_html / exam_tip_html / conclusion_html
     (only where X contains a TeX macro \\foo, to avoid clobbering literal '$').
  2. Diff old vs new narration chunks. Regenerate audio only for the
     chunks whose spoken text changed.
  3. Update content_html + narration_manifest in Supabase.
"""
import os
import re
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

SINGLE_DOLLAR = re.compile(r'(?<!\$)\$([^\$\n]{2,400})\$(?!\$)')
TEX_MACRO = re.compile(r'\\[A-Za-z]+')


def rewrite_dollar_delimiters(html: str) -> tuple[str, int]:
    """Replace $X$ with \\(X\\) where X contains a TeX macro. Returns (new_html, n_replaced)."""
    if not html or '$' not in html:
        return html, 0

    n = 0

    def repl(m):
        nonlocal n
        inner = m.group(1)
        if TEX_MACRO.search(inner):
            n += 1
            return f"\\({inner}\\)"
        return m.group(0)

    new = SINGLE_DOLLAR.sub(repl, html)
    return new, n


def lesson_subject_unit(sb, lesson_id):
    row = sb.table("lessons").select("id, lesson_number, unit_id").eq("id", lesson_id).single().execute().data
    unit = sb.table("units").select("id, slug, subject_id").eq("id", row["unit_id"]).single().execute().data
    subject = sb.table("subjects").select("id, slug, school_id").eq("id", unit["subject_id"]).single().execute().data
    return subject, unit, row


def main(apply: bool):
    sb = get_client()
    r2 = get_r2_client() if apply else None

    # Lesson IDs from the scan
    targets = [
        ("free", "science-aqa",        "chemistry-paper-1", 5),
        ("free", "science-aqa",        "chemistry-paper-1", 9),
        ("free", "separate-sciences",  "chemistry-paper-1", 5),
        ("free", "separate-sciences",  "chemistry-paper-1", 9),
    ]

    for _, subj_slug, unit_slug, lesson_no in targets:
        subj = sb.table("subjects").select("id, slug").eq("slug", subj_slug).is_("school_id", "null").execute().data
        if not subj:
            print(f"[SKIP] subject not found: {subj_slug}"); continue
        unit = sb.table("units").select("id, slug").eq("subject_id", subj[0]["id"]).eq("slug", unit_slug).execute().data
        if not unit:
            print(f"[SKIP] unit not found: {subj_slug}/{unit_slug}"); continue
        lesson_q = sb.table("lessons").select(
            "id, lesson_number, title, content_html, exam_tip_html, conclusion_html, narration_manifest"
        ).eq("unit_id", unit[0]["id"]).eq("lesson_number", lesson_no).execute().data
        if not lesson_q:
            print(f"[SKIP] lesson not found: {subj_slug}/{unit_slug}/L{lesson_no:02d}"); continue
        L = lesson_q[0]

        label = f"{subj_slug}/{unit_slug}/L{lesson_no:02d} \"{L['title'][:40]}\""

        new_content, n_c = rewrite_dollar_delimiters(L.get("content_html") or "")
        new_tip,     n_t = rewrite_dollar_delimiters(L.get("exam_tip_html") or "")
        new_concl,   n_x = rewrite_dollar_delimiters(L.get("conclusion_html") or "")
        n_total = n_c + n_t + n_x
        if n_total == 0:
            print(f"[NOOP] {label} — no single-$ LaTeX to fix")
            continue

        # Build before/after chunk maps to know which need regen
        old_combined = (L.get("content_html") or "") + (L.get("exam_tip_html") or "") + (L.get("conclusion_html") or "")
        new_combined = new_content + new_tip + new_concl
        old_chunks = dict(extract_narration_chunks(old_combined))
        new_chunks = dict(extract_narration_chunks(new_combined))

        changed_ids = [nid for nid, txt in new_chunks.items() if old_chunks.get(nid) != txt]
        print(f"[FIX]  {label}: {n_total} expressions, {len(changed_ids)} narration chunks need regen")
        for nid in changed_ids:
            old_t = (old_chunks.get(nid) or "")[:60]
            new_t = (new_chunks.get(nid) or "")[:60]
            print(f"        {nid}: '{old_t}' -> '{new_t}'")

        if not apply:
            continue

        # Regenerate the affected chunks
        voice_name, voice_label = get_voice_for_lesson(lesson_no)
        old_manifest = L.get("narration_manifest") or []
        new_manifest_by_id = {e.get("id"): dict(e) for e in old_manifest}
        for nid in changed_ids:
            text = new_chunks[nid]
            r2_key = f"{subj_slug}/{unit_slug}/narration_lesson-{lesson_no:02d}_{nid}.mp3"
            public_url = f"{AUDIO_PUBLIC_URL}/{r2_key}"
            print(f"        REGEN {nid} ({voice_label})...")
            mp3 = generate_audio_rest(text, voice_name)
            if mp3 is None:
                print(f"        FAIL  {nid}: TTS returned nothing")
                continue
            dur = get_mp3_duration(mp3)
            upload_bytes_to_r2(r2, AUDIO_BUCKET, r2_key, mp3, "audio/mpeg")
            new_manifest_by_id[nid] = {"id": nid, "src": public_url, "duration": dur}

        # Preserve original manifest order
        new_manifest = []
        seen = set()
        for e in old_manifest:
            mid = e.get("id")
            if mid in new_manifest_by_id:
                new_manifest.append(new_manifest_by_id[mid]); seen.add(mid)
        # Append any new ids that weren't there before (shouldn't happen, but safe)
        for mid, entry in new_manifest_by_id.items():
            if mid not in seen:
                new_manifest.append(entry)

        sb.table("lessons").update({
            "content_html": new_content,
            "exam_tip_html": new_tip if (L.get("exam_tip_html") or "") else None,
            "conclusion_html": new_concl if (L.get("conclusion_html") or "") else None,
            "narration_manifest": new_manifest,
        }).eq("id", L["id"]).execute()
        print(f"        WROTE {label}")


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    main(apply=apply)
    if not apply:
        print("\n[DRY RUN] re-run with --apply to write changes")
