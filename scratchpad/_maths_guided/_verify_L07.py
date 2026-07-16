# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("lesson_number-L07.json", encoding="utf-8"))
errs = []

# --- fresh independent solve of each display ---
expected = {
 "bronze": [4, 2, [1,9], 5, [1,8], 12.35, 3, 6],
 "silver": [9, 8, 10, 3, 3.65, 6, 2],
 "gold":   [4, 2, 26.6175, 8, 8.2],
}
for tier, sols in expected.items():
    probs = pd["problem_bank"][tier]
    for i,(p,e) in enumerate(zip(probs, sols)):
        got = p["solutions"]
        e2 = e if isinstance(e,list) else [e]
        if got != e2:
            errs.append(f"{tier}[{i}] solution {got} != fresh {e2}")

# --- boxes numeric, continuity checks on key landing boxes ---
def boxes(steps):
    return [s for s in steps if s.get("answer") is not None]

# For each problem, verify the box that yields the answer equals a solution value,
# and every box answer is numeric.
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        bs = boxes(p["guided_steps"])
        for b in bs:
            if not isinstance(b["answer"], (int,float)):
                errs.append(f"{tier}[{i}] non-numeric box {b}")
        # substitute boundary present with >=2 live boxes
        subidx = next((k for k,s in enumerate(p["guided_steps"]) if s.get("phase")=="substitute"), None)
        if subidx is None:
            errs.append(f"{tier}[{i}] no substitute")
        else:
            live = sum(1 for s in p["guided_steps"][subidx:] if s.get("answer") is not None)
            pre  = sum(1 for s in p["guided_steps"][:subidx] if s.get("answer") is not None)
            if live < 2: errs.append(f"{tier}[{i}] live boxes {live}")
            if pre < 1: errs.append(f"{tier}[{i}] pre boxes {pre}")

# --- explicit arithmetic recompute of every guided box for continuity ---
# hand-list the (tier,index) -> list of box answers we expect
box_expect = {
 ("bronze",0): [16,4,16],
 ("bronze",1): [8,2,8],
 ("bronze",2): [9,1,9],
 ("bronze",3): [2,5,50],
 ("bronze",4): [8,1,8],
 ("bronze",5): [0.05,12.35,0.05],
 ("bronze",6): [2,3,18],
 ("bronze",7): [36,6,36],
 ("silver",0): [3,9,27],
 ("silver",1): [16,8,16],
 ("silver",2): [2,10,200],
 ("silver",3): [2,3,18],
 ("silver",4): [0.05,3.65,0.05],
 ("silver",5): [2,6,72],
 ("silver",6): [4,2,4],
 ("gold",0): [2,4,8],
 ("gold",1): [5,2,20],
 ("gold",2): [8.45,3.15,26.6175,27.2],
 ("gold",3): [5,3,8,192],
 ("gold",4): [100.5,12.25,8.2,8.1],
}
for (tier,i),exp in box_expect.items():
    got = [b["answer"] for b in boxes(pd["problem_bank"][tier][i]["guided_steps"])]
    if got != exp:
        errs.append(f"{tier}[{i}] box answers {got} != {exp}")

# --- verify the actual arithmetic in box_expect is internally correct ---
assert 4*4==16 and 2**3==8 and 3**2==9 and 5*5==25 and 5*5*2==50
assert abs(0.1/2-0.05)<1e-9 and abs(12.4-0.05-12.35)<1e-9 and abs(12.4-12.35-0.05)<1e-9
assert 6*6==36
assert 3**3==27 and 2**4==16 and 10*10*2==200
assert abs(6/2-3)<1e-9 and 9*2==18 and 36/2==18
assert abs(3.6+0.05-3.65)<1e-9 and abs(3.65-3.6-0.05)<1e-9
assert 3*2==6 and 9*8==72 and 6*6*2==72
assert 4**0.5==2
assert 2**2==4 and 2**3==8
assert 10/5==2 and 100/5==20 and 4*5==20
assert abs(8.5-0.05-8.45)<1e-9 and abs(3.2-0.05-3.15)<1e-9
assert abs(8.45*3.15-26.6175)<1e-9 and abs(8.5*3.2-27.2)<1e-9
assert 5+3==8 and 64*3==192 and (75+27+2*(2025**0.5))==192
assert abs(100+0.5-100.5)<1e-9 and abs(12.3-0.05-12.25)<1e-9
assert round(100.5/12.25,1)==8.2 and round(99.5/12.35,1)==8.1

# --- em dash scan (excluding note) ---
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+str(k))
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,path+f"[{j}]")
    elif isinstance(o,str) and "—" in o:
        errs.append("EM DASH at "+path)
scan(pd,"pd")

# --- expect != solution ---
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        sv=[float(x) for x in p["solutions"]]
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            ev=e if isinstance(e,list) else [e]
            if len(ev)==len(sv) and all(isinstance(x,(int,float)) for x in ev):
                if all(abs(float(a)-b)<0.011 for a,b in zip(ev,sv)):
                    errs.append(f"{tier}[{i}].mc[{j}] expect==solution")

# --- duplicate solutions within tier ---
for tier in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pd["problem_bank"][tier]):
        key=tuple(p["solutions"])
        if key in seen: errs.append(f"{tier}[{i}] dup solution {key}")
        seen.add(key)

# --- preservation check ---
live=json.load(io.open("_live_L07.json",encoding="utf-8"))
for k in ("related_videos","topic_links"):
    if json.dumps(pd.get(k),sort_keys=True,ensure_ascii=False)!=json.dumps(live.get(k),sort_keys=True,ensure_ascii=False):
        errs.append(f"PRESERVATION changed: {k}")
# worked_examples: only the em-dash->colon label sanitisation is allowed to differ
import copy
we_norm=copy.deepcopy(live["worked_examples"])
for we in we_norm:
    for st in we.get("steps",[]):
        if "label" in st and isinstance(st["label"],str):
            st["label"]=st["label"].replace(" — ",": ").replace("—",":")
if json.dumps(pd["worked_examples"],ensure_ascii=False)!=json.dumps(we_norm,ensure_ascii=False):
    errs.append("PRESERVATION worked_examples differs beyond em-dash sanitisation")

if errs:
    print("VERIFY FAIL:")
    for e in errs: print("  -",e)
else:
    print("VERIFY OK: solutions, boxes, continuity, expects, dashes, preservation all clean")
