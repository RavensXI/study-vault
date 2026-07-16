import json
live = json.load(open("_checker_live_L06.json",encoding="utf-8"))
pb = live["problem_bank"]
issues=[]
# check hints plain (no LaTeX backslash, no HTML tag) and box answers numeric
def check_walk(prob, path):
    if "hint" in prob and ("\(" in prob["hint"] or "<" in prob["hint"]):
        issues.append(f"{path}.hint has LaTeX/HTML")
    for j,s in enumerate(prob.get("guided_steps",[])):
        if "answer" in s and not isinstance(s["answer"],(int,float)):
            issues.append(f"{path}.guided_steps[{j}].answer non-numeric: {s['answer']!r}")
        if "hint" in s and ("\(" in s["hint"] or "<" in s["hint"]):
            issues.append(f"{path}.guided_steps[{j}].hint has LaTeX/HTML")
for tier in ["bronze","silver","gold"]:
    for i,prob in enumerate(pb[tier]):
        check_walk(prob, f"{tier}[{i}]")
# teach walks numeric
for tier,t in live["guided"]["teach"].items():
    for j,s in enumerate(t["steps"]):
        if "answer" in s and not isinstance(s["answer"],(int,float)):
            issues.append(f"teach.{tier}.steps[{j}] non-numeric")
# opener numeric
for j,s in enumerate(live["guided"]["opener"]["steps"]):
    if "answer" in s and not isinstance(s["answer"],(int,float)):
        issues.append(f"opener.steps[{j}] non-numeric")
print("ISSUES:", issues if issues else "NONE")

# verify every bank problem has exactly one phase:substitute and >=2 live boxes after
for tier in ["bronze","silver","gold"]:
    for i,prob in enumerate(pb[tier]):
        steps=prob.get("guided_steps",[])
        pidx=[j for j,s in enumerate(steps) if s.get("phase")=="substitute"]
        if prob.get("input_type")!="multiple_choice" and not steps:
            print(f"{tier}[{i}] NO guided_steps")
            continue
        if len(pidx)!=1:
            print(f"{tier}[{i}] phase count = {len(pidx)}")
            continue
        p=pidx[0]
        live_boxes=sum(1 for s in steps[p:] if "answer" in s)
        before=sum(1 for s in steps[:p] if "answer" in s)
        if before<1 or live_boxes<2:
            print(f"{tier}[{i}] before={before} live={live_boxes}")
print("boundary check done")
