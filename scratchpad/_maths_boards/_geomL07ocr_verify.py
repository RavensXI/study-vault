# -*- coding: utf-8 -*-
"""Independent verification: recompute every box and every expect."""
import json, io

pd = json.load(io.open("lesson_maths-ocr_geometry-L07.json", encoding="utf-8"))
errs = []

# --- fresh-solved expected solutions (computed by hand from displays) ---
expected = {
    "bronze": [50, 70, 90, 35, 42, 100, 80, 40],
    "silver": [40, 55, 140, 130, 8, 20, 62],
    "gold": [10, 20, 48, 6, 18],
}
for tier, sols in expected.items():
    probs = pd["problem_bank"][tier]
    if len(probs) != len(sols):
        errs.append("%s length mismatch" % tier)
    for i, (p, s) in enumerate(zip(probs, sols)):
        if p["solutions"] != [s]:
            errs.append("%s[%d] solution %s != fresh-solve %s" % (tier, i, p["solutions"], [s]))

# --- every guided box must contain a numeric answer; final live box must land on solution ---
def last_box_value(steps):
    vals = [st["answer"] for st in steps if st.get("answer") is not None]
    return vals

# check that the solution value appears as a box answer in the walk (the solve-through box)
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        gs = p.get("guided_steps") or []
        boxvals = [st["answer"] for st in gs if st.get("answer") is not None]
        sol = p["solutions"][0]
        if sol not in boxvals:
            errs.append("%s[%d] solution %s not reached by any guided box %s" % (tier, i, sol, boxvals))
        # completion boundary: >=1 before phase, >=2 live at/after
        sub = None
        for j, st in enumerate(gs):
            if st.get("phase") == "substitute":
                sub = j; break
        if sub is None:
            errs.append("%s[%d] no phase boundary" % (tier, i))
        else:
            before = sum(1 for st in gs[:sub] if st.get("answer") is not None)
            after = sum(1 for st in gs[sub:] if st.get("answer") is not None)
            if before < 1: errs.append("%s[%d] no box before phase" % (tier, i))
            if after < 2: errs.append("%s[%d] only %d live boxes after phase" % (tier, i, after))

# --- reproduce every expect by committing the described error ---
def approx(a, b): return abs(float(a) - float(b)) < 0.011
expect_checks = {
    ("bronze", 0): [("double not halve", 100 * 2)],
    ("bronze", 1): [("halve not double", 35 / 2)],
    ("bronze", 2): [("diameter straight angle", 180)],
    ("bronze", 3): [("forget right angle 180-55", 180 - 55)],
    ("bronze", 4): [("supplementary 180-42", 180 - 42)],
    ("bronze", 5): [("copies angle A", 80)],
    ("bronze", 6): [("double not halve", 160 * 2)],
    ("bronze", 7): [("forget right angle 180-50", 180 - 50)],
    ("silver", 0): [("use 360: (360-20)/4", (360 - 20) / 4)],
    ("silver", 1): [("90-55", 90 - 55)],
    ("silver", 2): [("centre angle 40", 40)],
    ("silver", 3): [("(360-260)/2", (360 - 260) / 2)],
    ("silver", 5): [("3x-20=x -> x=10", 10)],
    ("silver", 6): [("180-28", 180 - 28)],
    ("gold", 0): [("forget factor 2: 8x-10=3x+5 -> 15/5", 15 / 5)],
    ("gold", 1): [("360/9", 360 / 9)],
    ("gold", 2): [("90-48", 90 - 48)],
    ("gold", 3): [("add: 3+8-4", 3 + 8 - 4)],
    ("gold", 4): [("144/8 as AB +8", 144 / 8 + 8)],
}
for (tier, i), checks in expect_checks.items():
    p = pd["problem_bank"][tier][i]
    mc = p.get("misconceptions") or []
    if not mc:
        errs.append("%s[%d] expected a misconception, none" % (tier, i)); continue
    exp = mc[0].get("expect")
    label, val = checks[0]
    if exp is None or not approx(exp, val):
        errs.append("%s[%d] expect %s != committed error %s (%s)" % (tier, i, exp, val, label))

# silver[4] should have empty misconceptions (no determinate error)
if pd["problem_bank"]["silver"][4].get("misconceptions"):
    errs.append("silver[4] should have no misconception")

# --- verify tier_guide examples arithmetic ---
# bronze: 130/2=65 ; silver: 4x-30=2x -> x=15, 4*15-30=30 ; gold: 5x-5=2(2x+5) -> x=15
assert 130 / 2 == 65
assert (4 * 15 - 30) == 30 and 30 == 2 * 15
assert (5 * 15 - 5) == 70 and (2 * 15 + 5) == 35 and 70 == 2 * 35

# --- opener boxes: 80/2=40, 100/2=50 ---
ob = [st["answer"] for st in pd["guided"]["opener"]["steps"] if st.get("answer") is not None]
if ob != [40, 50]:
    errs.append("opener boxes %s != [40,50]" % ob)

# --- teach walks: >=4 boxes each and land correctly ---
tb = [st["answer"] for st in pd["guided"]["teach"]["bronze"]["steps"] if st.get("answer") is not None]
ts = [st["answer"] for st in pd["guided"]["teach"]["silver"]["steps"] if st.get("answer") is not None]
tgg = [st["answer"] for st in pd["guided"]["teach"]["gold"]["steps"] if st.get("answer") is not None]
if tb != [90, 145, 35, 180]: errs.append("teach.bronze boxes %s" % tb)
if ts != [2, 30, 15, 30]: errs.append("teach.silver boxes %s" % ts)
if tgg != [36, 36, 6, 36]: errs.append("teach.gold boxes %s" % tgg)

# --- preservation: related_videos, worked_examples, topic_links unchanged vs live ---
live = json.load(io.open("_geomL07ocr_live.json", encoding="utf-8"))
for k in ("related_videos", "worked_examples", "topic_links"):
    if pd.get(k) != live.get(k):
        errs.append("PRESERVATION: %s changed" % k)

# --- no em dash anywhere student-facing (double-check) ---
def scan(o, path):
    if isinstance(o, dict):
        for kk, vv in o.items():
            if kk in ("note",): continue
            scan(vv, path + "." + str(kk))
    elif isinstance(o, list):
        for j, vv in enumerate(o): scan(vv, "%s[%d]" % (path, j))
    elif isinstance(o, str) and "—" in o:
        errs.append("EM DASH at " + path)
scan(pd, "pd")

if errs:
    print("VERIFY FAIL:")
    for e in errs: print("  -", e)
else:
    print("VERIFY PASS: all solutions, boxes, expects, examples, preservation clean")
