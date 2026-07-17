# -*- coding: utf-8 -*-
import json, math
pd = json.load(open("lesson_maths-eduqas_ratio-proportion-L06.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# independent fresh-solve of every problem (by hand-coded solver keyed to display intent)
def approx(a, b, tol=0.005): return abs(a-b) <= tol

# BRONZE
B = pb["bronze"]
checks = [
 (0, 80/4),                 # speed
 (1, (20-4)/(5-1)),         # gradient
 (2, 3+4+4),                # x2
 (3, 2*4-1),                # x1
 (4, 0),                    # accel constant
 (5, 3**2-4),               # x1
 (6, 48/6),                 # accel
]
for i, val in checks:
    if not approx(B[i]["solutions"][0], val):
        errs.append(f"bronze[{i}] solution {B[i]['solutions']} != {val}")
# B7 (index7) is MC conceptual: solutions [0] index, options[0]=Speed
if B[7]["options"][B[7]["solutions"][0]] != "Speed":
    errs.append("bronze[7] MC correct option not Speed")

# SILVER
S = pb["silver"]
x=3; x1=10/(x+1); x2=10/(x1+1)
sv = [
 (0, round(x2,2)),
 (1, (25-5)/4),
 (2, round((3**2+5)/(2*3),3)),
 (3, 2**3-2-5),                 # f(2)=1
 (4, (20-8)/3),
]
for i,val in sv:
    if not approx(S[i]["solutions"][0], val):
        errs.append(f"silver[{i}] solution {S[i]['solutions']} != {val}")
x=1; x2=math.sqrt(3*math.sqrt(3*x+1)+1)
if not approx(S[5]["solutions"][0], round(x2,2)):
    errs.append(f"silver[5] {S[5]['solutions']} != {round(x2,2)}")
x=4; x1=math.sqrt(2*x+3); x2=math.sqrt(2*x1+3)
if not approx(S[6]["solutions"][0], round(x2,3)):
    errs.append(f"silver[6] {S[6]['solutions']} != {round(x2,3)}")

# GOLD
G = pb["gold"]
if not approx(G[0]["solutions"][0], (13-1)/(4-0)): errs.append("gold[0]")
x=2.0
x1=(2*x**3+5)/(3*x**2); x2=(2*x1**3+5)/(3*x1**2)
if not approx(G[1]["solutions"][0], round(x2,3)): errs.append(f"gold[1] {G[1]['solutions']} vs {round(x2,3)}")
P10=2000*1.05**10; rate=round((round(P10)-2000)/10)
if not approx(G[2]["solutions"][0], rate): errs.append(f"gold[2] {G[2]['solutions']} vs {rate}")
h=[0,1,4,9,16]; area=0.5*1*(h[0]+h[-1]+2*(h[1]+h[2]+h[3]))
if not approx(G[3]["solutions"][0], area): errs.append(f"gold[3] {G[3]['solutions']} vs {area}")
if not approx(G[4]["solutions"][0], 5): errs.append("gold[4]")

# every expect != solution and (for single_value) is a plain number derivable
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol = p["solutions"]
        for j,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is not None and isinstance(e,(int,float)) and len(sol)==1:
                if approx(float(e), float(sol[0]), 0.011):
                    errs.append(f"{tier}[{i}].misc[{j}] expect==solution")

# guided walk: last box before/at a 'done' with the answer must equal solution for key problems
def last_answer_boxes(p):
    return [st["answer"] for st in p.get("guided_steps",[]) if st.get("answer") is not None]

# spot-check that the solution value appears as a box answer in each single_value walk
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p["input_type"]=="multiple_choice": continue
        boxes = last_answer_boxes(p)
        sol = p["solutions"][0]
        if not any(approx(float(b), float(sol)) for b in boxes):
            errs.append(f"{tier}[{i}] solution {sol} not produced by any guided box {boxes}")

# opener & teach boxes recompute
op = [st.get("answer") for st in pd["guided"]["opener"]["steps"] if st.get("answer") is not None]
if op != [160,140]: errs.append(f"opener boxes {op}")
tb = pd["guided"]["teach"]["bronze"]["steps"]
if [s.get("answer") for s in tb if s.get("answer") is not None] != [12,4,3,12]:
    errs.append("teach bronze boxes")
ts = pd["guided"]["teach"]["silver"]["steps"]
if [s.get("answer") for s in ts if s.get("answer") is not None] != [4,3,5,2.4,12]:
    errs.append("teach silver boxes")
tgd = pd["guided"]["teach"]["gold"]["steps"]
gvals=[s.get("answer") for s in tgd if s.get("answer") is not None]
if gvals != [74,27,2.7407,2.715,20]:
    errs.append(f"teach gold boxes {gvals}")

# figure label sanity: heights in trap svg present
disp = pb["gold"][3]["display"]
for lbl in ["0","1","4","9","16"]:
    if f">{lbl}</text>" not in disp: errs.append(f"trap svg missing height {lbl}")
# dt svg endpoint labels
if ">80</text>" not in pb["bronze"][0]["display"] or ">4</text>" not in pb["bronze"][0]["display"]:
    errs.append("dt svg labels")
if ">12</text>" not in pb["bronze"][4]["display"] or ">8</text>" not in pb["bronze"][4]["display"]:
    errs.append("st svg labels")

# em dash scan
def scan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+str(k))
    elif isinstance(o,list):
        for k,v in enumerate(o): scan(v,f"{path}[{k}]")
    elif isinstance(o,str) and "—" in o: errs.append("EM DASH "+path)
scan(pd)

print("ERRORS:" if errs else "ALL CHECKS PASS")
for e in errs: print(" -", e)
