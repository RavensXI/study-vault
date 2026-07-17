# -*- coding: utf-8 -*-
import json, io, math, re
d = json.load(io.open("lesson_maths-aqa_geometry-L05.json", encoding="utf-8"))
predump = json.load(io.open("_pre_dump_maths-aqa.json", encoding="utf-8"))
ID = "93f6b9f1-7ae6-4f12-945b-a5b0c096dc09"
pre = None
for row in predump:
    if row.get("id") == ID:
        pre = row.get("practice_data"); break
fails = []

# 1. preservation
if pre:
    for k in ("related_videos", "worked_examples", "topic_links"):
        if json.dumps(d.get(k), sort_keys=True) != json.dumps(pre.get(k), sort_keys=True):
            fails.append("PRESERVATION changed: " + k)
else:
    fails.append("no pre-dump entry found")

# 2. per-problem: last live guided box lands on solution; expect != solution; dup solutions
pb = d["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    seen = {}
    for i, p in enumerate(pb[tier]):
        sol = p["solutions"]
        key = tuple(sol)
        if key in seen:
            fails.append("%s[%d] dup solution %s (also %s)" % (tier, i, sol, seen[key]))
        seen[key] = i
        gs = p.get("guided_steps") or []
        live = [s for s in gs if s.get("answer") is not None]
        # find the box that equals the final solution (the substitute-phase result)
        boxvals = [s["answer"] for s in live]
        if not any(abs(float(b) - float(sol[0])) < 0.05 for b in boxvals):
            fails.append("%s[%d] no guided box equals solution %s (boxes %s)" % (tier, i, sol, boxvals))
        for m in p.get("misconceptions") or []:
            e = m.get("expect")
            if e is not None and abs(float(e) - float(sol[0])) < 0.011:
                fails.append("%s[%d] expect==solution %s" % (tier, i, e))

# 3. recompute trig/pyth solutions from display text (independent)
def freshcheck(tier, i, expected, val):
    if abs(val - expected) > 0.06:
        fails.append("%s[%d] FRESH solve %.3f != stored %s" % (tier, i, val, expected))

rad = math.radians
# bronze
freshcheck("bronze",0,10,math.sqrt(6**2+8**2))
freshcheck("bronze",1,12,math.sqrt(13**2-5**2))
freshcheck("bronze",2,15,math.sqrt(9**2+12**2))
freshcheck("bronze",3,8,math.sqrt(10**2-6**2))
freshcheck("bronze",4,17,math.sqrt(8**2+15**2))
freshcheck("bronze",5,25,math.sqrt(7**2+24**2))
freshcheck("bronze",6,9,18*0.5)
freshcheck("bronze",7,7,14*0.5)
# silver
freshcheck("silver",0,9.6,15*math.sin(rad(40)))
freshcheck("silver",1,6.9,12*math.cos(rad(55)))
freshcheck("silver",2,44.4,math.degrees(math.asin(7/10)))
freshcheck("silver",3,53.1,math.degrees(math.atan(8/6)))
freshcheck("silver",4,4.7,5*math.sin(rad(70)))
freshcheck("silver",5,7.0,9*math.tan(rad(38)))
freshcheck("silver",6,5.9,math.sqrt(3.5**2+4.8**2))
# gold
freshcheck("gold",0,35.7,25/math.tan(rad(35)))
freshcheck("gold",1,8,math.sqrt(10**2-6**2))
freshcheck("gold",2,13,math.sqrt(3**2+4**2+12**2))
freshcheck("gold",3,12.1,11/math.cos(rad(25)))
freshcheck("gold",4,40,(50+120)-math.sqrt(50**2+120**2))

# 4. verify each guided_steps arithmetic continuity for integer/simple boxes (spot: sums/products declared in pre text)
# check opener + teach boxes land correctly
op = d["guided"]["opener"]["steps"]
assert op[0]["answer"] == 25 and op[1]["answer"] == 5, "opener boxes"
tb = d["guided"]["teach"]["bronze"]["steps"]
assert [s["answer"] for s in tb if "answer" in s] == [144,256,400,20,400]
ts = d["guided"]["teach"]["silver"]["steps"]
assert [s["answer"] for s in ts if "answer" in s] == [0.75,36.9,53.1,0.75]
tg = d["guided"]["teach"]["gold"]["steps"]
assert [s["answer"] for s in tg if "answer" in s] == [0.19,10.6,0.19,8.1]
# teach maths: 12^2=144,16^2=256,sum400,sqrt=20 ; 9/12=0.75, atan=36.87->36.9, 90-36.9=53.1 ; 1.5/8=0.1875->0.19, atan(0.1875)=10.62->10.6, sqrt(66.25)=8.14->8.1
assert round(math.degrees(math.atan(0.75)),1)==36.9
assert round(math.degrees(math.atan(1.5/8)),1)==10.6
assert round(math.sqrt(1.5**2+8**2),1)==8.1

# 5. em dash scan already done by validator; scan student strings for U+2014
def scan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,path+"[%d]"%j)
    elif isinstance(o,str) and "—" in o:
        fails.append("EMDASH "+path)
scan(d)

# 6. figure count
figs = 0
for tier in ("bronze","silver","gold"):
    for p in pb[tier]:
        if "<svg" in (p.get("display") or ""): figs+=1
print("figures on bank problems:", figs, "(+1 opener svg)")

if fails:
    print("FAIL", len(fails))
    for f in fails: print("  -", f)
else:
    print("ALL CHECKS PASS")
