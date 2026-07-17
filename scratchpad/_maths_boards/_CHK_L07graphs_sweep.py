import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_L07graphs_live.json", encoding="utf-8"))

issues=[]
# em dash scan in student-facing strings (skip internal 'note')
def scan(obj, path):
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k=="note": continue
            scan(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            scan(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if "—" in obj or "–" in obj:
            issues.append(f"DASH at {path}: {obj[:80]}")
scan(pd, "pd")

# completion boundary check for single_value problems
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        if p.get("input_type")=="multiple_choice": continue
        gs=p.get("guided_steps",[])
        if not gs:
            issues.append(f"{tier}[{i}] no guided_steps"); continue
        # find first phase substitute index
        bidx=None
        boxes_before=0; boxes_after=0
        for j,s in enumerate(gs):
            isbox = "answer" in s
            if s.get("phase")=="substitute" and bidx is None:
                bidx=j
            if isbox:
                if bidx is None: boxes_before+=1
                else: boxes_after+=1
        if bidx is None:
            issues.append(f"{tier}[{i}] no phase:substitute boundary")
        else:
            if boxes_before<1: issues.append(f"{tier}[{i}] <1 box before boundary")
            if boxes_after<2: issues.append(f"{tier}[{i}] <2 boxes after boundary ({boxes_after})")
        # last box must equal solution
        lastbox=[s for s in gs if "answer" in s]
        if lastbox and p.get("solutions"):
            # the box that lands on solution should exist
            sol=p["solutions"][0]
            vals=[s["answer"] for s in lastbox]
            if sol not in vals:
                issues.append(f"{tier}[{i}] solution {sol} not among box answers {vals}")

# verify multiple_choice solution index in range and misconception expects in range
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        if p.get("input_type")=="multiple_choice":
            opts=p.get("options",[])
            sol=p["solutions"][0]
            if not (0<=sol<len(opts)):
                issues.append(f"{tier}[{i}] MC solution index {sol} out of range")
            for m in p.get("misconceptions",[]):
                e=m.get("expect")
                if e is not None and not (0<=e<len(opts)):
                    issues.append(f"{tier}[{i}] MC expect {e} out of range")
                if e is not None and e==sol:
                    issues.append(f"{tier}[{i}] MC expect equals correct answer {e}")

print("ISSUES:", len(issues))
for x in issues: print(" ", x)
