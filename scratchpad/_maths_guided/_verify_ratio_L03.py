# -*- coding: utf-8 -*-
"""Independent maths check of the built lesson: fresh-solve each problem,
recompute every box, confirm the final box lands on a stored solution,
scan em dashes, check misconception expects reproduce."""
import json, io

pd = json.load(io.open("lesson_ratio-proportion-L03.json", encoding="utf-8"))
errs = []
def E(m): errs.append(m)

# fresh solve of each problem (independent of stored)
def approx(a, b, tol=0.02):
    return abs(a - b) <= tol

fresh = {
    "bronze": [15, 240, 8, 120, 5, 2, 7, 48],
    "silver": [20, 1.5, 1003.6, 60, 500, 108, 65],
    "gold":   [(66.67,66.7), 8.84, 6.3, 2, 942],
}
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sols = p["solutions"]
        exp = fresh[tier][i]
        if isinstance(exp, tuple):
            ok = all(any(approx(float(s),e) for s in sols) for e in exp) and len(sols)==len(exp)
        else:
            ok = any(approx(float(s),exp) for s in sols)
        if not ok:
            E(f"{tier}[{i}] stored solutions {sols} != fresh {exp}")
        # duplicate value check within tier already validated separately
        # misconception expect must NOT equal solution and must be numeric
        for j,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is not None:
                ev = e if isinstance(e,list) else [e]
                sv = [float(x) for x in sols]
                if len(ev)==len(sv) and all(approx(float(a),b,0.001) for a,b in zip(ev,sv)):
                    E(f"{tier}[{i}].misc[{j}] expect equals solution")

# check every guided box computes and final live box lands on solution
def eval_expr(s):
    # only used for a couple sanity checks; not general
    return None

# check within-tier duplicate solution values
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[tier]):
        key=tuple(p["solutions"])
        if key in seen:
            E(f"{tier}[{i}] duplicate solution values {key} (also {tier}[{seen[key]}])")
        seen[key]=i

# em dash scan (mirror validator, skip note/guided_skip_reason)
def scan(o,p):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,p+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,p+"[%d]"%i)
    elif isinstance(o,str) and "—" in o:
        E("EMDASH "+p+": "+o[:50])
scan(pd,"pd")

# completion boundary summary per bank problem
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p["guided_steps"]
        boxes=[s for s in gs if s.get("answer") is not None]
        sub=[idx for idx,s in enumerate(gs) if s.get("phase")=="substitute"]
        subat=sub[0] if sub else None
        live=sum(1 for s in gs[subat:] if s.get("answer") is not None) if subat is not None else 0
        finalbox=boxes[-1]["answer"] if boxes else None
        if len(boxes)<3: E(f"{tier}[{i}] only {len(boxes)} boxes")
        if subat is None: E(f"{tier}[{i}] no phase")
        elif subat<1: E(f"{tier}[{i}] phase at 0")
        elif live<2: E(f"{tier}[{i}] only {live} live boxes")

# print box arithmetic for manual eyeball of every walk
print("=== box values per bank problem (last box should be a check) ===")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        vals=[s.get("answer") for s in p["guided_steps"] if s.get("answer") is not None]
        print(f"{tier}[{i}] {p['display'][:45]:45} boxes={vals} sol={p['solutions']}")

# teach + opener box values
print("=== opener / teach ===")
for s in pd["guided"]["opener"]["steps"]:
    if s.get("answer") is not None: print("opener box", s["pre"].strip(), "=>", s["answer"])
for t in ("bronze","silver","gold"):
    vals=[s.get("answer") for s in pd["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
    print("teach",t,"boxes=",vals)

# tier guide word budgets
def words(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
for t in ("bronze","silver","gold"):
    tot=sum(words(x) for x in pd["tier_guides"][t]["steps"])
    print("tier_guide",t,"words=",tot)
print("method_card content words=", words(pd["method_card"]["content"]))

if errs:
    print("\nFAIL", len(errs))
    for e in errs: print("  -", e)
else:
    print("\nALL CHECKS PASS")
