# -*- coding: utf-8 -*-
import json, re
import sympy as sp

x = sp.symbols('x')
d = json.load(open('_CHK_L06_live.json', encoding='utf-8'))
pd = d['practice_data']

def parse(tex):
    # strip \( \)
    s = tex.replace('\\(', '').replace('\\)', '').strip()
    s = s.replace('^', '**')
    # insert * between number/paren and x or (
    s = re.sub(r'(\d)([x(])', r'\1*\2', s)
    s = re.sub(r'\)\(', r')*(', s)
    s = re.sub(r'([x\)])(\()', r'\1*\2', s)
    s = s.replace('−', '-')
    return sp.expand(sp.sympify(s))

problems = 0
fails = 0
for t in ['bronze', 'silver', 'gold']:
    for i, p in enumerate(pd['problem_bank'][t]):
        problems += 1
        target = parse(p['display'].split('Factorise')[-1])
        opts = [parse(o) for o in p['options']]
        sol = p['solutions'][0]
        # exactly one option equals target?
        matches = [j for j, o in enumerate(opts) if sp.simplify(o - target) == 0]
        ok_sol = (matches == [sol])
        # duplicate expansions?
        dups = []
        for a in range(len(opts)):
            for b in range(a+1, len(opts)):
                if sp.simplify(opts[a]-opts[b]) == 0:
                    dups.append((a, b))
        status = 'OK'
        if not ok_sol:
            status = f'SOL-FAIL matches={matches} stored={sol}'; fails += 1
        if dups:
            status += f' DUP{dups}'; fails += 1
        # verify each expect option is genuinely != target (wrong)
        exp_bad = []
        for m in p.get('misconceptions', []):
            e = m.get('expect')
            if isinstance(e, int) and 0 <= e < len(opts):
                if sp.simplify(opts[e]-target) == 0:
                    exp_bad.append(e)
        if exp_bad:
            status += f' EXPECT-IS-CORRECT{exp_bad}'; fails += 1
        print(f'{t}[{i}] target={target} sol_opt={p["options"][sol]} -> {status}')

print(f'\nproblems={problems} fails={fails}')
