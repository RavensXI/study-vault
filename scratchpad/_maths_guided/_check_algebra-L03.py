# -*- coding: utf-8 -*-
import json, io, re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
x = sp.symbols('x')
TR = standard_transformations + (implicit_multiplication_application,)

def L2e(s):
    s = s.replace('\\(', '').replace('\\)', '').strip()
    s = re.sub(r'(?i)factorise', '', s).strip()
    s = s.replace('^2', '**2')
    return parse_expr(s, transformations=TR, local_dict={'x': x})

pd = json.load(io.open('lesson_algebra-L03.json', encoding='utf-8'))
errs = []

def check_walk_boundary(steps, path):
    # >=1 step before first phase:substitute, >=2 live boxes at/after
    sub = None
    for i,st in enumerate(steps):
        if st.get('phase')=='substitute' and sub is None: sub=i
    live_boxes = sum(1 for st in steps if st.get('answer') is not None)
    if sub is None:
        errs.append(path+" no substitute boundary"); return
    if sub < 1: errs.append(path+" boundary at 0")
    after = sum(1 for st in steps[sub:] if st.get('answer') is not None)
    if after < 2: errs.append(path+f" only {after} live boxes after boundary")

# problem bank
pb = pd['problem_bank']
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pb[tier]):
        path=f"{tier}[{i}]"
        target = sp.expand(L2e(p['display']))
        ci = p['solutions'][0]
        # correct option expands to target
        if sp.expand(L2e(p['options'][ci])) != target:
            errs.append(path+" correct option != target")
        # expects cover all distractors, none == correct
        exps=[m['expect'] for m in p['misconceptions']]
        if ci in exps: errs.append(path+" a misconception expect == correct index")
        if sorted(exps)!=sorted(j for j in range(len(p['options'])) if j!=ci):
            errs.append(path+f" expects {sorted(exps)} dont cover all distractors")
        # for each misconception verify the distractor it points at actually expands to something != target
        for m in p['misconceptions']:
            e=m['expect']
            if sp.expand(L2e(p['options'][e]))==target and 'not finished' not in m['message'] and 'still' not in m['message'] and 'not fully' not in m['message']:
                # distractor equals target but message doesn't acknowledge incomplete
                errs.append(path+f" expect {e} equals target but msg not incompleteness: {m['message'][:40]}")
        check_walk_boundary(p['guided_steps'], path+'.guided_steps')

# teach walks land right
def eval_box_chain(steps):
    return [st.get('answer') for st in steps if st.get('answer') is not None]

# opener check
op=pd['guided']['opener']['steps']
opb=[st['answer'] for st in op if st.get('answer') is not None]
if opb!=[6,2,3]: errs.append(f"opener boxes {opb} != [6,2,3]")

# teach boundary + box count
for tier in ('bronze','silver','gold'):
    t=pd['guided']['teach'][tier]
    nb=sum(1 for st in t['steps'] if st.get('answer') is not None)
    if nb<4: errs.append(f"teach.{tier} only {nb} boxes")

# Verify specific final check boxes rebuild originals for a sample by recomputing from display
# Bronze: last two boxes should be p and q (coefficients of original)
for tier,probs in (('bronze',pb['bronze']),):
    for i,p in enumerate(probs):
        e=sp.Poly(L2e(p['display']),x)
        coeffs=e.all_coeffs()  # highest first
        # linear px+q -> [p,q]; xcommon px^2+qx -> [p,q,0]
        boxes=[st['answer'] for st in p['guided_steps'] if st.get('answer') is not None]
        last2=boxes[-2:]
        if len(coeffs)==2:
            pcoef,qcoef=int(coeffs[0]),int(coeffs[1])
        else:
            pcoef,qcoef=int(coeffs[0]),int(coeffs[1])
        if last2!=[pcoef,qcoef]:
            errs.append(f"bronze[{i}] check boxes {last2} != original coeffs [{pcoef},{qcoef}]")

# Silver: last two check boxes = c then b
for i,p in enumerate(pb['silver']):
    poly=sp.Poly(L2e(p['display']),x).all_coeffs()  # [1,b,c]
    b,c=int(poly[1]),int(poly[2])
    boxes=[st['answer'] for st in p['guided_steps'] if st.get('answer') is not None]
    if boxes[-2:]!=[c,b]:
        errs.append(f"silver[{i}] final check {boxes[-2:]} != [c,b]=[{c},{b}]")
    # first two boxes read off c then b
    if boxes[:2]!=[c,b]:
        errs.append(f"silver[{i}] readoff {boxes[:2]} != [c,b]=[{c},{b}]")

# Gold simple: boxes [k,0,-k^2]; coeff: boxes[a,b,A,0]
for i,p in enumerate(pb['gold']):
    disp=L2e(p['display'])
    poly=sp.Poly(disp,x).all_coeffs()
    boxes=[st['answer'] for st in p['guided_steps'] if st.get('answer') is not None]
    A=int(poly[0]); C=int(poly[-1])  # A x^2 + C  (C negative)
    if A==1:
        k=int(round((-C)**0.5))
        if boxes!=[k,0,-k*k]: errs.append(f"gold[{i}] simple boxes {boxes} != [{k},0,{-k*k}]")
    else:
        a=int(round(A**0.5)); bnum=int(round((-C)**0.5))
        if boxes!=[a,bnum,A,0]: errs.append(f"gold[{i}] coeff boxes {boxes} != [{a},{bnum},{A},0]")

# em dash scan already done by validator; double check no em dash
def scan(o,pth=''):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ('note',): continue
            scan(v,pth+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,pth+f'[{i}]')
    elif isinstance(o,str) and '—' in o:
        errs.append('EMDASH at '+pth)
scan(pd)

if errs:
    print("PROBLEMS:")
    for e in errs: print("  -",e)
else:
    print("ALL CHECKS PASS: maths, boxes, boundaries, expects, opener, teach, no em dash")
