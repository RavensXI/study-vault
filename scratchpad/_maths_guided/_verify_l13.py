# -*- coding: utf-8 -*-
"""Independent fresh-solve verification of every problem, box, and expect."""
import json, io, re

pd = json.load(io.open("lesson_algebra-L13.json", encoding="utf-8"))
pb = pd["problem_bank"]
errors = []

def nth_term(seq):
    d = seq[1] - seq[0]
    c = seq[0] - d
    return d, c

# ---- fresh-solve every bank problem (independent), compare stored solution
def opt_val(p, idx):
    return p["options"][idx]

checks = []

# BRONZE
# B0 2,5,8,11 -> 3n-1 idx0
checks.append(("bronze[0]", nth_term([2,5,8,11]), (3,-1), 0))
# B1 6,10,14,18 -> 4n+2 idx0
checks.append(("bronze[1]", nth_term([6,10,14,18]), (4,2), 0))
# B2 1,4,7,10 -> 3n-2 idx1
checks.append(("bronze[2]", nth_term([1,4,7,10]), (3,-2), 1))
# B3 7,12,17,22 -> 5n+2 idx0
checks.append(("bronze[3]", nth_term([7,12,17,22]), (5,2), 0))
for tag, got, exp, idx in checks:
    if got != exp:
        errors.append(f"{tag} nth term {got} != {exp}")

# B0-B3, B5, B7 correct option index check against stored solutions
def check_mc(path, seq, correct_formula_str):
    tier, i = path.split("[")
    i = int(i[:-1])
    p = pb[tier][i]
    idx = p["solutions"][0]
    if opt_val(p, idx) != correct_formula_str:
        errors.append(f"{path} stored idx {idx} = {opt_val(p,idx)!r} != {correct_formula_str!r}")

check_mc("bronze[0]", None, "\\(3n - 1\\)")
check_mc("bronze[1]", None, "\\(4n + 2\\)")
check_mc("bronze[2]", None, "\\(3n - 2\\)")
check_mc("bronze[3]", None, "\\(5n + 2\\)")
check_mc("bronze[5]", None, "\\(2n + 1\\)")   # 3,5,7,9
check_mc("bronze[7]", None, "\\(5n + 5\\)")   # 10,15,20,25

# B4 single_value: 10th term of 2n+3 = 23
if pb["bronze"][4]["solutions"][0] != 2*10+3:
    errors.append("B4 sol wrong")

# B6 (new MC): first three of 4n-1 = 3,7,11 idx0
b6 = pb["bronze"][6]
if b6["options"][b6["solutions"][0]] != "\\(3, 7, 11\\)":
    errors.append("B6 correct option mismatch")
# expects: 4n only = 4,8,12 (idx1); n=0 start = -1,3,7 (idx3)
if b6["options"][1] != "\\(4, 8, 12\\)": errors.append("B6 opt1")
if b6["options"][3] != "\\(-1, 3, 7\\)": errors.append("B6 opt3")

# SILVER
check_mc("silver[0]", None, "\\(-3n + 23\\)")  # 20,17,14,11
check_mc("silver[1]", None, "\\(-7n + 57\\)")  # 50,43,36,29
check_mc("silver[3]", None, "\\(4n - 5\\)")    # -1,3,7,11
# S2 15th of 4,9,14,19: d=5,c=-1 ->5n-1, T15=74
d,c=nth_term([4,9,14,19]);
if d!=5 or c!=-1 or 5*15-1!=74: errors.append("S2 calc")
if pb["silver"][2]["solutions"][0]!=74: errors.append("S2 sol")
# S4 41 in 2,5,8,11: 3n-1=41 -> n=14
if (41+1)//3 != 14 or 3*14-1!=41: errors.append("S4 calc")
if pb["silver"][4]["solutions"][0]!=14: errors.append("S4 sol")
# S5 new: 31,25,19,13 -> -6n+37 idx0
d,c=nth_term([31,25,19,13])
if d!=-6 or c!=37: errors.append(f"S5 nth {d},{c}")
s5=pb["silver"][5]
if s5["options"][s5["solutions"][0]]!="\\(-6n + 37\\)": errors.append("S5 correct opt")
# verify all four terms
for n,t in zip([1,2,3,4],[31,25,19,13]):
    if -6*n+37 != t: errors.append(f"S5 term {n}")
