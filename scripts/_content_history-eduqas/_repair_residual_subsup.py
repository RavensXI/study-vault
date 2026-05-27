#!/usr/bin/env python3
"""Second-pass repair for residual malformed sub/sup that the first pass missed
(different patterns). All occurrences are in HTML body fields.

  &sub;2;            -> <sub>2</sub>      (CO&sub;2; -> CO<sub>2</sub>)
  &sub;f</sub>       -> <sub>f</sub>      (broken opening tag, R_f values)
  &sup;&#8315;⁹;     -> <sup>-9</sup>     (broken sup tag, negative powers)
  &sup;2;            -> <sup>2</sup>
  &sup;f</sup>       -> <sup>f</sup>
  ion charge &spades;:
     metal cation  X<sup>n</sup>&spades;          -> X<sup>n+</sup>
     poly. anion  </sub><sup>n</sup>&spades;      -> </sub><sup>n-</sup>
       (carbonate CO3^2-, sulfate SO4^2- get MINUS; Ca/Cu/Fe/Al/Mg get PLUS)

Dry-run by default; --apply writes. Re-emits a re-narration list.
"""
import argparse, html, json, re, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client

HTML_FIELDS = ['content_html', 'exam_tip_html', 'conclusion_html', 'hero_image_caption']
PLAIN_STR = ['description', 'title']
PLAIN_STRUCT = ['practice_questions', 'knowledge_checks', 'flashcard_questions', 'glossary_terms']
NARRATED = ['content_html', 'exam_tip_html', 'conclusion_html']
ALLF = HTML_FIELDS + PLAIN_STR + PLAIN_STRUCT

SUP2N = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5',
         '⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁺':'+','⁻':'-',
         '⁼':'=','⁽':'(','⁾':')'}
SUB2N = {chr(0x2080+i): str(i) for i in range(10)}
SUB2N.update({'₊':'+','₋':'-'})

def norm_run(content, table):
    content = html.unescape(content)
    return ''.join(table.get(c, c) for c in content)

SUPRUN = r'(?:&#\d+;|[⁰¹²³⁴-⁹⁺⁻⁼⁽⁾])+'
SUBRUN = r'(?:&#\d+;|[₀-₎])+'

def fix(s):
    if not isinstance(s, str) or '&' not in s:
        return s
    # ion charges first (anion rule before cation rule)
    s = re.sub(r'</sub><sup>(\d+)</sup>&spades;', r'</sub><sup>\1-</sup>', s)
    s = re.sub(r'([A-Za-z])<sup>(\d+)</sup>&spades;', r'\1<sup>\2+</sup>', s)
    # broken opening tags
    s = re.sub(r'&sub;([^&<;]+?)</sub>', r'<sub>\1</sub>', s)
    s = re.sub(r'&sup;([^&<;]+?)</sup>', r'<sup>\1</sup>', s)
    # sup with superscript-char content + stray ';'
    s = re.sub(r'&sup;(' + SUPRUN + r');', lambda m: '<sup>' + norm_run(m.group(1), SUP2N) + '</sup>', s)
    s = re.sub(r'&sub;(' + SUBRUN + r');', lambda m: '<sub>' + norm_run(m.group(1), SUB2N) + '</sub>', s)
    # plain digits + stray ';'
    s = re.sub(r'&sub;(\d+);', r'<sub>\1</sub>', s)
    s = re.sub(r'&sup;(\d+);', r'<sup>\1</sup>', s)
    return s

def walk(o):
    if isinstance(o, str): return fix(o)
    if isinstance(o, list): return [walk(x) for x in o]
    if isinstance(o, dict): return {k: walk(v) for k, v in o.items()}
    return o

def asc(s): return s.encode('ascii', 'backslashreplace').decode()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--apply', action='store_true')
    args = ap.parse_args(); sb = get_client()
    subjects = {s['id']: s['slug'] for s in sb.table('subjects').select('id,slug').execute().data}
    units = {u['id']: u for u in sb.table('units').select('id,slug,subject_id').execute().data}

    changed = []; renarrate = collections.defaultdict(list); samples = []
    page = 0; SIZE = 300; total = 0
    while True:
        rows = sb.table('lessons').select(','.join(['id','lesson_number','unit_id'] + ALLF)) \
                .range(page*SIZE, page*SIZE+SIZE-1).execute().data
        if not rows: break
        for r in rows:
            u = units.get(r['unit_id']) or {}; subj = subjects.get(u.get('subject_id'), '???')
            patch = {}; narr = []
            for f in ALLF:
                old = r.get(f)
                if old is None: continue
                new = walk(old) if f in PLAIN_STRUCT else fix(old)
                same = (json.dumps(new, ensure_ascii=False) == json.dumps(old, ensure_ascii=False)) if f in PLAIN_STRUCT else (new == old)
                if not same:
                    patch[f] = new
                    if f in NARRATED and isinstance(old, str) and 'data-narration-id' in old:
                        narr.append(f)
                    if len(samples) < 30 and isinstance(old, str):
                        m = re.search(r'&(sub|sup|spades);', old)
                        if m:
                            i = m.start(); samples.append((subj, u.get('slug'), r['lesson_number'], f,
                                asc(old[max(0,i-18):i+24]), asc(new[max(0,i-18):i+26])))
            if patch:
                changed.append((r['id'], patch))
                if narr: renarrate[subj].append((u.get('slug'), r['lesson_number']))
            total += 1
        page += 1
    print(f"scanned {total}; {len(changed)} lessons to fix", file=sys.stderr)
    print("=== samples ===")
    for subj, us, ln, f, o, n in samples:
        print(f"  [{subj} {us} L{ln} {f}]\n    OLD …{o}…\n    NEW …{n}…")
    print("\n=== re-narration (this pass) ===")
    for subj in sorted(renarrate):
        print(f"  {subj}: " + ', '.join(f'{us}/L{ln}' for us, ln in renarrate[subj]))
    if args.apply:
        for lid, patch in changed:
            sb.table('lessons').update(patch).eq('id', lid).execute()
        print(f"\nUpdated {len(changed)} lessons.")
    else:
        print("\n(dry-run)")

if __name__ == '__main__':
    main()
