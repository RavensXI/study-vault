# -*- coding: utf-8 -*-
import json
pd = json.load(open("_RVW_canonical.json", encoding="utf-8"))
issues = []

# Independent fresh solutions keyed by display substring
# GOLD
def approx(a,b,t=1e-6): return abs(a-b)<=t

# Verify each bank problem's stored solution by re-deriving from chemistry
checks = {
  # display key : (correct_answer, tolerance_for_check)
}

pb = pd["problem_bank"]
# Manually fresh-solved expected solutions:
expected = {
 ("gold",0): 40.0,   # %Ca CaCO3: 40/100*100
 ("gold",1): 13.9,   # %N KNO3: 14/101*100=13.861->13.9
 ("gold",2): 88.9,   # %O H2O: 16/18*100=88.89->88.9
 ("gold",3): 71.0,   # Mr=7.1/0.1
 ("gold",4): 98.0,   # Mr=4.9/0.05
 ("gold",5): 132.0,  # 3*44
 ("bronze",0): 58.5, # 23+35.5
 ("bronze",1): 18.0, # 2+16
 ("bronze",2): 44.0, # 12+32
 ("bronze",3): 100.0,# 40+12+48
 ("bronze",4): 2.0,  # 36/18
 ("bronze",5): 0.125,# 5.5/44
 ("bronze",6): 0.12, # 4.8/40
 ("bronze",7): 9.0,  # 0.5*18
 ("silver",0): 74.0, # 40+2*17
 ("silver",1): 148.0,# 24+2*62
 ("silver",2): 0.2,  # 11.7/58.5
 ("silver",3): 0.25, # 25/100
 ("silver",4): 25.0, # 0.25*100
 ("silver",5): 42.4, # 0.4*106
}
for (tier,i),exp in expected.items():
    sol = pb[tier][i]["solutions"][0]
    if not approx(float(sol),exp,0.02):
        issues.append("SOLUTION MISMATCH %s[%d]: stored %s, fresh %s"%(tier,i,sol,exp))

# Recompute every guided_steps box arithmetically by evaluating the pre expression
import re
def eval_box(pre):
    # extract "= " trailing arithmetic like "40 + 12 + 48 = "
    m = re.search(r'[:=]\s*([0-9.\s×xX*+\-/÷()]+?)\s*=\s*$', pre)
    if not m: return None
    expr = m.group(1).replace("×","*").replace("÷","/").replace("x","*").replace("X","*")
    expr = expr.replace("−","-")
    try:
        return eval(expr, {"__builtins__":{}})
    except Exception:
        return None

def scan_walk(steps, label):
    for j,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre = st.get("pre","")
        v = eval_box(pre)
        if v is None: continue
        if not approx(float(v), float(st["answer"]), 0.006):
            issues.append("BOX MISMATCH %s[%d]: pre=%r eval=%s stored=%s"%(label,j,pre,v,st["answer"]))

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        if gs: scan_walk(gs, "%s[%d].guided_steps"%(tier,i))
for tier in ("bronze","silver","gold"):
    t = pd["guided"]["teach"][tier]
    scan_walk(t["steps"], "teach.%s"%tier)
scan_walk(pd["guided"]["opener"]["steps"], "opener")

# Verify expects: recompute stated wrong-answer where determinate
exp_expected = {
 ("gold",1,0): 20.3,  # wrong_mr (one O): 14/69*100
 ("gold",1,1): 38.6,  # wrong_element K: 39/101*100
 ("gold",2,0): 94.1,  # wrong_mr (Mr17): 16/17*100
 ("gold",2,1): 11.1,  # wrong_element H: 2/18*100
 ("gold",3,1): 0.71,  # wrong_rearrange 7.1*0.1
 ("gold",4,1): 0.245, # 4.9*0.05
 ("gold",5,0): 84.0,  # wrong_mr 3*28
 ("bronze",1,0): 17.0,# 1+16
 ("bronze",2,0): 28.0,# 12+16
 ("bronze",3,0): 68.0,# 40+12+16
 ("bronze",4,0): 648.0,# 36*18
 ("bronze",5,0): 242.0,# 5.5*44
 ("bronze",6,0): 192.0,# 4.8*40
 ("bronze",7,0): 36.0, # 18/0.5
 ("silver",0,0): 57.0, # 40+16+1
 ("silver",1,0): 86.0, # 24+62
 ("silver",2,0): 684.45,# 11.7*58.5
 ("silver",3,0): 2500.0,# 25*100
 ("silver",4,0): 400.0, # 100/0.25
 ("silver",5,0): 33.2,  # 0.4*83
 ("gold",0,1): 0.4,     # forgot_multiply_100
}
for (tier,i,mi),exp in exp_expected.items():
    m = pb[tier][i]["misconceptions"][mi]
    got = m.get("expect")
    if got is None:
        issues.append("EXPECT is null but derivable %s[%d].mc[%d]: expected %s"%(tier,i,mi,exp))
    elif not approx(float(got),exp,0.02):
        issues.append("EXPECT MISMATCH %s[%d].mc[%d]: stored %s, derived %s"%(tier,i,mi,got,exp))

# Check expects sit outside accept window
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        acc = p.get("accept",0)
        sol = float(p["solutions"][0])
        for mi,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is None: continue
            if isinstance(e,list): continue
            if abs(float(e)-sol) <= (acc if acc else 0.011):
                issues.append("DEAD EXPECT %s[%d].mc[%d]: expect %s within accept(%s) of sol %s"%(tier,i,mi,e,acc,sol))

if issues:
    print("ISSUES (%d):"%len(issues))
    for x in issues: print("  -",x)
else:
    print("ALL CLEAN: solutions, boxes, expects, accept-windows verified")
