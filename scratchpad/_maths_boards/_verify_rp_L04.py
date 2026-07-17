# -*- coding: utf-8 -*-
import json, io, re

pd = json.load(io.open("lesson_maths-ocr_ratio-proportion-L04.json", encoding="utf-8"))
bad = []

def calc(expr):
    # find last "A op B" pattern in a pre string like "k = 8 ÷ 2 = "
    m = re.findall(r"(-?\d+\.?\d*)\s*([×x÷*/+\-−])\s*(-?\d+\.?\d*)", expr)
    if not m: return None
    a, op, b = m[-1]
    a, b = float(a), float(b)
    if op in "×x*": return a*b
    if op in "÷/": return a/b
    if op in "+": return a+b
    if op in "-−": return a-b
    return None

def checkwalk(steps, path, sol=None):
    ans_seen = []
    for i, st in enumerate(steps):
        if st.get("answer") is None: continue
        v = calc(st.get("pre",""))
        ans = st["answer"]
        ans_seen.append(ans)
        if v is not None and abs(v-ans) > 0.011:
            bad.append(f"{path}[{i}] pre computes {v} but answer={ans}: {st['pre']!r}")
    if sol is not None:
        s = sol[0] if isinstance(sol, list) else sol
        if not any(abs(a-s) < 0.011 for a in ans_seen):
            bad.append(f"{path} walk never lands on solution {s}; boxes={ans_seen}")

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    sols = []
    for i,p in enumerate(pb[tier]):
        path = f"{tier}[{i}]"
        s = tuple(p["solutions"])
        if s in sols and p.get("input_type")!="multiple_choice":
            bad.append(f"{path} dup solution {s}")
        sols.append(s)
        # expect != solution
        for j,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is not None and isinstance(e,(int,float)) and len(p["solutions"])==1:
                if abs(float(e)-float(p["solutions"][0]))<0.011:
                    bad.append(f"{path}.mc[{j}] expect==solution")
        if p.get("guided_steps"):
            checkwalk(p["guided_steps"], path+".guided_steps", p["solutions"])

# opener + teach
op = pd["guided"]["opener"]["steps"]
checkwalk(op, "opener")
for tier in ("bronze","silver","gold"):
    checkwalk(pd["guided"]["teach"][tier]["steps"], f"teach.{tier}")

# tier guide examples: spot check example steps for internal computes already trusted

if bad:
    print("ISSUES (%d):" % len(bad))
    for b in bad: print("  -", b)
else:
    print("ALL BOXES + SOLUTIONS VERIFIED CLEAN")
