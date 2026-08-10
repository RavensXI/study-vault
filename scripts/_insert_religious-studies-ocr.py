"""Insert OCR Religious Studies (J625) content into the scaffolded lesson rows.
Reads scripts/_content_religious-studies-ocr/lessons/*.json (each carries
_unit_slug + _lesson_number) and updates content fields by unit_slug+lesson_number,
leaving status pending_review. Usage: python scripts/_insert_religious-studies-ocr.py [--commit]"""
import sys, glob, json, argparse
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

SUBJECT_SLUG = 'religious-studies-ocr'
FIELDS = ['description', 'content_html', 'exam_tip_html', 'conclusion_html',
          'practice_questions', 'knowledge_checks', 'flashcard_questions',
          'glossary_terms', 'hero_image_caption', 'related_media']


def load_json(path):
    raw = open(path, 'rb').read()
    if raw[:3] == b'\xef\xbb\xbf':
        raw = raw[3:]
    return json.loads(raw.decode('utf-8'))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--commit', action='store_true')
    args = ap.parse_args(); sb = get_client()
    sid = sb.table('subjects').select('id').eq('slug', SUBJECT_SLUG).is_('school_id', 'null').single().execute().data['id']
    units = {u['slug']: u['id'] for u in sb.table('units').select('id,slug').eq('subject_id', sid).execute().data}
    paths = sorted(glob.glob('scripts/_content_religious-studies-ocr/lessons/*.json'))
    done = miss = 0
    for p in paths:
        try:
            data = load_json(p)
        except Exception as e:
            print(f"  [PARSE-FAIL] {p}: {e}"); miss += 1; continue
        uslug = data.get('_unit_slug'); ln = data.get('_lesson_number')
        if uslug not in units or ln is None:
            print(f"  [SKIP] {p}: unit={uslug} num={ln}"); miss += 1; continue
        row = sb.table('lessons').select('id').eq('unit_id', units[uslug]).eq('lesson_number', ln).execute().data
        if not row:
            print(f"  [NO-ROW] {uslug} L{ln}"); miss += 1; continue
        upd = {k: data[k] for k in FIELDS if k in data}
        if args.commit:
            sb.table('lessons').update(upd).eq('id', row[0]['id']).execute()
            print(f"  [OK] {uslug} L{ln:02d}")
        else:
            print(f"  [DRY] {uslug} L{ln:02d}: {len(data.get('content_html','') or '')} chars, "
                  f"{len(data.get('practice_questions',[]))}pq {len(data.get('knowledge_checks',[]))}kc "
                  f"{len(data.get('flashcard_questions',[]))}fc")
        done += 1
    print(f"\n{'COMMITTED' if args.commit else 'DRY'}: {done} lessons ({miss} skipped)")


if __name__ == '__main__':
    main()
