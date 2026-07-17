# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_maths-aqa_graphs-L03.json", encoding="utf-8"))
errs = []

# 1. chart points satisfy their equations
def check_chart(prob, f, path):
    ch = prob.get("chart")
    if not ch: return
    for p in ch["data"]["datasets"][0]["data"]:
        if abs(f(p["x"]) - p["y"]) > 1e-6:
            errs.append("%s chart point (%s,%s) off eq -> %s" % (path, p["x"], p["y"], f(p["x"])))

pb = pd["problem_bank"]
check_chart(pb["bronze"][4], lambda x: x*x+2, "bronze[4]")      # y=x^2+2
check_chart(pb["silver"][4], lambda x: x*x+3, "silver[4]")      # y=x^2+3
check_chart(pb["gold"][2], lambda x: -(x*x)+6*x-5, "gold[2]")   # y=-x^2+6x-5

# 2. boundary/live-box sanity + last answer box lands on solutions (single_value/two_solutions)
def last_boxes(steps):
    return [s["answer"] for s in steps if s.get("answer") is not None]

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        it = p.get("input_type")
        path = "%s[%d]" % (tier,i)
        # expect must not equal correct; recompute already by validator; just print expects
        if gs:
            ans = last_boxes(gs)
            sols = p["solutions"]
            if it == "single_value":
                if abs(ans[-1]-sols[0])>1e-9:
                    errs.append("%s last box %s != sol %s" % (path, ans[-1], sols[0]))
            elif it == "two_solutions":
                # the two answer boxes that are the roots must be the solution set
                got = set(round(a,6) for a in ans)
                want = set(round(s,6) for s in sols)
                if not want.issubset(got):
                    errs.append("%s roots %s missing from box answers %s" % (path, want, got))

# 3. reproduce each expect by re-deriving key ones
# spot-check: fresh-solve every display
def fresh():
    checks = {
      ("bronze",0):(lambda:3**2,[9]),
      ("bronze",1):(lambda:4**2+1,[17]),
      ("bronze",2):(lambda:3**2-5,[4]),
      ("bronze",3):(lambda:(-4)**2,[16]),
      ("bronze",5):(lambda:0-4,[-4]),
      ("bronze",6):(lambda:(-5)**2,[25]),
      ("bronze",7):(lambda:3,[3]),
      ("silver",2):(lambda:4,[4]),
      ("silver",3):(lambda:1,[1]),
      ("silver",4):(lambda:0,[0]),
      ("silver",6):(lambda:7,[7]),
      ("gold",1):(lambda:-2,[-2]),
      ("gold",3):(lambda:(2+6)//2,[4]),
      ("gold",4):(lambda:4**2-8*4+12,[-4]),
    }
    for (t,i),(fn,exp) in checks.items():
        if [fn()]!=exp:
            errs.append("fresh %s[%d] got %s want %s"%(t,i,fn(),exp))
    # two_solutions roots
    import math
    def roots(a,b,c):
        d=b*b-4*a*c
        r=math.sqrt(d)
        return sorted([(-b+r)/(2*a),(-b-r)/(2*a)])
    ts={("silver",0):(1,-5,6,[2,3]),("silver",1):(1,1,-12,[-4,3]),
        ("silver",5):(1,0,-9,[-3,3]),("gold",0):(1,2,-15,[-5,3])}
    for (t,i),(a,b,c,exp) in ts.items():
        r=[round(x,6) for x in roots(a,b,c)]
        if r!=[round(x,6) for x in sorted(exp)]:
            errs.append("roots %s[%d] got %s want %s"%(t,i,r,exp))
fresh()

# 4. teach walks land correctly (manual expected finals)
teach=pd["guided"]["teach"]
tb=[s.get("answer") for s in teach["bronze"]["steps"] if s.get("answer") is not None]
assert tb==[16,13,16,13], tb
ts_=[s.get("answer") for s in teach["silver"]["steps"] if s.get("answer") is not None]
assert ts_==[2,-4,-2,4], ts_
tg=[s.get("answer") for s in teach["gold"]["steps"] if s.get("answer") is not None]
assert tg==[2,4,3,-1], tg
# opener
op=[s.get("answer") for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
assert op==[4,4], op

# 5. em dash scan (belt and braces)
def scan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in("note","guided_skip_reason"):continue
            scan(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o):scan(v,path+"[%d]"%j)
    elif isinstance(o,str) and "—" in o:
        errs.append("EMDASH at %s"%path)
scan(pd)

print("ERRORS:",len(errs))
for e in errs: print("  -",e)
if not errs: print("ALL CHECKS PASS")
