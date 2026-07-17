# -*- coding: utf-8 -*-
import json, re
pd = json.load(open("lesson_maths-aqa_ratio-proportion-L04.json", encoding="utf-8"))
bad = []
def calc(pre):
    # parse "a OP b = " where OP in + - x/× ÷ /
    m = re.search(r'(-?\d+\.?\d*)\s*([+−×÷*/x-])\s*(-?\d+\.?\d*)\s*=', pre)
    if not m: return None
    a, op, b = float(m.group(1)), m.group(2), float(m.group(3))
    if op in "+": return a+b
    if op in "−-": return a-b
    if op in "×*x": return a*b
    if op in "÷/": return a/b
    return None
def check_walk(steps, path, sol=None):
    last=None
    for i,st in enumerate(steps):
        if st.get("answer") is None: continue
        exp=calc(st.get("pre",""))
        ans=st["answer"]
        if exp is not None and abs(exp-ans)>1e-6:
            bad.append("%s[%d] pre '%s' computes %s but answer=%s"%(path,i,st['pre'].strip(),exp,ans))
        last=ans
    if sol is not None:
        # some final box is a check; the SOLVE box should equal sol somewhere
        vals=[s["answer"] for s in steps if s.get("answer") is not None]
        if sol not in [round(v,6) for v in vals] and float(sol) not in vals:
            bad.append("%s solution %s not hit by any box %s"%(path,sol,vals))

pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0] if p.get("input_type")!="multiple_choice" else None
        if p.get("guided_steps"):
            check_walk(p["guided_steps"], "%s[%d].gs"%(tier,i), sol)
        # expect != solution
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is not None and p.get("input_type")!="multiple_choice" and isinstance(e,(int,float)):
                if abs(float(e)-float(p["solutions"][0]))<1e-6:
                    bad.append("%s[%d].misc[%d] expect==solution"%(tier,i,j))
# opener + teach
check_walk(pd["guided"]["opener"]["steps"], "opener")
for t in ("bronze","silver","gold"):
    check_walk(pd["guided"]["teach"][t]["steps"], "teach."+t)

# em dash sweep already by validator; double-check unicode minus not em
if bad:
    print("DEFECTS:")
    for b in bad: print("  -",b)
else:
    print("ALL BOX ARITHMETIC OK; all solutions hit; no expect==solution")
