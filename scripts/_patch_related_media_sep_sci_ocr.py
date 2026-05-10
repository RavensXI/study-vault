"""Patch related_media field only for all 57 separate-sciences-ocr lessons.

Updates Supabase lessons.related_media from the local JSON files.
Only touches related_media — no other fields.
"""

import sys
import os
import json
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client

LESSONS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '_content_separate-sciences-ocr',
    'lessons'
)


def main():
    dry_run = '--dry-run' in sys.argv
    sb = get_client()

    paths = sorted(glob.glob(os.path.join(LESSONS_DIR, '*.json')))
    print(f'Found {len(paths)} JSON files')

    ok = 0
    skipped = 0
    errors = 0

    for p in paths:
        slug = os.path.basename(p).replace('.json', '')
        with open(p, encoding='utf-8') as f:
            data = json.load(f)

        lid = data.get('_lesson_id')
        if not lid:
            print(f'  [SKIP] {slug}: no _lesson_id')
            skipped += 1
            continue

        related_media = data.get('related_media')
        if not related_media:
            print(f'  [SKIP] {slug}: no related_media')
            skipped += 1
            continue

        if dry_run:
            items_count = sum(len(cat.get('items', [])) for cat in related_media)
            print(f'  [DRY]  {lid[:8]} {slug}: {items_count} items across {len(related_media)} categories')
            ok += 1
        else:
            try:
                sb.table('lessons').update({'related_media': related_media}).eq('id', lid).execute()
                items_count = sum(len(cat.get('items', [])) for cat in related_media)
                print(f'  [OK]   {lid[:8]} {slug}: {items_count} items')
                ok += 1
            except Exception as e:
                print(f'  [ERR]  {slug}: {e}')
                errors += 1

    print(f'\nDone. {ok} updated, {skipped} skipped, {errors} errors.')


if __name__ == '__main__':
    main()
