import json
d=json.load(open('_live_L03.json'))
errs=[]
def approx(a,b,t=1e-9):
    return abs(a-b)<=t

# Verify guided_steps boxes evaluate: parse the "pre" arithmetic where it contains "= " at end
import re
def check_box(path, pre, answer):
    # extract last arithmetic expression before trailing '='
    # find pattern like "X op Y = " possibly with words
    m=re.findall(r'([-+]?\d[\d.]*)\s*([×÷+\-])\s*([-+]?\d[\d.]*)\s*=\s*$', pre.strip())
    if not m:
        # maybe form "= A ÷ B = " take last
        m2=re.findall(r'([-+]?\d[\d.]*)\s*([×÷+\-])\s*([-+]?\d[\d.]*)', pre)
        if m2:
            m=[m2[-1]]
    if not m:
        return None
    a,op,b=m[-1]
    a=float(a);b=float(b)
    if op=='×': r=a*b
    elif op=='÷': r=a/b
    elif op=='+': r=a+b
    elif op=='-': r=a-b
    if not approx(r,answer,1e-6):
        errs.append(f"{path}: pre '{pre.strip()}' computes {r} but answer={answer}")
    return r

# walk through guided teach
for tier,walk in d['guided']['teach'].items():
    for i,st in enumerate(walk['steps']):
        if 'answer' in st and 'pre' in st:
            check_box(f"guided.teach.{tier}.steps[{i}]", st['pre'], st['answer'])
# opener
for i,st in enumerate(d['guided']['opener']['steps']):
    if 'answer' in st and 'pre' in st:
        check_box(f"guided.opener.steps[{i}]", st['pre'], st['answer'])
# bank
for tier,probs in d['problem_bank'].items():
    if not isinstance(probs,list): continue
    for pi,p in enumerate(probs):
        for si,st in enumerate(p.get('guided_steps',[])):
            if 'answer' in st and 'pre' in st:
                check_box(f"problem_bank.{tier}[{pi}].guided_steps[{si}]", st['pre'], st['answer'])
print("BOX CHECK errors:", len(errs))
for e in errs: print("  ",e)
