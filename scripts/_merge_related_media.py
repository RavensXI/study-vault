"""Merge curated related_media from disk JSONs into Supabase, preserving any
'Podcasts' category already on the Supabase row (added by the parallel podcast
pipeline) while replacing all other categories with the freshly curated ones.

For each lesson JSON in scripts/_content_{slug}/lessons/:
  1. Read _lesson_id and related_media (4 new categories)
  2. Fetch current Supabase row.related_media
  3. Extract any Podcasts category from Supabase
  4. Merge: [Podcasts (if any), then other categories from disk]
  5. Write merged array back to Supabase

Usage:
  python scripts/_merge_related_media.py <subject-slug>            # dry-run
  python scripts/_merge_related_media.py <subject-slug> --apply    # write
"""
import argparse, glob, json, os, sys
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slug')
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    content_dir = f'scripts/_content_{args.slug}/lessons'
    if not os.path.isdir(content_dir):
        print(f'ERROR: {content_dir} not found')
        sys.exit(1)

    sb = get_client()
    files = sorted(glob.glob(os.path.join(content_dir, '*.json')))
    print(f'Found {len(files)} lesson JSONs for {args.slug}\n')

    ok = preserved_pod = no_pod = no_rm = fail = 0
    for path in files:
        slug = os.path.splitext(os.path.basename(path))[0]
        raw = open(path, 'rb').read()
        if raw[:3] == b'\xef\xbb\xbf':
            raw = raw[3:]
        data = json.loads(raw.decode('utf-8'))
        lid = data.get('_lesson_id')
        disk_rm = data.get('related_media') or []
        if not lid:
            print(f'  [skip] {slug}: no _lesson_id'); fail += 1; continue
        if not disk_rm:
            print(f'  [skip] {slug}: no related_media on disk'); no_rm += 1; continue

        row = sb.table('lessons').select('related_media').eq('id', lid).single().execute().data
        existing = row.get('related_media') or []
        podcast_cat = None
        for cat in existing if isinstance(existing, list) else []:
            if cat.get('category') == 'Podcasts':
                podcast_cat = cat
                break

        disk_rm_non_pod = [c for c in disk_rm if c.get('category') != 'Podcasts' and c.get('items')]
        merged = ([podcast_cat] if podcast_cat else []) + disk_rm_non_pod
        if podcast_cat:
            preserved_pod += 1
        else:
            no_pod += 1

        cat_summary = ' / '.join(c.get('category', '?') + f"({len(c.get('items') or [])})" for c in merged)
        print(f'  [{"APPLY" if args.apply else "dry  "}] {slug[:55]:55s} -> {cat_summary}')
        if args.apply:
            sb.table('lessons').update({'related_media': merged}).eq('id', lid).execute()
            ok += 1

    print(f'\nSummary for {args.slug}:')
    print(f'  Files processed   : {len(files)}')
    if args.apply:
        print(f'  Updated in DB     : {ok}')
    print(f'  Podcasts preserved: {preserved_pod}/{len(files)}')
    print(f'  No Podcasts in DB : {no_pod}')
    print(f'  No RM on disk     : {no_rm}')
    print(f'  Failures          : {fail}')


if __name__ == '__main__':
    main()
