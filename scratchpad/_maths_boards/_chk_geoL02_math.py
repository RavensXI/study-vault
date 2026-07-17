import json, math
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
live = json.load(open(base+"_chk_geoL02_live.json", encoding="utf-8"))
pb = live["problem_bank"]
issues=[]

def r1(x): return round(x,1)

# Independent fresh solves keyed by (tier,index)
expect_sol = {
 ("bronze",0):60, ("bronze",1):26, ("bronze",2):30, ("bronze",3):40,
 ("bronze",4):42, ("bronze",5):49, ("bronze",6):r1(2*math.pi*7), ("bronze",7):r1(math.pi*25),
 ("silver",0):r1(0.5*math.pi*36), ("silver",1):r1(120-math.pi*9), ("silver",2):8,
 ("silver",3):round(25.7/(math.pi+2)), ("silver",4):24, ("silver",5):r1(math.pi*(31.4/(2*math.pi))**2),
 ("silver",6):22,
 ("gold",0):r1(135/360*math.pi*64), ("gold",1):r1(72/360*2*math.pi*10),
 ("gold",2):round(math.pi*60+200), ("gold",3):round(math.sqrt(154/math.pi),1),
 ("gold",4):r1(math.pi*100-math.pi*36),
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]
        exp=expect_sol[(tier,i)]
        if abs(sol-exp)>0.05:
            issues.append(f"SOLUTION {tier}[{i}]: stored {sol} vs computed {exp}")
        # non-calc must be integer
        if not p.get("calculator", True) and abs(sol-round(sol))>1e-9:
            issues.append(f"NONCALC-DECIMAL {tier}[{i}]: {sol}")
        # final guided box must land on solution
        gs=p.get("guided_steps",[])
        boxes=[s for s in gs if "answer" in s]
        # find last box that equals solution? check the phase box / any
        # verify walk boxes are numeric
        for j,s in enumerate(gs):
            if "answer" in s and not isinstance(s["answer"],(int,float)):
                issues.append(f"NONNUMERIC {tier}[{i}].guided_steps[{j}]")
        # phase boundary counts
        phase_idx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        after=0
        if phase_idx:
            after=sum(1 for s in gs[phase_idx[0]:] if "answer" in s)
            before=sum(1 for s in gs[:phase_idx[0]] if "answer" in s)
            if after<2: issues.append(f"PHASE {tier}[{i}]: only {after} live boxes at/after")
            if before<1: issues.append(f"PHASE {tier}[{i}]: {before} boxes before")
        else:
            if p.get("input_type")!="multiple_choice" and gs:
                issues.append(f"NOPHASE {tier}[{i}]")
        # misconception expects reproduce - just report for manual, but check duplicate expects=solution
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and abs(e-sol)<1e-9:
                issues.append(f"EXPECT==SOL {tier}[{i}] pattern {m.get('pattern')}")
    # duplicate solutions within tier
    sols=[p["solutions"][0] for p in pb[tier]]
    dups=set(x for x in sols if sols.count(x)>1)
    if dups: issues.append(f"DUP SOLUTIONS {tier}: {dups}")

# Verify guided box arithmetic explicitly for a few flagged (all boxes: recompute chain not trivial generically)
print("SOLUTION/PHASE/STRUCTURE ISSUES:", len(issues))
for x in issues: print(" ",x)

# em dash sweep student-facing
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v,path+"/"+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o or " - " in o.replace("currentColor",""):
            if "—" in o:
                print("EMDASH:",path, o[:80])
walk(live)
print("done")
