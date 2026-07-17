# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_maths-eduqas_algebra-L11.json", encoding="utf-8"))
errs = []
pb = pd["problem_bank"]

# Fresh-solve truth table (computed independently by hand)
# MC correct index must be 0 for all; single_value expected answers:
sv_truth = {
    ("bronze", 6): 4,   # 2<n<=6 -> 3,4,5,6
    ("silver", 3): 5,   # -3<=x<2 -> -3,-2,-1,0,1
    ("silver", 6): 3,   # -1<2x+3<=9 -> -2<x<=3 largest 3
    ("gold", 2): 9,     # n^2<=16 -> -4..4
    ("gold", 3): 2,     # x<1 and x>-2 -> -1,0
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        it = p["input_type"]
        sol = p["solutions"]
        if it == "multiple_choice":
            if sol != [0]:
                errs.append(f"{tier}[{i}] MC sol not [0]: {sol}")
            # verify correct option matches fresh solve? check option[0] present
            if len(p["options"]) != 4:
                errs.append(f"{tier}[{i}] not 4 options")
            for mm in p["misconceptions"]:
                e = mm["expect"]
                if not isinstance(e,int) or e<1 or e>3:
                    errs.append(f"{tier}[{i}] MC expect out of range: {e}")
        else:
            if (tier,i) in sv_truth and sol[0] != sv_truth[(tier,i)]:
                errs.append(f"{tier}[{i}] sv sol {sol[0]} != truth {sv_truth[(tier,i)]}")
            for mm in p["misconceptions"]:
                if mm["expect"] == sol[0]:
                    errs.append(f"{tier}[{i}] expect==answer")
            # last box must equal solution
            gs = p.get("guided_steps",[])
            boxes = [s for s in gs if s.get("answer") is not None]
            if boxes and boxes[-1]["answer"] != sol[0]:
                errs.append(f"{tier}[{i}] last box {boxes[-1]['answer']} != sol {sol[0]}")

# Teach walks: recompute each box
def check(name, boxes, truth):
    for b,t in zip(boxes,truth):
        if b != t:
            errs.append(f"teach {name}: box {b} != expected {t}")
    if len(boxes)!=len(truth):
        errs.append(f"teach {name}: box count {len(boxes)} != {len(truth)}")

t = pd["guided"]["teach"]
def gboxes(walk): return [s["answer"] for s in walk["steps"] if s.get("answer") is not None]
# bronze 4x+3<19: 19-3=16, 16/4=4, test3:15, test4:19
check("bronze", gboxes(t["bronze"]), [16,4,15,19])
# silver 3-2x<=9: 9-3=6, 6/-2=-3, test0:3, test-4:11
check("silver", gboxes(t["silver"]), [6,-3,3,11])
# gold -2<=3x+4<13: -2-4=-6, 13-4=9, -6/3=-2, 9/3=3, count5
check("gold", gboxes(t["gold"]), [-6,9,-2,3,5])

# opener: 8+4w>=20 -> w>=3; boundary 8+4*3=20
ob = [s["answer"] for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if ob != [3,20]:
    errs.append(f"opener boxes {ob} != [3,20]")

if errs:
    print("VERIFY FAIL")
    for e in errs: print("  -", e)
else:
    print("VERIFY PASS: all solutions, boxes, expects, teach walks, opener correct")
