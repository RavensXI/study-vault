import json,re
live=json.load(open("_CHK_L03rp_live.json",encoding="utf-8"))["practice_data"]
issues=[]
# em dash sweep on student-facing strings
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue  # internal exempt
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o or "–" in o:
            issues.append(f"DASH at {path}: {o[:60]}")
walk(live,"pd")

# check each bank problem: final box lands on solution, check misconception expects
pb=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]
        gs=p.get("guided_steps",[])
        boxes=[s for s in gs if "answer" in s]
        if boxes:
            # find last non-check box that equals solution somewhere
            vals=[b["answer"] for b in boxes]
            if sol not in vals:
                issues.append(f"{tier}[{i}] solution {sol} not among box answers {vals}")
        # calculator false clean-ness
        if p.get("calculator")==False:
            if abs(sol-round(sol))>1e-9:
                issues.append(f"{tier}[{i}] non-calc non-integer solution {sol}")
print("issues:",len(issues))
for x in issues: print(" ",x)
print("done")
