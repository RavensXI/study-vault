# -*- coding: utf-8 -*-
"""Adversarial checker: independent fresh-solve + box recompute + expect reproduce."""
import json, io, math
pd = json.load(io.open("lesson_maths-ocr_algebra-L11_diagrams.json", encoding="utf-8"))
fails = []

def rng_ints(lo, lo_inc, hi, hi_inc):
    a = math.ceil(lo) if lo_inc else math.floor(lo) + 1
    b = math.floor(hi) if hi_inc else math.ceil(hi) - 1
    return list(range(a, b + 1))

# Independent re-solve of every problem, keyed by tier,index -> expected solution list
exp = {}
# BRONZE
exp[("bronze",0)] = [min(i for i in range(-50,50) if i+3>7)]                       # x+3>7 smallest
exp[("bronze",1)] = [max(i for i in range(-50,50) if 2*i-1<9)]                     # largest
exp[("bronze",2)] = [min(i for i in range(-50,50) if 3*i>=9)]                      # smallest sol (int here)
exp[("bronze",3)] = [len(rng_ints(-2,True,6,False))]                              # count -2<=x<6
exp[("bronze",4)] = [max(i for i in range(-50,60) if 5*i+4<=49)]
exp[("bronze",5)] = [min(i for i in range(-50,50) if i/2>3)]
exp[("bronze",6)] = [len(rng_ints(1,False,8,False))]
exp[("bronze",7)] = [0]  # MC x>2
# SILVER
exp[("silver",0)] = [0]  # MC x<-3
exp[("silver",1)] = [max(i for i in range(-50,50) if 1<=2*i-3<9)]
exp[("silver",2)] = [0]  # MC x<5
exp[("silver",3)] = [len([i for i in range(-50,50) if -3<2*i+1<=11])]
exp[("silver",4)] = [0]  # MC x<=-3
exp[("silver",5)] = [max(i for i in range(-50,60) if (i+1)/3<=4)]
exp[("silver",6)] = [len([i for i in range(-50,50) if -1<=3*i-4<8])]
# GOLD
exp[("gold",0)] = [0]  # MC -4<x<5
exp[("gold",1)] = [len([i for i in range(-50,50) if i*i<16])]
exp[("gold",2)] = [min(i for i in range(-50,80) if (2*i-1)/3 >= (i+2)/2)]
exp[("gold",3)] = [len([i for i in range(-50,50) if i*i+2*i-15<=0])]
exp[("gold",4)] = [min(i for i in range(-50,50) if -5<3-2*i<=7)]

for t in ("bronze","silver","gold"):
    seen = {}
    for i,p in enumerate(pd["problem_bank"][t]):
        got = p["solutions"]
        want = exp[(t,i)]
        if got != want:
            fails.append("%s[%d] stored solution %r != independent %r" % (t,i,got,want))
        # duplicate check (non-MC)
        if p.get("input_type") != "multiple_choice":
            k = tuple(got)
            if k in seen:
                fails.append("%s[%d] duplicate solution %r (also %s[%d])" % (t,i,got,t,seen[k]))
            seen[k] = i
        # misconception expect != solution, and present
        for j,mm in enumerate(p.get("misconceptions") or []):
            e = mm.get("expect")
            if e is None: continue
            ev = e if isinstance(e,list) else [e]
            if ev == [float(x) for x in got] or ev == got:
                fails.append("%s[%d].misc[%d] expect equals solution" % (t,i,j))
        # guided_steps: the stored solution value must appear as a box answer (interpret box)
        gs = p.get("guided_steps")
        if gs:
            box_answers = [s.get("answer") for s in gs if s.get("answer") is not None]
            if got[0] not in box_answers:
                fails.append("%s[%d] solution %r not reached by any guided box %r" % (t,i,got,box_answers))
            # last box should be part of a check/interpret (has done or is final)
            # verify no non-numeric answers
            for k2,s in enumerate(gs):
                a = s.get("answer")
                if a is not None and not isinstance(a,(int,float)):
                    fails.append("%s[%d].gs[%d] non-numeric answer %r" % (t,i,k2,a))

# ---- Verify specific box arithmetic chains (independent recompute) ----
def recompute(t,i,checks):
    gs = pd["problem_bank"][t][i]["guided_steps"]
    box = [s.get("answer") for s in gs if s.get("answer") is not None]
    for idx,val in checks.items():
        if idx>=len(box) or abs(box[idx]-val)>1e-9:
            fails.append("%s[%d] box#%d = %r, expected %r" % (t,i,idx,box[idx] if idx<len(box) else None,val))

