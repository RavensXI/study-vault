#!/usr/bin/env python3
"""Platform-wide garbling repair. Three fixes, field-aware:

  1. MOJIBAKE — ftfy.fix_text on any string with â€/Ã/Â markers (â€"→—, Â£→£ …).
  2. INVALID sub/sup entities — &sub2;/&sup8; etc. don't exist in HTML5:
       HTML body fields  -> <sub>2</sub> / <sup>8</sup>  (narration strips the
                            tag and reads the digit, e.g. "H two O")
       plain-text fields -> unicode ₂ / ⁸
     Plus &dj;→đ (the only other genuinely-invalid named entity found).
  3. VALID entities raw in PLAIN-TEXT fields — html.unescape → unicode
     (&mdash;→— &rsquo;→’ &eacute;→é …). HTML fields keep their valid entities.

Read-only dry-run by default; --apply writes to Supabase. Reports a re-narration
list: lessons whose NARRATED html (content_html/conclusion/exam_tip with
data-narration-id) changed.
"""
import argparse, html, json, re, sys, collections
from pathlib import Path
import ftfy
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client

HTML_FIELDS = ['content_html', 'exam_tip_html', 'conclusion_html', 'hero_image_caption']
PLAIN_STR = ['description', 'title']
PLAIN_STRUCT = ['practice_questions', 'knowledge_checks', 'flashcard_questions', 'glossary_terms']
NARRATED = ['content_html', 'exam_tip_html', 'conclusion_html']

SUB = {str(d): chr(0x2080 + d) for d in range(10)}
SUP = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
       '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
INVALID_NAMED = {'dj': 'đ'}   # đ

stats = collections.Counter()

def demojibake(s):
    if 'â€' not in s and 'Ã' not in s and 'Â' not in s:
        return s
    fixed = ftfy.fix_text(s)
    if fixed != s:
        stats['mojibake'] += 1
    return fixed

def subsup_html(s):
    s2 = re.sub(r'&sub(\d+);', r'<sub>\1</sub>', s)
    s2 = re.sub(r'&sup(\d+);', r'<sup>\1</sup>', s2)
    if s2 != s:
        stats['subsup_html'] += 1
    return s2

def subsup_plain(s):
    s2 = re.sub(r'&sub(\d+);', lambda m: ''.join(SUB[d] for d in m.group(1)), s)
    s2 = re.sub(r'&sup(\d+);', lambda m: ''.join(SUP[d] for d in m.group(1)), s2)
    if s2 != s:
        stats['subsup_plain'] += 1
    return s2

def invalid_named(s):
    for nm, ch in INVALID_NAMED.items():
        if '&' + nm + ';' in s:
            s = s.replace('&' + nm + ';', ch)
            stats['invalid_named'] += 1
    return s

def fix_html(s):
    if not isinstance(s, str):
        return s
    return invalid_named(subsup_html(demojibake(s)))

def fix_plain(s):
    if not isinstance(s, str):
        return s
    out = html.unescape(invalid_named(subsup_plain(demojibake(s))))
    if out != s and out == demojibake(s):
        pass
    return out

def walk_plain(obj):
    if isinstance(obj, str):
        return fix_plain(obj)
    if isinstance(obj, list):
        return [walk_plain(x) for x in obj]
    if isinstance(obj, dict):
        return {k: walk_plain(v) for k, v in obj.items()}
    return obj

def asc(s):
    return s.encode('ascii', 'backslashreplace').decode('ascii')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    sb = get_client()

    subjects = {s['id']: s['slug'] for s in sb.table('subjects').select('id,slug').execute().data}
    units = {u['id']: u for u in sb.table('units').select('id,slug,subject_id').execute().data}

    ALLF = HTML_FIELDS + PLAIN_STR + PLAIN_STRUCT
    changed = []          # (subj, unit_slug, lnum, id, patch, narrated_fields_changed)
    samples = collections.defaultdict(list)   # category -> [(loc, old, new)]
    per_subject = collections.Counter()
    renarrate = collections.defaultdict(list)  # subject -> [(unit_slug, lnum)]

    page = 0; SIZE = 300; total = 0
    while True:
        rows = sb.table('lessons').select(','.join(['id', 'lesson_number', 'unit_id'] + ALLF)) \
                .range(page * SIZE, page * SIZE + SIZE - 1).execute().data
        if not rows:
            break
        for r in rows:
            u = units.get(r['unit_id']) or {}
            subj = subjects.get(u.get('subject_id'), '???')
            uslug = u.get('slug', '?')
            patch = {}
            narrated_changed = []
            for f in ALLF:
                old = r.get(f)
                if old is None:
                    continue
                if f in PLAIN_STRUCT:
                    new = walk_plain(old)
                    diff = json.dumps(new, ensure_ascii=False) != json.dumps(old, ensure_ascii=False)
                elif f in HTML_FIELDS:
                    new = fix_html(old)
                    diff = new != old
                else:  # PLAIN_STR
                    new = fix_plain(old)
                    diff = new != old
                if diff:
                    patch[f] = new
                    if f in NARRATED and isinstance(old, str) and 'data-narration-id' in old:
                        narrated_changed.append(f)
                    # capture a sample
                    cat = ('subsup' if f in HTML_FIELDS else 'plain_or_subsup')
                    if len(samples[(subj, f)]) < 1:
                        o = old if isinstance(old, str) else json.dumps(old, ensure_ascii=False)
                        n = new if isinstance(new, str) else json.dumps(new, ensure_ascii=False)
                        m = re.search(r'&(sub|sup)\d+;|&[a-zA-Z]+;|â€|Â£|Ã', o)
                        if m:
                            i = m.start()
                            samples[(subj, f)].append((f, asc(o[max(0, i-22):i+30]), asc(n[max(0, i-22):i+30])))
            if patch:
                changed.append((subj, uslug, r['lesson_number'], r['id'], patch, narrated_changed))
                per_subject[subj] += 1
                if narrated_changed:
                    renarrate[subj].append((uslug, r['lesson_number'], narrated_changed))
            total += 1
        page += 1
    print(f"scanned {total} lessons; {len(changed)} need repair\n", file=sys.stderr)

    print("=== changes per subject ===")
    for subj, n in sorted(per_subject.items()):
        print(f"  {subj}: {n}")
    print(f"\n=== fix counts === {dict(stats)}")

    print("\n=== SAMPLES (one per subject+field) ===")
    for (subj, f), lst in sorted(samples.items()):
        for (ff, o, n) in lst:
            print(f"  [{subj} {ff}]\n    OLD …{o}…\n    NEW …{n}…")

    print("\n=== RE-NARRATION NEEDED (narrated html changed) ===")
    if not renarrate:
        print("  none")
    for subj in sorted(renarrate):
        items = renarrate[subj]
        print(f"  {subj}: {len(items)} lessons -> " +
              ', '.join(f"{us}/L{ln}" for us, ln, _ in items[:30]))

    if args.apply:
        print("\nAPPLYING…")
        ok = 0
        for subj, uslug, lnum, lid, patch, _ in changed:
            sb.table('lessons').update(patch).eq('id', lid).execute()
            ok += 1
            if ok % 50 == 0:
                print(f"  …{ok}/{len(changed)}", file=sys.stderr)
        print(f"Updated {ok} lessons.")
    else:
        print("\n(dry-run — pass --apply to write)")

if __name__ == '__main__':
    main()
