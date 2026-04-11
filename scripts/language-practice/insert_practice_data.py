"""
Insert language practice_data from JSON files into Supabase.
Usage: python scripts/language-practice/insert_practice_data.py [--subject spanish|french|german] [--dry-run]
"""
import os, sys, json, argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from supabase import create_client

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', choices=['spanish','french','german'], help='Single subject to process')
    parser.add_argument('--dry-run', action='store_true', help='Print what would be updated without writing')
    args = parser.parse_args()

    sb = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])
    data_dir = os.path.dirname(__file__)

    subjects = [args.subject] if args.subject else ['spanish', 'french', 'german']

    for slug in subjects:
        json_path = os.path.join(data_dir, f'{slug}_practice_data.json')
        if not os.path.exists(json_path):
            print(f'[SKIP] {json_path} not found')
            continue

        with open(json_path, 'r', encoding='utf-8') as f:
            lessons_data = json.load(f)

        print(f'\n=== {slug.upper()} — {len(lessons_data)} lessons ===')

        # Get subject (school-specific, not generic)
        subj = sb.table('subjects').select('id').eq('slug', slug).not_.is_('school_id', 'null').execute().data
        if not subj:
            print(f'  [ERROR] Subject {slug} not found (school-specific)')
            continue
        sid = subj[0]['id']

        # Get units
        units = sb.table('units').select('id, slug, name').eq('subject_id', sid).execute().data
        unit_map = {u['slug']: u['id'] for u in units}

        updated = 0
        for entry in lessons_data:
            unit_slug = entry['unit_slug']
            lesson_number = entry['lesson_number']
            practice_data = entry['practice_data']

            uid = unit_map.get(unit_slug)
            if not uid:
                print(f'  [ERROR] Unit {unit_slug} not found')
                continue

            # Find lesson
            lesson = sb.table('lessons').select('id, title').eq('unit_id', uid).eq('lesson_number', lesson_number).execute().data
            if not lesson:
                print(f'  [ERROR] Lesson {lesson_number} in {unit_slug} not found')
                continue

            lid = lesson[0]['id']
            title = lesson[0]['title']

            if args.dry_run:
                pb = practice_data.get('problem_bank', {})
                b = len(pb.get('bronze', []))
                s = len(pb.get('silver', []))
                g = len(pb.get('gold', []))
                print(f'  [DRY] L{lesson_number:02d} {title}: {b}B + {s}S + {g}G = {b+s+g} problems')
            else:
                sb.table('lessons').update({'practice_data': practice_data}).eq('id', lid).execute()
                print(f'  [OK] L{lesson_number:02d} {title}')
                updated += 1

        if not args.dry_run:
            print(f'  Updated {updated} lessons')

            # Update subjects.settings to add practice_units
            settings_result = sb.table('subjects').select('settings').eq('id', sid).execute().data
            settings = settings_result[0]['settings'] if settings_result else {}
            if not settings or not isinstance(settings, dict):
                settings = {}

            unit_slugs = list(unit_map.keys())
            settings['practice_units'] = unit_slugs
            sb.table('subjects').update({'settings': settings}).eq('id', sid).execute()
            print(f'  Updated settings.practice_units = {unit_slugs}')

if __name__ == '__main__':
    main()
