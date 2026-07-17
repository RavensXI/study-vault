# -*- coding: utf-8 -*-
import json, re
from fractions import Fraction

live = json.load(open("_CHK_psL02b_live.json", encoding="utf-8"))
pd = live["practice_data"]

findings = []

# 1) EM DASH scan (U+2014) in student-facing strings
EMDASH = "—"
def walk(obj, path):
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k == "note":  # internal exempt
                continue
            walk(v, path+"."+k)
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if EMDASH in obj:
            findings.append(("EMDASH", path, obj[:60]))
walk(pd, "practice_data")

# 2) recompute simple guided box arithmetic where pre contains "a OP b ="
opre = re.compile(r'(-?\d+\.?\d*)\s*([+\-−×x*÷/])\s*(-?\d+\.?\d*)\s*=\s*$')
def check_boxes(steps, path):
    for i,s in enumerate(steps):
        if "answer" not in s: continue
        pre = (s.get("pre") or "")
        # normalise
        m = opre.search(pre.replace("×","*").replace("−","-").replace("÷","/").replace("x","*"))
        if m:
            a=float(m.group(1)); op=m.group(2); b=float(m.group(3))
            if op in "+": r=a+b
            elif op=="-": r=a-b
            elif op in "*": r=a*b
            elif op=="/": r=a/b
            exp=s["answer"]
            if abs(r-exp) > 1e-6:
                findings.append(("BOX_ARITH", f"{path}[{i}]", f"pre='{pre}' computes {r} but answer={exp}"))

# gather all guided_steps
pb = pd["problem_bank"]
for tier in ["gold","bronze","silver"]:
    for idx,prob in enumerate(pb[tier]):
        gs = prob.get("guided_steps",[])
        check_boxes(gs, f"{tier}[{idx}].guided_steps")
        # verify final numeric boxes land on solutions for single_value
        sol = prob.get("solutions")
        it = prob.get("input_type")
        # last answer box
        ans_boxes=[s["answer"] for s in gs if "answer" in s]
        # for single_value, the substitute box(es) should include the solution
        if it=="single_value" and sol:
            if sol[0] not in ans_boxes:
                findings.append(("SOL_NOT_IN_BOXES", f"{tier}[{idx}]", f"sol={sol} boxes={ans_boxes}"))

# teach + opener boxes
for tier in ["gold","bronze","silver"]:
    check_boxes(pd["guided"]["teach"][tier]["steps"], f"teach.{tier}.steps")
check_boxes(pd["guided"]["opener"]["steps"], "opener.steps")

# 3) fraction simplification sanity for fraction-type solutions
for tier in ["gold","bronze","silver"]:
    for idx,prob in enumerate(pb[tier]):
        if prob.get("input_type")=="fraction":
            sol=prob["solutions"]
            if len(sol)==2:
                fr=Fraction(sol[0],sol[1])
                if (fr.numerator, fr.denominator)!=(sol[0],sol[1]):
                    findings.append(("FRACTION_NOT_SIMPLIFIED", f"{tier}[{idx}]", f"{sol} -> {fr}"))

print("FINDINGS:", len(findings))
for f in findings:
    print(f)
