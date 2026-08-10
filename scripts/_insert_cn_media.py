"""
Validate + insert agent-produced related_media for Cambridge National subjects.
Reads scripts/_cn_media/{slug}.out.json — list of {lesson_number, related_media}.
Validates structure + that NO OCR spec code remains, then updates lessons.

Usage: python scripts/_insert_cn_media.py [--commit]
"""
import sys, os, json, glob, re, argparse
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

DIR = 'scripts/_cn_media'
ALLOWED = {'Videos & Channels', 'Study Tools', 'Podcasts', 'Documentaries', 'Movies', 'TV Shows'}
CODE_RX = re.compile(r'\bR(?:038|041|047|057|093|180)\b|OCR Cambridge National|externally assessed', re.I)


def validate(rm, ctx, errs):
    if not isinstance(rm, list) or not rm:
        errs.append(f"{ctx}: related_media not a non-empty list")
        return
    for cat in rm:
        c = cat.get('category')
        if c not in ALLOWED:
            errs.append(f"{ctx}: bad category {c!r}")
        items = cat.get('items')
        if not isinstance(items, list) or not items:
            errs.append(f"{ctx}/{c}: no items")
            continue
        for it in items:
            for k in ('title', 'url', 'description'):
                if not it.get(k):
                    errs.append(f"{ctx}/{c}: item missing {k}")
            blob = (it.get('title', '') + ' ' + it.get('description', '') + ' ' + it.get('url', ''))
            if CODE_RX.search(blob):
                errs.append(f"{ctx}/{c}: spec code still present in {it.get('title','')[:40]!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--commit', action='store_true')
    args = ap.parse_args()
    sb = get_client()
    files = sorted(glob.glob(os.path.join(DIR, '*.out.json')))
    total_err = 0
    for path in files:
        slug = os.path.basename(path).replace('.out.json', '')
        data = json.load(open(path, encoding='utf-8'))
        sid = sb.table('subjects').select('id').eq('slug', slug).is_('school_id', 'null').single().execute().data['id']
        uid = sb.table('units').select('id').eq('subject_id', sid).order('sort_order').execute().data[0]['id']
        errs = []
        cats_added = {}
        for entry in data:
            ln = entry['lesson_number']
            rm = entry['related_media']
            validate(rm, f"L{ln:02d}", errs)
            for c in rm:
                cats_added[c['category']] = cats_added.get(c['category'], 0) + len(c.get('items', []))
        if errs:
            total_err += len(errs)
            print(f"FAIL {slug}: {len(errs)} errors")
            for e in errs[:15]:
                print("   -", e)
            continue
        print(f"OK {slug}: {len(data)} lessons | cats {cats_added}")
        if args.commit:
            for entry in data:
                row = sb.table('lessons').select('id').eq('unit_id', uid).eq('lesson_number', entry['lesson_number']).single().execute().data
                sb.table('lessons').update({'related_media': entry['related_media']}).eq('id', row['id']).execute()
            print(f"   committed {len(data)} lessons")
    print(f"\n{'COMMITTED' if args.commit else 'VALIDATED'}: {total_err} errors")
    sys.exit(1 if total_err else 0)


if __name__ == '__main__':
    main()
