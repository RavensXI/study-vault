# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_maths-eduqas_graphs-L03.json", encoding="utf-8"))
ok = True
def f(a,b,c,x): return a*x*x+b*x+c

# fresh-solve each single_value problem independently
checks = {
 # tier,index : expected solution
 ("bronze",0): f(1,3,2,2),       # 12
 ("bronze",1): f(1,-5,6,0),      # 6
 ("bronze",2): -7,               # y-int of x^2+4x-7
 ("bronze",3): f(1,0,-4,3),      # 5
 ("bronze",4): f(1,2,0,-1),      # -1
 ("bronze",5): 8,                # c = y-int 8
 ("bronze",7): f(1,-6,9,1),      # 4
 ("silver",0): (-1+5)/2,         # 2  TP x
 ("silver",1): f(1,-4,-5,2),     # -9 TP y at x=2
 ("silver",3): -2,               # other root of x^2-2x-8 (roots 4,-2)
 ("silver",4): f(1,3,-1,-2),     # -3
 ("silver",5): (2+6)/2,          # 4
 ("silver",6): f(2,-8,6,1),      # 0
 ("gold",0): f(-1,6,-5,3),       # 4 TP y (x=-b/2a=3)
 ("gold",1): 16,                 # k: 64-4k=0
 ("gold",2): -4,                 # (x-3)^2-4 TP y
 ("gold",3): 2,                  # -b/2a = 12/6
}
pb = pd["problem_bank"]
for (tier,i),exp in checks.items():
    got = pb[tier][i]["solutions"][0]
    if abs(got-exp) > 1e-9:
        ok=False; print("SOLUTION MISMATCH", tier, i, "stored",got,"computed",exp)

# check TP formula for silver0/1 uses roots -1,5 -> also verify roots of x^2-4x-5
import math
def roots(a,b,c):
    d=b*b-4*a*c; return ((-b-math.sqrt(d))/(2*a),(-b+math.sqrt(d))/(2*a))
assert set(round(r) for r in roots(1,-4,-5))=={-1,5}, "silver roots wrong"
assert set(round(r) for r in roots(1,-2,-8))=={4,-2}, "S3 roots wrong"
# G0 TP x
assert -6/(2*-1)==3
# G3 TP x
assert -(-12)/(2*3)==2

# verify duplicate solutions within each tier among non-MC
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[tier]):
        if p["input_type"]=="multiple_choice": continue
        k=tuple(p["solutions"])
        if k in seen:
            ok=False; print("DUP within",tier,":",k,"at",seen[k],"and",i)
        seen[k]=i

# verify every misconception expect reproduces a wrong (not equal to solution) determinate value
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"]
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is None: continue
            ev=e if isinstance(e,list) else [e]
            if len(ev)==len(sol) and all(abs(a-b)<1e-9 for a,b in zip(ev,sol)):
                ok=False; print("EXPECT==SOLUTION",tier,i,e)

# verify guided_steps last answers land on solution for single_value (final non-check box or check)
def walk_final_ok(tier,i):
    p=pb[tier][i]
    if "guided_steps" not in p: return True
    # last box answer should equal solution (check step) OR the phase solve box
    boxes=[s for s in p["guided_steps"] if s.get("answer") is not None]
    return abs(boxes[-1]["answer"]-p["solutions"][0])<1e-9 or any(abs(b["answer"]-p["solutions"][0])<1e-9 for b in boxes)
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p["input_type"]=="multiple_choice": continue
        if not walk_final_ok(tier,i):
            ok=False; print("WALK does not land on solution", tier,i,p["solutions"])

# verify S0 chart points satisfy y=x^2-4x-5 and marked roots are (-1,0),(5,0)
ch=pb["silver"][0]["chart"]
line=ch["data"]["datasets"][0]["data"]
for pt in line:
    if abs(pt["y"]-(pt["x"]**2-4*pt["x"]-5))>1e-9:
        ok=False; print("CHART point off curve",pt)
rootpts=ch["data"]["datasets"][1]["data"]
for pt in rootpts:
    if abs(pt["x"]**2-4*pt["x"]-5)>1e-9:
        ok=False; print("CHART root not on axis",pt)

# opener arch numbers: peak x=4 midpoint of 0,8; mirror of 2 about 4 is 6
assert (0+8)/2==4 and 4+(4-2)==6

print("ALL MATHS VERIFIED" if ok else "FAILURES ABOVE")
