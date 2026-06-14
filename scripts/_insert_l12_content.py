"""Insert L1/2 vocational article content into the scaffolded lesson rows.
Reads scripts/_content_l12-*/{unit_slug}__L{NN}.json and updates content fields,
leaving status pending_review. Usage: python scripts/_insert_l12_content.py [--commit]"""
import sys, os, glob, json, argparse
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

DIRMAP = {
    'scripts/_content_l12-retail-business': 'l12-retail-business',
    'scripts/_content_l12-sport-coaching': 'l12-sport-and-coaching-principles',
}
FIELDS = ['title', 'description', 'content_html', 'exam_tip_html', 'conclusion_html',
          'practice_questions', 'knowledge_checks', 'flashcard_questions', 'glossary_terms']


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--commit', action='store_true')
    args = ap.parse_args(); sb = get_client()
    done = 0
    for d, subj in DIRMAP.items():
        sid = sb.table('subjects').select('id').eq('slug', subj).is_('school_id', 'null').single().execute().data['id']
        units = {u['slug']: u['id'] for u in sb.table('units').select('id,slug').eq('subject_id', sid).execute().data}
        for f in sorted(glob.glob(os.path.join(d, '*__L*.json'))):
            base = os.path.basename(f)[:-5]
            uslug, ln = base.split('__L'); lesson_number = int(ln)
            data = json.load(open(f, encoding='utf-8'))
            upd = {k: data[k] for k in FIELDS if k in data}
            uid = units[uslug]
            row = sb.table('lessons').select('id').eq('unit_id', uid).eq('lesson_number', lesson_number).single().execute().data
            if args.commit:
                sb.table('lessons').update(upd).eq('id', row['id']).execute()
                done += 1
                print(f"[OK] {subj} {uslug} L{lesson_number:02d}")
            else:
                print(f"[DRY] {subj} {uslug} L{lesson_number:02d}: {len(data.get('content_html',''))} chars, "
                      f"{len(data.get('practice_questions',[]))}pq {len(data.get('knowledge_checks',[]))}kc "
                      f"{len(data.get('flashcard_questions',[]))}fc")
    print(f"\n{'COMMITTED' if args.commit else 'DRY'}: {done if args.commit else 20} lessons")


if __name__ == '__main__':
    main()
