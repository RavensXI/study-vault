import json, re
from fractions import Fraction as F
pd=json.load(open("_CHK_algL07ocr_live.json",encoding="utf-8"))

# 1. Em-dash scan in student-facing strings (exclude internal 'note')
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='note': continue
            yield from walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            yield from walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        yield path,o
emd=[(p,s) for p,s in walk(pd) if '—' in s or '–' in s]
print("EM DASHES:", emd if emd else "none")

# 2. Verify every guided_steps final numeric boxes for bank problems land on solutions.
# Collect box answers (skip say-only) and ensure the two "bracket-solve" boxes match solutions,
# and the last check box == 0.
issues=[]
for tier in ['gold','bronze','silver']:
    for i,p in enumerate(pd['problem_bank'][tier]):
        gs=p.get('guided_steps',[])
        boxes=[s for s in gs if 'answer' in s]
        if not boxes: issues.append(f"{tier}[{i}] no boxes"); continue
        last=boxes[-1]
        if last['answer']!=0:
            issues.append(f"{tier}[{i}] last check box answer={last['answer']} (expected 0)")
        # phase count
        pcnt=sum(1 for s in gs if s.get('phase')=='substitute')
        # boxes at/after first phase
        idx=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
        if idx:
            after=[s for s in gs[idx[0]:] if 'answer' in s]
            before=gs[:idx[0]]
            if len(after)<2: issues.append(f"{tier}[{i}] <2 live boxes after boundary ({len(after)})")
            if len(before)<1: issues.append(f"{tier}[{i}] <1 step before boundary")
        else:
            issues.append(f"{tier}[{i}] no phase:substitute boundary")
print("BOX/BOUNDARY ISSUES:", issues if issues else "none")

# 3. Reproduce misconception expects for 'negated' = negation of solutions (as set)
mis=[]
for tier in ['gold','bronze','silver']:
    for i,p in enumerate(pd['problem_bank'][tier]):
        sol=sorted([F(str(x)) for x in p['solutions']])
        for j,m in enumerate(p.get('misconceptions',[])):
            chk=m.get('check'); exp=m.get('expect')
            if chk=='negated':
                neg=sorted([-x for x in sol])
                if exp is None or sorted([F(str(x)) for x in exp])!=neg:
                    mis.append(f"{tier}[{i}].mis[{j}] negated expect={exp} but -roots={[str(x) for x in neg]}")
            if chk=='partial' and exp is not None:
                mis.append(f"{tier}[{i}].mis[{j}] partial should be null, got {exp}")
print("MISCONCEPTION (negated/partial) ISSUES:", mis if mis else "none")
