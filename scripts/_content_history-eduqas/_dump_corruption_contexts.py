#!/usr/bin/env python3
"""Dump the exact corrupted strings (ascii-safe repr) so we can decide the
correct fix for each. Real accented chars show as \\xNN; literal broken
entities show as &reacute; etc."""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client

sb = get_client()
subjects = {s['slug']: s for s in sb.table('subjects').select('id,slug').execute().data}
subj = subjects['history-aqa']
units = {u['id']: u for u in sb.table('units').select('id,slug,subject_id').execute().data
         if u.get('subject_id') == subj['id']}
unit_ids = list(units)

PLAIN = ['practice_questions', 'knowledge_checks', 'flashcard_questions', 'glossary_terms', 'description']
HTMLF = ['content_html', 'exam_tip_html', 'conclusion_html', 'hero_image_caption']

def a(s):  # ascii-safe
    return s.encode('ascii', 'backslashreplace').decode('ascii')

rows = sb.table('lessons').select(','.join(['id','lesson_number','unit_id','title'] + PLAIN + HTMLF)) \
        .in_('unit_id', unit_ids).execute().data

print('========== ALL &reacute; CONTEXTS ==========')
n = 0
for r in rows:
    for f in PLAIN + HTMLF:
        v = r.get(f)
        s = v if isinstance(v, str) else ('' if v is None else str(v))
        for m in re.finditer(r'&reacute;', s):
            i = m.start(); seg = s[max(0,i-30):i+35]
            print(f"  [{units[r['unit_id']]['slug']} L{r['lesson_number']} {f}] …{a(seg)}…")
            n += 1
print(f'  total &reacute;: {n}')

print('\n========== ENTITIES IN PLAIN-TEXT FIELDS (render as literal junk) ==========')
ENT = re.compile(r'&[a-zA-Z#][a-zA-Z0-9]{0,12};')
for r in rows:
    for f in PLAIN:
        v = r.get(f)
        s = v if isinstance(v, str) else ('' if v is None else str(v))
        ents = ENT.findall(s)
        # ignore structural entities that are legitimately needed even in text JSON
        bad = [e for e in ents if e not in ('&amp;', '&lt;', '&gt;')]
        if bad:
            print(f"  [{units[r['unit_id']]['slug']} L{r['lesson_number']} {f}] {sorted(set(bad))}")

print('\n========== britain-health-people DESCRIPTIONS (full) ==========')
bhp = next(uid for uid,u in units.items() if u['slug']=='britain-health-people')
for r in sorted([x for x in rows if x['unit_id']==bhp], key=lambda x:x['lesson_number']):
    print(f"  L{r['lesson_number']}: {a(r.get('description') or '')}")