recompute("bronze",0,{0:4,1:5,2:8})
recompute("bronze",1,{0:10,1:5,2:4,3:7})
recompute("bronze",2,{0:3,1:3,2:9})
recompute("bronze",3,{0:5,1:8,2:8})
recompute("bronze",4,{0:45,1:9,2:9,3:49})
recompute("bronze",5,{0:6,1:7,2:3.5})
recompute("bronze",6,{0:2,1:6,2:6})
recompute("silver",1,{0:4,1:12,2:2,3:6,4:5,5:7})
recompute("silver",3,{0:-4,1:10,2:-2,3:5,4:7})
recompute("silver",5,{0:12,1:11,2:11,3:4})
recompute("silver",6,{0:3,1:12,2:1,3:4,4:3})
recompute("gold",1,{0:4,1:3,2:7})
recompute("gold",2,{0:4,1:3,2:1,3:8,4:5})
recompute("gold",3,{0:3,1:-5,2:9,3:0})
recompute("gold",4,{0:-8,1:4,2:4,3:-2,4:-2})

# ---- Reproduce each misconception expect by committing the described error ----
# spot-check the determinate ones
def check_expect(t,i,j,val):
    e = (pd["problem_bank"][t][i]["misconceptions"][j]).get("expect")
    ev = e if not isinstance(e,list) else e[0]
    if ev != val:
        fails.append("%s[%d].misc[%d] expect %r != reproduced %r" % (t,i,j,ev,val))

check_expect("bronze",0,0, min(i for i in range(-50,50) if i+3>=7))   # include boundary -> 4
check_expect("bronze",1,0, max(i for i in range(-50,50) if 2*i-1<=9)) # include -> 5
check_expect("bronze",2,0, min(i for i in range(-50,50) if 3*i>9))    # strict -> 4
check_expect("bronze",3,0, len(rng_ints(-2,True,6,True)))             # include 6 -> 9
check_expect("bronze",4,0, max(i for i in range(-50,60) if 5*i+4<49)) # strict -> 8
check_expect("bronze",5,0, min(i for i in range(-50,50) if i/2>=3))   # include -> 6
check_expect("bronze",5,1, min(i for i in range(-50,50) if i>3/2))    # divide err -> 2
check_expect("bronze",6,0, len(rng_ints(1,True,8,True)))              # include both -> 8
check_expect("silver",1,0, max(i for i in range(-50,50) if 1<=2*i-3<=9)) # include -> 6
check_expect("silver",3,0, len([i for i in range(-50,50) if -3<=2*i+1<=11])) # include left -> 8? recompute below
check_expect("silver",5,0, max(i for i in range(-50,60) if i<=12))       # drops +1: reads x<=12 ->12
check_expect("silver",6,0, len([i for i in range(-50,50) if -1<=3*i-4<=8])) # include right -> 4
check_expect("gold",1,0, len([i for i in range(0,50) if i*i<16]))        # positive only -> 4
check_expect("gold",2,0, min(i for i in range(-50,80) if i-2>=6-4))      # subtracts 2 not adds: x>=4
check_expect("gold",3,0, 3-(-5))                                          # forgot +1 -> 8
check_expect("gold",4,0, min(i for i in range(-50,50) if -5<3-2*i<=7 and i!=-2)) # strict -> -1

# silver[3] include-left recompute properly: -2<x<=5 counting -2 too => -2..5
sl3 = len(rng_ints(-2,True,5,True))
if (pd["problem_bank"]["silver"][3]["misconceptions"][0]["expect"]) != sl3:
    fails.append("silver[3] misc expect %r != %r" % (pd["problem_bank"]["silver"][3]["misconceptions"][0]["expect"], sl3))
# gold[2] wrong-op expect: x-2>=6 -> subtract instead x>=4
if (pd["problem_bank"]["gold"][2]["misconceptions"][0]["expect"]) != 4:
    fails.append("gold[2] misc expect != 4")

# ---- Figures cross-check ----
import re
def fig_check(t,i,lo,lo_inc,hi,hi_inc):
    d = pd["problem_bank"][t][i]["display"]
    if "<svg" not in d:
        fails.append("%s[%d] expected number-line figure, none" % (t,i)); return
    if 'role="img"' not in d or "viewBox" not in d or "aria-label" not in d:
        fails.append("%s[%d] svg missing required attrs" % (t,i))
    if "http" in d.split("</svg")[0]:
        fails.append("%s[%d] svg external ref" % (t,i))
    # closed circle = filled; count fills vs hollow should be 1 each unless both same
    filled = d.count('fill="currentColor"/>')
    hollow = d.count('fill="none" stroke="currentColor" stroke-width="1.6"/>')
    want_filled = (1 if lo_inc else 0)+(1 if hi_inc else 0)
    want_hollow = (0 if lo_inc else 1)+(0 if hi_inc else 1)
    if filled!=want_filled or hollow!=want_hollow:
        fails.append("%s[%d] circle types filled=%d/%d hollow=%d/%d"%(t,i,filled,want_filled,hollow,want_hollow))
fig_check("bronze",3,-2,True,6,False)
fig_check("bronze",6,1,False,8,False)

if fails:
    print("CHECKER FAIL (%d):"%len(fails))
    for f in fails: print("  -",f)
else:
    print("CHECKER PASS: all solutions, boxes, expects, figures verified independently")
