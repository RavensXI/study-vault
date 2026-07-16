# -*- coding: utf-8 -*-
import json, io, re

pd = json.load(io.open('lesson_graphs-L01.json', encoding='utf-8'))
problems_ok = True

def norm(s):
    return (s.replace("−","-").replace("×","*").replace("÷","/")
             .replace("½","(1/2)").replace("¼","(1/4)"))

def try_eval(pre):
    # take text before the trailing '='
    if "=" not in pre: return None
    expr = pre.rsplit("=",1)[0]
    # only keep if it looks purely arithmetic
    e = norm(expr).strip()
    e2 = e.replace(" ","")
    if not re.fullmatch(r"[0-9\.\+\-\*/\(\)]+", e2):
        return None
    # handle patterns like '0.5*6' from '½ × 6'
    try:
        return eval(e2)
    except Exception:
        return None

def check_steps(steps, label):
    global problems_ok
    for i, st in enumerate(steps):
        if st.get("answer") is None:
            continue
        pre = st.get("pre","")
        val = try_eval(pre)
        if val is not None:
            if abs(val - st["answer"]) > 1e-9:
                print("MISMATCH %s[%d]: pre=%r eval=%s answer=%s" % (label,i,pre,val,st["answer"]))
                problems_ok = False
        else:
            print("  (manual) %s[%d]: pre=%r answer=%s" % (label,i,pre,st["answer"]))

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for j,p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        if gs:
            check_steps(gs, "%s[%d]" % (tier,j))
            # final live box(es) should include the solution somewhere
        # last-arith landing check done above

print("--- OPENER ---")
check_steps(pd["guided"]["opener"]["steps"], "opener")
for t in ("bronze","silver","gold"):
    print("--- TEACH %s ---" % t)
    check_steps(pd["guided"]["teach"][t]["steps"], "teach."+t)

print("problems_ok:", problems_ok)
