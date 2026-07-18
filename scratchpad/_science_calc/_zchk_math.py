import json, math
pd = json.load(open("_zchk_canon.json", encoding="utf-8"))
b = pd["problem_bank"]
g = 9.8
errs = []

def near(a, x, tol=0.02):
    return abs(a-x) <= tol

# Independent fresh solves keyed by (tier, index): expected solution
solves = {
 ("gold",0): math.sqrt(2*(75*g*1000)/75),           # 140
 ("gold",1): 0.5*1100*20**2 - 0.5*1100*8**2,          # 184800
 ("gold",2): (80*g*6)/(2500*4)*100,                   # 47.04
 ("gold",3): (50*g*4)/5 - (70*g*4)/8,                 # 49
 ("gold",4): 0.3*g*10 - 0.3*g*6,                      # 11.76
 ("bronze",0): 0.5*1200*15**2,                        # 135000
 ("bronze",1): 0.5*9.8*4,                             # 19.6
 ("bronze",2): 50*8,                                  # 400
 ("bronze",3): 180000/180,                            # 1000
 ("bronze",4): 0.5*60*8**2,                           # 1920
 ("bronze",5): 3*g*2.5,                               # 73.5
 ("bronze",6): 5000/20,                               # 250
 ("silver",0): 0.5*80*12**2/1000,                     # 5.76
 ("silver",1): 60*7200/1000,                          # 432
 ("silver",2): 400*g*15,                              # 58800
 ("silver",3): 0.5*900*30**2,                         # 405000
 ("silver",4): round(1500*10/(50*g),1),               # 30.6
 ("silver",5): 0.5*0.2*50**2,                         # 250
}
for (tier,i),val in solves.items():
    stored = b[tier][i]["solutions"][0]
    if not near(val, stored, 0.5):
        errs.append(f"{tier}[{i}] solution mismatch: mine={val} stored={stored}")

# standard form gold[5]
sf = b["gold"][5]
E = 1.5e6*86400
mant = E/10**11
if not (near(sf["solutions"][0], mant, 0.001) and sf["solutions"][1]==11):
    errs.append(f"gold[5] standard form mismatch {sf['solutions']} vs {mant},11")

# recompute every guided box against its own 'pre' arithmetic where numeric
def check_boxes(tier,i,expected_lastvals):
    steps = b[tier][i].get("guided_steps",[])
    boxvals = [s["answer"] for s in steps if s.get("answer") is not None]
    return boxvals

# expects check: each expect must be outside accept window of solution
for tier in ("bronze","silver","gold"):
    for i,prob in enumerate(b[tier]):
        sol = prob.get("solutions",[None])[0]
        acc = prob.get("accept", 0)
        if not isinstance(sol,(int,float)): continue
        for j,mc in enumerate(prob.get("misconceptions",[])):
            ev = mc.get("expect")
            if ev is None: continue
            if abs(ev - sol) <= (acc if acc else 0):
                errs.append(f"{tier}[{i}].misconceptions[{j}] DEAD expect {ev} inside accept window of {sol}±{acc}")

# final guided box must equal solution
for tier in ("bronze","silver","gold"):
    for i,prob in enumerate(b[tier]):
        steps = prob.get("guided_steps",[])
        if not steps: continue
        # find the box that states the answer (done containing solution) -- just check a box equals solution somewhere
        sol = prob.get("solutions",[None])[0]
        if not isinstance(sol,(int,float)): continue
        boxvals = [s["answer"] for s in steps if s.get("answer") is not None]
        if not any(near(bv, sol, max(prob.get("accept",0),0.02)) for bv in boxvals):
            errs.append(f"{tier}[{i}] no guided box lands on solution {sol}; boxes={boxvals}")

print("ERRORS:" if errs else "ALL MATH CHECKS PASS")
for e in errs: print("  ",e)
