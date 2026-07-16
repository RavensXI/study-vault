import json,re
live=json.load(open("_live_L02_v2.json",encoding="utf-8"))
# em dash scan across all strings
emdash=[]
nonnum=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o or "–" in o:
            emdash.append((path,o))
def walk_answers(o,path):
    if isinstance(o,dict):
        if "answer" in o and not isinstance(o["answer"],(int,float)):
            nonnum.append((path,o["answer"]))
        for k,v in o.items():
            walk_answers(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk_answers(v,f"{path}[{i}]")
walk(live,"root")
walk_answers(live,"root")
print("EM/EN DASHES:", len(emdash))
for p,s in emdash: print("  ",p,":",s[:80])
print("NON-NUMERIC answer boxes:", len(nonnum))
for p,a in nonnum: print("  ",p,":",a)
# check every guided_steps final boxes land on solutions - already done manually; verify boundary counts
print("\n-- boundary live-box counts --")
for tier in ["bronze","silver","gold"]:
    for i,prob in enumerate(live["problem_bank"][tier]):
        gs=prob.get("guided_steps")
        if not gs: 
            print(tier,i,"NO guided_steps"); continue
        # find phase index (box steps only)
        boxes=[(j,s) for j,s in enumerate(gs) if "answer" in s]
        pidx=None
        for j,s in enumerate(gs):
            if s.get("phase")=="substitute": pidx=j
        if pidx is None:
            print(tier,i,"NO phase tag"); continue
        before=[b for b in boxes if b[0]<pidx]
        atafter=[b for b in boxes if b[0]>=pidx]
        flag="" if (len(before)>=1 and len(atafter)>=2) else "  <<< VIOLATION"
        print(f"{tier}[{i}] before={len(before)} at/after={len(atafter)}{flag}")
