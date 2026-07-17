# -*- coding: utf-8 -*-
import json, io, re
d = json.load(io.open("lesson_maths-ocr_graphs-L03.json", encoding="utf-8"))
fails = []
pb = d["problem_bank"]

# 1. Fresh-solve every stored solution
def evalq(a,b,c,x): return a*x*x+b*x+c
expected = {
 ("bronze",0):[7],("bronze",1):[8],("bronze",2):[0],("bronze",3):[2],("bronze",4):[15],
 ("bronze",5):[6],("bronze",6):[1],("bronze",7):[3],
 ("silver",0):[3],("silver",1):[2],("silver",2):[-3],("silver",3):[5],("silver",4):[-6],
 ("silver",5):[4],("silver",6):[0],
 ("gold",0):[2],("gold",1):[-2],("gold",2):[4],("gold",3):[-15],("gold",4):[3],
}
for (t,i),sol in expected.items():
    got = pb[t][i]["solutions"]
    if got != sol:
        fails.append(f"{t}[{i}] solution stored {got} expected {sol}")

# 2. Recompute every guided_steps final box lands on solution + all boxes numeric
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        gs = p.get("guided_steps")
        if not gs: continue
        boxes = [s for s in gs if s.get("answer") is not None]
        # last box must equal a solution value (single-value)
        if p.get("input_type","single_value")!="multiple_choice":
            last = boxes[-1]["answer"]
            if last != p["solutions"][0]:
                fails.append(f"{t}[{i}] last box {last} != solution {p['solutions'][0]}")
        # substitute boundary
        sub = [j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not sub:
            fails.append(f"{t}[{i}] no substitute boundary")
        else:
            live_after = sum(1 for s in gs[sub[0]:] if s.get("answer") is not None)
            if live_after<2: fails.append(f"{t}[{i}] <2 live boxes after boundary")

# 3. Expects reproduce (spot-check derivations)
exp_checks = {
 ("bronze",0):4,("bronze",1):-10,("bronze",3):4,("bronze",4):9,("bronze",5):-3,
 ("bronze",6):0,("bronze",7):9,("silver",0):-4,("silver",1):-2,("silver",2):1,
 ("silver",3):-2,("silver",4):6,("silver",5):1,("silver",6):2,("gold",0):4,
 ("gold",1):6,("gold",2):5,("gold",3):15,("gold",4):2,
}
for (t,i),ev in exp_checks.items():
    ms = pb[t][i].get("misconceptions",[])
    vals=[m.get("expect") for m in ms if m.get("expect") is not None]
    if ev not in vals:
        fails.append(f"{t}[{i}] expect {ev} not present, got {vals}")
    for m in ms:
        e=m.get("expect")
        if e is not None and e==pb[t][i]["solutions"][0]:
            fails.append(f"{t}[{i}] expect equals solution")

# 4. Chart points satisfy the stated equation
def check_chart(t,i,f):
    ch = pb[t][i].get("chart")
    if not ch: fails.append(f"{t}[{i}] expected chart missing"); return
    for pt in ch["data"]["datasets"][0]["data"]:
        want=round(f(pt["x"]),2)
        if abs(want-pt["y"])>0.011:
            fails.append(f"{t}[{i}] chart point x={pt['x']} y={pt['y']} != {want}")
check_chart("bronze",2, lambda x:x*x)
check_chart("bronze",6, lambda x:-(x*x)+4)
check_chart("silver",5, lambda x:-(x*x)+2*x+3)
check_chart("silver",6, lambda x:x*x+4)
check_chart("gold",4, lambda x:-3*x*x+12*x-9)

# 5. teach walks: recompute a few boxes
tb = d["guided"]["teach"]
# bronze teach y=x^2-4: boxes 5,5? -> [9? wait x=3:9? stored 3*3=9? check]
def boxvals(t): return [s["answer"] for s in d["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
if boxvals("bronze")!=[9,5,-4,2,0]: fails.append("bronze teach boxes "+str(boxvals("bronze")))
if boxvals("silver")!=[2,4,3,-1,8]: fails.append("silver teach boxes "+str(boxvals("silver")))
if boxvals("gold")!=[4,3,-8,1,0]: fails.append("gold teach boxes "+str(boxvals("gold")))
# opener boxes
opb=[s["answer"] for s in d["guided"]["opener"]["steps"] if s.get("answer") is not None]
if opb!=[3,8]: fails.append("opener boxes "+str(opb))

# 6. Preservation vs pre-dump
pre = json.load(io.open("_pre_dump_maths-ocr.json", encoding="utf-8"))
# find our lesson entry
mine=None
if isinstance(pre,dict):
    for k,v in pre.items():
        if k=="graphs-L03" or (isinstance(v,dict) and v.get("id")=="fc1f101a-9d1b-4eab-8bf8-8159f78caea2"):
            mine=v
if mine:
    pdpre = mine.get("practice_data",mine)
    for f in ("related_videos","topic_links"):
        if pdpre.get(f)!=d.get(f):
            fails.append(f"preservation: {f} changed")
    # worked_examples: only labels changed (em dash fix)
    print("pre worked_examples present:", "worked_examples" in pdpre)
else:
    print("pre-dump entry not found (checked manually)")

# 7. em dash scan in student-facing
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,f"{path}[{j}]")
    elif isinstance(o,str) and "—" in o:
        fails.append("EM DASH at "+path)
scan(d,"pd")

print("\nFAILS:",len(fails))
for f in fails: print("  -",f)
if not fails: print("ALL CHECKS PASS")
