"""Dump Cambridge National lessons that still contain prose spec-code refs, so a
remediation agent can craft exact find/replace pairs. One file per subject."""
import sys, re, os, json
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client
sb = get_client()

TARGETS = {
    'cambridge-nationals-creative-imedia': [6],
    'cambridge-nationals-engineering-design': [1, 2, 3, 4, 5],
    'cambridge-nationals-engineering-manufacture': [1, 3, 4, 5],
    'cambridge-nationals-engineering-programmable-systems': [1, 4, 5],
    'cambridge-nationals-sport-science': [1, 2, 3, 4, 5, 7, 10],
}
OUTDIR = 'scripts/_cn_remediation'
os.makedirs(OUTDIR, exist_ok=True)

for slug, nums in TARGETS.items():
    sid = sb.table('subjects').select('id').eq('slug', slug).is_('school_id', 'null').single().execute().data['id']
    uid = sb.table('units').select('id').eq('subject_id', sid).order('sort_order').execute().data[0]['id']
    lines = []
    for n in nums:
        l = sb.table('lessons').select('lesson_number,title,content_html,exam_tip_html,conclusion_html').eq('unit_id', uid).eq('lesson_number', n).single().execute().data
        lines.append('=' * 80)
        lines.append(f"LESSON {n}: {l['title']}")
        for fld in ('content_html', 'exam_tip_html', 'conclusion_html'):
            lines.append(f"\n----- {fld} -----")
            lines.append(l.get(fld) or '(empty)')
    open(os.path.join(OUTDIR, slug + '.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
    print(f"wrote {OUTDIR}/{slug}.txt ({len(nums)} lessons)")
