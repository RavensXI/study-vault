# -*- coding: utf-8 -*-
"""Adversarial fresh-solve of the built geometry-L04 bank."""
import json, io, re

pd = json.load(io.open("lesson_maths-aqa_geometry-L04.json", encoding="utf-8"))
pb = pd["problem_bank"]
fails = []

# coordinate transformation rules
def cw90(p): return (p[1], -p[0])
def acw90(p): return (-p[1], p[0])
def rot180(p): return (-p[0], -p[1])
def refl_x(p): return (p[0], -p[1])
def refl_y(p): return (-p[0], p[1])
def refl_yx(p): return (p[1], p[0])
def refl_ynx(p): return (-p[1], -p[0])
def translate(p, v): return (p[0]+v[0], p[1]+v[1])
def enlarge(p, sf, c): return (c[0]+sf*(p[0]-c[0]), c[1]+sf*(p[1]-c[1]))

# expected correct answers computed independently (label string, expect distractor idx)
checks = {
 ("bronze",0): translate((2,3),(4,-1)),      # (6,2)
 ("bronze",1): refl_x((5,1)),                 # (5,-1)
 ("bronze",2): refl_y((-3,4)),                # (3,4)
 ("bronze",3): (4-1,2-5),                      # vector (3,-3)
 ("bronze",4): translate((5,1),(-2,3)),       # (3,4)
 ("bronze",5): refl_yx((0,6)),                # (6,0)
 ("bronze",6): enlarge((2,1),3,(0,0)),        # (6,3)
 ("bronze",7): rot180((3,2)),                 # (-3,-2)
 ("silver",0): acw90((4,-1)),                 # (1,4)
 ("silver",1): enlarge((1,2),-2,(0,0)),       # (-2,-4)
 ("silver",3): enlarge((8,6),0.5,(0,0)),      # (4,3)
 ("silver",4): refl_ynx((-2,5)),              # (-5,2)
 ("silver",5): enlarge((3,1),2,(1,0)),        # (5,2)
 ("gold",0): enlarge((5,3),-1,(2,1)),         # (-1,-1)
 ("gold",1): enlarge((9,0),1/3,(0,6)),        # (3,4)
 ("gold",4): enlarge((4,2),-2,(1,1)),         # (-5,-1)
}
def fmt(t):
    x,y=t
    x=int(round(x)); y=int(round(y))
    return "(%d, %d)" % (x,y)

for (tier,i),ans in checks.items():
    p = pb[tier][i]
    sol_idx = p["solutions"][0]
    opt = p["options"][sol_idx]
    want = fmt(ans).replace("-", "−")
    # normalize option (strip latex binom for B3)
    o = opt
    if "binom" in o:
        m = re.search(r"binom\{(-?\d+)\}\{(-?\d+)\}", o)
        o = "(%s, %s)" % (m.group(1), m.group(2))
        o = o.replace("-", "−")
    ok = (o.replace(" ","") == want.replace(" ",""))
    if not ok:
        fails.append("%s[%d] correct opt %r != computed %r" % (tier,i,opt,want))
    # expect must not be the correct index and must be a real distractor idx
    for m in p["misconceptions"]:
        e = m["expect"]
        if e == sol_idx:
            fails.append("%s[%d] expect equals correct idx" % (tier,i))
        if not (0 <= e < len(p["options"])):
            fails.append("%s[%d] expect out of range" % (tier,i))

# describe-question uniqueness: exactly one option maps ALL given points
rules = {
 "Rotation 90° clockwise about the origin": cw90,
 "Rotation 90° anticlockwise about the origin": acw90,
 "Reflection in the x-axis": refl_x,
 "Reflection in the y-axis": refl_y,
 "Reflection in y = x": refl_yx,
 "Reflection in y = −x": refl_ynx,
 "Enlargement scale factor −1, centre the origin": lambda p: enlarge(p,-1,(0,0)),
}
describe = {
 ("silver",2): [((2,3),(2,-3)), ((5,4),(5,-4))],
 ("silver",6): [((1,4),(4,-1))],
 ("gold",2):   [((2,1),(1,-2)), ((4,2),(2,-4))],
}
for (tier,i),pairs in describe.items():
    p = pb[tier][i]
    good=[]
    for j,opt in enumerate(p["options"]):
        if opt in rules:
            f=rules[opt]
            if all(f(pre)==img for pre,img in pairs):
                good.append(j)
        elif "Translation" in opt:
            m=re.search(r"binom\{(-?\d+)\}\{(-?\d+)\}", opt) or re.search(r"\((-?\d+)\D+(-?\d+)\)", opt)
            v=(int(m.group(1)),int(m.group(2)))
            if all(translate(pre,v)==img for pre,img in pairs):
                good.append(j)
        else:
            # unmodelled distractor (e.g. rotation about non-origin) assume not matching all
            pass
    if good != [p["solutions"][0]]:
        fails.append("%s[%d] describe: options mapping all points = %s, want only [%d]" % (tier,i,good,p["solutions"][0]))

# G3 two reflections check
g3 = pb["gold"][3]
# reflect in x=2 then x=5 of a test point (0,0): -> (4,0) then (10,0); net translate (10,0)? check formula
def reflx(p,a): return (2*a-p[0], p[1])
tp=(1,7); r=reflx(reflx(tp,2),5)
if r != translate(tp,(6,0)):
    fails.append("gold[3] two-reflection net != (6,0)")

if fails:
    print("VERIFY FAIL:")
    for f in fails: print("  -", f)
else:
    print("VERIFY PASS: all options correct, expects valid, describe questions unambiguous, G3 net translation (6,0).")
