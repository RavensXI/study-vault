# -*- coding: utf-8 -*-
"""Independent adversarial check of the built shard: fresh-solve every problem,
recompute every guided/teach/opener box, reproduce every misconception expect."""
import json, io, math
PI = math.pi
pd = json.load(io.open("lesson_maths-aqa_geometry-L02.json", encoding="utf-8"))
errs = []

def approx(a, b, tol=0.06):
    return abs(a - b) <= tol

# --- fresh solutions (computed from the display maths, independently) ---
expected = {
 "bronze": [60, 26, 30, 40, 42, 49, round(14*PI,1), round(25*PI,1)],
 "silver": [round(0.5*PI*36,1), round(120-PI*9,1), 8, 5, 24, round(25*PI,1), 22],
 "gold":   [round(0.375*PI*64,1), round(0.2*2*PI*10,1), round(PI*60+200), 7, round(64*PI,1)],
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        got = p["solutions"][0]
        exp = expected[tier][i]
        if not approx(float(got), float(exp)):
            errs.append("SOLUTION %s[%d] stored %s expected %s" % (tier,i,got,exp))

# --- box continuity: for every walk, boxes must be numeric and land on solution ---
def walk_boxes(steps):
    return [s for s in steps if s.get("answer") is not None]

# spot-recompute key box values per problem type by re-deriving from the pre text is
# hard generically; instead assert final live box (the check) or phase result equals a
# known quantity. We recompute each walk's declared answers against a manual table.
manual = {
 # tier,i : list of box answers we independently expect (in order)
 ("bronze",0): [50,10,60,60],
 ("bronze",1): [13,26,26],
 ("bronze",2): [60,30,30],
 ("bronze",3): [40,40,40],
 ("bronze",4): [14,7,42,42],
 ("bronze",5): [7,49,28],
 ("bronze",6): [14,round(14*PI,1),round(14*PI,1)],
 ("bronze",7): [25,round(25*PI,1),round(25*PI,1)],
 ("silver",0): [6,36,round(0.5*PI*36,1),12],
 ("silver",1): [120,9,round(PI*9,2),round(120-PI*9,1),28.3],
 ("silver",2): [4.5,8,36],
 ("silver",3): [round(PI+2,2),5,25.7],
 ("silver",4): [24,12,24,24],
 ("silver",5): [round(2*PI,2),5,round(25*PI,1),round(10*PI,1)],
 ("silver",6): [30,8,22,8],
 ("gold",0): [64,0.375,round(0.375*PI*64,1),round(0.375*PI*64,1)],
 ("gold",1): [0.2,round(20*PI,1),round(0.2*round(20*PI,1),1),63],
 ("gold",2): [round(PI*60),200,round(PI*60)+200,round(PI*60)],
 ("gold",3): [round(154/PI),7,round(49*PI)],
 ("gold",4): [round(100*PI,1),round(36*PI,1),round(round(100*PI,1)-round(36*PI,1),1),round(64*PI,1)],
}
for (tier,i),want in manual.items():
    boxes = [b["answer"] for b in walk_boxes(pd["problem_bank"][tier][i]["guided_steps"])]
    if len(boxes)!=len(want) or not all(approx(float(a),float(b)) for a,b in zip(boxes,want)):
        errs.append("BOXES %s[%d] got %s want %s" % (tier,i,boxes,want))
    # final answer-bearing 'phase' path should reach solution somewhere in boxes
    sol = pd["problem_bank"][tier][i]["solutions"][0]
    if not any(approx(float(b),float(sol)) for b in boxes):
        errs.append("WALK %s[%d] no box equals solution %s" % (tier,i,sol))

# --- teach walks land correctly ---
teach_final = {
 "bronze":[14,7,42,84,42], "silver":[10,100,314.2,157.1,314.2], "gold":[36,113.1,0.25,28.3,113.2]}
for tier,want in teach_final.items():
    boxes=[b["answer"] for b in walk_boxes(pd["guided"]["teach"][tier]["steps"])]
    if boxes!=want:
        errs.append("TEACH %s got %s want %s"%(tier,boxes,want))

# opener boxes
op=[b["answer"] for b in pd["guided"]["opener"]["steps"] if b.get("answer") is not None]
if op!=[15,16]:
    errs.append("OPENER boxes %s want [15,16]"%op)

# --- expects reproduce the described error ---
exp_table = {
 ("bronze",0): 34, ("bronze",1): 36, ("bronze",2): 60, ("bronze",3): 20,
 ("bronze",4): 84, ("bronze",5): 196, ("bronze",6): round(49*PI,1), ("bronze",7): round(10*PI,1),
 ("silver",0): [round(PI*36,1), round(0.5*PI*144,1)],
 ("silver",1): round(120+PI*9,1),
 ("silver",2): 4, ("silver",3): round(25.7/PI), ("silver",4): 12,
 ("silver",5): round(100*PI,1), ("silver",6): 30,
 ("gold",0): [round(PI*64,1), round(0.375*2*PI*8,1)],
 ("gold",1): round(0.2*PI*100,1),
 ("gold",2): round(2*PI*60+200),
 ("gold",3): round(154/PI),
 ("gold",4): round(16*PI,1),
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        want = exp_table.get((tier,i))
        wl = want if isinstance(want,list) else [want]
        got = [m["expect"] for m in p["misconceptions"]]
        for w in wl:
            if not any(approx(float(g),float(w)) for g in got):
                errs.append("EXPECT %s[%d] want %s in %s"%(tier,i,w,got))

# duplicate solutions within tier
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pd["problem_bank"][tier]):
        k=tuple(p["solutions"])
        if k in seen: errs.append("DUP %s[%d] %s == %s[%d]"%(tier,i,k,tier,seen[k]))
        seen[k]=i

if errs:
    print("VERIFY FAIL (%d):"%len(errs))
    for e in errs: print("  -",e)
else:
    print("VERIFY OK: all solutions, boxes, teach/opener, expects, no dups")
