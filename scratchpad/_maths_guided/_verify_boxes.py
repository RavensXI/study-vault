# -*- coding: utf-8 -*-
import json, io, re
d = json.load(io.open("lesson_number-L04.json", encoding="utf-8"))

def norm(expr):
    expr=expr.replace("×","*").replace("÷","/").replace("−","-")
    return expr

def try_eval_pre(pre, ans):
    # find trailing arithmetic before final "= "
    # take substring after last ':' or start, look for pattern like "A op B [op C] = "
    if "= " not in pre and not pre.rstrip().endswith("="): return None
    seg = pre
    # get the chunk right before the final =
    m = re.search(r'([0-9\.\s\*\+\-/×÷−\(\)]+)=\s*$', norm(seg))
    if not m: return None
    e = m.group(1).strip()
    # must contain an operator to be a real computation
    if not re.search(r'[\*\+\-/]', e): return None
    try:
        val = eval(e, {"__builtins__":{}})
    except Exception:
        return None
    return val

issues=0; checked=0
def walk(steps, label):
    global issues, checked
    for j,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre=st.get("pre","")
        v=try_eval_pre(pre, st["answer"])
        if v is None: continue
        checked+=1
        if abs(v-st["answer"])>1e-9:
            issues+=1; print(f"BOX ARITH MISMATCH {label}[{j}] pre={pre!r} eval={v} answer={st['answer']}")

pb=d["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        walk(p["guided_steps"], f"{tier}[{i}].gs")
for tier in ["bronze","silver","gold"]:
    walk(d["guided"]["teach"][tier]["steps"], f"teach.{tier}")
walk(d["guided"]["opener"]["steps"], "opener")
print(f"checked {checked} computable boxes, {issues} mismatches")
