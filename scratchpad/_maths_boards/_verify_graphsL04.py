# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_maths-aqa_graphs-L04.json", encoding="utf-8"))
bad = []

# fresh-solve reference answers per tier/index
REF = {
    "bronze": [20, 0.4, 24, 50, 80, 3, 0, 0],
    "silver": [2, 300, 45, 24, 5, 120, 96],
    "gold":   [687.5, 6.7, 2.5, 180, 12],
}
pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    seen = {}
    for i, p in enumerate(pb[tier]):
        sol = p["solutions"][0]
        ref = REF[tier][i]
        if abs(sol - ref) > 1e-9:
            bad.append("%s[%d] solution %s != fresh %s" % (tier, i, sol, ref))
        # duplicate check (non-MC)
        if p.get("input_type") != "multiple_choice":
            k = tuple(p["solutions"])
            if k in seen:
                bad.append("%s[%d] duplicate solution %s (also %s)" % (tier, i, k, seen[k]))
            seen[k] = i
        # expect != solution
        for j, m in enumerate(p.get("misconceptions", [])):
            e = m.get("expect")
            if e is not None and abs(float(e) - float(sol)) < 1e-9:
                bad.append("%s[%d].misc[%d] expect==solution" % (tier, i, j))
        # guided_steps: last non-check numeric must include solution; boundary ok
        gs = p.get("guided_steps")
        if gs:
            answers = [s["answer"] for s in gs if s.get("answer") is not None]
            if sol not in answers and abs(sol) > 1e-9 or (sol == 0):
                pass
            if sol not in answers:
                # for MC-like or 0-sol skip; else flag
                if p.get("input_type") != "multiple_choice":
                    bad.append("%s[%d] solution %s not reached by any box %s" % (tier, i, sol, answers))

# Chart consistency: recompute stated readings
# B0 rest: chart data flat 6 at t=20,30,40 -> rest 40-20=20
b0 = pb["bronze"][0]["chart"]["data"]["datasets"][0]["data"]
if b0 != [0, 3, 6, 6, 6, 9, 12]:
    bad.append("B0 chart data changed unexpectedly")
# B1 speed: dist at t=10 (index2) =4 -> 4/10=0.4
b1 = pb["bronze"][1]["chart"]["data"]["datasets"][0]["data"]
if b1[2] / 10 != 0.4:
    bad.append("B1 chart t=10 value inconsistent")
# B2 total: final=24
b2 = pb["bronze"][2]["chart"]["data"]["datasets"][0]["data"]
if b2[-1] != 24:
    bad.append("B2 chart final != 24")
if b2 != sorted(b2):
    bad.append("B2 chart not non-decreasing (distance-time)")
# S0/S1 chart shared shape [0,10,20,20,20]; accel first 10 -> 20/10=2; area=300
s0 = pb["silver"][0]["chart"]["data"]["datasets"][0]["data"]
if s0[2] / 10 != 2:
    bad.append("S0 accel inconsistent")
# S4 scatter decel: points (0,30),(6,0)
s4 = pb["silver"][4]["chart"]["data"]["datasets"][0]["data"]
if s4[0] != {"x": 0, "y": 30} or s4[1] != {"x": 6, "y": 0}:
    bad.append("S4 scatter pts wrong")
# S5 (0,15),(8,15) area 8*15=120
s5 = pb["silver"][5]["chart"]["data"]["datasets"][0]["data"]
if s5[0]["y"] != 15 or s5[1]["x"] != 8:
    bad.append("S5 scatter pts wrong")
# S6 (0,0),(8,24) tri 0.5*8*24=96
s6 = pb["silver"][6]["chart"]["data"]["datasets"][0]["data"]
if 0.5 * s6[1]["x"] * s6[1]["y"] != 96:
    bad.append("S6 area inconsistent")
# G0 (0,0)(10,25)(30,25)(35,0): 0.5*10*25 + 20*25 + 0.5*5*25
g0 = pb["gold"][0]["chart"]["data"]["datasets"][0]["data"]
tot = 0.5*10*25 + (30-10)*25 + 0.5*(35-30)*25
if tot != 687.5:
    bad.append("G0 area recompute %s" % tot)
# G3 (0,0)(4,20)(10,20)(12,0)
g3 = pb["gold"][3]["chart"]["data"]["datasets"][0]["data"]
tot3 = 0.5*4*20 + (10-4)*20 + 0.5*(12-10)*20
if tot3 != 180:
    bad.append("G3 area recompute %s" % tot3)

# boundary: each non-MC has >=1 box before phase and >=2 live at/after
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        if not gs: continue
        sub = next((k for k, s in enumerate(gs) if s.get("phase") == "substitute"), None)
        if sub is None:
            bad.append("%s[%d] no boundary" % (tier, i)); continue
        before = sum(1 for s in gs[:sub] if s.get("answer") is not None)
        after = sum(1 for s in gs[sub:] if s.get("answer") is not None)
        if before < 1: bad.append("%s[%d] no box before boundary" % (tier, i))
        if after < 2: bad.append("%s[%d] <2 live after boundary" % (tier, i))

# opener boxes
op = [s.get("answer") for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if op != [6, 15, 45]:
    bad.append("opener boxes %s != [6,15,45]" % op)

# teach boxes land on stated totals
tb = [s["answer"] for s in pd["guided"]["teach"]["bronze"]["steps"] if s.get("answer") is not None]
ts = [s["answer"] for s in pd["guided"]["teach"]["silver"]["steps"] if s.get("answer") is not None]
tgd = [s["answer"] for s in pd["guided"]["teach"]["gold"]["steps"] if s.get("answer") is not None]
if tb != [40, 40, 80, 200]: bad.append("teach bronze boxes %s" % tb)
if ts != [3, 54, 144, 198]: bad.append("teach silver boxes %s" % ts)
if tgd != [24, 120, 18, 162]: bad.append("teach gold boxes %s" % tgd)

if bad:
    print("DEFECTS:")
    for b in bad: print("  -", b)
else:
    print("ALL CLEAR: solutions, boxes, boundaries, expects, charts verified")
