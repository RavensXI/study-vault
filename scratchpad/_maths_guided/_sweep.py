import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
L=json.load(open("_live_graphs_l01.json",encoding="utf-8"))
issues=[]

# em dash scan on student-facing strings (exclude internal 'note')
def scan(obj,path):
    if isinstance(obj,str):
        if "—" in obj: issues.append(f"EM DASH at {path}: {obj}")
    elif isinstance(obj,dict):
        for k,v in obj.items():
            if k=="note": continue
            scan(v,f"{path}.{k}")
    elif isinstance(obj,list):
        for i,v in enumerate(obj): scan(v,f"{path}[{i}]")
scan(L,"root")

# numeric boxes + completion boundary check
def check_steps(steps,path):
    live_boxes=[s for s in steps if 'answer' in s]
    for i,s in enumerate(steps):
        if 'answer' in s:
            a=s['answer']
            if not isinstance(a,(int,float)) or isinstance(a,bool):
                issues.append(f"NON-NUMERIC answer at {path}[{i}]: {a!r}")
    # boundary
    sub_idx=[i for i,s in enumerate(steps) if s.get('phase')=='substitute']
    if sub_idx:
        first=sub_idx[0]
        before_boxes=sum(1 for s in steps[:first] if 'answer' in s)
        after_boxes=sum(1 for s in steps[first:] if 'answer' in s)
        if before_boxes<1: issues.append(f"BOUNDARY {path}: <1 box before substitute")
        if after_boxes<2: issues.append(f"BOUNDARY {path}: only {after_boxes} live box(es) at/after")

for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(L["problem_bank"][tier]):
        gs=p.get("guided_steps")
        if gs: check_steps(gs,f"{tier}[{i}].guided_steps")
        elif p.get("input_type")!="multiple_choice" and "guided_skip_reason" not in p:
            issues.append(f"MISSING guided_steps {tier}[{i}]")
# teach + opener numeric
for t in ["bronze","silver","gold"]:
    for i,s in enumerate(L["guided"]["teach"][t]["steps"]):
        if 'answer' in s and not isinstance(s['answer'],(int,float)):
            issues.append(f"NON-NUMERIC teach.{t}[{i}]")
for i,s in enumerate(L["guided"]["opener"]["steps"]):
    if 'answer' in s and not isinstance(s['answer'],(int,float)):
        issues.append(f"NON-NUMERIC opener[{i}]")

print("ISSUES:",len(issues))
for x in issues: print(" ",x)
