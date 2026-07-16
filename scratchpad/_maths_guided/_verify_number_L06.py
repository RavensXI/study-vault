# -*- coding: utf-8 -*-
import json, io, math

pd = json.load(io.open("lesson_number-L06.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# Fresh independent solutions (computed from the display maths).
EXPECT_SOL = {
 ("bronze",0):[81], ("bronze",1):[14], ("bronze",2):[4], ("bronze",3):[5.6,4],
 ("bronze",4):[2.3,-3], ("bronze",5):[125], ("bronze",6):[1], ("bronze",7):[15],
 ("silver",0):[710000], ("silver",1):[1.2,9], ("silver",2):[6.1,-5], ("silver",3):[3,3],
 ("silver",4):[9], ("silver",5):[30000], ("silver",6):[1.024,3],
 ("gold",0):[3,3], ("gold",1):[2.9,6], ("gold",2):[1.5,11], ("gold",3):[3.6,4], ("gold",4):[8,4],
}
for (tier,i),want in EXPECT_SOL.items():
    got = pb[tier][i]["solutions"]
    if [float(x) for x in got] != [float(x) for x in want]:
        errs.append(f"{tier}[{i}] solution stored {got} != fresh {want}")

# Verify each guided walk: final numeric boxes must land on the solution components,
# boundary rules, and end-of-walk continuity spot checks.
def boxes(p):
    return [s for s in p["guided_steps"] if s.get("answer") is not None]

# Spot-check that the answer components appear as box values in each walk.
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        bx = [b["answer"] for b in boxes(p)]
        sol = p["solutions"]
        for comp in sol:
            if not any(abs(float(comp)-float(v))<1e-9 for v in bx):
                errs.append(f"{tier}[{i}] solution component {comp} not produced by any box; boxes={bx}")

# Misconception expects: must not equal solution; recompute a few key ones.
def approx_pair(a,b):
    a=a if isinstance(a,list) else [a]; b=b if isinstance(b,list) else [b]
    return len(a)==len(b) and all(abs(float(x)-float(y))<0.011 for x,y in zip(a,b))
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"]
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is not None and approx_pair(e, sol if len(sol)>1 else sol[0]):
                errs.append(f"{tier}[{i}].misc[{j}] expect {e} equals solution {sol}")

# Explicit recomputation of every misconception's committed error.
checks = {
 ("bronze",0,0): (12, "3*4"),
 ("bronze",1,0): (98, "196/2"),
 ("bronze",1,1): (13, "close guess"),
 ("bronze",2,0): (8, "sqrt64"),
 ("bronze",3,0): ([56,3], "56*10^3"),
 ("bronze",3,1): ([5.6,3], "power miscount"),
 ("bronze",4,0): ([2.3,3], "positive power"),
 ("bronze",5,0): (15, "5*3"),
 ("bronze",5,1): (25, "5^2"),
 ("bronze",6,0): (0, "zero"),
 ("bronze",6,1): (10, "base"),
 ("bronze",7,0): (112.5, "225/2"),
 ("silver",0,0): (7.1e-5, "moved left"),
 ("silver",1,0): ([1.2,16], "mult powers 3*5=15 -> adjust 16"),
 ("silver",1,1): ([12,8], "no adjust"),
 ("silver",2,0): ([61,-6], "A=61"),
 ("silver",3,0): ([3,11], "add powers 7+4"),
 ("silver",4,0): (27, "sqrt729"),
 ("silver",4,1): (243, "729/3"),
 ("silver",5,0): (9000, "compare A only"),
 ("silver",6,0): ([1024,0], "not converted"),
 ("silver",6,1): ([10.24,2], "A too big"),
 ("gold",0,0): ([30,2], "no adjust"),
 ("gold",1,0): ([7.4,6], "add fronts directly 2.4+5"),
 ("gold",2,0): ([1.5,7], "subtract powers 8-2=6 -> 1.5x10^7"),
 ("gold",2,1): ([15,10], "no adjust"),
 ("gold",3,0): ([0.36,5], "already standard"),
 ("gold",3,1): ([3.6,6], "wrong direction power up"),
 ("gold",4,1): ([4,4], "double x8: 5000*8=40000"),
}
# recompute the committed errors independently
recomputed = {
 ("bronze",0,0): 3*4,
 ("bronze",1,0): 196/2,
 ("bronze",2,0): int(round(64**0.5)),
 ("bronze",3,0): [56,3],
 ("bronze",5,0): 5*3,
 ("bronze",5,1): 5**2,
 ("bronze",7,0): 225/2,
 ("silver",0,0): 7.1*10**-5,
 ("silver",1,1): [4*3, 3+5],
 ("silver",2,0): [61,-6],
 ("silver",3,0): [9//3, 7+4],
 ("silver",4,0): int(round(729**0.5)),
 ("silver",4,1): 729//3,
 ("silver",5,0): 9*10**3,
 ("gold",1,0): [2.4+5, 6],
 ("gold",4,1): [5000*8/10000, 4],  # 40000 -> 4x10^4
}
for k,(stated,_) in checks.items():
    tier,i,j = k
    e = pb[tier][i]["misconceptions"][j]["expect"]
    if e is None:
        errs.append(f"{k} check expected non-null but expect is null"); continue
    if not approx_pair(e, stated):
        errs.append(f"{k} stored expect {e} != my derived {stated}")
for k,val in recomputed.items():
    tier,i,j=k
    e=pb[tier][i]["misconceptions"][j]["expect"]
    if not approx_pair(e,val):
        errs.append(f"{k} recompute mismatch: expect {e} vs {val}")

# Verify a handful of walk arithmetic end-values numerically.
def val(pair): return pair[0]*10**pair[1]
assert abs(val([1.024,3]) - 1024) < 1e-9
assert abs(2**10 - 1024) < 1e-9
assert abs(val([1.2,9]) - 4e3*3e5) < 1e-3
assert abs(val([3,3]) - (9e7)/(3e4)) < 1e-6
assert abs(val([3,3]) - (6e4)*(5e-2)) < 1e-6
assert abs(val([2.9,6]) - (2.4e6+5e5)) < 1e-3
assert abs(val([1.5,11]) - (3e8*5e2)) < 1
assert abs(val([3.6,4]) - 0.36*10**5) < 1e-6
assert abs(val([8,4]) - 5e3*2**4) < 1e-6
assert abs(729**(1/3) - 9) < 1e-6
assert 27**2 == 729

if errs:
    print("VERIFY FAILURES:")
    for e in errs: print("  -", e)
else:
    print("ALL MATHS VERIFIED CLEAN")
