#!/usr/bin/env python3
"""Platform-wide garbling sweep. Scans every lesson in every subject for:
  A. broken/unknown HTML entities (e.g. &reacute;) — render as literal junk
  B. valid HTML entities left raw in PLAIN-TEXT fields (description / questions
     / glossary) — render as literal junk in non-HTML contexts
  C. true mojibake: U+FFFD replacement char, or 'â€' / 'Ã' byte-damage digraphs

Read-only. Aggregates per subject so we know where to fix."""
import sys, re, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client

sb = get_client()

subjects = {s['id']: s['slug'] for s in sb.table('subjects').select('id,slug').execute().data}
units = {u['id']: u for u in sb.table('units').select('id,slug,subject_id').execute().data}

PLAIN = ['description', 'practice_questions', 'knowledge_checks',
         'flashcard_questions', 'glossary_terms']
HTMLF = ['content_html', 'exam_tip_html', 'conclusion_html', 'hero_image_caption', 'title']
ALLF = PLAIN + HTMLF

VALID = {'amp','lt','gt','quot','apos','nbsp','mdash','ndash','rsquo','lsquo',
         'rdquo','ldquo','hellip','rarr','larr','uarr','darr','harr',
         'eacute','egrave','agrave','acirc','aacute','auml','aring','aelig',
         'ccedil','eacute','ecirc','euml','iacute','icirc','iuml','igrave',
         'ntilde','oacute','ocirc','ouml','ograve','oslash','otilde','uacute',
         'ucirc','uuml','ugrave','yacute','yuml','szlig','scaron','zcaron',
         'ccaron','rcaron','scedil','tcedil','ncedil','lstrok','dstrok',
         'OElig','oelig','Aring','Auml','Ouml','Uuml','Eacute','Ccedil',
         'deg','pound','euro','cent','yen','curren','copy','reg','trade',
         'times','divide','plusmn','frac12','frac14','frac34','sup2','sup3',
         'sup1','middot','bull','dagger','Dagger','sect','para','prime',
         'Prime','micro','permil','ordf','ordm','iexcl','iquest','laquo',
         'raquo','Zdot','zdot','minus','infin','ne','le','ge','asymp',
         'alpha','beta','gamma','delta','pi','mu','Omega','deg'}

ENT = re.compile(r'&([a-zA-Z#][a-zA-Z0-9]{0,12});')
MOJI = re.compile(r'�|â€|Ã[\x80-\xbf©³¨¡]|Â[\x80-\xbf°£©]')

# per subject -> counters
broken = collections.defaultdict(collections.Counter)     # subj -> {entity: n}
broken_lessons = collections.defaultdict(set)
plain_ent = collections.defaultdict(collections.Counter)  # subj -> {entity: n}
plain_lessons = collections.defaultdict(set)
moji = collections.defaultdict(int)
moji_lessons = collections.defaultdict(set)
moji_ex = collections.defaultdict(list)
subj_lesson_count = collections.Counter()

def s_of(v):
    return v if isinstance(v, str) else ('' if v is None else str(v))

page = 0; SIZE = 300; total = 0
while True:
    rows = sb.table('lessons').select(','.join(['id','lesson_number','unit_id'] + ALLF)) \
            .range(page*SIZE, page*SIZE + SIZE - 1).execute().data
    if not rows:
        break
    for r in rows:
        u = units.get(r['unit_id'])
        subj = subjects.get(u['subject_id'], '???') if u else '???'
        subj_lesson_count[subj] += 1
        key = (subj, r['unit_id'], r['lesson_number'])
        for f in ALLF:
            s = s_of(r.get(f))
            if not s:
                continue
            for m in ENT.finditer(s):
                name = m.group(1)
                if name.startswith('#'):
                    continue
                if name.lower() not in {v.lower() for v in VALID}:
                    broken[subj][m.group(0)] += 1
                    broken_lessons[subj].add(key)
                elif f in PLAIN:
                    plain_ent[subj][m.group(0)] += 1
                    plain_lessons[subj].add(key)
            mm = MOJI.search(s)
            if mm:
                moji[subj] += len(MOJI.findall(s))
                moji_lessons[subj].add(key)
                if len(moji_ex[subj]) < 2:
                    i = mm.start()
                    moji_ex[subj].append(f"{f}: …{s[max(0,i-25):i+25].encode('ascii','backslashreplace').decode()}…")
        total += 1
    page += 1
    print(f"  …scanned {total} lessons", file=sys.stderr)

print(f"\n================ SWEEP: {total} lessons across {len(subj_lesson_count)} subjects ================\n")

all_subj = sorted(set(list(broken) + list(plain_ent) + list(moji)))
if not all_subj:
    print("CLEAN — no garbling found in any subject.")
for subj in all_subj:
    bl = len(broken_lessons[subj]); pl = len(plain_lessons[subj]); ml = len(moji_lessons[subj])
    print(f"### {subj}  ({subj_lesson_count[subj]} lessons)")
    if broken[subj]:
        print(f"   A. BROKEN entities  [{bl} lessons]: " +
              ', '.join(f'{e}×{n}' for e, n in broken[subj].most_common(12)))
    if plain_ent[subj]:
        print(f"   B. entities in PLAIN-TEXT fields  [{pl} lessons]: " +
              ', '.join(f'{e}×{n}' for e, n in plain_ent[subj].most_common(12)))
    if moji[subj]:
        print(f"   C. MOJIBAKE  [{ml} lessons, {moji[subj]} hits]: " + ' | '.join(moji_ex[subj]))
    print()
