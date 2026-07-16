import json, io, re
live=json.load(io.open("_chk02_live.json",encoding="utf-8"))
issues=[]

# em dash scan in student-facing strings (exclude 'note')
EM=re.compile(r'[—–]')
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            scan(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if EM.search(o): issues.append(f"EM DASH at {path}: {o[:60]}")
scan(live,"")

# check all guided_steps boxes numeric answer and boundary rules
def check_walk(steps,path):
    boxes=[s for s in steps if "answer" in s]
    for i,s in enumerate(steps):
        if "answer" in s and not isinstance(s["answer"],(int,float)):
            issues.append(f"NON-NUMERIC answer {path}[{i}]: {s['answer']}")
    # boundary
    bidx=[i for i,s in enumerate(steps) if s.get("phase")=="substitute"]
    if bidx:
        first=bidx[0]
        before=[s for s in steps[:first] if "answer" in s]
        after=[s for s in steps[first:] if "answer" in s]
        if len(before)<1: issues.append(f"BOUNDARY {path}: <1 box before")
        if len(after)<2: issues.append(f"BOUNDARY {path}: <2 boxes after ({len(after)})")

pb=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for pi,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if gs: check_walk(gs,f"{tier}[{pi}].guided_steps")
        elif p.get("input_type")!="multiple_choice" and "guided_skip_reason" not in p:
            issues.append(f"MISSING guided_steps {tier}[{pi}]")

# tier guide step word budgets <=115
for t,g in live["tier_guides"].items():
    wc=sum(len(re.sub(r'\\(.*?\\)','x',s).split()) for s in g["steps"])
    if wc>115: issues.append(f"tier_guides.{t} steps words={wc} >115")

print("ISSUES:", len(issues))
for i in issues: print(" -",i)
