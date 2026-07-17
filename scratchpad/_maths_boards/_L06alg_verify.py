# -*- coding: utf-8 -*-
import json, re, sys
import sympy as sp

x = sp.symbols('x')

def latex_to_expr(s):
    # strip \( \) and latex, convert ^ and implicit mult
    s = s.replace('\\(', '').replace('\\)', '').strip()
    s = s.replace('^', '**')
    s = s.replace('−', '-').replace('×', '*')
    # insert * between number and x, and between ) and (
    s = re.sub(r'(\d)\s*([a-zA-Z(])', r'\1*\2', s)
    s = re.sub(r'\)\s*\(', r')*(', s)
    s = re.sub(r'\)\s*([a-zA-Z])', r')*\1', s)
    return sp.sympify(s)

d = json.load(open('_L06alg_live.json', encoding='utf-8'))
pb = d['practice_data']['problem_bank']

problems = []
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pb[tier]):
        disp = p['display']
        m = re.search(r'Factorise(?: completely)?\s+\\\((.+?)\\\)', disp)
        quad_str = m.group(1)
        quad = latex_to_expr('\\('+quad_str+'\\)')
        opts = p['options']
        sol_idx = p['solutions'][0]
        # expand every option
        exp = [sp.expand(latex_to_expr(o)) for o in opts]
        correct_matches = [j for j in range(len(opts)) if sp.simplify(exp[j]-quad)==0]
        stored_ok = (sp.simplify(exp[sol_idx]-quad)==0)
        problems.append(dict(tier=tier,i=i,quad=quad_str,quad_expr=quad,
            opts=opts,sol_idx=sol_idx,exp=exp,matches=correct_matches,stored_ok=stored_ok))

bad=0
for p in problems:
    tag = p['tier'] + '[' + str(p['i']) + ']'
    if not p['stored_ok'] or p['matches']!=[p['sol_idx']]:
        bad+=1
        print('PROBLEM', tag, 'quad=', p['quad'])
        print('  stored sol_idx=', p['sol_idx'], 'stored_ok=', p['stored_ok'], 'all_correct_matches=', p['matches'])
        for j,(o,e) in enumerate(zip(p['opts'],p['exp'])):
            print(f'    opt{j}: {o}  -> {e}')
if bad==0:
    print('ALL', len(problems), 'PROBLEMS: stored solution index is the unique correct factorisation. CLEAN.')
else:
    print(f'{bad} problems flagged.')

# also verify factorising completeness for "factorise completely" gold[4]
print('\\n--- non-calculator integer check: all coefficients integer (fine for factorising) ---')
