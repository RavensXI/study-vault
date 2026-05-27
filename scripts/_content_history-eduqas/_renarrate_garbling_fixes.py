#!/usr/bin/env python3
"""Re-narrate the lessons whose narrated HTML changed in the platform-wide
garbling repair. Reuses the standard narration pipeline (voice = Ollie odd /
Ada even, per-segment MP3s keyed {slug}/{unit}/narration_lesson-NN_nid.mp3,
narration_manifest rebuilt).

Only UNIQUELY-slugged subjects here. `science` and `design-technology` are
EXCLUDED — their slugs are shared across schools and the slug-based R2 keys
collide, so they're held for Tom.

Detect (default) verifies each lesson resolves and that the computed R2 key
matches the existing manifest's src. --apply regenerates.
"""
import argparse, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL
from lib.narration import extract_narration_chunks, generate_audio_rest, get_mp3_duration, get_voice_for_lesson, AZURE_KEY

WORK = {
    'astronomy-edexcel': ['naked-eye-astronomy/11', 'naked-eye-astronomy/12', 'telescopic-astronomy/14'],
    'computer-science-aqa': ['data-representation/2'],
    'computer-science-edexcel': ['computational-thinking/5', 'computational-thinking/4'],
    'computer-science-eduqas': ['algorithms-programming-software/4'],
    'design-technology-eduqas': ['materials-and-properties/1', 'materials-and-properties/2', 'materials-and-properties/3', 'materials-and-properties/4'],
    'electronics-eduqas': ['discovering-electronics/3'],
    'engineering-aqa': ['engineering-materials/2', 'engineering-materials/3', 'engineering-systems/7'],
    'food-preparation-and-nutrition': ['nutrition-and-health/11'],
    'food-preparation-and-nutrition-eduqas': ['food-science-and-nutrition/8'],
    'geology-eduqas': ['earth-climate-and-solar-system/4'],
    'health-social-care-eduqas': ['self-concept-measuring-health/4'],
    'history-eduqas': ['warfare-britain-c500-present/8'],
    'physical-education-aqa': ['human-body-and-movement/5', 'human-body-and-movement/6', 'human-body-and-movement/7', 'human-body-and-movement/15'],
    'physical-education-edexcel': ['fitness-and-body-systems/5', 'fitness-and-body-systems/6', 'fitness-and-body-systems/7', 'fitness-and-body-systems/8', 'fitness-and-body-systems/9'],
    'physical-education-ocr': ['physical-factors-affecting-performance/7', 'physical-factors-affecting-performance/8'],
    'religious-studies-edexcel': ['paper-1-islam/4', 'paper-1-islam/5', 'paper-2-islam/3', 'paper-2-islam/4', 'paper-1-christianity/4', 'paper-2-christianity/3'],
    'science-aqa': ['chemistry-paper-1/11', 'chemistry-paper-2/10'],
    'science-ocr-b': ['chemistry-paper-1/2', 'biology-paper-2/4', 'physics-paper-1/5', 'physics-paper-1/7', 'physics-paper-2/2'],
    'separate-sciences-edexcel': ['chemistry-paper-1/2', 'chemistry-paper-2/1', 'chemistry-paper-2/2', 'chemistry-paper-2/3', 'chemistry-paper-2/4', 'chemistry-paper-2/5', 'chemistry-paper-2/7', 'chemistry-paper-2/8', 'physics-paper-1/1', 'physics-paper-1/2', 'biology-paper-1/2', 'biology-paper-2/5', 'biology-paper-2/7', 'biology-paper-2/8'],
    'separate-sciences-ocr': ['physics-paper-1/3', 'physics-paper-1/4', 'physics-paper-2/7', 'biology-paper-2/3', 'chemistry-paper-2/1', 'chemistry-paper-2/2', 'chemistry-paper-2/3', 'chemistry-paper-2/5'],
    'separate-sciences-ocr-b': ['physics-radiation-waves/2', 'physics-energy-electricity/1', 'chemistry-analysis-useful-products/2', 'chemistry-analysis-useful-products/3'],
}


