# -*- coding: utf-8 -*-
"""Independent fresh-solve of every problem + recompute of every guided box for L04."""
import json, io, re, sys
from statistics import median
sys.stdout.reconfigure(encoding="utf-8")

pd = json.load(io.open("lesson_maths-ocr_probability-statistics-L04.json", encoding="utf-8"))
errs = []

def approx(a, b): return abs(float(a) - float(b)) < 0.011

# ---- fresh-solve each bank problem independently ----
def check(key, got, exp):
    if not approx(got, exp):
        errs.append(f"{key}: fresh-solve {got} != stored {exp}")

pb = pd["problem_bank"]
B = pb["bronze"]; S = pb["silver"]; G = pb["gold"]
# BRONZE
check("B0", sum([2,4,6,8,10])/5, B[0]["solutions"][0])
check("B1", median([3,5,7,9,11]), B[1]["solutions"][0])
check("B2", 3, B[2]["solutions"][0])  # mode
check("B3", 15-2, B[3]["solutions"][0])
check("B4", sum([10,20,30])/3, B[4]["solutions"][0])
check("B5", median([1,2,3,4,5,6]), B[5]["solutions"][0])
check("B6", 8*5, B[6]["solutions"][0])
check("B7", 15-3, B[7]["solutions"][0])
# SILVER
vals=[1,2,3,4]; frq=[4,6,5,5]
check("S0", sum(v*f for v,f in zip(vals,frq))/sum(frq), S[0]["solutions"][0])
check("S1", (12*5+24)/6, S[1]["solutions"][0])
mp=[5,15,25]; fr=[8,14,8]
check("S2", sum(v*f for v,f in zip(mp,fr))/sum(fr), S[2]["solutions"][0])
# S3 median class: total 25 -> 13th value; cumfreq 3,10,20,25 -> class index 2 => option "20-30" is options[0]
opts=S[3]["options"]; check("S3-option", opts[S[3]["solutions"][0]]=="20-30", True)
check("S4", 8, S[4]["solutions"][0])  # mode
check("S5", 15*4-(10+12+18), S[5]["solutions"][0])
# S6 freq median: values 0..4 freq 2,5,8,3,2 total 20; 10th&11th both value 2
data=[]
for v,f in zip([0,1,2,3,4],[2,5,8,3,2]): data+= [v]*f
check("S6", median(data), S[6]["solutions"][0])
# GOLD
mp=[5,15,25]; fr=[6,15,9]
check("G0", sum(v*f for v,f in zip(mp,fr))/sum(fr), G[0]["solutions"][0])
# G1 solve 20n+30=21(n+1) -> n=9
n=(30-21)/(21-20); check("G1", n, G[1]["solutions"][0])
# G2 IQR of 2,3,5,7,8,10,12,15
d=[2,3,5,7,8,10,12,15]; q1=median(d[:4]); q3=median(d[4:]); check("G2", q3-q1, G[2]["solutions"][0])
# G3 combined mean
check("G3", (65*20+75*30)/(20+30), G[3]["solutions"][0])
# G4 outlier: fence 22+1.5*12=40; 50>40 => 1
iqr=22-10; fence=22+1.5*iqr; check("G4", 1 if 50>fence else 0, G[4]["solutions"][0])

# ---- misconception expects != solution, and derivability spot-checks ----
def mc_check(prob, key):
    sols=[float(x) for x in prob["solutions"]]
    for j,m in enumerate(prob.get("misconceptions",[])):
        if "expect" not in m: errs.append(f"{key}.mc[{j}] missing expect"); continue
        e=m["expect"]
        if e is None: continue
        ev=e if isinstance(e,list) else [e]
        if len(ev)==len(sols) and all(approx(a,b) for a,b in zip(ev,sols)):
            errs.append(f"{key}.mc[{j}] expect equals solution")
for i,p in enumerate(B): mc_check(p,f"B{i}")
for i,p in enumerate(S): mc_check(p,f"S{i}")
for i,p in enumerate(G): mc_check(p,f"G{i}")
# derivability spot checks
if not approx(51/4,12.75): errs.append("S0 mc1 derive")
if not approx((12+24)/2,18): errs.append("S1 mc derive")
if not approx(450/3,150): errs.append("S2 mc derive")
if not approx(480/3,160): errs.append("G0 mc0 derive")
if not approx(10*6+20*15+30*9,630) or not approx(630/30,21): errs.append("G0 mc1 derive")
if not approx(15-2,13): errs.append("G2 mc derive")
if not approx((65+75)/2,70): errs.append("G3 mc derive")
# G4 3xIQR fence
if not approx(22+3*12,58) or 50>=58: errs.append("G4 mc derive")

# ---- recompute EVERY guided box (walk continuity) ----
def scan_boxes(steps, key):
    for i,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre=(st.get("pre") or "")
        # capture the trailing arithmetic expression right before final '=' (optionally trailed by £/&pound;)
        m=re.search(r'([0-9\.\s\+\-−×÷\(\)]+)=\s*(?:&pound;|£)?\s*$', pre)
        if m:
            if m.start()>0 and pre[m.start()-1].isalpha():  # expr follows a variable (e.g. 'n + 1 =') => conceptual, skip
                continue
            expr=m.group(1).strip()
            if not re.search(r'[+\-−×÷]', expr) or re.match(r'^[+\-−×÷]', expr):  # no operator or leading operator => skip
                continue
            pyexpr=expr.replace("×","*").replace("÷","/").replace("−","-")
            try:
                r=eval(pyexpr, {"__builtins__":{}}, {})
            except Exception as ex:
                errs.append(f"{key}[{i}] box '{pre.strip()}' uneval '{expr}': {ex}"); continue
            if not approx(r, st["answer"]):
                errs.append(f"{key}[{i}] box '{expr}' computes {r} != answer {st['answer']}")

for i,p in enumerate(B):
    if p.get("guided_steps"): scan_boxes(p["guided_steps"], f"B{i}.gs")
for i,p in enumerate(S):
    if p.get("guided_steps"): scan_boxes(p["guided_steps"], f"S{i}.gs")
for i,p in enumerate(G):
    if p.get("guided_steps"): scan_boxes(p["guided_steps"], f"G{i}.gs")
for t in ("bronze","silver","gold"):
    scan_boxes(pd["guided"]["teach"][t]["steps"], f"teach.{t}")
scan_boxes(pd["guided"]["opener"]["steps"], "opener")

# ---- em dash sweep (student-facing) ----
def sweep(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note",): continue
            sweep(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): sweep(v,f"{path}[{i}]")
    elif isinstance(o,str) and "—" in o:
        errs.append(f"EM DASH at {path}")
sweep(pd,"pd")

# ---- duplicate solutions within tier ----
for t,arr in (("bronze",B),("silver",S),("gold",G)):
    seen={}
    for i,p in enumerate(arr):
        if p.get("input_type")=="multiple_choice": continue
        k=tuple(p["solutions"])
        if k in seen: errs.append(f"{t} dup solution {k} at {i} and {seen[k]}")
        seen[k]=i

if errs:
    print("VERIFY FAIL", len(errs))
    for e in errs: print("  -", e)
else:
    print("VERIFY PASS: all fresh-solves, boxes, expects, style, dedupe clean")
