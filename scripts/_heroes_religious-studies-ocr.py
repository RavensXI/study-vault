"""Set hero images for religious-studies-ocr from the hero_keywords embedded in
each lesson JSON (scripts/_content_religious-studies-ocr/lessons/*.json).
Unsplash first, hero-index fallback on 403/no-result. Live Unsplash regular URLs
(stable). Usage: python scripts/_heroes_religious-studies-ocr.py [--commit]"""
import sys, glob, json, time, argparse
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client
from lib.unsplash import search_unsplash, trigger_unsplash_download
from lib.hero_index import search_heroes

SLUG = 'religious-studies-ocr'


def load_json(path):
    raw = open(path, 'rb').read()
    if raw[:3] == b'\xef\xbb\xbf':
        raw = raw[3:]
    return json.loads(raw.decode('utf-8'))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--commit', action='store_true')
    args = ap.parse_args(); sb = get_client()
    sid = sb.table('subjects').select('id,name').eq('slug', SLUG).is_('school_id', 'null').single().execute().data
    sname = sid['name']; sid = sid['id']
    units = {u['slug']: u['id'] for u in sb.table('units').select('id,slug').eq('subject_id', sid).execute().data}
    unsplash_dead = False
    downloaded = reused = none = 0
    for path in sorted(glob.glob('scripts/_content_religious-studies-ocr/lessons/*.json')):
        d = load_json(path)
        uslug = d.get('_unit_slug'); ln = d.get('_lesson_number')
        kws = d.get('hero_keywords') or []
        cap = d.get('hero_image_caption') or sname
        if uslug not in units or ln is None or not kws:
            print(f"  [SKIP] {path}"); continue
        url = None; ph = ''; src = None
        if not unsplash_dead:
            for q in kws:
                try:
                    r = search_unsplash(q, per_page=6)
                except Exception as ex:
                    if '403' in str(ex):
                        unsplash_dead = True; print('  Unsplash rate-limited; index fallback'); break
                    continue
                if r:
                    url = r[0]['url']; ph = r[0].get('photographer', ''); src = 'unsplash'
                    try: trigger_unsplash_download(r[0].get('_download_location', ''))
                    except Exception: pass
                    break
                time.sleep(0.3)
        if not url:
            m = search_heroes(' '.join(kws), min_score=3)
            if m: url = m[0]['hero_url']; src = 'index'
        caption = (cap.rstrip('.') + f" (Photo: {ph} / Unsplash)") if (src == 'unsplash' and ph) else cap
        if args.commit and url:
            row = sb.table('lessons').select('id').eq('unit_id', units[uslug]).eq('lesson_number', ln).single().execute().data
            sb.table('lessons').update({'hero_image_url': url, 'hero_image_alt': cap[:120],
                'hero_image_caption': caption, 'hero_image_position': 'center center'}).eq('id', row['id']).execute()
        if src == 'unsplash': downloaded += 1
        elif src == 'index': reused += 1
        else: none += 1
        print(f"  {uslug} L{ln:02d}: {src or 'NONE'}")
    print(f"\n{SLUG}: {downloaded} unsplash + {reused} index + {none} none = {downloaded+reused}/{downloaded+reused+none}")


if __name__ == '__main__':
    main()
