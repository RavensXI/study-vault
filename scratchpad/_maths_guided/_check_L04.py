import json
live=json.load(open("_live_L04.json",encoding="utf-8"))

# 1. em-dash scan across all string values
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,path+"["+str(i)+"]")
    elif isinstance(o,str):
        yield path,o

emdash=[]
for p,s in walk(live):
    if "—" in s:  # em dash
        # note fields exempt
        if p.endswith(".note"): continue
        emdash.append((p,s))
print("EM DASHES (student-facing):", len(emdash))
for p,s in emdash: print("  ",p,"::",s[:80])

# non-numeric answer boxes
badans=[]
def scan_steps(steps,base):
    for i,st in enumerate(steps):
        if isinstance(st,dict) and "answer" in st:
            a=st["answer"]
            if not isinstance(a,(int,float)):
                badans.append((base+"["+str(i)+"]",a))
# teach
for tier in live["guided"]["teach"]:
    scan_steps(live["guided"]["teach"][tier]["steps"],"guided.teach."+tier+".steps")
scan_steps(live["guided"]["opener"]["steps"],"guided.opener.steps")
for tier in live["problem_bank"]:
    if tier.endswith("_description"): continue
    for j,prob in enumerate(live["problem_bank"][tier]):
        if "guided_steps" in prob:
            scan_steps(prob["guided_steps"],tier+"["+str(j)+"].guided_steps")
print("NON-NUMERIC answer boxes:", badans)

# check phase boundaries: >=2 live boxes at/after phase, >=1 step before
print("\nBOUNDARY CHECK:")
for tier in live["problem_bank"]:
    if tier.endswith("_description"): continue
    for j,prob in enumerate(live["problem_bank"][tier]):
        if prob.get("input_type")=="multiple_choice": continue
        gs=prob.get("guided_steps")
        if not gs:
            print(f"  {tier}[{j}] NO guided_steps (skip_reason={prob.get('guided_skip_reason')})")
            continue
        pidx=[i for i,s in enumerate(gs) if s.get("phase")=="substitute"]
        boxes_after=sum(1 for s in gs if s.get("phase")=="substitute" or (pidx and gs.index(s)>=pidx[0]) )
        if not pidx:
            print(f"  {tier}[{j}] NO phase tag")
            continue
        first=pidx[0]
        live_boxes=sum(1 for i,s in enumerate(gs) if i>=first and "answer" in s)
        before=first
        flag="" if (before>=1 and live_boxes>=2) else "  <-- VIOLATION"
        print(f"  {tier}[{j}] first_phase@{first} steps_before={before} live_boxes>={live_boxes}{flag}")
