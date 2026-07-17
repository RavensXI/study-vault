# -*- coding: utf-8 -*-
import json, re
from fractions import Fraction as F

live = json.load(open("_ADVCHK_L07eq_live.json", encoding="utf-8"))
pb = live["problem_bank"]

# Manually transcribe each problem's quadratic (a,b,c after rearrange to =0),
# what is asked, and the stored solution. Then verify independently.
# We parse roots via quadratic formula in exact fractions.
import math
def roots(a,b,c):
    disc = b*b-4*a*c
    s = math.isqrt(disc) if disc>=0 else None
    assert s is not None and s*s==disc, f"non-perfect disc {disc} for {a},{b},{c}"
    r1 = F(-b+s,2*a); r2 = F(-b-s,2*a)
    return sorted([r1,r2])

problems = {
 # tier: list of (a,b,c, ask_fn(roots)->expected_answer_as_list, stored)
 "gold":[
   (2,5,-3, lambda r: [ [x for x in r if x>0][0].numerator ], [1]),   # positive numerator
   (3,-1,-2, lambda r: (lambda s:[s.numerator,s.denominator])(sum(r)), [1,3]), # sum as frac
   (6,1,-2, lambda r: [ [x for x in r if x<0][0].denominator ], [3]),  # negative denominator
   (1,-3,-4, lambda r: [ int(r[0]*r[1]) ], [-4]),                       # product (after rearrange x^2-x=2x+4)
   (4,0,-9, lambda r: (lambda p:[p.numerator,p.denominator])([x for x in r if x>0][0]), [3,2]), # positive as frac
 ],
 "bronze":[
   (1,5,0, lambda r: [ int([x for x in r if x!=0][0]) ], [-5]),
   (1,0,-9, lambda r: [ int([x for x in r if x>0][0]) ], [3]),
   (1,7,10, lambda r: [ int(max(r)) ], [-2]),
   (1,-4,0, lambda r: [ int([x for x in r if x!=0][0]) ], [4]),
   (1,0,-25, lambda r: [ int([x for x in r if x>0][0]) ], [5]),
   (1,1,-6, lambda r: [ int([x for x in r if x>0][0]) ], [2]),
   (1,-6,5, lambda r: [ int(min(r)) ], [1]),
   (1,2,-8, lambda r: [ int([x for x in r if x<0][0]) ], [-4]),
 ],
 "silver":[
   (1,-5,6, lambda r: [ int(sum(r)) ], [5]),
   (1,3,-18, lambda r: [ int([x for x in r if x>0][0]) ], [3]),
   (1,-2,-35, lambda r: [ int([x for x in r if x<0][0]) ], [-5]),
   (1,-7,12, lambda r: [ int(max(r)) ], [4]),   # x^2=7x-12
   (1,4,-12, lambda r: [ int([x for x in r if x>0][0]) ], [2]),  # x^2+4x=12
   (1,-8,7, lambda r: [ int(max(r)) ], [7]),    # x^2=8x-7
   (1,-10,25, lambda r: [ len(set(r)) ], [1]),  # how many distinct
 ],
}

fails=[]
for tier,specs in problems.items():
    for i,(a,b,c,ask,stored) in enumerate(specs):
        rr = roots(a,b,c)
        got = ask(rr)
        live_sol = pb[tier][i]["solutions"]
        ok = got==live_sol==stored
        disp = pb[tier][i]["display"]
        status = "OK " if ok else "FAIL"
        if not ok: fails.append((tier,i,disp,got,live_sol))
        print(f"{status} {tier}[{i}] roots={[str(x) for x in rr]} computed={got} stored={live_sol} :: {disp}")

print("\nFAILS:", len(fails))
for f in fails: print("  ", f)
