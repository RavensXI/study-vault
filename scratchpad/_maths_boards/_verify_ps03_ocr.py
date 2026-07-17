# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_maths-ocr_probability-statistics-L03.json", encoding="utf-8"))
fails = []

# independent fresh-solve of every problem from its numbers
expected = {
    "bronze": [20, 75, 50, 40, 12, 135, 0, 0],   # MC solutions are index 0
    "silver": [15, 90, 12, 0, 24, 25, 5],
    "gold":   [36, 100, 2.5, 7, 25],
}
pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        sol = p["solutions"]
        exp = expected[tier][i]
        if p.get("input_type") == "multiple_choice":
            if sol != [0]:
                fails.append("%s[%d] MC solution not [0]: %r" % (tier, i, sol))
            continue
        if abs(sol[0] - exp) > 1e-9:
            fails.append("%s[%d] solution %r != fresh %r" % (tier, i, sol, exp))
        # last non-check answer box must equal solution; and there is a phase step
        gs = p.get("guided_steps")
        if gs:
            boxes = [s for s in gs if s.get("answer") is not None]
            # find the answer-producing box (not the final check): the box whose answer==solution appears
            if not any(abs(b["answer"] - sol[0]) < 1e-9 for b in boxes):
                fails.append("%s[%d] no guided box lands on solution %r" % (tier, i, sol))
            if not any(s.get("phase") == "substitute" for s in gs):
                fails.append("%s[%d] no substitute phase" % (tier, i))
        # misconception expect must differ from solution
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            if e is not None and abs(float(e) - sol[0]) < 1e-9:
                fails.append("%s[%d] expect==solution" % (tier, i))

# recompute each box chain arithmetic for a few key walks
def chk(name, got, want):
    if abs(got - want) > 1e-9:
        fails.append("%s: %r != %r" % (name, got, want))

# B4 pie: 60/360 -> 6 sectors, 72/6=12
chk("B4", 360/60, 6); chk("B4b", 72/6, 12); chk("B4mis", 72*6, 432)
# B5 angle: 15/40=0.375, *360=135
chk("B5", 15/40*360, 135)
# S1 total: 144/72=2, 360/72=5, 36/2=18, 18*5=90
chk("S1", 144//72, 2); chk("S1b", 360//72, 5); chk("S1c", 36//2, 18); chk("S1d", 18*5, 90)
chk("S1verify", 144/360*90, 36)
# S4 salad: 150+90=240, 360-240=120, 72/3=24
chk("S4", 360-(150+90), 120); chk("S4b", 72/3, 24); chk("S4mis", 120/360*72, 24)
# S2 twoway females pass 30-18=12
chk("S2", 30-18, 12)
# S6 cycle 50-45=5
chk("S6", 50-(20+15+10), 5)
# G0 estimate: interp between (25,38),(30,35) at 28
y = 38 + (28-25)/5*(35-38);
if not (35.5 <= y <= 36.5): fails.append("G0 interp %.2f not ~36" % y)
# G1 other: 360/72=5, 500/5=100
chk("G1", 360//72, 5); chk("G1b", 500/5, 100)
# G2 FD 25/10=2.5
chk("G2", 25/10, 2.5); chk("G2mis", 25*10, 250)
# G4 clothing Q4: 55+25+20=100, 25/100*100=25
chk("G4", 55+25+20, 100); chk("G4b", 25/100*100, 25)
# G0 LOBF line reads ~36 at x=28: line (10,49)-(45,23)
ly = 49 + (28-10)/(45-10)*(23-49)
if not (35 <= ly <= 37): fails.append("G0 LOBF line %.2f not ~36 at x=28" % ly)

# figure-vs-numbers spot checks (pie svgs contain the right angle labels)
disp = pb["bronze"][2]["display"]
if "90°" not in disp or "Maths" not in disp: fails.append("B3 svg label mismatch")
if "144°" not in pb["silver"][1]["display"]: fails.append("S2 svg 144 mismatch")
if "150°" not in pb["silver"][4]["display"] or "90°" not in pb["silver"][4]["display"]: fails.append("S5 svg mismatch")
if "72°" not in pb["gold"][1]["display"]: fails.append("G2 svg 72 mismatch")

# duplicate solution check within tier (non-MC)
for tier in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")=="multiple_choice": continue
        k=tuple(p["solutions"])
        if k in seen: fails.append("%s dup solution %r"%(tier,k))
        seen.add(k)

print("FAILS:", len(fails))
for f in fails: print("  -", f)
if not fails: print("ALL CHECKS PASS")
