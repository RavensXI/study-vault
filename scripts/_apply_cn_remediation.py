"""
Apply agent-produced surgical find/replace edits to Cambridge National lessons.
Reads scripts/_cn_remediation/{slug}.replacements.json — a list of
{lesson_number, field, old, new}. Each `old` MUST occur exactly once in that
lesson's field, or the edit is refused (never a fuzzy/partial apply).

Usage: python scripts/_apply_cn_remediation.py [--commit]
"""
import sys, os, json, glob, argparse
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client

DIR = 'scripts/_cn_remediation'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--commit', action='store_true')
    args = ap.parse_args()
    sb = get_client()

    applied = refused = 0
    for path in sorted(glob.glob(os.path.join(DIR, '*.replacements.json'))):
        slug = os.path.basename(path).replace('.replacements.json', '')
        reps = json.load(open(path, encoding='utf-8'))
        sid = sb.table('subjects').select('id').eq('slug', slug).is_('school_id', 'null').single().execute().data['id']
        uid = sb.table('units').select('id').eq('subject_id', sid).order('sort_order').execute().data[0]['id']
        print(f"=== {slug}: {len(reps)} replacements")
        # group by lesson
        by_lesson = {}
        for r in reps:
            by_lesson.setdefault(r['lesson_number'], []).append(r)
        for ln, rs in sorted(by_lesson.items()):
            row = sb.table('lessons').select('id,content_html,exam_tip_html,conclusion_html').eq('unit_id', uid).eq('lesson_number', ln).single().execute().data
            upd = {}
            fields = {f: row.get(f) or '' for f in ('content_html', 'exam_tip_html', 'conclusion_html')}
            for r in rs:
                fld, old, new = r['field'], r['old'], r['new']
                cur = upd.get(fld, fields.get(fld, ''))
                cnt = cur.count(old)
                if cnt != 1:
                    refused += 1
                    print(f"  REFUSE L{ln:02d} {fld}: old occurs {cnt}x (need 1): {old[:60]!r}")
                    continue
                upd[fld] = cur.replace(old, new)
                applied += 1
                print(f"  OK L{ln:02d} {fld}: {old[:45]!r} -> {new[:45]!r}")
            if upd and args.commit:
                sb.table('lessons').update(upd).eq('id', row['id']).execute()
    print(f"\n{'COMMITTED' if args.commit else 'DRY-RUN'}: {applied} applied, {refused} refused")


if __name__ == '__main__':
    main()
