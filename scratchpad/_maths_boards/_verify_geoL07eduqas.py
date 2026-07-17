# -*- coding: utf-8 -*-
"""Adversarial self-check: fresh-solve answers, recompute arithmetic boxes,
reproduce expects, cross-check figure numbers against text."""
import json, io, re

pd = json.load(io.open("lesson_maths-eduqas_geometry-L07.json", encoding="utf-8"))
problems = 0
fails = []

# 1) independent fresh-solve of every single_value answer
EXPECT = {  # tier,idx -> correct answer by independent reasoning
 ("bronze",0):70,  # 140/2
 ("bronze",1):68,  # 34*2
 ("bronze",2):90,  # semicircle
 ("bronze",3):48,  # same segment
 ("bronze",5):55,  # same segment
 ("bronze",7):45,  # 90/2
 ("silver",0):108, # 180-72
 ("silver",2):12,  # equal tangents
 ("silver",3):95,  # 180-85
 ("silver",4):40,  # 90-50
 ("silver",5):280, # 360-2*40
 ("silver",6):30,  # 3x=90
 ("gold",0):130,   # 2*65
 ("gold",1):25,    # 6x=150
 ("gold",3):64,    # (180-52)/2
 ("gold",4):56,    # 180-90-34
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        problems+=1
        if p["input_type"]=="multiple_choice":
            if p["solutions"]!=[0]: fails.append("%s[%d] MC solutions not [0]"%(tier,i))
            continue
        want = EXPECT.get((tier,i))
        got = p["solutions"][0]
        if want!=got: fails.append("%s[%d] answer %s expected %s"%(tier,i,got,want))

# 2) recompute arithmetic boxes: eval trailing "<expr> = " before the blank
def arith(pre):
    s=pre.replace("×","*").replace("÷","/").replace("−","-")
    m=re.search(r"([0-9\(\)\+\-\*/\.\s]+?)\s*=\s*$", s)
    if not m: return None
    expr=m.group(1).strip()
    if not re.search(r"[\+\-\*/]",expr): return None
    try:
        v=eval(expr); return v
    except Exception: return None

def walk_boxes(steps,label):
    for j,st in enumerate(steps):
        if st.get("answer") is None: continue
        v=arith(st.get("pre",""))
        if v is not None:
            if abs(v-st["answer"])>1e-9:
                fails.append("%s[%d] box arithmetic %s != answer %s (pre=%r)"%(label,j,v,st["answer"],st["pre"]))

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        if p.get("guided_steps"): walk_boxes(p["guided_steps"],"%s[%d].gs"%(tier,i))
walk_boxes(pd["guided"]["opener"]["steps"],"opener")
for tier in ("bronze","silver","gold"):
    walk_boxes(pd["guided"]["teach"][tier]["steps"],"teach.%s"%tier)

# 3) expects reproduce the committed error (spot the key ones)
def find(tier,i): return pd["problem_bank"][tier][i]
checks = [
 ("bronze",0,280, 140*2),         # doubled instead of halved
 ("bronze",1,17, 34/2),           # halved instead of doubled
 ("silver",4,50, 50),             # copied tangent-chord
 ("silver",5,80, 2*40),           # forgot reflex -> non-reflex 80
 ("silver",5,320,360-40),         # forgot double
 ("gold",1,15, 30/2),             # set equal: 4x=2x+30 -> x=15
 ("gold",3,128,180-52),           # forgot halve -> centre 128
]
for tier,i,exp,val in checks:
    if abs(exp-val)>1e-9: fails.append("expect derivation %s[%d]: stored %s vs derived %s"%(tier,i,exp,val))
    # confirm the misconception with that expect exists
    ms=[m for m in find(tier,i)["misconceptions"] if m.get("expect")==exp]
    if not ms: fails.append("no misconception with expect %s in %s[%d]"%(exp,tier,i))

# 4) figure number cross-check: every angle-degree token in the SVG text must
# appear in the problem text (or be '?','x','2x' etc)
DEG=re.compile(r">(\d+)°<")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        disp=p["display"]
        svg=disp.split("</svg>")[0] if "<svg" in disp else ""
        text=disp.split("</svg>")[1] if "</svg>" in disp else disp
        for num in DEG.findall(svg):
            if num not in re.sub(r"[^0-9]"," ",text).split():
                fails.append("%s[%d] figure shows %s° not in text"%(tier,i,num))

print("problems:",problems)
if fails:
    print("FAILS (%d):"%len(fails))
    for f in fails: print("  -",f)
else:
    print("ALL CHECKS CLEAN: answers, box arithmetic, expects, figure numbers")
