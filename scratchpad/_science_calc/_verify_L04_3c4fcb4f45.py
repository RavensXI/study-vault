# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_higher-calculations-L04@3c4fcb4f45.json", encoding="utf-8"))
errs = []

# Independent fresh solutions (computed by hand, encoded here)
expected = {
    "bronze": [12, 0.2, 56, 75, 1.2, 100],
    "silver": [1.2, 2.4, 80, 45.9, 0.6],
    "gold":   [80, 75.7, 14.4, 84],
}
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    exp = expected[tier]
    probs = pb[tier]
    assert len(probs)==len(exp), (tier, len(probs))
    seen=set()
    for i,p in enumerate(probs):
        sol = p["solutions"][0]
        if abs(sol-exp[i])>0.05:
            errs.append(f"{tier}[{i}] stored {sol} != fresh {exp[i]}")
        k=tuple(p["solutions"])
        if k in seen: errs.append(f"{tier}[{i}] duplicate sol {k}")
        seen.add(k)
        # misconception expects outside accept
        acc = p.get("accept")
        for m in p.get("misconceptions",[]):
            if "expect" not in m: errs.append(f"{tier}[{i}] missing expect")
            e=m.get("expect")
            if e is not None:
                ev = e[0] if isinstance(e,list) else e
                win = acc if acc is not None else 0.005
                if abs(ev-sol) <= win:
                    errs.append(f"{tier}[{i}] expect {ev} within accept of {sol}")
        # every non-mc problem has guided_steps ending with check, boundary valid
        gs=p.get("guided_steps")
        if not gs: errs.append(f"{tier}[{i}] no guided_steps"); continue
        boxes=[s for s in gs if s.get("answer") is not None]
        if len(boxes)<3: errs.append(f"{tier}[{i}] <3 boxes")
        sub=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not sub: errs.append(f"{tier}[{i}] no substitute boundary")
        else:
            live=[s for s in gs[sub[0]:] if s.get("answer") is not None]
            if len(live)<2: errs.append(f"{tier}[{i}] <2 live after boundary")
        if not gs[-1].get("done"): errs.append(f"{tier}[{i}] last step no done/check")

# ---- recompute every box arithmetically from its pre-text where deterministic ----
# Manual check of the finishing-box lands on stored solution
finish = {
 ("bronze",0):12,("bronze",1):0.2,("bronze",2):56,("bronze",3):75,("bronze",4):1.2,("bronze",5):100,
 ("silver",0):1.2,("silver",1):2.4,("silver",2):80,("silver",3):45.9,("silver",4):0.6,
 ("gold",0):80,("gold",1):75.7,("gold",2):14.4,("gold",3):84,
}
for (tier,i),val in finish.items():
    gs = pb[tier][i]["guided_steps"]
    sub=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"][0]
    # the substitute box should compute the answer (or a step toward it)
    subbox = gs[sub]
    # nothing automatic; just ensure the stored solution appears as some box answer
    box_answers=[s["answer"] for s in gs if s.get("answer") is not None]
    if not any(abs(a-val)<0.05 for a in box_answers):
        errs.append(f"{tier}[{i}] solution {val} not reached by any box")

# teach walks >=4 boxes
for tier in ("bronze","silver","gold"):
    t=pd["guided"]["teach"][tier]
    nb=sum(1 for s in t["steps"] if s.get("answer") is not None)
    if nb<4: errs.append(f"teach.{tier} {nb} boxes")

# opener box arithmetic
op=pd["guided"]["opener"]["steps"]
ob=[s for s in op if s.get("answer") is not None]
if not (abs(ob[0]["answer"]-72)<0.01 and abs(ob[1]["answer"]-12)<0.01):
    errs.append("opener boxes wrong")

# em dash scan
def scan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note",): continue
            scan(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,f"{path}[{j}]")
    elif isinstance(o,str) and "—" in o: errs.append("EMDASH "+path)
scan(pd)

if errs:
    print("FAIL", len(errs))
    for e in errs: print(" -",e)
else:
    print("ALL VERIFY CHECKS PASS")
