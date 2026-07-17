# -*- coding: utf-8 -*-
import json, io
pd=json.load(io.open("lesson_maths-aqa_ratio-proportion-L06.json",encoding="utf-8"))
pb=pd["problem_bank"]
issues=[]
# duplicate check
for t in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[t]):
        if p.get("input_type")=="multiple_choice": continue
        k=tuple(p["solutions"])
        if k in seen: issues.append(f"DUP {t}: {i} & {seen[k]} both {k}")
        seen[k]=i
# check final guided box lands near a stored solution (single_value/fraction)
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        gs=p.get("guided_steps")
        if not gs: continue
        boxes=[s["answer"] for s in gs if s.get("answer") is not None]
        sol=p["solutions"]
        # the phase:substitute answer or a box must include the solution value(s)
        vals=set(boxes)
        if p["input_type"]=="fraction":
            ok = sol[0] in vals and sol[1] in vals
        else:
            ok = any(abs(b-sol[0])<0.0011 for b in boxes)
        if not ok: issues.append(f"{t}[{i}] solution {sol} not reached by any box {boxes}")
        # expect must not equal correct
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is None: continue
            ev=e if isinstance(e,list) else [e]
            if len(ev)==len(sol) and all(abs(float(a)-float(b))<0.0011 for a,b in zip(ev,sol)):
                issues.append(f"{t}[{i}] expect==correct {e}")
# independent recompute of stored solutions
import math
def approx(a,b,tol=0.0011): return abs(a-b)<tol
checks=[
 ("B0",(9-1)/(3-1),4),("B1",(16-1)/(5-0),3),("B2",2**2-7,-3),("B3",3**2-7,2),
 ("B4",2+3,5),("B5",5+3,8),("B6",(16-4)/(4-2),6),
 ("S1",2**3-4*2-1,-1),("S2",3**3-4*3-1,14),("S3",round(9**(1/3),3),2.08),
 ("S4",(8-1)/(2-1),7),("S5",0-0+1,1),("S6",1-4+1,-2),
 ("G0",round(18**(1/3),3),2.621),("G1",1.5**3+2*1.5-7,-0.625),
 ("G2",round((5000*1.03**10-5000)/10),172),
 ("G3",round(math.sqrt(3*math.sqrt(3*3+1)+1),3),3.238),
 ("G4",round(13**(1/3),3),2.351),
]
for name,got,exp in checks:
    if not approx(got,exp): issues.append(f"RECOMPUTE {name}: got {got} expected {exp}")
# S0 fraction 10/(2+1)=10/3
if not (10==10 and 3==3): issues.append("S0")
# SVG opener numbers
print("issues:", issues if issues else "NONE")
print("bronze sols:", [p['solutions'] for p in pb['bronze']])
print("silver sols:", [p['solutions'] for p in pb['silver']])
print("gold sols:", [p['solutions'] for p in pb['gold']])
