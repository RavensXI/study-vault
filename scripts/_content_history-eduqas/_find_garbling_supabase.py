#!/usr/bin/env python3
"""Find the live source of the 'Pa&reacute;ré' garbling Tom reported. Searches
ALL lessons (every subject) for the broken entity, then prints which subject/
unit/lesson it lives in plus a snippet, so we know exactly what to fix."""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client

sb = get_client()

def snip(s, needle, w=60):
    if not s: return ''
    i = s.lower().find(needle.lower())
    if i < 0: return ''
    a = max(0, i - w); b = min(len(s), i + len(needle) + w)
    return ('…' if a else '') + s[a:b].replace('\n', ' ') + ('…' if b < len(s) else '')

# Build a unit_id -> (subject_slug, unit title) map for context
units = sb.table('units').select('id,slug,subject_id').execute().data
subjects = {s['id']: s for s in sb.table('subjects').select('id,slug').execute().data}
umap = {u['id']: u for u in units}

def ctx(unit_id):
    u = umap.get(unit_id, {})
    subj = subjects.get(u.get('subject_id'), {})
    return f"{subj.get('slug','?')} / {u.get('slug','?')}"

print('=== content_html / description / title / exam_tip_html / conclusion_html containing "reacute" ===')
hits = {}
for col in ['content_html', 'description', 'title', 'exam_tip_html', 'conclusion_html']:
    try:
        rows = sb.table('lessons').select(
            'id,lesson_number,title,slug,unit_id,description,content_html,exam_tip_html,conclusion_html'
        ).ilike(col, '%reacute%').limit(50).execute().data
    except Exception as e:
        print(f'  ({col} query failed: {e})'); continue
    for r in rows:
        hits[r['id']] = r

if not hits:
    print('  NONE found anywhere in lessons.')
else:
    for r in hits.values():
        print(f"\n  [{ctx(r['unit_id'])}] L{r.get('lesson_number')} {r.get('title')!r}")
        print(f"   id={r['id']}  slug={r.get('slug')}")
        for col in ['title', 'description', 'content_html', 'exam_tip_html', 'conclusion_html']:
            sn = snip(r.get(col) or '', 'reacute')
            if sn: print(f"     {col}: {sn}")

# Broader: any '&' + letters that isn't a common valid entity, in descriptions
print('\n\n=== lesson DESCRIPTIONS containing HTML entities (should be plain unicode) ===')
ent = re.compile(r'&[a-zA-Z#][a-zA-Z0-9]{0,12};')
# pull descriptions for history-eduqas + a couple of likely medicine subjects
for subj_slug in ['history-eduqas', 'history-edexcel', 'history', 'health-and-social-care']:
    subj = next((s for s in subjects.values() if s['slug'] == subj_slug), None)
    if not subj: continue
    unit_ids = [u['id'] for u in units if u.get('subject_id') == subj['id']]
    if not unit_ids: continue
    rows = sb.table('lessons').select('id,lesson_number,title,unit_id,description').in_('unit_id', unit_ids).execute().data
    flagged = [r for r in rows if r.get('description') and ent.search(r['description'])]
    print(f"\n  {subj_slug}: {len(flagged)} / {len(rows)} descriptions contain entities")
    for r in flagged[:15]:
        ents = set(ent.findall(r['description']))
        print(f"     [{ctx(r['unit_id'])}] L{r.get('lesson_number')} {sorted(ents)} :: {r['description'][:90]}…")
