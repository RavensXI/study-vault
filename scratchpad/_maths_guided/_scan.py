import json, io
live=json.load(io.open("_live_graphs_L07.json",encoding="utf-8"))

# 1. em dash scan in student-facing strings (exclude internal 'note')
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            scan(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o or "–" in o:
            print("EMDASH/ENDASH at",path,":",repr(o[:80]))
scan(live,"")
print("emdash scan done")

# 2. all guided_steps/teach/opener boxes: answer must be numeric
def check_boxes(steps,path):
    for i,s in enumerate(steps):
        if "answer" in s:
            a=s["answer"]
            if not isinstance(a,(int,float)) or isinstance(a,bool):
                print("NON-NUMERIC box",f"{path}[{i}]",a)
for t in ["bronze","silver","gold"]:
    check_boxes(live["guided"]["teach"][t]["steps"],f"teach.{t}")
check_boxes(live["guided"]["opener"]["steps"],"opener")
for t in ["bronze","silver","gold"]:
    for j,p in enumerate(live["problem_bank"][t]):
        if "guided_steps" in p:
            check_boxes(p["guided_steps"],f"{t}[{j}].guided_steps")
print("numeric box scan done")

# 3. boundary check: >=1 box before phase substitute, >=2 live boxes at/after
for t in ["bronze","silver","gold"]:
    for j,p in enumerate(live["problem_bank"][t]):
        gs=p.get("guided_steps")
        if not gs: continue
        boxes=[(i,s) for i,s in enumerate(gs) if "answer" in s]
        phase_idx=[i for i,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not phase_idx:
            print(f"{t}[{j}] NO phase substitute (has guided_steps)")
            continue
        first=min(phase_idx)
        before=[b for b in boxes if b[0]<first]
        after=[b for b in boxes if b[0]>=first]
        if len(before)<1: print(f"{t}[{j}] <1 box before boundary")
        if len(after)<2: print(f"{t}[{j}] <2 boxes at/after boundary: {len(after)}")
print("boundary scan done")

# 4. last box lands on stored solution
for t in ["bronze","silver","gold"]:
    for j,p in enumerate(live["problem_bank"][t]):
        gs=p.get("guided_steps")
        if not gs: continue
        sol=p["solutions"][0]
        boxes=[s["answer"] for s in gs if "answer" in s]
        # find the box that equals solution
        if sol not in boxes:
            print(f"{t}[{j}] solution {sol} not among boxes {boxes}")
print("solution-in-boxes scan done")
