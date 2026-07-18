# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_higher-calculations-L05@b2761124fc.json", encoding="utf-8"))
errs = []

# em dash check across all strings
def scan(o, p):
    if isinstance(o, dict):
        for k, v in o.items(): scan(v, p+"."+str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): scan(v, p+"[%d]"%i)
    elif isinstance(o, str) and "—" in o:
        errs.append("EMDASH "+p)
scan(pd, "pd")

# check each problem: last live boxes land on solution; expects outside accept and != correct
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i, pr in enumerate(pb[tier]):
        path = f"{tier}[{i}]"
        sols = pr["solutions"]
        it = pr.get("input_type","single_value")
        acc = pr.get("accept", 0.005)
        # verify guided_steps final numeric boxes trend and boundary math already checked by validator;
        # here confirm the walk's answer that states the solution appears among boxes
        if it != "multiple_choice":
            boxes = [st["answer"] for st in pr["guided_steps"] if st.get("answer") is not None]
            if sols[0] not in boxes:
                errs.append(f"{path} solution {sols[0]} not hit by any box; boxes={boxes}")
        # expects
        for j, mc in enumerate(pr.get("misconceptions",[])):
            e = mc.get("expect", "MISSING")
            if e == "MISSING":
                errs.append(f"{path}.mc[{j}] missing expect")
            if isinstance(e,(int,float)):
                if abs(e - sols[0]) <= acc:
                    errs.append(f"{path}.mc[{j}] expect {e} inside accept of {sols[0]} (acc {acc})")

# recompute physics answers independently
def alpha_mass(A): return A-4
def alpha_at(Z): return Z-2
def beta_at(Z): return Z+1
checks = {
 ("bronze",0):alpha_mass(226), ("bronze",1):alpha_at(88), ("bronze",2):beta_at(6),
 ("bronze",3):800/16, ("bronze",4):2000/8, ("bronze",5):alpha_mass(238),
 ("bronze",6):beta_at(82), ("bronze",7):beta_at(27),
 ("silver",0):20/4, ("silver",1):30/3, ("silver",2):alpha_mass(241),
 ("silver",3):beta_at(38), ("silver",4):50/(2**5), ("silver",5):alpha_mass(210),
 ("gold",0):52/4, ("gold",1):2**7, ("gold",3):20, ("gold",4):120/4, ("gold",5):beta_at(53),
}
for (t,i),exp in checks.items():
    got = pb[t][i]["solutions"][0]
    if abs(got-exp) > 1e-9:
        errs.append(f"{t}[{i}] stored {got} != computed {exp}")

# gold[2] must be MC with numeric solution
g2 = pb["gold"][2]
if g2.get("input_type")!="multiple_choice" or g2["solutions"]!=[1]:
    errs.append("gold[2] not converted to MC properly")

# dup solutions within tier (single_value only)
for tier in ("bronze","silver","gold"):
    seen={}
    for i,pr in enumerate(pb[tier]):
        if pr.get("input_type")=="multiple_choice": continue
        k=tuple(pr["solutions"])
        if k in seen: errs.append(f"{tier} dup solution {k} at {i} and {seen[k]}")
        seen[k]=i

# each problem has hint or equation_hint
for tier in ("bronze","silver","gold"):
    for i,pr in enumerate(pb[tier]):
        if not (pr.get("hint") or pr.get("equation_hint")):
            errs.append(f"{tier}[{i}] no hint")

print("ERRORS:", len(errs))
for e in errs: print(" -", e)
if not errs: print("ALL INDEPENDENT CHECKS PASS")
