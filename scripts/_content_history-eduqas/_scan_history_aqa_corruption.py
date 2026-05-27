#!/usr/bin/env python3
"""Scope the encoding corruption in the history-aqa (Unity) subject. Reports
every text field containing mojibake / replacement chars / broken entities,
so we know the full extent before repairing."""
import sys, re, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client

sb = get_client()

subjects = {s['slug']: s for s in sb.table('subjects').select('id,slug').execute().data}
subj = subjects['history-aqa']
units = {u['id']: u for u in sb.table('units').select('id,slug,subject_id').execute().data
         if u.get('subject_id') == subj['id']}
unit_ids = list(units)

TEXT_FIELDS = ['title', 'slug', 'description', 'content_html', 'exam_tip_html',
               'conclusion_html', 'hero_image_caption', 'practice_questions',
               'knowledge_checks', 'flashcard_questions', 'glossary_terms']

# Markers of corruption:
#   �  = replacement char (shown as �)
#   â€, Ã, Â = classic UTF-8-misread-as-1252 mojibake lead bytes
#   &reacute; / other non-standard entities
MARKERS = ['�', 'â€', 'Ã', 'Â', '&reacute;']
ENT = re.compile(r'&([a-zA-Z#][a-zA-Z0-9]{0,12});')
VALID = {'amp','lt','gt','quot','apos','nbsp','mdash','ndash','rsquo','lsquo',
         'rdquo','ldquo','hellip','rarr','larr','eacute','egrave','agrave',
         'ccedil','deg','pound','copy','reg','times','frac12','frac14','frac34',
         'middot','bull','sect','para','scedil','dstrok'}

rows = sb.table('lessons').select(','.join(['id','lesson_number','unit_id'] + TEXT_FIELDS)) \
        .in_('unit_id', unit_ids).execute().data
print(f"history-aqa: {len(rows)} lessons across {len(unit_ids)} units\n")

def jstr(v):
    return v if isinstance(v, str) else ('' if v is None else str(v))

marker_hits = collections.Counter()
field_hits = collections.Counter()
affected = {}   # lesson id -> set(fields)
desc_examples = []

for r in rows:
    for f in TEXT_FIELDS:
        s = jstr(r.get(f))
        if not s: continue
        hit = False
        for mk in MARKERS:
            if mk in s:
                marker_hits[mk] += s.count(mk); hit = True
        for m in ENT.finditer(s):
            if m.group(1).lower() not in VALID and not m.group(1).startswith('#'):
                marker_hits['badentity:' + m.group(0)] += 1; hit = True
        if hit:
            field_hits[f] += 1
            affected.setdefault(r['id'], (r, set()))[1].add(f)
            if f == 'description':
                desc_examples.append((units[r['unit_id']]['slug'], r['lesson_number'], s))

print('=== corruption markers (count) ===')
for mk, n in marker_hits.most_common():
    show = mk.replace('�', '<U+FFFD �>')
    print(f'  {show!r}: {n}')
print('\n=== fields affected (lesson count) ===')
for f, n in field_hits.most_common():
    print(f'  {f}: {n}')
print(f'\n=== {len(affected)} distinct lessons affected ===')
for r, fields in affected.values():
    print(f"  [{units[r['unit_id']]['slug']}] L{r['lesson_number']}  fields={sorted(fields)}  id={r['id']}")

print('\n=== description examples (full text) ===')
for uslug, ln, s in desc_examples[:20]:
    print(f"  [{uslug}] L{ln}: {s}")
