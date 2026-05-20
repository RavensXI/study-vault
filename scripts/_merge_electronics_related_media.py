"""Merge curated related_media from disk JSONs into Supabase lesson rows.

Preserves any 'Podcasts' category already present on the Supabase row (added
by the parallel podcast pipeline) — strips out and replaces everything else.

For each lesson JSON in scripts/_content_electronics-eduqas/lessons/:
  1. Read _lesson_id and related_media (4 new categories: Videos & Channels,
     Documentaries, Study Tools, Articles & Web)
  2. Fetch current Supabase row.related_media
  3. Extract any Podcasts category from Supabase
  4. Merge: [Podcasts (if any), then the 4 new categories from disk] — Podcasts
     first means lesson-loader.js still finds it for the audio player; sidebar
     display order is Videos > Documentaries > Study Tools > Articles
  5. Write merged array back to Supabase

Usage:
  python scripts/_merge_electronics_related_media.py             # dry-run
  python scripts/_merge_electronics_related_media.py --apply     # write
"""
import argparse, glob, json, os, sys
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

CONTENT_DIR = 'scripts/_content_electronics-eduqas/lessons'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    sb = get_client()
    files = sorted(glob.glob(os.path.join(CONTENT_DIR, '*.json')))
    print(f'Found {len(files)} lesson JSONs\n')

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
            print(f'  [skip] {slug}: no related_media in disk JSON'); no_rm += 1; continue

        # Fetch current Supabase row
        row = sb.table('lessons').select('related_media').eq('id', lid).single().execute().data
        existing = row.get('related_media') or []
        podcast_cat = None
        if isinstance(existing, list):
            for cat in existing:
                if cat.get('category') == 'Podcasts':
                    podcast_cat = cat
                    break

        # Filter disk_rm to exclude any Podcasts the agent slipped in
        disk_rm_non_pod = [c for c in disk_rm if c.get('category') != 'Podcasts']
        # Also drop empty-items categories (agents output [] for Documentaries when no fit)
        disk_rm_non_pod = [c for c in disk_rm_non_pod if c.get('items')]

        merged = []
        if podcast_cat:
            merged.append(podcast_cat)
            preserved_pod += 1
        else:
            no_pod += 1
        merged.extend(disk_rm_non_pod)

        cat_summary = ' / '.join(c.get('category', '?') + f"({len(c.get('items') or [])})" for c in merged)
        print(f'  [{"APPLY" if args.apply else "dry  "}] {slug[:55]:55s} -> {cat_summary}')
        if args.apply:
            sb.table('lessons').update({'related_media': merged}).eq('id', lid).execute()
            ok += 1

    print(f'\nSummary:')
    print(f'  Files processed   : {len(files)}')
    if args.apply:
        print(f'  Updated in DB     : {ok}')
    print(f'  Podcasts preserved: {preserved_pod}/{len(files)}')
    print(f'  No Podcasts in DB : {no_pod}')
    print(f'  No RM on disk     : {no_rm}')
    print(f'  Failures          : {fail}')


if __name__ == '__main__':
    main()
