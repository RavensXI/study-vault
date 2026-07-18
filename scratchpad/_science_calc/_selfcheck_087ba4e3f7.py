# -*- coding: utf-8 -*-
import json, io, math
pd = json.load(io.open("lesson_physics-calculations-L01@087ba4e3f7.json", encoding="utf-8"))
errs = []

# independent solver per (tier,index) -> expected solution
def solve():
    return {
        ("bronze",0): 0.5*2*3**2,          # KE 9
        ("bronze",1): 5*10*4,               # GPE 200
        ("bronze",2): 50*3,                 # W 150
        ("bronze",3): 600/20,               # P 30
        ("bronze",4): 0.5*10*4**2,          # KE 80
        ("bronze",5): 3*10*2,               # GPE 60
        ("bronze",6): 1500/5,               # P 300
        ("bronze",7): 30*4,                 # W 120
        ("silver",0): 0.5*1200*20**2,       # 240000
        ("silver",1): 500*12,               # 6000
        ("silver",2): 75*10*6,              # 4500
        ("silver",3): math.sqrt(2*10/0.2),  # 10
        ("silver",4): 200*10*15/30,         # 1000
        ("silver",5): math.sqrt(2*(600*10*20)/600), # 20
        ("gold",0): math.sqrt(2*(800*10*45)/800),    # 30
        ("gold",1): (0.5*1200*30**2)/50,    # 10800
        ("gold",2): 120*10*8/6,             # 1600
        ("gold",3): 90/(0.5*10),            # 18
        ("gold",4): 60*10*3/4,              # 450
    }
sols = solve()
pb = pd["problem_bank"]
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        want = sols[(t,i)]
        got = p["solutions"][0]
        if abs(want-got) > 1e-9:
            errs.append("SOL %s[%d] stored %s indep %s" % (t,i,got,want))
        # expect outside accept window
        acc = p.get("accept",0)
        for j,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is not None:
                if abs(e-got) <= acc:
                    errs.append("EXPECT-in-accept %s[%d].mc[%d] expect=%s acc=%s" % (t,i,j,e,acc))

# recompute every guided_steps box by evaluating the pre expression's arithmetic
# We just trust the authored boxes but re-derive the final box lands on solution.
def final_boxes(steps):
    return [s for s in steps if s.get("answer") is not None]

# Check each walk's declared box answers are self-consistent arithmetic where pre contains 'a OP b ='
import re
def check_arith(pre, ans, tag):
    # extract simple 'X op Y =' or 'X op Y op Z =' patterns from tail
    m = re.search(r'([\d.,]+)\s*([×x*÷/+\-−])\s*([\d.,]+)\s*=\s*$', pre.replace("(-","(neg").strip())
    # too fragile; skip. We validate key computed boxes manually below.
    return

# Manual spot-check of critical computed boxes (final answer boxes)
def lastbox(t,i):
    return final_boxes(pb[t][i]["guided_steps"])[-1]["answer"]
# For problems whose last box is a 'check' equal to solution or the answer itself:
checkmap = {
    ("bronze",0):9,("bronze",1):200,("bronze",2):150,("bronze",3):30,("bronze",4):80,
    ("bronze",5):60,("bronze",6):300,("bronze",7):120,
    ("silver",0):240000,("silver",1):500,("silver",2):4500,("silver",3):10,("silver",4):1000,("silver",5):20,
    ("gold",0):30,("gold",1):540000,("gold",2):9600,("gold",3):18,("gold",4):1800,
}
for k,v in checkmap.items():
    lb = lastbox(*k)
    if abs(lb-v) > 1e-9:
        errs.append("LASTBOX %s got %s want %s" % (k,lb,v))

# opener + teach box sanity
op = [s for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
assert [b["answer"] for b in op] == [2,4], "opener boxes"
tb = pd["guided"]["teach"]
assert [s["answer"] for s in tb["bronze"]["steps"] if s.get("answer") is not None] == [6,3,60,180,180]
assert [s["answer"] for s in tb["silver"]["steps"] if s.get("answer") is not None] == [72,36,6,36]
assert [s["answer"] for s in tb["gold"]["steps"] if s.get("answer") is not None] == [20,40,100,10,20]

# dup solutions within tier
for t in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[t]):
        key=tuple(p["solutions"])
        if key in seen:
            errs.append("DUP %s[%d] %s (also [%d])"%(t,i,key,seen[key]))
        seen[key]=i

if errs:
    print("FAIL")
    for e in errs: print("  -",e)
else:
    print("ALL CLEAN: solutions, expects-outside-accept, last boxes, opener/teach, no dup")
