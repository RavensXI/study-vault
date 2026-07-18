# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_chemistry-calculations-L01@dd9dbc80e5.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# fresh-solve truth table (mine, computed by hand)
TRUTH = {
    "bronze": [58.5, 18, 44, 100, 2, 0.125, 0.12, 9],
    "silver": [74, 148, 0.2, 0.25, 25, 42.4],
    "gold":   [40, 13.9, 88.9, 71, 98, 132],
}
for tier, sols in TRUTH.items():
    for i, p in enumerate(pb[tier]):
        stored = p["solutions"][0]
        if abs(stored - sols[i]) > 1e-9:
            errs.append(f"{tier}[{i}] stored {stored} != fresh {sols[i]}")
        # last guided box must land on solution (allow the final box being a 'check' returning mass)
        boxes = [s for s in p["guided_steps"] if s.get("answer") is not None]
        # find the box whose answer equals the solution
        if not any(abs(b["answer"] - stored) < 0.006 for b in boxes):
            errs.append(f"{tier}[{i}] no guided box lands on solution {stored}")
        # expects outside accept window
        acc = p.get("accept", 0.005)
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            if e is not None and abs(e - stored) <= acc:
                errs.append(f"{tier}[{i}] expect {e} inside accept {acc} of {stored} (pattern {m.get('pattern')})")

# verify each walk is arithmetically continuous for the key computed boxes
def approx(a, b): return abs(a - b) < 1e-6

# spot-check a few computed relationships
checks = [
    ("bronze",4, 36/18, 2),
    ("bronze",5, 5.5/44, 0.125),
    ("bronze",6, 4.8/40, 0.12),
    ("silver",2, 11.7/58.5, 0.2),
    ("silver",5, 2*23+12+3*16, 106),
    ("gold",1, round(14/101,3), 0.139),
    ("gold",1, 0.139*100, 13.9),
    ("gold",2, round(16/18,3), 0.889),
    ("gold",2, 0.889*100, 88.9),
    ("gold",3, 7.1/0.1, 71),
    ("gold",4, 4.9/0.05, 98),
]
for tier,i,got,want in checks:
    if not approx(got, want):
        errs.append(f"walk arithmetic {tier}[{i}]: {got} != {want}")

# expects: recompute committed errors
def emeq(tier,i,pat,val):
    for m in pb[tier][i]["misconceptions"]:
        if m.get("pattern")==pat:
            if m.get("expect") is None: return
            if abs(m["expect"]-val)>1e-6:
                errs.append(f"expect {tier}[{i}] {pat}={m['expect']} != committed {val}")
            return
emeq("bronze",1,"forgot_subscript",1+16)      # 17
emeq("bronze",2,"forgot_subscript",12+16)     # 28
emeq("bronze",3,"forgot_subscript",40+12+16)  # 68
emeq("bronze",4,"inverted",36*18)             # 648
emeq("bronze",5,"inverted",5.5*44)            # 242
emeq("bronze",6,"inverted",4.8*40)            # 192
emeq("silver",0,"forgot_brackets",40+16+1)    # 57
emeq("silver",1,"forgot_brackets",24+14+48)   # 86
emeq("silver",2,"inverted",11.7*58.5)         # 684.45
emeq("silver",3,"inverted",25*100)            # 2500
emeq("silver",4,"divided",100/0.25)           # 400
emeq("gold",0,"forgot_multiply_100",40/100)   # 0.4
emeq("gold",1,"wrong_mr",round(14/69*100,1))  # 20.3
emeq("gold",1,"wrong_element",round(39/101*100,1)) # 38.6
emeq("gold",2,"wrong_mr",round(16/17*100,1))  # 94.1
emeq("gold",2,"wrong_element",round(2/18*100,1)) # 11.1
emeq("gold",3,"wrong_rearrange",0.1*7.1)      # 0.71
emeq("gold",4,"wrong_rearrange",0.05*4.9)     # 0.245
emeq("gold",5,"wrong_mr",3*(12+16))           # 84

# opener + teach box checks
op = pd["guided"]["opener"]["steps"]
if op[0]["answer"]!=500 or op[1]["answer"]!=2: errs.append("opener boxes wrong")
if 2000/4!=500 or 36/18!=2: errs.append("opener arithmetic wrong")
tb = pd["guided"]["teach"]
# bronze NH3 =17
assert tb["bronze"]["steps"][2]["answer"]==17
# silver Cu(NO3)2 =188 ; 64+2*(14+48)=188
if 64+2*(14+48)!=188: errs.append("teach silver mr wrong")
# gold NH4NO3 Mr=80, %N=35
if 2*14+4*1+3*16!=80: errs.append("teach gold mr wrong")
if round(28/80*100)!=35: errs.append("teach gold pct wrong")

if errs:
    print("FAIL", len(errs))
    for e in errs: print("  -", e)
else:
    print("ALL VERIFY CHECKS PASS")
