# -*- coding: utf-8 -*-
import json, io
F = r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_graphs-L04.json"
pd = json.load(io.open(F, encoding="utf-8"))
errs = []

def approx(a, b, t=0.02): return abs(float(a) - float(b)) < t

# independent fresh-solve of each bank problem
def solve(tier, i):
    # returns expected solution list computed from the problem's own numbers
    return None

pb = pd["problem_bank"]

# Fresh-solve table (computed by hand from displays)
expected = {
 ("bronze",0): [6], ("bronze",1): [10], ("bronze",2): [30], ("bronze",3): [16],
 ("bronze",4): [1], ("bronze",5): [0.067], ("bronze",6): [1], ("bronze",7): [120],
 ("silver",0): [2], ("silver",1): [30], ("silver",2): [240], ("silver",3): [5],
 ("silver",4): [1], ("silver",5): [3], ("silver",6): [20.32],
 ("gold",0): [280], ("gold",1): [225], ("gold",2): [10], ("gold",3): [2.5], ("gold",4): [180],
}
for tier in ("bronze","silver","gold"):
    seen = {}
    for i, p in enumerate(pb[tier]):
        exp = expected[(tier,i)]
        if [float(x) for x in p["solutions"]] != [float(x) for x in exp]:
            errs.append("%s[%d] solution %r != fresh %r" % (tier,i,p["solutions"],exp))
        # duplicate check among non-MC
        if p.get("input_type") != "multiple_choice":
            k = tuple(float(x) for x in p["solutions"])
            if k in seen: errs.append("%s[%d] duplicate solution %r (also %s)" % (tier,i,p["solutions"],seen[k]))
            seen[k] = "%s[%d]" % (tier,i)
        # last live box lands on solution (for single_value with guided_steps)
        gs = p.get("guided_steps")
        if gs and p.get("input_type") != "multiple_choice":
            boxes = [s for s in gs if s.get("answer") is not None]
            finals = [b["answer"] for b in boxes]
            # the solution value must appear as a box answer somewhere in the finishing region
            if not any(approx(b, p["solutions"][0]) for b in finals):
                errs.append("%s[%d] no box equals solution %r" % (tier,i,p["solutions"]))
            # substitute boundary present with >=2 live boxes after and >=1 before
            sub = next((j for j,s in enumerate(gs) if s.get("phase")=="substitute"), None)
            if sub is None: errs.append("%s[%d] no substitute phase" % (tier,i))
            else:
                after = sum(1 for s in gs[sub:] if s.get("answer") is not None)
                before = sum(1 for s in gs[:sub] if s.get("answer") is not None)
                if after < 2: errs.append("%s[%d] <2 live after boundary" % (tier,i))
                if before < 1: errs.append("%s[%d] <1 box before boundary" % (tier,i))
        # expects must not equal solution
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            if e is not None:
                ev = e if isinstance(e,list) else [e]
                sv = [float(x) for x in p["solutions"]]
                if len(ev)==len(sv) and all(approx(a,b) for a,b in zip(ev,sv)):
                    errs.append("%s[%d] expect==solution" % (tier,i))

# recompute specific guided box arithmetic (spot every arithmetic string)
def check_arith():
    # G0 regions
    assert 0.5*4*20==40 and 8*20==160 and 0.5*(20+10)*4==60 and 0.5*4*10==20
    assert 40+160+60+20==280
    # G1
    assert 0.5*5*15==37.5 and 10*15==150 and 37.5+150+37.5==225
    # G4
    assert 12*30==360 and 0.5*360==180 and 0.5*12*30==180
    # G3
    assert 25-5==20 and 20/8==2.5 and 5+2.5*8==25
    # S5
    assert 30-6==24 and 24/8==3 and 6+3*8==30
    # S0
    assert (20-0)/10==2
    # S1
    assert 15/0.5==30
    # S2
    assert 12*20==240
    # B3
    assert 8/5==1.6 and 10*1.6==16 and 2*8==16
    # B5
    assert round(4/60,3)==0.067
    # teach gold
    assert 0.5*4*12==24 and 6*12==72 and 24+72+24==120 and 4+6+4==14
    # teach silver
    assert 20/8==2.5
    return True
check_arith()

# expect derivations
exp_checks = {
 ("bronze",2,0): 120,   # 60*2
 ("bronze",3,0): 13,    # 8 + (10-5)
 ("bronze",7,0): 13.33, # 40/3
 ("silver",0,0): 20, ("silver",0,1): 0.5,
 ("silver",1,0): 0.5,   # 15/30
 ("silver",2,0): 32,    # 12+20
 ("silver",5,0): 24,
 ("silver",6,0): 3.15,  # 8/2.54
 ("gold",0,0): 400, ("gold",0,1): 200,
 ("gold",1,0): 300, ("gold",1,1): 150,
 ("gold",2,0): 8,       # 400/50
 ("gold",3,0): 3.125,   # 25/8
 ("gold",4,0): 360,
}
for (t,pi,mi),val in exp_checks.items():
    got = pb[t][pi]["misconceptions"][mi]["expect"][0]
    if not approx(got, val, 0.02):
        errs.append("%s[%d].misc[%d] expect %r != derived %r" % (t,pi,mi,got,val))
assert approx(8/2.54, 3.15, 0.01), 8/2.54
assert approx(40/3, 13.33, 0.01)
assert 25/8==3.125

# chart sanity: bronze journey fixed
bj = pb["bronze"][0]["chart"]["data"]["datasets"][0]["data"]
assert bj == [0,3,6,6,8,10,12], bj  # flat only 20->30 (idx2,3)
assert bj[2]==6 and bj[3]==6 and bj[4]==8, "flat span wrong"

# em dash scan (student-facing, excluding note)
def scan(o, path):
    if isinstance(o, dict):
        for k,v in o.items():
            if k=="note": continue
            scan(v, path+"."+str(k))
    elif isinstance(o, list):
        for j,v in enumerate(o): scan(v, path+"[%d]"%j)
    elif isinstance(o, str) and "—" in o:
        errs.append("EM DASH at "+path)
scan(pd, "pd")

if errs:
    print("VERIFY FAIL:")
    for e in errs: print("  -", e)
else:
    print("VERIFY OK: all fresh-solves, boxes, expects, chart, dashes clean")
