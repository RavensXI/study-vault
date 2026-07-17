# -*- coding: utf-8 -*-
import json, io, math
pd = json.load(io.open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\lesson_maths-eduqas_ratio-proportion-L05.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# Independent fresh-solve of each problem: (tier, idx, computed_answer)
# Derived by hand from each display, recomputed here from raw parameters.
def d(a,b): return a/b
solve = {
 ("bronze",0): 3*25,                 # k=12/4=3; y=3*25
 ("bronze",1): 45/9,                 # k
 ("bronze",2): 4*9,                  # y=4*3^2
 ("bronze",3): (48/16)*36,           # k=3; y=3*36
 ("bronze",4): math.sqrt(32/(50/25)),# k=2; 32=2x^2 -> x
 ("bronze",5): (6/3)*5,              # k=2; y=2*5
 ("bronze",6): math.sqrt(108/3),     # x^2=36 -> x
 ("bronze",7): 56/8,                 # k
 ("silver",0): (5*4)/16,             # k=20; y=20/16
 ("silver",1): (40/8)*27,            # k=5; y=5*27
 ("silver",2): (3*8)/4,              # k=24; x=24/4
 ("silver",3): (12/4)*10,            # k=3; y=3*10
 ("silver",4): 3**2,                 # multiplier 3^2
 ("silver",5): math.sqrt((36*1)/4),  # k=36; x^2=9 -> x
 ("silver",6): (20*4)/16,            # k=80; F=80/16
 ("gold",0): 0,                      # MC: correct index 0 (=9b)
 ("gold",1): (10*2)/4,               # k=20; y=20/4
 ("gold",2): math.sqrt((100*9)/25),  # k=900; d^2=36 -> d
 ("gold",3): 2**3,                   # n = 2^3 = 8
 ("gold",4): (14/(10/5))**2,         # k=2; sqrtL=7; L=49
}

for tier in ("bronze","silver","gold"):
    seen_sv = {}
    for i,p in enumerate(pb[tier]):
        sol = p["solutions"][0]
        comp = solve[(tier,i)]
        if abs(comp - sol) > 1e-9:
            errs.append(f"{tier}[{i}] fresh-solve {comp} != stored {sol}")
        # final box lands on solution (single_value only)
        if p.get("input_type") != "multiple_choice":
            boxes = [s for s in p.get("guided_steps",[]) if s.get("answer") is not None]
            if boxes:
                fb = boxes[-1]["answer"]
                # final box may be a check that rebuilds the given, not the answer;
                # ensure SOME box equals the solution
                if not any(abs(b["answer"]-sol)<1e-9 for b in boxes):
                    errs.append(f"{tier}[{i}] no guided box equals solution {sol}")
            # duplicate single_value solutions within tier
            key = round(sol,6)
            if key in seen_sv:
                errs.append(f"{tier}[{i}] DUP single_value solution {sol} (also {tier}[{seen_sv[key]}])")
            seen_sv[key] = i
        # misconception expects must not equal correct answer
        for j,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is not None and p.get("input_type")!="multiple_choice" and abs(float(e)-sol)<1e-9:
                errs.append(f"{tier}[{i}].misc[{j}] expect==answer")

# recompute EVERY guided box arithmetically where the pre encodes 'A op B ='
import re
def check_walk(steps, path):
    for i,s in enumerate(steps):
        a = s.get("answer")
        if a is None: continue
        pre = s.get("pre","")
        # find last 'number OP number =' pattern
        m = re.findall(r'(\d+\.?\d*)\s*([×x÷*/+\-−])\s*(\d+\.?\d*)\s*=\s*$', pre)
        if m:
            x,op,y = m[-1]
            x,y=float(x),float(y)
            val = {"×":x*y,"x":x*y,"*":x*y,"÷":x/y,"/":x/y,"+":x+y,"-":x-y,"−":x-y}[op]
            if abs(val-a)>1e-9:
                errs.append(f"{path}[{i}] pre says {x}{op}{y}={a} but ={val}")

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        check_walk(p.get("guided_steps",[]), f"{tier}[{i}].gs")
for tier in ("bronze","silver","gold"):
    check_walk(pd["guided"]["teach"][tier]["steps"], f"teach.{tier}")
check_walk(pd["guided"]["opener"]["steps"], "opener")

# tier_guide word budgets + method_card
def words(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
for t in ("bronze","silver","gold"):
    tot = sum(words(x) for x in pd["tier_guides"][t]["steps"])
    print(f"tier_guide {t}: {tot} words")
print("method_card content words:", words(pd["method_card"]["content"]))

if errs:
    print("\nERRORS:")
    for e in errs: print("  -", e)
else:
    print("\nALL CHECKS CLEAN: fresh-solve, boxes, expects, dup-check, arithmetic")
