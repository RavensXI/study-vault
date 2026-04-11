"""
Merge per-unit JSON files into per-language files and insert into Supabase.
Combines spanish_people-and-lifestyle.json + spanish_popular-culture.json + spanish_communication-and-world.json
into spanish_practice_data.json, then inserts.

Usage: python scripts/language-practice/merge_and_insert.py [--subject spanish|french|german] [--dry-run]
"""
import os, sys, json, argparse

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from supabase import create_client

UNITS = {
    'spanish': ['people-and-lifestyle', 'popular-culture', 'communication-and-world'],
    'french': ['people-and-lifestyle', 'popular-culture', 'communication-and-world'],
    'german': ['people-and-lifestyle', 'popular-culture', 'communication-and-world'],
}

def validate_practice_data(pd, lesson_label):
    """Basic validation of practice_data structure."""
    issues = []
    if not pd.get('method_card'):
        issues.append('missing method_card')
    if not pd.get('problem_bank'):
        issues.append('missing problem_bank')
    else:
        pb = pd['problem_bank']
        b = len(pb.get('bronze', []))
        s = len(pb.get('silver', []))
        g = len(pb.get('gold', []))
        if b < 6: issues.append(f'only {b} bronze problems (need 8)')
        if s < 4: issues.append(f'only {s} silver problems (need 6)')
        if g < 4: issues.append(f'only {g} gold problems (need 6)')

        # Check each problem has input_type
        for tier in ['bronze', 'silver', 'gold']:
            for i, p in enumerate(pb.get(tier, [])):
                if 'input_type' not in p:
                    issues.append(f'{tier}[{i}] missing input_type')
    return issues

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', choices=['spanish','french','german'])
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--merge-only', action='store_true', help='Only merge files, skip DB insert')
    args = parser.parse_args()

    data_dir = os.path.dirname(__file__)
    subjects = [args.subject] if args.subject else ['spanish', 'french', 'german']

    for slug in subjects:
        units = UNITS[slug]
        all_lessons = []
        missing_files = []

        for unit_slug in units:
            fpath = os.path.join(data_dir, f'{slug}_{unit_slug}.json')
            if not os.path.exists(fpath):
                missing_files.append(fpath)
                continue
            with open(fpath, 'r', encoding='utf-8') as f:
                unit_data = json.load(f)
            print(f'  Loaded {slug}_{unit_slug}.json: {len(unit_data)} lessons')
            all_lessons.extend(unit_data)

        if missing_files:
            print(f'  [WARN] Missing files: {missing_files}')

        if not all_lessons:
            print(f'  [SKIP] No data for {slug}')
            continue

        # Validate
        total_problems = 0
        for entry in all_lessons:
            pd = entry.get('practice_data', {})
            label = f'{slug} {entry["unit_slug"]} L{entry["lesson_number"]:02d}'
            issues = validate_practice_data(pd, label)
            if issues:
                print(f'  [WARN] {label}: {", ".join(issues)}')

            pb = pd.get('problem_bank', {})
            total_problems += len(pb.get('bronze', [])) + len(pb.get('silver', [])) + len(pb.get('gold', []))

        # Write merged file
        merged_path = os.path.join(data_dir, f'{slug}_practice_data.json')
        with open(merged_path, 'w', encoding='utf-8') as f:
            json.dump(all_lessons, f, ensure_ascii=False, indent=2)
        print(f'\n=== {slug.upper()}: {len(all_lessons)} lessons, {total_problems} problems → {merged_path} ===\n')

        if args.merge_only:
            continue

        # Insert to Supabase
        sb = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

        subj = sb.table('subjects').select('id').eq('slug', slug).not_.is_('school_id', 'null').execute().data
        if not subj:
            print(f'  [ERROR] Subject {slug} not found')
            continue
        sid = subj[0]['id']

        unit_rows = sb.table('units').select('id, slug').eq('subject_id', sid).execute().data
        unit_map = {u['slug']: u['id'] for u in unit_rows}

        updated = 0
        for entry in all_lessons:
            uid = unit_map.get(entry['unit_slug'])
            if not uid:
                print(f'  [ERROR] Unit {entry["unit_slug"]} not found')
                continue

            lesson_rows = sb.table('lessons').select('id, title').eq('unit_id', uid).eq('lesson_number', entry['lesson_number']).execute().data
            if not lesson_rows:
                print(f'  [ERROR] Lesson {entry["lesson_number"]} not found in {entry["unit_slug"]}')
                continue

            lid = lesson_rows[0]['id']
            title = lesson_rows[0]['title']

            if args.dry_run:
                pb = entry['practice_data'].get('problem_bank', {})
                n = len(pb.get('bronze',[])) + len(pb.get('silver',[])) + len(pb.get('gold',[]))
                print(f'  [DRY] L{entry["lesson_number"]:02d}: {title} ({n} problems)')
            else:
                sb.table('lessons').update({'practice_data': entry['practice_data']}).eq('id', lid).execute()
                print(f'  [OK] L{entry["lesson_number"]:02d}: {title}')
                updated += 1

        if not args.dry_run and updated > 0:
            # Update subjects.settings.practice_units
            settings_result = sb.table('subjects').select('settings').eq('id', sid).execute().data
            settings = settings_result[0].get('settings') or {}
            if not isinstance(settings, dict):
                settings = {}
            settings['practice_units'] = list(unit_map.keys())
            sb.table('subjects').update({'settings': settings}).eq('id', sid).execute()
            print(f'  Updated {updated} lessons + practice_units = {list(unit_map.keys())}')

if __name__ == '__main__':
    main()
