import json, math
live=json.load(open("_CHK_live_geomL02.json",encoding="utf-8"))
pi=math.pi
# expected box answers computed independently for each bank problem, in order
exp = {
 ("gold",0):[200,188.5,388,200],
 ("gold",1):[0.375,64,75.4,135],
 ("gold",2):[63.66,7.98,50.1,200],
 ("gold",3):[56.55,0.2122,76,12],
 ("gold",4):[100,36,201.1,64],
 ("bronze",0):[5,45,5],
 ("bronze",1):[19,38,38],
 ("bronze",2):[60,30,60],
 ("bronze",3):[5,40,5],
 ("bronze",4):[43.98,44.0,42],
 ("bronze",5):[25,78.5,75],
 ("bronze",6):[14,84,42,84],
 ("bronze",7):[12,144,12],
 ("silver",0):[9,81,254.5,18],
 ("silver",1):[6.28,5,31.4],
 ("silver",2):[32,15,47,32],
 ("silver",3):[100,25,78.5,314],
 ("silver",4):[20,10,6,60],
 ("silver",5):[14,22.0,36,7],
 ("silver",6):[16.0,4,50.3],
}
bad=[]
for (tier,idx),vals in exp.items():
    prob=live["problem_bank"][tier][idx]
    boxes=[s for s in prob["guided_steps"] if "answer" in s]
    got=[b["answer"] for b in boxes]
    if got!=vals:
        bad.append(f"{tier}[{idx}] boxes got {got} exp {vals}")
# teach
tb={"bronze":[18,72,36,72],"silver":[10,100,314.2,20],"gold":[0.125,64,8,25.1,45]}
for t,vals in tb.items():
    boxes=[s["answer"] for s in live["guided"]["teach"][t]["steps"] if "answer" in s]
    if boxes!=vals: bad.append(f"teach.{t} got {boxes} exp {vals}")
# opener
ob=[s["answer"] for s in live["guided"]["opener"]["steps"] if "answer" in s]
if ob!=[12,14]: bad.append(f"opener got {ob}")
print("MISMATCHES:", len(bad))
for b in bad: print(" ",b)

# completion boundary: check >=1 before phase and >=2 live boxes from phase
for tier in ["bronze","silver","gold"]:
    for idx,prob in enumerate(live["problem_bank"][tier]):
        steps=prob["guided_steps"]
        pidx=[i for i,s in enumerate(steps) if s.get("phase")=="substitute"]
        boxes_before=sum(1 for s in steps[:pidx[0]] if "answer" in s) if pidx else -1
        live_boxes=sum(1 for s in steps[pidx[0]:] if "answer" in s) if pidx else -1
        if not pidx or boxes_before<1 or live_boxes<2:
            print(f"BOUNDARY {tier}[{idx}]: before={boxes_before} live={live_boxes} phase={bool(pidx)}")
print("boundary check done")
