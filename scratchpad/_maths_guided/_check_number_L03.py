# -*- coding: utf-8 -*-
import json, io, math
pd = json.load(io.open("lesson_number-L03.json", encoding="utf-8"))
live = json.load(io.open("_live_number_L03.json", encoding="utf-8"))
prob=[]

# 1. independent fresh solve of each problem
solve = {
 "gold": [
   ("estimate (6.12*48.7)/0.236 -> (6*50)/0.2", 300/0.2, 1500),
   ("0.07*0.004", round(0.07*0.004,8), 0.00028),
   ("4.56/0.08", 4.56/0.08, 57),
   ("0.009950 -> 3sf", 0.00995, 0.00995),
   ("estimate (sqrt99+4.1^2)/1.97 -> (10+16)/2", (10+16)/2, 13),
 ],
 "bronze": [
   ("4.673->1dp", 4.7, 4.7),
   ("12.345->2dp", 12.35, 12.35),
   ("8.049->1dp", 8.0, 8),
   ("3647->nearest100", 3600, 3600),
   ("0.562->1sf", 0.6, 0.6),
   ("3.2+4.58", round(3.2+4.58,4), 7.78),
   ("5.7-2.35", round(5.7-2.35,4), 3.35),
   ("0.3*4", round(0.3*4,4), 1.2),
 ],
 "silver": [
   ("0.003482->2sf", 0.0035, 0.0035),
   ("45982->3sf", 46000, 46000),
   ("estimate 31.2*4.87 ->30*5", 30*5, 150),
   ("estimate 198/0.48 ->200/0.5", 200/0.5, 400),
   ("2.4*0.3", round(2.4*0.3,4), 0.72),
   ("6.5/0.5", 6.5/0.5, 13),
   ("estimate sqrt83 ~9", 9, 9),
 ],
}
for tier in ("bronze","silver","gold"):
    for i,(desc,mine,stored) in enumerate(solve[tier]):
        p=pd["problem_bank"][tier][i]
        sol=p["solutions"][0]
        ok1 = abs(mine-stored)<1e-6
        ok2 = abs(stored-sol)<1e-6
        if not (ok1 and ok2):
            prob.append(f"SOLVE {tier}[{i}] {desc}: mine={mine} stored={stored} banksol={sol}")

# 2. final-answer box of each walk must equal solution
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        gs=p["guided_steps"]
        boxes=[s for s in gs if s.get("answer") is not None]
        sol=p["solutions"][0]
        # the answer-stating box is the one whose answer equals the solution somewhere pre-check
        if not any(abs(b["answer"]-sol)<1e-6 for b in boxes):
            prob.append(f"WALK {tier}[{i}] no box lands on solution {sol}; box answers={[b['answer'] for b in boxes]}")
        # completion boundary: >=1 pre, >=2 live after
        sub=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
        if sub:
            first=sub[0]
            live_after=sum(1 for s in gs[first:] if s.get('answer') is not None)
            if live_after<2: prob.append(f"WALK {tier}[{i}] <2 live boxes after boundary")
            if first<1: prob.append(f"WALK {tier}[{i}] boundary at 0")
        else:
            prob.append(f"WALK {tier}[{i}] no substitute boundary")

# 3. misconception expects != correct and numeric
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        sol=p["solutions"][0]
        for j,m in enumerate(p["misconceptions"]):
            e=m["expect"]
            if e is None: continue
            if abs(float(e)-sol)<0.011:
                prob.append(f"EXPECT {tier}[{i}].mis[{j}] expect {e} too close to sol {sol}")

# 4. preservation
def strip_dash(s): return s.replace(" — ", ": ").replace("—", ": ") if isinstance(s,str) else s
if pd["related_videos"] != live["related_videos"]:
    prob.append("related_videos changed")
if pd["topic_links"] != live["topic_links"]:
    prob.append("topic_links changed")
# worked_examples: equal after dedash of live
import copy
lwe=copy.deepcopy(live["worked_examples"])
for we in lwe:
    we["question"]=strip_dash(we.get("question"))
    for st in we.get("steps",[]):
        st["label"]=strip_dash(st.get("label"))
        st["content"]=strip_dash(st.get("content"))
if pd["worked_examples"]!=lwe:
    prob.append("worked_examples changed beyond dedash")

# 5. em dash scan of whole doc (excl note)
def scan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,f"{path}[{j}]")
    elif isinstance(o,str) and "—" in o:
        prob.append(f"EMDASH {path}")
scan(pd)

# 6. hints plain text (no latex/html)
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        h=p["hint"]
        if "\(" in h or "<" in h: prob.append(f"HINT {tier}[{i}] not plain")

print("PROBLEMS:" if prob else "ALL CHECKS PASS")
for x in prob: print("  -",x)