# S6 how many of 5,8,11 <50: 3n+2<50 -> n<16 -> 15
d,c=nth_term([5,8,11]);
if d!=3 or c!=2: errors.append("S6 nth")
cnt=len([n for n in range(1,1000) if 3*n+2<50])
if cnt!=15 or pb["silver"][6]["solutions"][0]!=15: errors.append(f"S6 count {cnt}")

# GOLD
# G0 3n+7=100 -> 31
if (100-7)//3!=31 or 3*31+7!=100 or pb["gold"][0]["solutions"][0]!=31: errors.append("G0")
# G1 4n+1=3n+5 -> 4
if not(4*4+1==3*4+5==17) or pb["gold"][1]["solutions"][0]!=4: errors.append("G1")
# G2 sum first5 2n+1 = 3+5+7+9+11=35
if sum(2*n+1 for n in range(1,6))!=35 or pb["gold"][2]["solutions"][0]!=35: errors.append("G2")
# G3 3rd=11,7th=27 -> 4n-1 idx0
g3=pb["gold"][3]
d=(27-11)//(7-3); cc=11-d*3
if d!=4 or cc!=-1: errors.append("G3 nth")
if g3["options"][g3["solutions"][0]]!="\\(4n - 1\\)": errors.append("G3 opt")
# G4 first >200 in 3,8,13,18: 5n-2>200 -> n=41 -> 203
d,c=nth_term([3,8,13,18])
n=min(k for k in range(1,1000) if d*k+c>200)
if d!=5 or c!=-2 or n!=41 or d*n+c!=203 or pb["gold"][4]["solutions"][0]!=203: errors.append("G4")

print("Problem/solution checks:", "OK" if not errors else errors)

# ---- verify every guided_steps / teach / opener box numerically continuous & final lands on solution
# We re-derive expected box answers from the pre-text arithmetic where possible by eval-ing the visible sum.
def eval_expr(s):
    # extract the arithmetic expression right before '=' at end of pre
    s2 = s.replace("×","*").replace("÷","/").replace("−","-").replace("−","-")
    m = re.search(r"([-()0-9\.\s\*/\+]+)=\s*$", s2)
    if not m: return None
    expr = m.group(1).strip()
    # guard: must contain an operator
    if not re.search(r"[\*/\+\-]", expr.strip("-() ")):
        # could be like "y = " with nothing; skip
        pass
    try:
        return eval(expr, {"__builtins__":{}}, {})
    except Exception:
        return None

box_errs=[]
def check_walk(steps, tag):
    for i,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre=st.get("pre","")
        ev=eval_expr(pre)
        ans=st["answer"]
        if ev is not None and abs(ev-ans)>1e-9:
            box_errs.append(f"{tag}[{i}] pre-arith {ev} != answer {ans} :: {pre!r}")

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if gs: check_walk(gs, f"{tier}[{i}].gs")
        # last box must equal a solution value (for single_value)
        if gs and p.get("input_type")!="multiple_choice":
            live=[s for s in gs if s.get("answer") is not None]
            # final check box answer should equal solution OR the check target
check_walk(pd["guided"]["opener"]["steps"], "opener")
for tier in ("bronze","silver","gold"):
    check_walk(pd["guided"]["teach"][tier]["steps"], f"teach.{tier}")

print("Box arithmetic (auto-parsed):", "OK" if not box_errs else box_errs)

# ---- misconception expects must NOT equal correct answer; report all expects for manual eyeball
print("\n-- misconception expects --")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"]
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            flag=""
            if e is not None and isinstance(e,(int,float)) and len(sol)==1 and abs(float(e)-sol[0])<0.011:
                flag=" <<< EQUALS SOLUTION!"
            print(f"{tier}[{i}].m[{j}] pattern={m.get('pattern')} expect={e} sol={sol}{flag}")
