import sys, re
sys.path.insert(0, 'scripts')
from lib.supabase_client import get_client
sb = get_client()

SLUGS = ['cambridge-nationals-child-development', 'cambridge-nationals-creative-imedia',
         'cambridge-nationals-engineering-design', 'cambridge-nationals-engineering-manufacture',
         'cambridge-nationals-engineering-programmable-systems', 'cambridge-nationals-sport-science']

# Only REAL leaks: the specific OCR unit codes + spec-structure phrases.
patterns = [
    (re.compile(r'\bR(?:038|041|047|057|093|180)\b'), 'OCR-code'),
    (re.compile(r'[Tt]opic [Aa]rea\s*\d?(?:\.\d)?'), 'topic-area'),
    (re.compile(r'\b[Ss]pecification\s+\d\.\d'), 'spec-NN'),
    (re.compile(r'\b[Tt]opics?\s+\d\.\d'), 'topics-NN'),
    (re.compile(r'externally assessed', re.I), 'ext-assessed'),
]


def strip(html):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html or ''))


total = 0
for slug in SLUGS:
    sid = sb.table('subjects').select('id').eq('slug', slug).is_('school_id', 'null').single().execute().data['id']
    units = sb.table('units').select('id,slug,subtitle').eq('subject_id', sid).order('sort_order').execute().data
    out = []
    for u in units:
        for rx, lbl in patterns:
            for m in rx.finditer(u.get('subtitle') or ''):
                out.append(f"  UNIT.subtitle [{lbl}]: ...{(u['subtitle'])[max(0,m.start()-30):m.end()+25]}...")
        ls = sb.table('lessons').select('lesson_number,title,description,content_html,exam_tip_html,conclusion_html').eq('unit_id', u['id']).order('lesson_number').execute().data
        for l in ls:
            blob = ' || '.join([l.get('title') or '', l.get('description') or '',
                                strip(l.get('content_html')), strip(l.get('exam_tip_html')), strip(l.get('conclusion_html'))])
            for rx, lbl in patterns:
                for m in rx.finditer(blob):
                    out.append(f"  L{l['lesson_number']:02d} [{lbl}]: ...{blob[max(0,m.start()-35):m.end()+30]}...")
    total += len(out)
    print(f"=== {slug}: {len(out)}")
    for h in out:
        print(h)
print(f"\nTOTAL residual prose refs: {total}")
