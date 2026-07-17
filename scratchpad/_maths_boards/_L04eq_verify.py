# -*- coding: utf-8 -*-
import json, io, math
pd = json.load(io.open("lesson_maths-eduqas_algebra-L04.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# Independent fresh-solve of every bank problem
def solve():
    R = {}
    R[("bronze",0)] = [3*4+2]
    R[("bronze",1)] = [2*7+2*3]
    R[("bronze",2)] = [3**2+1]
    R[("bronze",3)] = [5*(-2)-3]
    R[("bronze",4)] = [6*9]
    R[("bronze",5)] = [2*5**2]
    R[("bronze",6)] = [10+2*3]
    R[("bronze",7)] = [6**2-4*6]
    R[("silver",0)] = [(-4)**2+3*(-4)-5]
    R[("silver",4)] = [(7+3)/2]
    R[("silver",5)] = [0.5*4*5**2]
    R[("silver",6)] = [5*(68-32)/9]
    return R
expected = solve()
for (tier,i),val in expected.items():
    stored = pb[tier][i]["solutions"]
    if [float(x) for x in stored] != [float(x) for x in val]:
        errs.append(f"SOLUTION {tier}[{i}] stored={stored} recomputed={val}")

# MC option-0 correctness (symbolic, checked by hand -> assert index)
for tier in ("silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")=="multiple_choice" and p["solutions"]!=[0]:
            errs.append(f"MC {tier}[{i}] solutions!=[0]: {p['solutions']}")

# Verify each guided_steps chain lands on the stored solution, boxes numeric, continuity of check
def check_walk(tier,i,p):
    gs = p.get("guided_steps")
    if not gs: return
    boxvals = [s["answer"] for s in gs if s.get("answer") is not None]
    # final answer box should equal solution (the 'done' answer step). We check the
    # main-answer box (the step whose done confirms y=... or the last non-check).
    sol = float(p["solutions"][0])
    if sol not in [float(b) for b in boxvals]:
        errs.append(f"WALK {tier}[{i}] solution {sol} not among box values {boxvals}")

for tier in ("bronze","silver"):
    for i,p in enumerate(pb[tier]):
        check_walk(tier,i,p)

# Recompute each box arithmetic literally from its pre text where it's "a OP b = "
import re
def literal(pre):
    # parse patterns like "3 × 4 = " ,  "10 + 2 = ", "(−4) × (−4) = "
    t = pre.replace("−","-").replace("×","*").replace("÷","/")
    m = re.search(r"([-−()0-9.\s*/+]+)=\s*$", t)
    if not m: return None
    expr = m.group(1).strip()
    # guard: only simple arithmetic tokens
    if not re.fullmatch(r"[-()0-9.\s*/+]+", expr): return None
    try:
        return eval(expr)
    except Exception:
        return None

def recompute_boxes(label, steps, tier=None, i=None):
    for j,s in enumerate(steps):
        if s.get("answer") is None: continue
        v = literal(s.get("pre",""))
        if v is not None:
            if abs(float(v)-float(s["answer"]))>1e-9:
                errs.append(f"BOX {label}[{j}] pre='{s['pre']}' evals {v} but answer={s['answer']}")

for tier in ("bronze","silver"):
    for i,p in enumerate(pb[tier]):
        if p.get("guided_steps"):
            recompute_boxes(f"{tier}[{i}].gs", p["guided_steps"])
recompute_boxes("opener", pd["guided"]["opener"]["steps"])
for t in ("bronze","silver","gold"):
    recompute_boxes(f"teach.{t}", pd["guided"]["teach"][t]["steps"])

# Verify misconception expects != solution and are present
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=[float(x) for x in p["solutions"]]
        for k,m in enumerate(p.get("misconceptions",[])):
            if "expect" not in m: errs.append(f"EXPECT missing {tier}[{i}][{k}]")
            e=m.get("expect")
            if e is not None:
                ev=[float(e)] if not isinstance(e,list) else [float(x) for x in e]
                if len(ev)==len(sol) and all(abs(a-b)<0.011 for a,b in zip(ev,sol)):
                    errs.append(f"EXPECT==solution {tier}[{i}][{k}]")

# duplicate solutions within tier (non-MC)
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")=="multiple_choice": continue
        key=tuple(p["solutions"])
        if key in seen: errs.append(f"DUP {tier}[{i}] {key} same as [{seen[key]}]")
        seen[key]=i

if errs:
    print("FAILURES:")
    for e in errs: print("  -",e)
else:
    print("ALL CHECKS PASS: solutions, walk chains, box arithmetic, expects, no dups")
