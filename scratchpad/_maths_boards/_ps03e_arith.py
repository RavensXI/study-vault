# -*- coding: utf-8 -*-
import json, sys, re
sys.stdout.reconfigure(encoding="utf-8")
shard = json.load(open("_ps03e_shard.json", encoding="utf-8"))
bad=[]
def evalexpr(s):
    s=s.replace("−","-").replace("×","*").replace("÷","/").replace("°","")
    s=s.replace("(","(").replace(")",")")
    try: return eval(s,{"__builtins__":{}})
    except Exception: return None
def scan(steps,path):
    for i,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre=(st.get("pre") or "")
        # find trailing arithmetic "= " ending
        m=re.search(r"([0-9.\s\+\-−×÷\*/\(\)°]+?)\s*=\s*$", pre)
        if not m: continue
        expr=m.group(1).strip()
        # skip if it references a variable like x
        val=evalexpr(expr)
        if val is None: continue
        if abs(float(val)-float(st["answer"]))>0.01:
            bad.append(f"{path}[{i}] '{expr}' = {val} but answer={st['answer']}")
pb=shard["problem_bank"]
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        if p.get("guided_steps"): scan(p["guided_steps"],f"{t}[{i}].gs")
g=shard["guided"]
scan(g["opener"]["steps"],"opener")
for t in ("bronze","silver","gold"):
    scan(g["teach"][t]["steps"],f"teach.{t}")
print("arith mismatches:",len(bad))
for b in bad: print("  -",b)
if not bad: print("ALL EMBEDDED ARITHMETIC CONSISTENT")