def resolve(sb):
    """-> list of (slug, unit_slug, lesson_number, unit_id, lesson_id, manifest)"""
    out, problems = [], []
    for slug, items in WORK.items():
        subs = sb.table('subjects').select('id').eq('slug', slug).execute().data
        if len(subs) != 1:
            problems.append(f'{slug}: {len(subs)} subject rows (expected 1) — SKIP'); continue
        sid = subs[0]['id']
        for it in items:
            uslug, ln = it.rsplit('/', 1); ln = int(ln)
            u = sb.table('units').select('id').eq('subject_id', sid).eq('slug', uslug).execute().data
            if not u:
                problems.append(f'{slug}/{it}: unit not found'); continue
            L = sb.table('lessons').select('id,narration_manifest').eq('unit_id', u[0]['id']).eq('lesson_number', ln).execute().data
            if not L:
                problems.append(f'{slug}/{it}: lesson not found'); continue
            out.append((slug, uslug, ln, u[0]['id'], L[0]['id'], L[0].get('narration_manifest')))
    return out, problems


def renarrate(sb, r2, slug, uslug, ln, unit_id, lesson_id):
    voice_name, voice_label = get_voice_for_lesson(ln)
    L = (sb.table('lessons').select('id,title,content_html,exam_tip_html,conclusion_html,narration_manifest')
         .eq('id', lesson_id).single().execute().data)
    combined = (L.get('content_html') or '') + (L.get('exam_tip_html') or '') + (L.get('conclusion_html') or '')
    chunks = extract_narration_chunks(combined)
    if not chunks:
        return 0, 'no chunks'
    # Overwrite audio exactly where it already lives: derive each segment's R2 key
    # from the existing manifest (handles legacy key prefixes, e.g. food-technology).
    old = {e['id']: e['src'] for e in (L.get('narration_manifest') or [])}
    base = AUDIO_PUBLIC_URL + '/'
    manifest = []
    for nid, text in chunks:
        if nid in old and old[nid].startswith(base):
            r2_key = old[nid][len(base):]
        else:
            r2_key = f"{slug}/{uslug}/narration_lesson-{ln:02d}_{nid}.mp3"   # fallback
        mp3 = generate_audio_rest(text, voice_name)
        if mp3 is None:
            return len(manifest), f'FAILED at {nid}'
        d = get_mp3_duration(mp3)
        upload_bytes_to_r2(r2, AUDIO_BUCKET, r2_key, mp3, 'audio/mpeg')
        manifest.append({'id': nid, 'src': f'{base}{r2_key}', 'duration': d})
    sb.table('lessons').update({'narration_manifest': manifest}).eq('id', lesson_id).execute()
    return len(manifest), voice_label


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--apply', action='store_true')
    ap.add_argument('--limit', type=int, default=None)
    args = ap.parse_args()
    if not AZURE_KEY:
        print('ERROR: AZURE_SPEECH_KEY not set'); sys.exit(1)
    sb = get_client()
    work, problems = resolve(sb)
    print(f"resolved {len(work)} lessons across {len(WORK)} subjects")
    for p in problems:
        print('  PROBLEM:', p)
    if not args.apply:
        # detect: confirm computed key matches existing manifest src
        mism = 0
        for slug, uslug, ln, uid, lid, manifest in work[:args.limit]:
            exp = f"{AUDIO_PUBLIC_URL}/{slug}/{uslug}/narration_lesson-{ln:02d}_"
            first = (manifest[0]['src'] if manifest else None)
            ok = bool(first and first.startswith(exp))
            if not ok: mism += 1
            print(f"  {'OK ' if ok else 'KEY-MISMATCH '}{slug}/{uslug}/L{ln}  clips={len(manifest) if manifest else 0}")
            if not ok and first:
                print(f"      existing src: {first}")
                print(f"      computed pfx: {exp}")
        print(f"\nkey mismatches: {mism}. (dry-run — pass --apply to regenerate)")
        return
    r2 = get_r2_client(); t0 = time.time(); done = 0; total_clips = 0
    for slug, uslug, ln, uid, lid, manifest in (work[:args.limit] if args.limit else work):
        n, info = renarrate(sb, r2, slug, uslug, ln, uid, lid)
        total_clips += n; done += 1
        print(f"  [{done}/{len(work)}] {slug}/{uslug}/L{ln}: {n} clips ({info})")
    print(f"\nDONE: {done} lessons, {total_clips} clips, {time.time()-t0:.0f}s")


if __name__ == '__main__':
    main()
