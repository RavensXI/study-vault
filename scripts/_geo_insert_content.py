"""Insert generated geography content JSONs into Supabase.

Reads scripts/_geo_gen_{board}/*.json (and any subdirectories), validates each
output via _validate_content_json.py, then updates the matching lesson row
(by lesson_id from the _meta block) in Supabase.

Usage:
    python scripts/_geo_insert_content.py --board aqa
    python scripts/_geo_insert_content.py --all
    python scripts/_geo_insert_content.py --all --dry-run
"""
import sys, os, json, glob, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
from lib.supabase_client import get_client
from _validate_content_json import validate_file

DIRS = {
    'aqa': 'scripts/_geo_gen_aqa',
    'edexcel-a': 'scripts/_geo_gen_edexcel_a',
    'edexcel-b': 'scripts/_geo_gen_edexcel_b',
    'ocr': 'scripts/_geo_gen_ocr',
    'eduqas': 'scripts/_geo_gen_eduqas',
}

CONTENT_KEYS = [
    'description', 'content_html', 'exam_tip_html', 'conclusion_html',
    'practice_questions', 'knowledge_checks', 'flashcard_questions',
    'glossary_terms', 'hero_image_caption',
]


def collect_jsons(board_dir):
    """Find all lesson JSON files in board_dir + subdirs (skip _meta files)."""
    files = []
    for path in glob.glob(os.path.join(board_dir, '**', '*.json'), recursive=True):
        name = os.path.basename(path)
        if name.startswith('_'): continue
        if name in ('_plan.json', '_reference.json', '_todo.json'): continue
        if name.startswith('_slice'): continue
        files.append(path)
    return sorted(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board', choices=list(DIRS.keys()))
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if args.all:
        boards = list(DIRS.keys())
    elif args.board:
        boards = [args.board]
    else:
        parser.error('Provide --board or --all')
        return

    sb = get_client()
    grand_total = 0
    grand_fail = 0
    for board in boards:
        d = DIRS[board]
        if not os.path.isdir(d):
            print(f'[SKIP] {board}: dir missing')
            continue
        files = collect_jsons(d)
        print(f'\n=== {board} ({len(files)} files) ===')
        ok = fail = 0
        for f in files:
            try:
                violations = validate_file(f)
            except Exception as e:
                print(f'  [PARSE-ERR] {f}: {e}')
                grand_fail += 1; fail += 1
                continue
            if violations:
                print(f'  [VALIDATE-FAIL] {f}: {violations[:3]}')
                grand_fail += 1; fail += 1
                continue
            with open(f, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            meta = data.get('_meta') or {}
            lesson_id = meta.get('lesson_id')
            if not lesson_id:
                print(f'  [NO-META] {f}')
                grand_fail += 1; fail += 1
                continue
            payload = {k: data[k] for k in CONTENT_KEYS if k in data}
            payload['status'] = 'pending_review'
            if args.dry_run:
                print(f'  [DRY] {os.path.basename(f)} → lesson {lesson_id[:8]} ({len(payload)} keys)')
            else:
                sb.table('lessons').update(payload).eq('id', lesson_id).execute()
                print(f'  [OK] {os.path.basename(f)} → lesson {lesson_id[:8]}')
            ok += 1
            grand_total += 1
        print(f'  {board}: {ok} inserted, {fail} failed')
    print(f'\n[DONE] {grand_total} inserted, {grand_fail} failed across all boards')


if __name__ == '__main__':
    main()
