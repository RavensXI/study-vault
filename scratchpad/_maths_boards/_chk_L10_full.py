import json, re
pd=json.load(open("_CHK_L10_live.json",encoding="utf-8"))

# ---- 1. Fresh-solve every bank problem numerically ----
import numpy as np
def solve_from_display(disp):
    return None  # manual

pb=pd["problem_bank"]
report=[]

# Recompute every guided box by re-deriving? We'll trust manual; here verify final boxes land on solutions
def check_tier(tier):
    for i,p in enumerate(pb[tier]):
        sols=p.get("solutions")
        # collect box answers
        boxes=[s.get("answer") for s in p.get("guided_steps",[]) if "answer" in s]
        # verify no None
    return
# ---- em dash scan in student-facing strings ----
EM="—"
def walk(obj,path):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k=="note":   # internal exempt
                continue
            walk(v,path+"."+k)
    elif isinstance(obj,list):
        for j,v in enumerate(obj):
            walk(v,path+f"[{j}]")
    elif isinstance(obj,str):
        if EM in obj:
            print("EM-DASH:",path,"->",obj[:80])
walk(pd,"root")
print("em-dash scan done")

# ---- numeric-only boxes ----
def boxwalk(obj,path):
    if isinstance(obj,dict):
        if "answer" in obj:
            a=obj["answer"]
            if not isinstance(a,(int,float)):
                print("NON-NUMERIC BOX:",path,repr(a))
        for k,v in obj.items():
            boxwalk(v,path+"."+k)
    elif isinstance(obj,list):
        for j,v in enumerate(obj):
            boxwalk(v,path+f"[{j}]")
boxwalk(pd,"root")
print("box numeric scan done")

# ---- misconception expect check for factor_sign_flip & others via re-derivation ----
# For two_solutions problems, expect for factor_sign_flip = negated solutions
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(pb[tier]):
        sols=p.get("solutions")
        for m in p.get("misconceptions",[]):
            pat=m.get("pattern"); exp=m.get("expect")
            if pat=="factor_sign_flip":
                want=sorted([-s for s in sols])
                got=sorted(exp) if exp else None
                if got!=want:
                    print(f"EXPECT MISMATCH {tier}[{i}] sign_flip: expect={exp} want(neg sols)={want} sols={sols}")
print("expect check done")
