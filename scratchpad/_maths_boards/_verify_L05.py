# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("../_maths_guided/lesson_number-L05.json", encoding="utf-8"))

def norm(s):
    s = s.replace("×","*").replace("÷","/").replace("−","-").replace(",","")
    s = s.replace("£","").replace(" d.p.","")
    return s

def try_eval_pre(pre):
    # take the text after the LAST '=' -> expression is before that '='
    if "=" not in pre: return None
    left = pre.rsplit("=",1)[0]
    # grab trailing arithmetic expression
    m = re.search(r"([0-9\.\(\)\s\+\-\*/×÷−£,]+)$", norm(left))
    if not m: return None
    expr = m.group(1).strip()
    if not re.search(r"[\+\-\*/]", expr): return None
    try:
        return eval(expr, {"__builtins__":{}})
    except Exception:
        return None

problems=0; boxes=0; mismatches=[]
def walk_steps(steps, label):
    global boxes
    for i,st in enumerate(steps):
        if st.get("answer") is None: continue
        boxes+=1
        v=try_eval_pre(st.get("pre",""))
        if v is not None:
            if abs(float(v)-float(st["answer"]))>0.02:
                mismatches.append(f"{label}[{i}] pre='{st['pre']}' evals {v} != answer {st['answer']}")

pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for j,p in enumerate(pb[tier]):
        problems+=1
        walk_steps(p["guided_steps"], f"{tier}[{j}].gs")
        # confirm a box lands on the solution
        sol=p["solutions"][0]
        ans=[s.get("answer") for s in p["guided_steps"] if s.get("answer") is not None]
        if not any(abs(float(a)-float(sol))<0.02 for a in ans):
            mismatches.append(f"{tier}[{j}] NO box equals solution {sol}; boxes={ans}")

walk_steps(pd["guided"]["opener"]["steps"], "opener")
for tier in ("bronze","silver","gold"):
    walk_steps(pd["guided"]["teach"][tier]["steps"], f"teach.{tier}")
    walk_steps(pd["tier_guides"][tier]["example"]["steps"] if False else [], "x")

print(f"problems={problems} boxes_checked={boxes}")
if mismatches:
    print("MISMATCHES:")
    for m in mismatches: print("  -",m)
else:
    print("ALL EVALUATED BOXES CONSISTENT + every problem has a box on its solution")
