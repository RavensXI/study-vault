# -*- coding: utf-8 -*-
"""Independent adversarial fresh-solve of the final shard."""
import json, io
from math import gcd
pd = json.load(io.open("lesson_maths-ocr_ratio-proportion-L01.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# fresh solvers keyed by display fragment
def solve(disp):
    d = disp
    if d.startswith("Simplify"):
        import re
        a,b = map(int, re.findall(r"\d+", d.split(".")[0])[:2])
        g = gcd(a,b); return a//g
    return None

expected = {
 ("bronze",0):3,("bronze",1):4,("bronze",2):40,("bronze",3):18,("bronze",4):2,
 ("bronze",5):300,("bronze",6):5,("bronze",7):60,
 ("silver",0):180,("silver",1):75,("silver",2):56,("silver",3):2.5,("silver",4):1500,
 ("silver",5):100,("silver",6):750,
 ("gold",0):84,("gold",1):8,("gold",2):2,("gold",3):15,("gold",4):1,
}
for tier in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pb[tier]):
        sol = p["solutions"]
        if tuple(sol) in seen:
            errs.append("%s[%d] DUP solution %r"%(tier,i,sol))
        seen.add(tuple(sol))
        exp = expected[(tier,i)]
        if abs(sol[0]-exp) > 1e-9:
            errs.append("%s[%d] solution %r != fresh %r :: %s"%(tier,i,sol,exp,p["display"]))
        # simplify problems: verify via gcd
        s = solve(p["display"])
        if s is not None and s != sol[0]:
            errs.append("%s[%d] simplify recompute %r != %r"%(tier,i,s,sol[0]))
        # walk lands on solution
        vals=[st["answer"] for st in (p.get("guided_steps") or []) if st.get("answer") is not None]
        if sol[0] not in vals:
            errs.append("%s[%d] walk %r missing sol %r"%(tier,i,vals,sol[0]))
        # expect != sol, and present
        for j,m in enumerate(p.get("misconceptions",[])):
            if "expect" not in m: errs.append("%s[%d].mis[%d] no expect"%(tier,i,j))
            elif m["expect"]==sol[0]: errs.append("%s[%d].mis[%d] expect==sol"%(tier,i,j))

# teach walks land correctly
teach_expect={"bronze":30,"silver":48,"gold":100}
for t,tw in pd["guided"]["teach"].items():
    vals=[s["answer"] for s in tw["steps"] if s.get("answer") is not None]
    if teach_expect[t] not in vals:
        errs.append("teach.%s missing target %r in %r"%(t,teach_expect[t],vals))
    if sum(1 for s in tw["steps"] if s.get("answer") is not None)<4:
        errs.append("teach.%s <4 boxes"%t)

# em dash sweep on student-facing (already validated) + word budgets sanity
for t,g in pd["tier_guides"].items():
    w=sum(len(s.split()) for s in g["steps"])
    if w>115: errs.append("tier_guides.%s %d words"%(t,w))

print("ERRORS:", len(errs))
for e in errs: print("  -",e)
if not errs: print("INDEPENDENT CHECK CLEAN")
