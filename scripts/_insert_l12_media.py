"""Validate + insert L1/2 related_media (scripts/_l12_media/{slug}.out.json =
list of {unit_slug, lesson_number, related_media}). Usage: --commit to write."""
import sys, os, glob, json, re, argparse
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

DIR = 'scripts/_l12_media'
ALLOWED = {'Videos & Channels', 'Study Tools', 'Podcasts', 'Documentaries', 'Movies', 'TV Shows'}
CODE_RX = re.compile(r'\b5299QA\b|\b5259QA\b|[Tt]opic [Aa]rea|externally assessed', re.I)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--commit', action='store_true')
    args = ap.parse_args(); sb = get_client()
    total_err = 0
    for path in sorted(glob.glob(os.path.join(DIR, 'l12-*.out.json'))):
        slug = os.path.basename(path).replace('.out.json', '')
        data = json.load(open(path, encoding='utf-8'))
        sid = sb.table('subjects').select('id').eq('slug', slug).is_('school_id', 'null').single().execute().data['id']
        units = {u['slug']: u['id'] for u in sb.table('units').select('id,slug').eq('subject_id', sid).execute().data}
        errs = []; cats = {}
        for e in data:
            rm = e['related_media']; ctx = f"{e['unit_slug']}/L{e['lesson_number']}"
            if not isinstance(rm, list) or not rm:
                errs.append(f"{ctx}: empty related_media"); continue
            for c in rm:
                if c.get('category') not in ALLOWED:
                    errs.append(f"{ctx}: bad cat {c.get('category')!r}")
                cats[c.get('category')] = cats.get(c.get('category'), 0) + len(c.get('items', []))
                for it in c.get('items', []):
                    for k in ('title', 'url', 'description'):
                        if not it.get(k): errs.append(f"{ctx}/{c.get('category')}: item missing {k}")
                    if CODE_RX.search(it.get('title', '') + it.get('description', '') + it.get('url', '')):
                        errs.append(f"{ctx}: spec code in {it.get('title','')[:30]!r}")
        if errs:
            total_err += len(errs); print(f"FAIL {slug}: {len(errs)} errors")
            for x in errs[:12]: print('   -', x)
            continue
        print(f"OK {slug}: {len(data)} lessons | cats {cats}")
        if args.commit:
            for e in data:
                uid = units[e['unit_slug']]
                row = sb.table('lessons').select('id').eq('unit_id', uid).eq('lesson_number', e['lesson_number']).single().execute().data
                sb.table('lessons').update({'related_media': e['related_media']}).eq('id', row['id']).execute()
            print(f"   committed {len(data)} lessons")
    print(f"\n{'COMMITTED' if args.commit else 'VALIDATED'}: {total_err} errors")
    sys.exit(1 if total_err else 0)


if __name__ == '__main__':
    main()
