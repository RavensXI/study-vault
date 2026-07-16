# -*- coding: utf-8 -*-
import json, re
live=json.load(open("_CHK_graphsL02_live.json",encoding="utf-8"))
mism=[]

def norm(s):
    s=s.replace("−","-").replace("×","*").replace("÷","/").replace("½","0.5")
    return s

def try_eval(pre):
    # find an arithmetic expression before '='
    p=norm(pre)
    # take substring up to last '=' that has an operator
    # grab pattern like "... : EXPR = " -> EXPR is last chunk before '='
    if "=" not in p: return None
    left=p.split("=")[0]
    # extract trailing arithmetic: keep only chars in number/operator set, from the right
    m=re.findall(r'[-+*/(). 0-9]+$', left)
    if not m: return None
    expr=m[0].strip().strip(':').strip()
    # must contain an operator between numbers
    if not re.search(r'\d\s*[-+*/]\s*\(?-?\d', expr): return None
    try:
        return eval(expr)
    except Exception:
        return None

for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        for j,s in enumerate(p.get("guided_steps",[])):
            if "answer" not in s: continue
            v=try_eval(s.get("pre",""))
            if v is not None and abs(v-s["answer"])>1e-9:
                mism.append(f"{tier}[{i}].guided_steps[{j}] pre={s['pre']!r} eval={v} answer={s['answer']}")
# teach + opener
for tier,w in live["guided"]["teach"].items():
    for j,s in enumerate(w["steps"]):
        if "answer" not in s: continue
        v=try_eval(s.get("pre",""))
        if v is not None and abs(v-s["answer"])>1e-9:
            mism.append(f"teach.{tier}[{j}] pre={s['pre']!r} eval={v} answer={s['answer']}")
for j,s in enumerate(live["guided"]["opener"]["steps"]):
    if "answer" not in s: continue
    v=try_eval(s.get("pre",""))
    if v is not None and abs(v-s["answer"])>1e-9:
        mism.append(f"opener[{j}] pre={s['pre']!r} eval={v} answer={s['answer']}")

print("arithmetic mismatches:", len(mism))
for m in mism: print("  ",m)

# final box lands on solution check
print("\n--- final answer box vs stored solution ---")
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        gs=p.get("guided_steps",[])
        # find the 'c' or 'm' answer box (not the check). The solution box is the one whose pre mentions 'c =' or 'm ='
        solbox=[s for s in gs if "answer" in s and re.search(r'(so\s+c\s*=|=\s*m\s*=|m\s*=\s*$|c,\s*so\s*c\s*=)', norm(s.get("pre","")))]
        stored=p["solutions"][0]
        hit=any(abs(s["answer"]-stored)<1e-9 for s in gs if "answer" in s)
        print(f"{tier}[{i}] stored={stored} present_in_boxes={hit}")
