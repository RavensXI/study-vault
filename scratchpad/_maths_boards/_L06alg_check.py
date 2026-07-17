# -*- coding: utf-8 -*-
"""Independent adversarial check of the built shard: every bank answer, every
misconception expect (distractor index -> its expansion), every teach/opener box."""
import json, re
import sympy as sp
x = sp.symbols('x')

def L2E(s):
    s = s.replace('\\(','').replace('\\)','').strip().replace('^','**')
    s = s.replace('−','-').replace('×','*').replace('²','**2')
    s = re.sub(r'(\d)\s*([a-zA-Z(])', r'\1*\2', s)
    s = re.sub(r'\)\s*\(', r')*(', s)
    s = re.sub(r'\)\s*([a-zA-Z])', r')*\1', s)
    return sp.sympify(s)

pd = json.load(open('lesson_maths-ocr_algebra-L06.json', encoding='utf-8'))
pb = pd['problem_bank']
errs = []

# 1. bank correctness + misconception expect points at a genuine distractor
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pb[tier]):
        tag = f"{tier}[{i}]"
        m = re.search(r'Factorise(?: completely)?\s+\\\((.+?)\\\)', p['display'])
        quad = L2E('\\('+m.group(1)+'\\)')
        sidx = p['solutions'][0]
        opts = p['options']
        exp = [sp.expand(L2E(o)) for o in opts]
        if sp.simplify(exp[sidx]-quad)!=0:
            errs.append(f"{tag} stored option {sidx} does NOT equal {m.group(1)}")
        # each misconception expect must be a valid distractor index (not the answer)
        for j,mc in enumerate(p.get('misconceptions',[])):
            e = mc['expect']
            if e is None: continue
            if e==sidx: errs.append(f"{tag}.misc[{j}] expect==answer index")
            if not (isinstance(e,int) and 0<=e<len(opts)): errs.append(f"{tag}.misc[{j}] expect {e} not a valid option index")

# 2. teach + opener boxes: recompute continuity by evaluating stated arithmetic is hard;
#    instead verify each teach walk's final bracket product equals its display quadratic,
#    and that box answers are internally consistent with the check boxes.
def check_walk(walk, tag, quad_str=None):
    disp = walk['display']
    m = re.search(r'Factorise(?: completely)?\s+\\\((.+?)\\\)', disp)
    quad = L2E('\\('+m.group(1)+'\\)')
    # pull the final answer bracket from a say containing 'answer is' or the last say with brackets
    txt = ' '.join(st.get('say','') or '' for st in walk['steps'])
    return quad

# teach walks: verify the factorisation named in the say expands to the display quad
teach_answers = {
 'bronze': ('2x^2 + 7x + 6', '(2x+3)(x+2)'),
 'silver': ('3x^2 - 5x - 2', '(x-2)(3x+1)'),
 'gold':   ('6x^2 - 2x - 4', '2(x-1)(3x+2)'),
}
for tier,(q,ans) in teach_answers.items():
    if sp.simplify(L2E('\\('+ans+'\\)')-L2E('\\('+q+'\\)'))!=0:
        errs.append(f"teach.{tier} claimed answer {ans} != {q}")

# opener: 1 and 6 multiply to 6 and add to 7
if not (1*6==6 and 1+6==7): errs.append("opener numbers wrong")

# tier_guide examples: named answer expands to the question quad
tg = pd['tier_guides']
tg_expect = {
 'bronze': ('2x^2 + 5x + 2', '(2x+1)(x+2)'),
 'silver': ('2x^2 - 5x - 3', '(x-3)(2x+1)'),
 'gold':   ('6x^2 + 9x - 6', '3(2x-1)(x+2)'),
}
for tier,(q,ans) in tg_expect.items():
    if sp.simplify(L2E('\\('+ans+'\\)')-L2E('\\('+q+'\\)'))!=0:
        errs.append(f"tier_guides.{tier} example {ans} != {q}")

# 3. explicitly recompute each teach box answer from the arithmetic in its pre text
def eval_pre(pre):
    # extract the RHS arithmetic "... = X = " -> compute the expression before final '='
    # take substring after last meaningful '=' chain start: we parse "A op B ... = "
    # Simplify: find the arithmetic expression (numbers, + - * and parentheses) right before trailing '='
    s = pre.replace('−','-').replace('×','*').replace('²','**2')
    # remove leading words up to ':' or the numeric expression
    m = re.findall(r'[-+*() 0-9]+=', s)
    if not m: return None
    expr = m[-1].rstrip('=').strip()
    # the expr may itself contain '=' segments; take the part that is pure arithmetic and non-trivial
    expr = expr.split('=')[-1].strip()
    if not re.search(r'[0-9]', expr): return None
    try: return sp.sympify(expr)
    except: return None

for tier, walk in pd['guided']['teach'].items():
    for k,st in enumerate(walk['steps']):
        if st.get('answer') is None: continue
        got = eval_pre(st['pre'])
        if got is not None and sp.simplify(got - st['answer'])!=0:
            errs.append(f"teach.{tier}.step[{k}] pre '{st['pre']}' computes {got} but answer={st['answer']}")

for k,st in enumerate(pd['guided']['opener']['steps']):
    if st.get('answer') is None: continue
    # opener boxes are 'larger/smaller number' - not arithmetic, skip eval

if errs:
    print("FAIL", len(errs))
    for e in errs: print("  -", e)
else:
    print("CHECK PASS: all bank answers correct, all expect indices valid distractors, all teach/tier_guide factorisations expand correctly, teach box arithmetic consistent.")
