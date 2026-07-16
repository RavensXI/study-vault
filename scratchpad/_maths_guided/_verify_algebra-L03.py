# -*- coding: utf-8 -*-
import json, io, re
import sympy as sp

x = sp.symbols('x')

def latex_to_expr(s):
    # strip \( \)
    s = s.replace('\\(', '').replace('\\)', '').strip()
    # remove "Factorise"
    s = re.sub(r'(?i)factorise', '', s).strip()
    # ^2 -> **2
    s = s.replace('^2', '**2').replace('^{2}', '**2')
    # implicit multiplication: insert * between number/paren and x or (
    # handle things like 3x -> 3*x, 2x**2, (x+5)(x-5), 4x**2
    # sympy sympify with implicit? use transformations
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
    tr = standard_transformations + (implicit_multiplication_application,)
    return parse_expr(s, transformations=tr, local_dict={'x': x})

pd = json.load(io.open('_fresh_L03_pd.json', encoding='utf-8'))
pb = pd['problem_bank']
for tier in ('bronze','silver','gold'):
    print('==== '+tier+' ====')
    for i,p in enumerate(pb[tier]):
        disp = p['display']
        target = sp.expand(latex_to_expr(disp))
        correct_idx = p['solutions'][0]
        matches = []
        exps = []
        for j,opt in enumerate(p['options']):
            try:
                e = sp.expand(latex_to_expr(opt))
            except Exception as ex:
                e = 'ERR:'+str(ex)
            exps.append(e)
            if e == target:
                matches.append(j)
        ok = (matches == [correct_idx])
        print(f"[{i}] {disp}  target={target}")
        print(f"    stored correct={correct_idx}  expand-matches={matches}  {'OK' if ok else '*** MISMATCH ***'}")
        for j,(opt,e) in enumerate(zip(p['options'],exps)):
            print(f"      opt{j}: {opt}  -> {e}")
