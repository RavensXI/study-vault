"""Azure TTS narration for Health and Social Care
(health-social-care-eduqas).

12 article lessons across 1 unit:
  - enterprise-and-marketing-concepts            (12)

Voice: Odd lesson_number -> Ollie / Even -> Ada.
R2 key: health-social-care-eduqas/{unit_slug}/narration_lesson-{NN}_{nid}.mp3
"""
import argparse, io, os, sys, time

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
from lib.narration import extract_narration_chunks, generate_audio_rest, get_mp3_duration, get_voice_for_lesson, AZURE_KEY

SUBJECT_SLUG = "health-social-care-eduqas"
ARTICLE_UNITS = [
    "growth-development-lifespan",
    "self-concept-measuring-health",
]


def process_lesson(sb, r2_client, unit_slug, unit_id, lesson_number, dry_run=False):
    voice_name, voice_label = get_voice_for_lesson(lesson_number)
    print(f"\n  {unit_slug} / L{lesson_number:02d} ({voice_label})")
    print(f"  {'=' * 54}")
    t0 = time.time()
    L = (sb.table("lessons")
         .select("id, lesson_number, title, content_html, exam_tip_html, conclusion_html")
         .eq("unit_id", unit_id).eq("lesson_number", lesson_number).single().execute().data)
    print(f"  Title: {L['title']}")
    combined = ((L.get("content_html") or "") + (L.get("exam_tip_html") or "") + (L.get("conclusion_html") or ""))
    if not combined.strip():
        print("  SKIP: no content_html"); return 0, 0, 0.0
    chunks = extract_narration_chunks(combined)
    if not chunks:
        print("  ERROR: no narration IDs"); return 0, 0, 0.0
    print(f"  {len(chunks)} chunks")
    if dry_run:
        total = sum(len(t) for _, t in chunks)
        print(f"  [DRY] {total:,} chars"); return 0, total, 0.0

    manifest = []
    chars = generated = 0
    dur = 0.0
    for nid, text in chunks:
        r2_key = f"{SUBJECT_SLUG}/{unit_slug}/narration_lesson-{lesson_number:02d}_{nid}.mp3"
        public_url = f"{AUDIO_PUBLIC_URL}/{r2_key}"
        chars += len(text)
        disp = (text[:70] + "...") if len(text) > 70 else text
        disp = disp.encode("ascii", errors="replace").decode("ascii")
        print(f"    {nid}: {disp}")
        mp3 = generate_audio_rest(text, voice_name)
        if mp3 is None:
            print(f"    FAILED {nid}"); continue
        d = get_mp3_duration(mp3); dur += d
        upload_bytes_to_r2(r2_client, AUDIO_BUCKET, r2_key, mp3, "audio/mpeg")
        manifest.append({"id": nid, "src": public_url, "duration": d})
        generated += 1
        print(f"           -> {len(mp3)/1024:.0f} KB, {d:.1f}s")
    if not manifest:
        return 0, 0, 0.0
    sb.table("lessons").update({"narration_manifest": manifest}).eq("id", L["id"]).execute()
    elapsed = time.time() - t0
    print(f"  Manifest updated ({len(manifest)} clips, {dur:.1f}s audio, {elapsed:.1f}s)")
    return generated, chars, elapsed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--unit", choices=ARTICLE_UNITS, default=None)
    ap.add_argument("--lesson", type=int, default=None)
    args = ap.parse_args()

    if not AZURE_KEY:
        print("ERROR: AZURE_SPEECH_KEY not set"); sys.exit(1)

    print("Health and Social Care - TTS Narration")
    print("=" * 60)
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG).is_("school_id", "null").execute()
    if not sub.data:
        print(f"ERROR: subject '{SUBJECT_SLUG}' not found"); sys.exit(1)
    sid = sub.data[0]["id"]
    units = sb.table("units").select("id, slug").eq("subject_id", sid).in_("slug", ARTICLE_UNITS).execute().data
    umap = {u["slug"]: u["id"] for u in units}

    targets = [args.unit] if args.unit else ARTICLE_UNITS
    work = []
    for slug in targets:
        uid = umap[slug]
        q = sb.table("lessons").select("lesson_number").eq("unit_id", uid).order("lesson_number")
        if args.lesson:
            q = q.eq("lesson_number", args.lesson)
        for r in q.execute().data:
            work.append((slug, uid, r["lesson_number"]))
    print(f"Lessons to narrate: {len(work)}\n")
    if not work:
        return

    r2 = None if args.dry_run else get_r2_client()
    t0 = time.time()
    total_clips = total_chars = 0
    results = []
    for slug, uid, n in work:
        try:
            clips, chars, el = process_lesson(sb, r2, slug, uid, n, dry_run=args.dry_run)
            total_clips += clips; total_chars += chars
            results.append((slug, n, clips, chars, el, None))
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append((slug, n, 0, 0, 0.0, str(e)))
    elapsed = time.time() - t0

    print(f"\n{'=' * 60}\nSUMMARY\n{'=' * 60}")
    for slug, n, clips, chars, el, err in results:
        status = f"ERROR: {err}" if err else f"{clips} clips, {el:.1f}s"
        print(f"  {slug:<40} L{n:02d}   {status}")
    print(f"\nTOTAL: {total_clips} clips, {total_chars:,} chars, {elapsed:.1f}s")
    if total_chars > 0:
        print(f"Estimated Azure cost: ${total_chars * 16 / 1_000_000:.2f}")


if __name__ == "__main__":
    main()
