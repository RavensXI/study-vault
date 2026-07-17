# -*- coding: utf-8 -*-
import json, re, sympy as sp

x, y, a, p, q = sp.symbols('x y a p q')
LOC = {'x': x, 'y': y, 'a': a, 'p': p, 'q': q}
live = json.load(open('_live_ocr_algL03.json', encoding='utf-8'))

def latex2expr(s):
    s = s.replace('\\(', '').replace('\\)', '')
    s = s.strip()
    s = s.replace('^', '**')
    s = re.sub(r'(\d)([a-z(])', r'\1*\2', s)   # 6x -> 6*x, 3( -> 3*(
    s = re.sub(r'([a-z])\(', r'\1*(', s)        # x( -> x*(
    s = re.sub(r'\)\(', r')*(', s)              # )( -> )*(
    s = re.sub(r'([a-z])([a-z])', r'\1*\2', s)  # xy -> x*y
    return sp.sympify(s, locals=LOC)

fails = []
for tier in ('bronze', 'silver', 'gold'):
    for i, pr in enumerate(live['problem_bank'][tier]):
        disp = pr['display']
        m = re.search(r'\\\((.+?)\\\)', disp)
        target = sp.expand(latex2expr(m.group(1)))
        cidx = pr['solutions'][0]
        exp = [sp.expand(latex2expr(o)) == target for o in pr['options']]
        okc = exp[cidx]
        ndupe = sum(exp)
        flag = ''
        if not okc:
            flag += ' !CORRECT_DOESNT_EXPAND'
            fails.append((tier, i, 'correct option does not expand to target'))
        if ndupe > 1:
            # only a defect if a NON-correct option is a FULL factorisation too
            flag += ' MULTI_EXPAND=%d' % ndupe
        print(tier, i, m.group(1), '-> correctExpands=%s dupes=%d%s' % (okc, ndupe, flag))
print('---FAILS---', fails)
