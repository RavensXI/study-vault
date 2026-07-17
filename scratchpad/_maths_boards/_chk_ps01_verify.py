# -*- coding: utf-8 -*-
import json, re
from fractions import Fraction as F

pd = json.load(open("_CHK_ps01_LIVE.json", encoding="utf-8"))
issues = []

# ---------- 1. em dash / external ref sweep ----------
def walk_strings(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            yield from walk_strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o

for path, s in walk_strings(pd):
    if path.endswith(".note"):  # internal notes exempt from em dash rule
        continue
    if "—" in s:
        issues.append(f"EM DASH in {path}: {s[:80]}")
    if "http://" in s and "youtube" not in s and "youtu" not in s:
        pass
    # external refs in svg
    if "<svg" in s:
        for bad in ["xlink:href","<script","href=\"http","url(http","<image"]:
            if bad in s:
                issues.append(f"EXTERNAL/SCRIPT in svg {path}: {bad}")
        # hard-coded dark text fills
        for m in re.finditer(r'<text[^>]*fill="([^"]+)"', s):
            fill = m.group(1)
            if fill != "currentColor":
                issues.append(f"NON-currentColor text fill in {path}: {fill}")

# ---------- 2. reproduce every misconception expect quick sanity ----------
# (manual list of committed-error checks)
def frac(n,d): return [n,d]

checks = []
def add(label, cond):
    checks.append((label, cond))

# gold[0] one order only -> 35/132
add("gold0 expect", pd["problem_bank"]["gold"][0]["misconceptions"][0]["expect"]==[35,132])
# gold1 (2/3)^3 -> 8/27
add("gold1 expect", pd["problem_bank"]["gold"][1]["misconceptions"][0]["expect"]==[8,27])
# gold2 one path 0.3 -> 3/10
add("gold2 expect", pd["problem_bank"]["gold"][2]["misconceptions"][0]["expect"]==[3,10])
# gold3 P(no heads) 1/16
add("gold3 expect", pd["problem_bank"]["gold"][3]["misconceptions"][0]["expect"]==[1,16])
# gold4 HT only 2/9
add("gold4 expect", pd["problem_bank"]["gold"][4]["misconceptions"][0]["expect"]==[2,9])

# ---------- 3. fresh-solve solutions ----------
def solvematch(tier,i,expected):
    got = pd["problem_bank"][tier][i]["solutions"]
    add(f"{tier}[{i}] sol {got} vs {expected}", got==expected)

solvematch("gold",0,[35,66])
solvematch("gold",1,[14,55])
solvematch("gold",2,[19,50])
solvematch("gold",3,[15,16])
solvematch("gold",4,[4,9])
solvematch("bronze",0,[5,8])
solvematch("bronze",1,[1,2])
solvematch("bronze",2,[3,5])
solvematch("bronze",3,[7,12])
solvematch("bronze",4,[2,5])
solvematch("bronze",5,[3,10])
solvematch("bronze",6,[10])
solvematch("bronze",7,[2,11])
solvematch("silver",0,[1,4])
solvematch("silver",1,[4,25])
solvematch("silver",2,[5,14])
solvematch("silver",3,[3,20])
solvematch("silver",4,[3,8])
solvematch("silver",5,[7,10])
solvematch("silver",6,[27,64])

# independent recompute of the trickier ones
add("gold0 recompute", F(7,12)*F(5,11)+F(5,12)*F(7,11)==F(35,66))
add("gold1 recompute", F(8,12)*F(7,11)*F(6,10)==F(14,55))
add("gold2 recompute", F(6,10)*F(5,10)+F(4,10)*F(2,10)==F(19,50))
add("gold3 recompute", 1-F(1,2)**4==F(15,16))
add("gold4 recompute", 2*(F(2,3)*F(1,3))==F(4,9))
add("silver2 recompute", F(5,8)*F(4,7)==F(5,14))
add("silver6 recompute", F(3,4)**3==F(27,64))

# ---------- 4. completion boundary: >=1 before phase, >=2 boxes at/after ----------
def boundary(tier,i):
    steps = pd["problem_bank"][tier][i].get("guided_steps",[])
    boxes = [s for s in steps if "answer" in s]
    # index of first phase==substitute among all steps
    firstphase = None
    for idx,s in enumerate(steps):
        if s.get("phase")=="substitute":
            firstphase=idx; break
    if firstphase is None:
        return add(f"{tier}[{i}] boundary","NOPHASE"==False)
    before_boxes = [s for s in steps[:firstphase] if "answer" in s]
    after_boxes = [s for s in steps[firstphase:] if "answer" in s]
    add(f"{tier}[{i}] boundary before>=1 ({len(before_boxes)}) after>=2 ({len(after_boxes)})",
        len(before_boxes)>=1 and len(after_boxes)>=2)

for t in ["gold","bronze","silver"]:
    for i in range(len(pd["problem_bank"][t])):
        if isinstance(pd["problem_bank"][t][i],dict) and pd["problem_bank"][t][i].get("input_type")!="multiple_choice":
            boundary(t,i)

# ---------- 5. every box numeric ----------
def numeric_boxes():
    for t in ["gold","bronze","silver"]:
        for i,p in enumerate(pd["problem_bank"][t]):
            if not isinstance(p,dict): continue
            for j,s in enumerate(p.get("guided_steps",[])):
                if "answer" in s and not isinstance(s["answer"],(int,float)):
                    issues.append(f"NON-NUMERIC box {t}[{i}].guided_steps[{j}]: {s['answer']}")
    for tier,walk in pd["guided"]["teach"].items():
        for j,s in enumerate(walk["steps"]):
            if "answer" in s and not isinstance(s["answer"],(int,float)):
                issues.append(f"NON-NUMERIC teach.{tier}[{j}]")
    for j,s in enumerate(pd["guided"]["opener"]["steps"]):
        if "answer" in s and not isinstance(s["answer"],(int,float)):
            issues.append(f"NON-NUMERIC opener[{j}]")
numeric_boxes()

print("=== check results ===")
fails=0
for label,cond in checks:
    if cond is not True:
        print("FAIL:", label); fails+=1
print(f"{len(checks)} checks, {fails} failed")
print("=== issues ===")
for x in issues: print(x)
print(f"total issues: {len(issues)}")
