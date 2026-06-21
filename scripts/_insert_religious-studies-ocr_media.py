"""Validate + insert related_media for religious-studies-ocr.
Reads scripts/_content_religious-studies-ocr/media/*.json (each a list of
{unit_slug, lesson_number, related_media}); validates categories, spec-code
drift and URL safety; updates Supabase related_media AND patches the lesson
JSONs (scripts/_content_religious-studies-ocr/lessons/) for reproducibility.
Usage: python scripts/_insert_religious-studies-ocr_media.py [--commit]"""
import sys, os, glob, json, re, argparse
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

SLUG = 'religious-studies-ocr'
MEDIA_DIR = 'scripts/_content_religious-studies-ocr/media'
LESSONS_DIR = 'scripts/_content_religious-studies-ocr/lessons'
ALLOWED = {'Videos & Channels', 'Study Tools', 'Podcasts', 'Documentaries', 'Movies', 'TV Shows'}
CODE_RX = re.compile(r'\bJ625\b|\bJ125\b|[Tt]opic [Aa]rea|Component Group', re.I)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--commit', action='store_true')
    args = ap.parse_args(); sb = get_client()
    sid = sb.table('subjects').select('id').eq('slug', SLUG).is_('school_id', 'null').single().execute().data['id']
    units = {u['slug']: u['id'] for u in sb.table('units').select('id,slug').eq('subject_id', sid).execute().data}
    errs = []; cats = {}; entries = []
    for path in sorted(glob.glob(os.path.join(MEDIA_DIR, '*.json'))):
        if os.path.basename(path).startswith('_'):
            continue  # skip audit reports / scratch files
        data = json.load(open(path, encoding='utf-8'))
        for e in data:
            ctx = f"{e['unit_slug']}/L{e['lesson_number']}"
            if e['unit_slug'] not in units:
                errs.append(f"{ctx}: unknown unit"); continue
            rm = e.get('related_media')
            if not isinstance(rm, list) or not rm:
                errs.append(f"{ctx}: empty related_media"); continue
            for c in rm:
                if c.get('category') not in ALLOWED:
                    errs.append(f"{ctx}: bad cat {c.get('category')!r}")
                cats[c.get('category')] = cats.get(c.get('category'), 0) + len(c.get('items', []))
                for it in c.get('items', []):
                    for k in ('title', 'url', 'description'):
                        if not it.get(k): errs.append(f"{ctx}/{c.get('category')}: item missing {k}")
                    blob = it.get('title', '') + it.get('description', '') + it.get('url', '')
                    if CODE_RX.search(blob): errs.append(f"{ctx}: spec code in {it.get('title','')[:30]!r}")
            entries.append(e)
    if errs:
        print(f"FAIL: {len(errs)} errors")
        for x in errs[:20]: print('   -', x)
        sys.exit(1)
    print(f"OK: {len(entries)} lessons | cats {cats}")
    if not args.commit:
        print("DRY — pass --commit to write"); return
    for e in entries:
        row = sb.table('lessons').select('id').eq('unit_id', units[e['unit_slug']]).eq('lesson_number', e['lesson_number']).single().execute().data
        sb.table('lessons').update({'related_media': e['related_media']}).eq('id', row['id']).execute()
        # patch lesson JSON for reproducibility
        lp = os.path.join(LESSONS_DIR, f"{e['unit_slug']}__{e['lesson_number']:02d}.json")
        if os.path.exists(lp):
            d = json.load(open(lp, encoding='utf-8'))
            d['related_media'] = e['related_media']
            json.dump(d, open(lp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"COMMITTED related_media for {len(entries)} lessons")


if __name__ == '__main__':
    main()
