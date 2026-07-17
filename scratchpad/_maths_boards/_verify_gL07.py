# -*- coding: utf-8 -*-
import json, math, re

SHARD="lesson_maths-ocr_graphs-L07.json"
pd=json.load(open(SHARD,encoding="utf-8"))
fails=[]; notes=[]

def last_boxes(steps):
    return [s for s in steps if s.get("answer") is not None]

# 1. guided_steps final boxes vs solutions + continuity of arithmetic in each numeric box
# We just recompute the arithmetic embedded in pre-text like "7 + 3 =" etc where present.
arith=re.compile(r"(-?\d+)\s*([+\-×])\s*\(?(-?\d+)\)?\s*=\s*$")
def check_walk(path, steps):
    for i,s in enumerate(steps):
        if s.get("answer") is None: continue
        pre=s.get("pre","")
        m=arith.search(pre.replace("−","-"))
        if m:
            a=int(m.group(1)); op=m.group(2); b=int(m.group(3))
            val = a+b if op=="+" else (a-b if op=="-" else a*b)
            if val!=s["answer"]:
                fails.append(f"{path}[{i}] arithmetic '{pre.strip()}' -> {val} != box {s['answer']}")

pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    seen={}
    for idx,p in enumerate(pb[tier]):
        path=f"{tier}[{idx}]"
        it=p.get("input_type")
        sols=p["solutions"]
        # duplicate SV check
        if it!="multiple_choice":
            key=tuple(sols)
            if key in seen: fails.append(f"{path} dup solution {sols} (also {seen[key]})")
            seen[key]=path
        gs=p.get("guided_steps")
        if gs:
            check_walk(path+".gs", gs)
            fb=last_boxes(gs)
            # find the box that equals the solution (single_value walks land the new value)
            # boundary check
            sub=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
            if not sub: fails.append(f"{path} no substitute boundary")
        # expect != correct
        for j,m in enumerate(p.get("misconceptions") or []):
            e=m.get("expect")
            if e is not None and it!="multiple_choice":
                if len(sols)==1 and abs(float(e)-float(sols[0]))<0.011:
                    fails.append(f"{path}.mis[{j}] expect==correct {e}")

# 2. Manual maths recompute of every problem answer
def V(cond,msg):
    if not cond: fails.append("MATH "+msg)
# BRONZE
V(7+3==pb["bronze"][0]["solutions"][0]==10,"B1")
V(1-3==pb["bronze"][1]["solutions"][0]==-2,"B2")
V(pb["bronze"][2]["solutions"]==[0],"B3 up")
V(pb["bronze"][3]["solutions"]==[2],"B4 left")
V(5-4==pb["bronze"][4]["solutions"][0]==1,"B5")
V(pb["bronze"][5]["solutions"]==[0],"B6 x-axis")
V(pb["bronze"][6]["solutions"]==[1],"B7 y-axis")
V(pb["bronze"][7]["solutions"][0]==-6,"B8")
# SILVER
V(pb["silver"][0]["solutions"][0]==2,"S1 -2->2")
V(7-4==pb["silver"][1]["solutions"][0]==3,"S2")
V(3+5==pb["silver"][2]["solutions"][0]==8,"S3")
V(pb["silver"][3]["solutions"][0]==-2,"S4 xcomp left2")
V(6-2==pb["silver"][4]["solutions"][0]==4,"S5")
V(pb["silver"][5]["solutions"][0]==-5,"S6")
V(pb["silver"][6]["solutions"][0]==-7,"S7")
# GOLD
V(0-4==pb["gold"][0]["solutions"][0]==-4,"G1 vertex y")
V(pb["gold"][1]["solutions"]==[1],"G2 -sin x")
V(-6+4==pb["gold"][2]["solutions"][0]==-2,"G3")
V(pb["gold"][3]["solutions"]==[0],"G4")
V(pb["gold"][4]["solutions"]==[1],"G5 (4,3)")

# 3. chart points satisfy equations
for tier,idx in [("gold",0),("silver",3)]:
    ch=pb[tier][idx].get("chart")
    if ch:
        line=ch["data"]["datasets"][0]["data"]
        for pt in line:
            if abs(pt["x"]**2 - pt["y"])>1e-9: fails.append(f"{tier}[{idx}] parabola point {pt} not on y=x^2")
ch=pb["gold"][1]["chart"]
for pt in ch["data"]["datasets"][0]["data"]:
    if abs(math.sin(math.radians(pt["x"]))-pt["y"])>0.002: fails.append(f"gold[1] sin point {pt} off")

# 4. SVG theme safety
svg=pd["guided"]["opener"]["display"]
if "http" in svg.lower() or "xlink" in svg.lower(): fails.append("opener svg external ref")
if "currentColor" not in svg: fails.append("opener svg no currentColor text")
if "fill-opacity" not in svg: fails.append("opener svg region fill not translucent")

# 5. expects reproduce (MC = option index of wrong answer)
def opt_idx(p,text):
    for i,o in enumerate(p["options"]):
        if o==text: return i
    return None
# B3 expect Right idx3
V(pb["bronze"][2]["misconceptions"][0]["expect"]==pb["bronze"][2]["options"].index("Right"),"B3 expect=Right idx")
V(pb["bronze"][3]["misconceptions"][0]["expect"]==pb["bronze"][3]["options"].index("Right"),"B4 expect=Right idx")
V(pb["bronze"][5]["misconceptions"][0]["expect"]==pb["bronze"][5]["options"].index("y-axis"),"B6 expect=y-axis idx")
V(pb["bronze"][6]["misconceptions"][0]["expect"]==pb["bronze"][6]["options"].index("x-axis"),"B7 expect=x-axis idx")
V(pb["gold"][1]["misconceptions"][0]["expect"]==pb["gold"][1]["options"].index("y = sin(−x)"),"G2 expect idx")
V(pb["gold"][4]["misconceptions"][0]["expect"]==0,"G5 expect yes idx0")
V(pb["gold"][4]["misconceptions"][1]["expect"]==3,"G5 expect (8,3) idx3")
V(pb["gold"][4]["misconceptions"][2]["expect"]==2,"G5 expect (6,3) idx2")

# 6. Preservation vs pre-dump
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre-dump structure?
entry=None
if isinstance(pre,dict):
    for k,v in pre.items():
        vv=v.get("practice_data") if isinstance(v,dict) and "practice_data" in v else v
        if isinstance(vv,dict) and vv.get("slug")=="graph-transformations":
            entry=vv; break
        if isinstance(v,dict) and v.get("slug")=="graph-transformations":
            entry=v; break
print("pre-dump entry found:", entry is not None)
if entry:
    ppd=entry.get("practice_data",entry)
    # topic_links, related_videos identical
    if ppd.get("topic_links")!=pd["topic_links"]: fails.append("topic_links changed vs pre-dump")
    if ppd.get("related_videos")!=pd["related_videos"]: fails.append("related_videos changed vs pre-dump")
    # worked_examples identical except em-dash label fix
    pwe=ppd.get("worked_examples"); nwe=pd["worked_examples"]
    if len(pwe)!=len(nwe): fails.append("worked_examples count changed")
    else:
        for a,b in zip(pwe,nwe):
            if a.get("question")!=b.get("question"): fails.append("we question changed: "+str(a.get("question")))
            if a.get("difficulty")!=b.get("difficulty"): fails.append("we difficulty changed")

print("\nRESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
for f in fails: print("  -",f)
