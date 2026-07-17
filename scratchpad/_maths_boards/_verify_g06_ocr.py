# -*- coding: utf-8 -*-
"""Independently recompute every numeric box + expect; assert equality with the
assembled lesson JSON. FAIL loudly on any mismatch."""
import json, math
R = math.radians
def r1(x): return round(x, 1)
def r4(x): return round(x, 4)

pd = json.load(open("lesson_maths-ocr_geometry-L06.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

def boxvals(p):
    return [s["answer"] for s in p.get("guided_steps", []) if s.get("answer") is not None]

# expected box-answer sequences, computed independently
exp = {}
exp[("bronze",0)] = ([24.0, 1.0, 24, 24], [24])       # area 8,6,90
exp[("bronze",1)] = ([60.0, 0.5, 30, 30], [30])
exp[("bronze",2)] = ([20.0, r4(math.sin(R(60))), 17.3, 17.3], [17.3])
exp[("bronze",3)] = ([74, 0.0, 74, r1(math.sqrt(74))], [8.6])
# bronze4 = MC, no steps
exp[("bronze",5)] = ([40.5, r4(math.sin(R(45))), 28.6, 28.6], [28.6])
exp[("bronze",6)] = ([0, 96, 0.0, 90], [90])
exp[("bronze",7)] = ([0.5, 20, 10], [20])
exp[("silver",0)] = ([185, r4(2*8*11*math.cos(R(55))), r4(185-2*8*11*math.cos(R(55))), r1(math.sqrt(185-2*8*11*math.cos(R(55))))], [9.2])
exp[("silver",1)] = ([r4(15*math.sin(R(42))), r4(math.sin(R(65))), 11.1, 15], [11.1])
exp[("silver",2)] = ([-14, 126, r4(-14/126), r1(math.degrees(math.acos(-14/126)))], [96.4])
exp[("silver",3)] = ([110.5, r4(math.sin(R(72))), 105.1, 105.1], [105.1])
exp[("silver",4)] = ([r4(12*math.sin(R(40))), r4(12*math.sin(R(40))/9), r1(math.degrees(math.asin(12*math.sin(R(40))/9))), 81], [59.0])
exp[("silver",5)] = ([61, r4(2*5*6*math.cos(R(100))), r4(61-2*5*6*math.cos(R(100))), r1(math.sqrt(61-2*5*6*math.cos(R(100))))], [8.5])
exp[("silver",6)] = ([12, 60, 0.2, r1(math.degrees(math.acos(0.2))), 14.7], [14.7])
exp[("gold",0)] = ([60, r4(40/60), r1(math.degrees(math.asin(40/60))), 40], [41.8])
exp[("gold",1)] = ([-24, 144, r4(-24/144), r1(math.degrees(math.acos(-24/144)))], [99.6])
exp[("gold",2)] = ([r4(7*math.sin(R(100))), r4(7*math.sin(R(100))/10), r1(math.degrees(math.asin(7*math.sin(R(100))/10))), 236.4], [43.6])
exp[("gold",3)] = ([17, 1836, r1(math.sqrt(1836)), 42.8], [42.8])
exp[("gold",4)] = ([96, r4(math.sin(R(65))), 87, 87], [87])

for (tier, idx), (seq, sol) in exp.items():
    p = pb[tier][idx]
    bv = boxvals(p)
    if bv != seq:
        errs.append("%s[%d] box seq mismatch:\n   got %s\n   exp %s" % (tier, idx, bv, seq))
    if p["solutions"] != sol:
        errs.append("%s[%d] solution mismatch: got %s exp %s" % (tier, idx, p["solutions"], sol))
    # final box must equal solution (single-answer probs)
    if len(sol) == 1 and bv:
        # find the box that states the final answer (== solution) exists
        if sol[0] not in bv:
            errs.append("%s[%d] no box equals solution %s" % (tier, idx, sol))

# recompute the fresh-solve for each display-level answer, compare to solutions
fresh = {
 ("bronze",0): r1(0.5*8*6*math.sin(R(90))), ("bronze",1): r1(0.5*10*12*math.sin(R(30))),
 ("bronze",2): r1(0.5*5*8*math.sin(R(60))), ("bronze",3): r1(math.sqrt(5**2+7**2-2*5*7*math.cos(R(90)))),
 ("bronze",5): r1(0.5*9*9*math.sin(R(45))), ("bronze",6): r1(math.degrees(math.acos((36+64-100)/(2*6*8)))),
 ("bronze",7): r1(10/math.sin(R(30))),
 ("silver",0): r1(math.sqrt(8**2+11**2-2*8*11*math.cos(R(55)))), ("silver",1): r1(15*math.sin(R(42))/math.sin(R(65))),
 ("silver",2): r1(math.degrees(math.acos((49+81-144)/(2*7*9)))), ("silver",3): r1(0.5*13*17*math.sin(R(72))),
 ("silver",4): r1(math.degrees(math.asin(12*math.sin(R(40))/9))), ("silver",5): r1(math.sqrt(5**2+6**2-2*5*6*math.cos(R(100)))),
 ("silver",6): r1(0.5*5*6*math.sin(math.acos(0.2))),
 ("gold",0): r1(math.degrees(math.asin(40/(0.5*10*12)))), ("gold",1): r1(math.degrees(math.acos((64+81-169)/(2*8*9)))),
 ("gold",2): r1(math.degrees(math.asin(7*math.sin(R(100))/10))),
 ("gold",3): r1(math.sqrt(17*9*6*2)), ("gold",4): r1(8*12*math.sin(R(65))),
}
for (tier, idx), val in fresh.items():
    got = pb[tier][idx]["solutions"][0]
    if abs(got - val) > 1e-9:
        errs.append("%s[%d] FRESH-SOLVE mismatch: stored %s, solve %s" % (tier, idx, got, val))

# misconception expects independent recompute
mexp = {
 ("bronze",0): [8*6*math.sin(R(90))],
 ("bronze",1): [10*12*math.sin(R(30))],
 ("bronze",2): [r1(5*8*math.sin(R(60)))],
 ("bronze",3): [74],
 ("bronze",5): [r1(9*9*math.sin(R(45)))],
 ("bronze",6): [0],
 ("bronze",7): [10*math.sin(R(30))],
 ("silver",0): [r1(math.sqrt(185+2*8*11*math.cos(R(55)))), 84.1],
 ("silver",1): [r1(15*math.sin(R(65))/math.sin(R(42)))],
 ("silver",2): [r1(math.degrees(math.acos(14/126)))],
 ("silver",3): [r1(13*17*math.sin(R(72)))],
 ("silver",4): [r1(math.degrees(math.asin(9*math.sin(R(40))/12)))],
 ("silver",5): [r1(math.sqrt(61-2*5*6*abs(math.cos(R(100)))))],
 ("silver",6): [15],
 ("gold",0): [r1(math.degrees(math.asin(40/120)))],
 ("gold",1): [r1(math.degrees(math.acos(24/144)))],
 ("gold",2): [r1(180-math.degrees(math.asin(7*math.sin(R(100))/10)))],
 ("gold",3): [1836],
 ("gold",4): [r1(0.5*96*math.sin(R(65)))],
}
for (tier, idx), vals in mexp.items():
    ms = pb[tier][idx].get("misconceptions", [])
    stored = [m["expect"] for m in ms if m.get("expect") is not None]
    for v in vals:
        if not any(abs(s - v) < 0.05 for s in stored):
            errs.append("%s[%d] misconception expect %s not found in %s" % (tier, idx, v, stored))

# opener + teach walks
op = [s["answer"] for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if op != [60, 10]:
    errs.append("opener boxes %s != [60,10]" % op)
tb = [s["answer"] for s in pd["guided"]["teach"]["bronze"]["steps"] if s.get("answer") is not None]
if tb != [35.0, r4(math.sin(R(40))), 22.5, 22.5]:
    errs.append("teach bronze %s" % tb)
ts = [s["answer"] for s in pd["guided"]["teach"]["silver"]["steps"] if s.get("answer") is not None]
c3 = 117-2*6*9*math.cos(R(55))
if ts != [117, r4(2*6*9*math.cos(R(55))), r4(c3), r1(math.sqrt(c3))]:
    errs.append("teach silver %s (expect third=%s)" % (ts, r1(math.sqrt(c3))))
tg = [s["answer"] for s in pd["guided"]["teach"]["gold"]["steps"] if s.get("answer") is not None]
sinA = 9*math.sin(R(45))/7
if tg != [r4(9*math.sin(R(45))), r4(sinA), r1(math.degrees(math.asin(sinA))), r1(180-math.degrees(math.asin(sinA)))]:
    errs.append("teach gold %s" % tg)

if errs:
    print("VERIFY FAIL (%d):" % len(errs))
    for e in errs: print("  -", e)
    raise SystemExit(1)
print("VERIFY PASS: all boxes, solutions, fresh-solves, expects, opener, teach walks reconcile.")
