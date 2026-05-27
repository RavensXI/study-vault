#!/usr/bin/env python3
"""Repair encoding garbling in the Unity history-aqa subject (pre-existing, not
from the Eduqas build).

Two fixes:
  1. Strip the broken `&reacute;` entity (a spurious insertion in "Pa&reacute;ré"
     -> "Paré"), everywhere it appears.
  2. In PLAIN-TEXT fields (description + the structured question/glossary lists),
     decode any remaining HTML entities (&mdash; &pound; &rsquo; &deg; &eacute;
     …) to their unicode characters — they currently render as literal junk.

HTML body fields keep their valid entities (they render correctly there); only
the broken &reacute; is removed from them.

Dry-run by default. Pass --apply to write to Supabase.
"""
import argparse, html, json, sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client

PLAIN_STRUCT = ['practice_questions', 'knowledge_checks', 'flashcard_questions', 'glossary_terms']
PLAIN_STR = ['description']
HTML_FIELDS = ['content_html', 'exam_tip_html', 'conclusion_html', 'hero_image_caption']

def fix_plain(s):
    if not isinstance(s, str):
        return s
    return html.unescape(s.replace('&reacute;', ''))

def fix_html(s):
    if not isinstance(s, str):
        return s
    return s.replace('&reacute;', '')

def walk_plain(obj):
    if isinstance(obj, str):
        return fix_plain(obj)
    if isinstance(obj, list):
        return [walk_plain(x) for x in obj]
    if isinstance(obj, dict):
        return {k: walk_plain(v) for k, v in obj.items()}
    return obj

def a(s):
    return s.encode('ascii', 'backslashreplace').decode('ascii')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    sb = get_client()

    subj = next(s for s in sb.table('subjects').select('id,slug').execute().data if s['slug'] == 'history-aqa')
    units = {u['id']: u for u in sb.table('units').select('id,slug,subject_id').execute().data
             if u.get('subject_id') == subj['id']}
    rows = sb.table('lessons').select(
        ','.join(['id', 'lesson_number', 'unit_id'] + PLAIN_STRUCT + PLAIN_STR + HTML_FIELDS)
    ).in_('unit_id', list(units)).execute().data

    changed = []   # (row, {field: newval}, [sample strings])
    reacute_html_lessons = set()
    for r in rows:
        patch = {}
        for f in PLAIN_STRUCT:
            old = r.get(f)
            if old is None:
                continue
            new = walk_plain(old)
            if json.dumps(new, ensure_ascii=False) != json.dumps(old, ensure_ascii=False):
                patch[f] = new
        for f in PLAIN_STR:
            old = r.get(f)
            if isinstance(old, str):
                new = fix_plain(old)
                if new != old:
                    patch[f] = new
        for f in HTML_FIELDS:
            old = r.get(f)
            if isinstance(old, str) and '&reacute;' in old:
                patch[f] = fix_html(old)
                reacute_html_lessons.add((units[r['unit_id']]['slug'], r['lesson_number']))
        if patch:
            changed.append((r, patch))

    print(f"history-aqa: {len(changed)} / {len(rows)} lessons need repair\n")
    for r, patch in changed:
        print(f"  [{units[r['unit_id']]['slug']} L{r['lesson_number']}] fields: {sorted(patch)}")
    print(f"\nLessons with &reacute; in NARRATED html (need re-narration): "
          f"{sorted(reacute_html_lessons)}")

    # show a few before/after samples
    print('\n--- SAMPLE before/after ---')
    shown = 0
    for r, patch in changed:
        for f, new in patch.items():
            old = r.get(f)
            o = json.dumps(old, ensure_ascii=False) if not isinstance(old, str) else old
            n = json.dumps(new, ensure_ascii=False) if not isinstance(new, str) else new
            # find first differing entity region
            m = re.search(r'&(reacute|mdash|pound|rsquo|deg|bull|rarr|eacute|egrave|aacute|ouml|iacute|OElig|Zdot|scaron);', o)
            if not m:
                continue
            i = m.start()
            print(f"  [{units[r['unit_id']]['slug']} L{r['lesson_number']} {f}]")
            print(f"    OLD …{a(o[max(0,i-25):i+30])}…")
            # locate roughly the same area in new
            print(f"    NEW …{a(n[max(0,i-25):i+25])}…")
            shown += 1
            break
        if shown >= 12:
            break

    if args.apply:
        print('\nAPPLYING…')
        ok = 0
        for r, patch in changed:
            sb.table('lessons').update(patch).eq('id', r['id']).execute()
            ok += 1
        print(f'Updated {ok} lessons.')
    else:
        print('\n(dry-run — pass --apply to write)')

if __name__ == '__main__':
    main()
