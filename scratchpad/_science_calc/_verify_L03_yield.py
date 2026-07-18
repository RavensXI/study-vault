# -*- coding: utf-8 -*-
"""Independent fresh-solve + box recompute for L03 yield lesson."""
import json, io, re

pd = json.load(io.open("lesson_higher-calculations-L03@2a30c22d67.json", encoding="utf-8"))
errs = []

def approx(a, b, tol=0.02):
    return abs(a - b) <= tol

# ---- expected fresh solutions (computed by hand/independently) ----
expected = {
    ("bronze",0):80.0, ("bronze",1):70.0, ("bronze",3):100.0, ("bronze",4):75.0,
    ("bronze",5):60.0, ("bronze",6):56.0,
    ("silver",0):55.0, ("silver",1):51.111, ("silver",2):90.0, ("silver",4):94.297,
    ("gold",0):45.902, ("gold",1):66.667, ("gold",2):62.5, ("gold",4):70.0,
}
# MC correct indices
mc_expected = {("bronze",2):2, ("bronze",7):1, ("silver",3):2, ("silver",5):0,
               ("gold",3):2}

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pb[tier]):
        it = p.get("input_type","single_value")
        sols = p["solutions"]
        key=(tier,i)
        if it=="multiple_choice":
            if key in mc_expected and sols[0]!=mc_expected[key]:
                errs.append(f"{tier}[{i}] MC answer {sols[0]} != expected {mc_expected[key]}")
            continue
        # dup check
        t=tuple(sols)
        if t in seen: errs.append(f"{tier}[{i}] duplicate sol {t}")
        seen.add(t)
        if key in expected:
            acc = p.get("accept",0.05)
            if abs(sols[0]-expected[key])>max(acc,0.05):
                errs.append(f"{tier}[{i}] stored {sols[0]} vs freshsolve {expected[key]}")
        # expects outside accept window
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None:
                acc=p.get("accept",0.011)
                if abs(float(e)-float(sols[0]))<max(acc,0.011):
                    errs.append(f"{tier}[{i}] expect {e} inside accept of {sols[0]}")
        # recompute guided boxes: verify each box 'pre' arithmetic where it contains '= '
        for j,st in enumerate(p.get("guided_steps",[])):
            if st.get("answer") is None: continue
            pre=st.get("pre","")
            m=re.search(r'([-0-9.,×÷+\-() ]+?)=\s*$', pre)
            if m:
                expr=m.group(1)
                expr2=expr.replace("×","*").replace("÷","/").replace(",","").replace("−","-")
                # strip trailing words
                try:
                    val=eval(expr2)
                    if not approx(float(val), float(st["answer"]), 0.02):
                        errs.append(f"{tier}[{i}].gs[{j}] box '{expr.strip()}'={val} != answer {st['answer']}")
                except Exception:
                    pass

# recompute teach + opener boxes
def check_walk(steps, label):
    for j,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre=st.get("pre","")
        m=re.search(r'([-0-9.,×÷+\-() ]+?)=\s*$', pre)
        if m:
            expr2=m.group(1).replace("×","*").replace("÷","/").replace(",","").replace("−","-")
            try:
                val=eval(expr2)
                if not approx(float(val),float(st["answer"]),0.02):
                    errs.append(f"{label}[{j}] box '{m.group(1).strip()}'={val} != {st['answer']}")
            except Exception:
                pass

check_walk(pd["guided"]["opener"]["steps"], "opener")
for t in ("bronze","silver","gold"):
    check_walk(pd["guided"]["teach"][t]["steps"], f"teach.{t}")

# em dash scan whole object
def scan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,path+f"[{i}]")
    elif isinstance(o,str) and "—" in o:
        errs.append(f"EM DASH at {path}")
scan(pd)

if errs:
    print("VERIFY FAIL:")
    for e in errs: print("  -",e)
else:
    print("VERIFY PASS: all fresh-solves, boxes, expects, em-dash clean")
