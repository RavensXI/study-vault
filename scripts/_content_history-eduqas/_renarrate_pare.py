#!/usr/bin/env python3
"""Re-narrate the one Paré lesson (history-aqa / britain-health-people / L4)
whose narrated HTML had the broken 'Pa&reacute;ré'. Single uniquely-slugged
Unity subject — no slug collision. Overwrites audio in place via the existing
manifest's keys."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL
from lib.narration import extract_narration_chunks, generate_audio_rest, get_mp3_duration, get_voice_for_lesson, AZURE_KEY

SLUG, USLUG, LN = 'history-aqa', 'britain-health-people', 4

def main():
    if not AZURE_KEY:
        print('ERROR: AZURE_SPEECH_KEY not set'); sys.exit(1)
    sb = get_client()
    subs = sb.table('subjects').select('id,school_id').eq('slug', SLUG).execute().data
    print(f"'{SLUG}' subject rows: {len(subs)}")
    if len(subs) != 1:
        print('ABORT: slug not unique — would risk collision'); sys.exit(1)
    sid = subs[0]['id']
    uid = sb.table('units').select('id').eq('subject_id', sid).eq('slug', USLUG).execute().data[0]['id']
    L = (sb.table('lessons').select('id,title,content_html,exam_tip_html,conclusion_html,narration_manifest')
         .eq('unit_id', uid).eq('lesson_number', LN).single().execute().data)
    print(f"Lesson: {L['title']}")
    voice_name, voice_label = get_voice_for_lesson(LN)
    combined = (L.get('content_html') or '') + (L.get('exam_tip_html') or '') + (L.get('conclusion_html') or '')
    chunks = extract_narration_chunks(combined)
    print(f"{len(chunks)} chunks, voice {voice_label}")
    # sanity: confirm the Paré chunks now read cleanly (no stray entity)
    bad = [t for _, t in chunks if '&reacute' in t or 'reacute' in t]
    print(f"chunks still containing broken Paré entity: {len(bad)}")
    old = {e['id']: e['src'] for e in (L.get('narration_manifest') or [])}
    base = AUDIO_PUBLIC_URL + '/'
    r2 = get_r2_client(); manifest = []; t0 = time.time()
    for nid, text in chunks:
        r2_key = old[nid][len(base):] if (nid in old and old[nid].startswith(base)) \
                 else f"{SLUG}/{USLUG}/narration_lesson-{LN:02d}_{nid}.mp3"
        mp3 = generate_audio_rest(text, voice_name)
        if mp3 is None:
            print(f"FAILED at {nid}"); sys.exit(1)
        upload_bytes_to_r2(r2, AUDIO_BUCKET, r2_key, mp3, 'audio/mpeg')
        manifest.append({'id': nid, 'src': f'{base}{r2_key}', 'duration': get_mp3_duration(mp3)})
    sb.table('lessons').update({'narration_manifest': manifest}).eq('id', L['id']).execute()
    print(f"DONE: {len(manifest)} clips, {time.time()-t0:.0f}s")
    # show a Paré chunk so we can confirm it reads right
    for _, t in chunks:
        if 'Par' in t:
            print('  sample:', t[:90].encode('ascii', 'backslashreplace').decode()); break

if __name__ == '__main__':
    main()
