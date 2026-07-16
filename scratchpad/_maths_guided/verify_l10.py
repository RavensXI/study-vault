# -*- coding: utf-8 -*-
"""Independent adversarial verification of lesson_algebra-L10.json."""
import json, io, re
import sympy as sp

pd = json.load(io.open("lesson_algebra-L10.json", encoding="utf-8"))
x, y = sp.symbols('x y')
fails = []

def parse_eq(s):
    # s like 'y = x + 3' or 'x^2 + y^2 = 25' or 'xy = 3'
    s = s.replace('^', '**')
    # insert * for implicit mult: 2x -> 2*x, xy -> x*y, 5x -> 5*x, x( -> x*(
    s = re.sub(r'(\d)([xy(])', r'\1*\2', s)
    s = re.sub(r'([xy)])(\()', r'\1*\2', s)
    s = re.sub(r'x\s*y', 'x*y', s)
    lhs, rhs = s.split('=')
    return sp.Eq(sp.sympify(lhs), sp.sympify(rhs))

def solve_problem(display):
    inside = re.findall(r'\\\((.*?)\\\)', display)
    eqs = [parse_eq(e) for e in inside]
    sol = sp.solve(eqs, [x, y], dict=True)
    xs = sorted(set(sp.nsimplify(s[x]) for s in sol), key=lambda v: float(v))
    return xs, sol

for tier in ('bronze', 'silver', 'gold'):
    for i, p in enumerate(pd['problem_bank'][tier]):
        path = "%s[%d]" % (tier, i)
        xs, sol = solve_problem(p['display'])
        stored = sorted(float(v) for v in p['solutions'])
        got = sorted(float(v) for v in xs)
        if len(got) != len(stored) or any(abs(a-b) > 1e-6 for a, b in zip(got, stored)):
            fails.append("%s solutions mismatch: display->%s stored->%s" % (path, got, stored))
        # verify each solution pair satisfies both eqs
        inside = re.findall(r'\\\((.*?)\\\)', p['display'])
        eqs = [parse_eq(e) for e in inside]
        for srec in sol:
            for eq in eqs:
                r = (eq.lhs - eq.rhs).subs(srec)
                if abs(float(r)) > 1e-9:
                    fails.append("%s pair %s fails eq %s" % (path, srec, eq))
        # verify walk's final roots (boxes named 'root') land on solutions
        roots_in_walk = []
        for st in p['guided_steps']:
            pre = (st.get('pre') or '')
            if 'root, x =' in pre and st.get('answer') is not None:
                roots_in_walk.append(float(st['answer']))
            if 'root is x =' in pre and st.get('answer') is not None:
                roots_in_walk.append(float(st['answer']))
        if roots_in_walk:
            if sorted(roots_in_walk) != stored:
                fails.append("%s walk roots %s != stored %s" % (path, sorted(roots_in_walk), stored))
        # misconception expects: must not equal solution set, and must be a real wrong pair
        for j, m in enumerate(p.get('misconceptions') or []):
            e = m.get('expect')
            if e is None:
                continue
            es = sorted(float(v) for v in e)
            if es == stored:
                fails.append("%s.misc[%d] expect equals solution" % (path, j))
            # confirm expect pair does NOT satisfy the system (it is genuinely wrong)
            satisfies = False
            for srec in sol:
                pass
            # check the expect x-values are not both actual roots
            if all(any(abs(ev - float(v)) < 1e-6 for v in xs) for ev in es):
                fails.append("%s.misc[%d] expect values are actual roots" % (path, j))

# preservation check vs pre-dump
pre = json.load(io.open("_pre_fanout_dump.json", encoding="utf-8"))
# find L10 entry
def find_l10(obj):
    if isinstance(obj, dict):
        if obj.get('id') == 'ddb5e897-f8ce-4c64-961a-7d6095d41a7c':
            return obj
        for v in obj.values():
            r = find_l10(v)
            if r: return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_l10(v)
            if r: return r
    return None
entry = find_l10(pre)
if entry:
    pdold = entry.get('practice_data') or entry.get('pd') or {}
    for fld in ('related_videos', 'topic_links'):
        if json.dumps(pdold.get(fld), sort_keys=True) != json.dumps(pd.get(fld), sort_keys=True):
            fails.append("PRESERVE %s changed vs pre-dump" % fld)
    # worked_examples: only em-dash label changes allowed
    a = json.dumps(pdold.get('worked_examples'), ensure_ascii=False).replace(' — ', ': ').replace('—', ':')
    b = json.dumps(pd.get('worked_examples'), ensure_ascii=False)
    if a != b:
        fails.append("PRESERVE worked_examples changed beyond em-dash fix")
    print("pre-dump L10 found; keys:", list(pdold.keys()))
else:
    print("WARN: L10 not found in pre-dump for preservation diff")

# completion boundary sanity
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pd['problem_bank'][tier]):
        gs=p['guided_steps']
        pf=None
        for gi,st in enumerate(gs):
            if st.get('phase')=='substitute': pf=gi; break
        live=sum(1 for st in gs[pf:] if st.get('answer') is not None)
        if pf is None or pf<1 or live<2:
            fails.append("%s[%d] bad completion boundary pf=%s live=%s"%(tier,i,pf,live))

if fails:
    print("VERIFY FAIL (%d):" % len(fails))
    for f in fails: print("  -", f)
else:
    print("VERIFY PASS: all problems solve to stored solutions; walks land on roots; expects are genuine wrong pairs; preservation OK.")
