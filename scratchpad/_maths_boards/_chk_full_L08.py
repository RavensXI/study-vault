import json, re
live = json.load(open("_chk_live_L08.json", encoding="utf-8"))
pb = live["problem_bank"]
issues=[]

def fnum(s):
    return s

# check final guided box lands on solution; check phase boundary; check em dash
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        it = p.get("input_type")
        sol = p.get("solutions")
        gs = p.get("guided_steps")
        if it=="multiple_choice":
            if gs: issues.append(f"{tier}[{i}] MC has guided_steps")
            continue
        if not gs:
            issues.append(f"{tier}[{i}] no guided_steps"); continue
        # final box answer
        boxes=[s for s in gs if "answer" in s]
        last=boxes[-1]["answer"]
        if sol and abs(float(last)-float(sol[0]))>1e-9:
            issues.append(f"{tier}[{i}] final box {last} != solution {sol[0]}")
        # phase boundary
        pidx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not pidx:
            issues.append(f"{tier}[{i}] no phase boundary")
        else:
            b=pidx[0]
            before=len([s for s in gs[:b] if "answer" in s])
            after=len([s for s in gs[b:] if "answer" in s])
            if before<1: issues.append(f"{tier}[{i}] <1 box before phase")
            if after<2: issues.append(f"{tier}[{i}] <2 live boxes after phase ({after})")

# em dash scan on student-facing
def scan(obj,path):
    if isinstance(obj,str):
        if "—" in obj: issues.append(f"EM DASH at {path}: {obj[:60]}")
    elif isinstance(obj,dict):
        for k,v in obj.items():
            if k=="note": continue
            scan(v,f"{path}.{k}")
    elif isinstance(obj,list):
        for j,v in enumerate(obj): scan(v,f"{path}[{j}]")
scan(live,"")

# chart y=x^2 points check where display mentions y = x^2
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        disp=p.get("display","")
        ch=p.get("chart")
        if ch and "x^2" in disp.replace(" ",""):
            for pt in ch["data"]["datasets"][0]["data"]:
                if abs(pt["y"]-pt["x"]**2)>1e-9:
                    issues.append(f"{tier}[{i}] chart pt {pt} not on y=x^2")

print("ISSUES:" if issues else "ALL CLEAN")
for x in issues: print(" -",x)
