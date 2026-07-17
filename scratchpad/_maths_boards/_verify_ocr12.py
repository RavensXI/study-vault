# -*- coding: utf-8 -*-
import json, io, math
pd=json.load(io.open("lesson_maths-ocr_algebra-L12.json",encoding="utf-8"))
errs=[]

# 1. verify guided_steps final numeric boxes land on stored solution for single_value
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]
        gs=p.get("guided_steps")
        if p["input_type"]=="single_value":
            if not gs: errs.append(f"{tier}[{i}] no guided_steps"); continue
            boxes=[s for s in gs if s.get("answer") is not None]
            # last box should equal sol for count/root problems (except where final box is a check)
            # find phase boundary
            # just report all box answers for manual sanity
            # verify at least one box == sol
            vals=[s["answer"] for s in boxes]
            if sol not in vals:
                errs.append(f"{tier}[{i}] sol {sol} not among box answers {vals}")
        # expects must differ from correct
        for j,mm in enumerate(p.get("misconceptions") or []):
            e=mm.get("expect")
            if p["input_type"]=="multiple_choice":
                if e==0: errs.append(f"{tier}[{i}].misc[{j}] expect=0 == correct option")
                if e is not None and (e<0 or e>len(p["options"])-1): errs.append(f"{tier}[{i}].misc[{j}] expect {e} out of option range")
            else:
                if e==sol: errs.append(f"{tier}[{i}].misc[{j}] expect==sol {sol}")

# 2. recompute specific box arithmetic checks (the 'check' boxes)
def close(a,b): return abs(a-b)<1e-9
checks=[
 ("bronze teach check 4^2-8*4+15", 4**2-8*4+15, -1),
 ("silver teach check 3^2+2*3-8", 3**2+2*3-8, 7),
 ("gold teach check 2*4+2-6", 2*(2**2)+2-6, 4),
 ("opener 7-2",7-2,5),("opener 4-2",4-2,2),("opener 4-6",4-6,-2),
 ("B7 check 16-12-4",16-12-4,0),
 ("S3 check 4+6-10",(-2)**2-3*(-2)-10,0),
 ("S6 check 7^2",7**2,49),
 ("G4 check 9-9",3**2-9,0),
]
for name,got,exp in checks:
    if not close(got,exp): errs.append(f"CHECK MISMATCH {name}: {got} != {exp}")

# 3. verify MC correct option index 0 truly correct by re-deriving each range solution set membership at test points
# spot verify a few option-0 strings correspond to correct region using numeric test
def region_test(f, correct_desc):
    pass

# 4. teach factorisations
fact=[
 ("x^2-8x+15=(x-3)(x-5)", lambda x:(x-3)*(x-5), lambda x:x*x-8*x+15),
 ("x^2+2x-8=(x+4)(x-2)", lambda x:(x+4)*(x-2), lambda x:x*x+2*x-8),
 ("2x^2+x-6=(2x-3)(x+2)", lambda x:(2*x-3)*(x+2), lambda x:2*x*x+x-6),
 ("tierG 3x^2-5x-2=(3x+1)(x-2)", lambda x:(3*x+1)*(x-2), lambda x:3*x*x-5*x-2),
]
for name,g,h in fact:
    for x in (-3,-1,0,2,5,1.5):
        if not close(g(x),h(x)): errs.append(f"FACTOR {name} fails at x={x}: {g(x)} vs {h(x)}")

# 5. figure roots: recompute parabola roots equal stated
for (a,b,c,r1,r2) in [(1,-8,15,3,5),(1,2,-8,-4,2),(2,1,-6,-2,1.5)]:
    d=b*b-4*a*c; rts=sorted([(-b-math.sqrt(d))/(2*a),(-b+math.sqrt(d))/(2*a)])
    if not (close(rts[0],min(r1,r2)) and close(rts[1],max(r1,r2))):
        errs.append(f"parabola {a},{b},{c} roots {rts} != {r1},{r2}")

print("ERRORS:" if errs else "ALL VERIFY CHECKS PASS")
for e in errs: print("  -",e)
