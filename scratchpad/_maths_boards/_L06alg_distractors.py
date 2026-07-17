# -*- coding: utf-8 -*-
import json, re
import sympy as sp
x = sp.symbols('x')

def latex_to_expr(s):
    s = s.replace('\\(','').replace('\\)','').strip().replace('^','**')
    s = s.replace('−','-').replace('×','*')
    s = re.sub(r'(\d)\s*([a-zA-Z(])', r'\1*\2', s)
    s = re.sub(r'\)\s*\(', r')*(', s)
    s = re.sub(r'\)\s*([a-zA-Z])', r')*\1', s)
    return sp.sympify(s)

d = json.load(open('_L06alg_live.json', encoding='utf-8'))
pb = d['practice_data']['problem_bank']
for tier in ('bronze','silver','gold'):
    print('==== '+tier.upper()+' ====')
    for i,p in enumerate(pb[tier]):
        disp=p['display']
        m=re.search(r'Factorise(?: completely)?\s+\\\((.+?)\\\)',disp)
        quad=latex_to_expr('\\('+m.group(1)+'\\)')
        c=sp.Poly(quad,x).all_coeffs()  # [a,b,c]
        print(f'{tier}[{i}] {m.group(1)}   a,b,c={c}   ac={c[0]*c[2]}, need sum={c[1]}')
        for j,o in enumerate(p['options']):
            e=sp.expand(latex_to_expr(o))
            mark='<<CORRECT' if j==p['solutions'][0] else ''
            ec=sp.Poly(e,x).all_coeffs() if e.has(x) else e
            eq = '= quad' if sp.simplify(e-quad)==0 else ('mid diff: '+str(sp.Poly(e,x).all_coeffs()))
            print(f'    opt{j}: {o:28s} -> {e}   {mark}')
