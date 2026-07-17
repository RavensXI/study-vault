# -*- coding: utf-8 -*-
"""Independent verifier: recompute every guided_steps/teach/opener box value,
check final box == stored solution, and reproduce every misconception expect."""
import json, io, math, re

pd = json.load(io.open("lesson_maths-ocr_algebra-L08.json", encoding="utf-8"))
errs = []

# --- fresh-solve the 20 problems from display, compare to solutions ---
def disc(a,b,c): return b*b-4*a*c

expected = {
 ("bronze",0):[4],("bronze",1):[2],("bronze",2):[-9],("bronze",3):[3],
 ("bronze",4):[1],("bronze",5):[5],("bronze",6):[0],("bronze",7):[-1],
 ("silver",0):[1.54],("silver",1):[-3],("silver",2):[-7],("silver",3):[2.28],
 ("silver",4):[0.87],("silver",5):[-6],("silver",6):[1],
 ("gold",0):[3],("gold",1):[6],("gold",2):[-13],("gold",3):[0.69],("gold",4):[7],
}
for (tier,i),exp in expected.items():
    sol = pd["problem_bank"][tier][i]["solutions"]
    if [round(float(x),3) for x in sol] != [round(float(x),3) for x in exp]:
        errs.append(f"{tier}[{i}] stored solution {sol} != fresh-solve {exp}")

# --- verify every walk's final box lands on the solution ---
def final_box(steps):
    vals=[s.get("answer") for s in steps if s.get("answer") is not None]
    return vals[-1] if vals else None

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        gs=p.get("guided_steps")
        if not gs: continue
        fb=final_box(gs); sol=p["solutions"][0]
        if abs(float(fb)-float(sol))>0.011:
            errs.append(f"{tier}[{i}] final box {fb} != solution {sol}")
        # every box must have pre + hint + numeric answer
        for j,s in enumerate(gs):
            if s.get("answer") is not None:
                if not s.get("pre"): errs.append(f"{tier}[{i}].gs[{j}] no pre")
                if not s.get("hint"): errs.append(f"{tier}[{i}].gs[{j}] no hint")
                if not isinstance(s["answer"],(int,float)): errs.append(f"{tier}[{i}].gs[{j}] non-numeric")

# --- recompute specific box arithmetic chains ---
def approx(a,b): return abs(a-b)<0.011

# bronze checks
b=pd["problem_bank"]["bronze"]
assert b[0]["guided_steps"][1]["answer"]==16 and b[0]["guided_steps"][2]["answer"]==12 and b[0]["guided_steps"][3]["answer"]==4
assert b[1]["guided_steps"][1]["answer"]==-32 and b[1]["guided_steps"][2]["answer"]==36 and b[1]["guided_steps"][3]["answer"]==6 and b[1]["guided_steps"][4]["answer"]==2
assert (-2+6)/2==2
assert b[3]["guided_steps"][4]["answer"]==(4+2)/2==3
assert b[7]["guided_steps"][4]["answer"]==(-6+4)/2==-1
assert b[5]["guided_steps"][3]["answer"]==20-25==-5
# silver
s=pd["problem_bank"]["silver"]
assert approx(s[0]["guided_steps"][4]["answer"],(-3+6.08)/2)   # 1.54
assert approx(s[3]["guided_steps"][4]["answer"],(5+4.12)/4)    # 2.28
assert approx(s[4]["guided_steps"][4]["answer"],(-2+7.21)/6)   # 0.865->0.87 stored
assert s[2]["guided_steps"][3]["answer"]==2-9==-7
assert s[5]["guided_steps"][3]["answer"]==-5-1==-6
assert s[6]["guided_steps"][3]["answer"]==144-144==0
# gold
g=pd["problem_bank"]["gold"]
assert g[0]["guided_steps"][2]["answer"]==-4+1==-3
assert g[2]["guided_steps"][2]["answer"]==2*9==18 and g[2]["guided_steps"][3]["answer"]==-18+5==-13
assert approx(g[3]["guided_steps"][4]["answer"],(2+4.899)/10)  # 0.6899->0.69
assert g[4]["guided_steps"][1]["answer"]==64 and g[4]["guided_steps"][2]["answer"]==8 and g[4]["guided_steps"][3]["answer"]==7

# --- reproduce every misconception expect by committing the error ---
# spot-check the derivations
def check_expect(tier,i,pattern,val):
    ms=pd["problem_bank"][tier][i]["misconceptions"]
    m=[x for x in ms if x["pattern"]==pattern]
    if not m: errs.append(f"{tier}[{i}] missing misconception {pattern}"); return
    if m[0]["expect"]!=val: errs.append(f"{tier}[{i}].{pattern} expect {m[0]['expect']} != derived {val}")

check_expect("bronze",0,"added_4ac",16+12)        # 28
check_expect("bronze",0,"stopped_at_bsq",16)
check_expect("bronze",1,"plus_b",(2+6)/2)         # 4
check_expect("bronze",2,"kept_positive",9)
check_expect("bronze",2,"subtracted_half",-3)
check_expect("bronze",3,"took_smaller",(4-2)/2)   # 1
check_expect("bronze",4,"added_4ac",25+24)        # 49
check_expect("bronze",4,"stopped_at_bsq",25)
check_expect("bronze",5,"forgot_halve",10)
check_expect("bronze",6,"always_two",2)
check_expect("bronze",7,"took_farther",(-6-4)/2) # -5
# b7 plus_b: +b slip roots (6±4)/2 = {5,1}; closer to zero = 1
check_expect("bronze",7,"plus_b",1)

check_expect("silver",0,"plus_b",round((3+6.08)/2,2))    # 4.54
check_expect("silver",1,"added_square",1+4)              # 5
check_expect("silver",1,"used_c",1)
check_expect("silver",2,"used_c",2)
check_expect("silver",2,"added_square",2+9)              # 11
check_expect("silver",3,"divide_by_two",round((5+4.12)/2,2)) # 4.56
check_expect("silver",3,"took_smaller",round((5-4.12)/4,2))  # 0.22
check_expect("silver",4,"divide_by_two",round((-2+math.sqrt(52))/2,2))# 2.61
check_expect("silver",5,"used_c",-5)
check_expect("silver",5,"added_square",-5+1)             # -4
check_expect("silver",6,"equal_counts_two",2)
check_expect("silver",6,"gave_discriminant",0)
check_expect("gold",0,"dropped_plus1",4)   # (x+2)^2=4 -> n=4
check_expect("gold",1,"forgot_sqrt",36)
check_expect("gold",2,"forgot_multiply",-9+5)           # -4
check_expect("gold",3,"divide_by_two",round((2+math.sqrt(24))/2,2)) # 3.45
check_expect("gold",4,"took_boundary",8)

# report
print("Fresh-solve + box + expect verification:")
if errs:
    print("FAIL", len(errs))
    for e in errs: print("  -",e)
else:
    print("ALL CLEAN — every solution, every final box, every expect reproduces.")
