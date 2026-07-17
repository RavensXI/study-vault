import json, math
live=json.load(open("_CHK_graphsL06_LIVE.json",encoding="utf-8"))
bank=live["problem_bank"]
issues=[]

# Fresh-solve each bank problem based on display semantics (manual solutions expected)
expected={
 ("gold",0):[150],("gold",1):[300],("gold",2):[225],("gold",3):[-0.5],("gold",4):[0.5],
 ("bronze",0):[1],("bronze",1):[0],("bronze",2):[0.5],("bronze",3):[360],("bronze",4):[180],
 ("bronze",5):[90],("bronze",6):[3],("bronze",7):[-1],
 ("silver",0):[0.5],("silver",1):[-0.5],("silver",2):[0],("silver",3):[-1],("silver",4):[90],
 ("silver",5):[180],("silver",6):[2],
}
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(bank[tier]):
        exp=expected.get((tier,i))
        got=p["solutions"]
        if got!=exp:
            issues.append(f"{tier}[{i}] solution stored {got} expected {exp} :: {p['display']}")
        # final guided box must land on solution
        gs=p.get("guided_steps",[])
        boxes=[s for s in gs if "answer" in s]
        if boxes:
            last=boxes[-1]["answer"]
            if abs(float(last)-float(exp[0]))>1e-9:
                issues.append(f"{tier}[{i}] final guided box {last} != solution {exp[0]}")
        # boundary check
        phase_idx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        live_boxes_after=[s for s in gs[(phase_idx[0] if phase_idx else 0):] if "answer" in s] if phase_idx else []
        before=[s for s in gs[:phase_idx[0]] if "answer" in s] if phase_idx else []
        if not phase_idx:
            issues.append(f"{tier}[{i}] NO phase boundary")
        else:
            if len(before)<1: issues.append(f"{tier}[{i}] <1 box before boundary")
            if len(live_boxes_after)<2: issues.append(f"{tier}[{i}] <2 live boxes after boundary ({len(live_boxes_after)})")

# Verify chart points satisfy stated curve
def chk_chart(p, tier, i):
    ch=p.get("chart")
    if not ch: return
    for ds in ch["data"]["datasets"]:
        lab=ds.get("label","")
        for pt in ds["data"]:
            x,y=pt["x"],pt["y"]
            if lab=="y = sin x":
                if abs(y-round(math.sin(math.radians(x)),4))>0.002:
                    issues.append(f"{tier}[{i}] chart sin pt ({x},{y}) wrong")
            elif lab=="y = cos x":
                if abs(y-round(math.cos(math.radians(x)),4))>0.002:
                    issues.append(f"{tier}[{i}] chart cos pt ({x},{y}) wrong")
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(bank[tier]):
        chk_chart(p,tier,i)

# Teach walks final boxes
print("=== ISSUES ===")
for x in issues: print(x)
print("total:", len(issues))
