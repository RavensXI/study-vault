"""Set hero images for the L1/2 port subjects from the agent-written keyword files
scripts/_l12_media/_hero_keywords_{slug}.json (list of {unit_slug, lesson_number,
hero_keywords, caption}). Unsplash first, hero-index fallback on 403/no-result.
Usage: python scripts/_heroes_l12.py [--commit]"""
import sys, os, json, time, argparse
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client
from lib.unsplash import search_unsplash, trigger_unsplash_download
from lib.hero_index import search_heroes

SLUGS = ['l12-retail-business', 'l12-sport-and-coaching-principles']


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--commit', action='store_true')
    args = ap.parse_args(); sb = get_client()
    unsplash_dead = False
    for slug in SLUGS:
        kw = json.load(open(f'scripts/_l12_media/_hero_keywords_{slug}.json', encoding='utf-8'))
        sid = sb.table('subjects').select('id,name').eq('slug', slug).is_('school_id', 'null').single().execute().data
        sname = sid['name']; sid = sid['id']
        units = {u['slug']: u['id'] for u in sb.table('units').select('id,slug').eq('subject_id', sid).execute().data}
        reused = downloaded = 0
        for e in kw:
            url = None; ph = ''; src = None
            if not unsplash_dead:
                for q in e['hero_keywords']:
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
                    time.sleep(0.4)
            if not url:
                m = search_heroes(' '.join(e['hero_keywords']), min_score=3)
                if m: url = m[0]['hero_url']; src = 'index'
            cap = e['caption']
            caption = (cap.rstrip('.') + f" (Photo: {ph} / Unsplash)") if (src == 'unsplash' and ph) else cap
            if args.commit and url:
                row = sb.table('lessons').select('id').eq('unit_id', units[e['unit_slug']]).eq('lesson_number', e['lesson_number']).single().execute().data
                sb.table('lessons').update({'hero_image_url': url, 'hero_image_alt': e.get('caption', sname)[:120],
                    'hero_image_caption': caption, 'hero_image_position': 'center center'}).eq('id', row['id']).execute()
            if src == 'unsplash': downloaded += 1
            elif src == 'index': reused += 1
            print(f"  {slug} {e['unit_slug']} L{e['lesson_number']:02d}: {src or 'NONE'}")
        print(f"{slug}: {downloaded} unsplash + {reused} index = {downloaded+reused}/{len(kw)}")


if __name__ == '__main__':
    main()
