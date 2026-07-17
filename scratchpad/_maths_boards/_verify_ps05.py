# -*- coding: utf-8 -*-
import json, io
live = json.load(io.open("_live_ps05.json", encoding="utf-8"))
new  = json.load(io.open("lesson_maths-aqa_probability-statistics-L05.json", encoding="utf-8"))
errs=[]

# 1. preservation of untouched top-level fields
for f in ("related_videos","topic_links","worked_examples","method_card"):
    if json.dumps(live.get(f),sort_keys=True)!=json.dumps(new.get(f),sort_keys=True):
        errs.append("PRESERVATION changed: "+f)

# 2. every guided_steps final box lands on the problem solution; count live boxes after phase
pb=new["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        sol=p.get("solutions")
        if not gs: continue
        boxes=[st for st in gs if st.get("answer") is not None]
        last=boxes[-1]["answer"]
        if abs(float(last)-float(sol[-1]))>1e-9:
            errs.append(f"{tier}[{i}] last box {last} != sol {sol}")
        # phase
        sub=[j for j,st in enumerate(gs) if st.get("phase")=="substitute"]
        if not sub: errs.append(f"{tier}[{i}] no phase")
        else:
            live_after=sum(1 for st in gs[sub[0]:] if st.get("answer") is not None)
            if live_after<2: errs.append(f"{tier}[{i}] <2 live after phase")

# 3. expects must not equal solution and must be list len==sol len
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p.get("solutions")
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is None: continue
            if not isinstance(e,list) or len(e)!=len(sol):
                errs.append(f"{tier}[{i}] expect shape {e} vs sol {sol}")
            elif all(abs(float(a)-float(b))<1e-9 for a,b in zip(e,sol)):
                errs.append(f"{tier}[{i}] expect==sol")

# 4. tier sizes preserved
for tier in ("bronze","silver","gold"):
    if len(pb[tier])!=len(live["problem_bank"][tier]):
        errs.append(f"tier size changed {tier}")

# 5. multiset of solutions preserved per tier (except bronze B3 10->8 and B5 20->25, silver reorder)
def sols(bank): return sorted([tuple(x["solutions"]) for x in bank])
print("bronze sols new:", sols(pb["bronze"]))
print("bronze sols live:",sols(live["problem_bank"]["bronze"]))
print("silver sols new:", sols(pb["silver"]))
print("silver sols live:",sols(live["problem_bank"]["silver"]))
print("gold sols new:",   sols(pb["gold"]))
print("gold sols live:",  sols(live["problem_bank"]["gold"]))

# 6. charts added
for tier,idx in (("gold",2),("gold",3),("silver",4)):
    print(f"{tier}[{idx}] has chart:", "chart" in pb[tier][idx], "| labels:",
          pb[tier][idx]["chart"]["data"]["labels"], pb[tier][idx]["chart"]["data"]["datasets"][0]["data"])

print("\nERRORS:", errs if errs else "NONE")
