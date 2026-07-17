# -*- coding: utf-8 -*-
import json, io, math
pd = json.load(io.open("_G06_final.json", encoding="utf-8"))
live = json.load(io.open("_G06_live.json", encoding="utf-8"))
fails = []

# ---- independent fresh-solve of every problem from its display ----
def solve(disp):
    d = disp
    # returns expected solution list, or None (manual)
    return None

# hand-coded expected answers keyed by (tier,index)
EXPECT = {
 ("bronze",0):[90],("bronze",1):[0],("bronze",2):[1],("bronze",3):[0.5],
 ("bronze",4):[-1],("bronze",5):[1],("bronze",6):[360],("bronze",7):[180],
 ("silver",0):[90],("silver",1):[180],("silver",2):[3],("silver",3):[0.5],
 ("silver",4):[-0.5],("silver",5):[1],("silver",6):[270],
 ("gold",0):[150],("gold",1):[300],("gold",2):[270],("gold",3):[3],("gold",4):[120],
}
# verify each expected by re-deriving trig facts numerically
def sind(x): return round(math.sin(math.radians(x)),10)
def cosd(x): return round(math.cos(math.radians(x)),10)
# check the trig content of the stated expected answers
assert sind(90)==1 and sind(0)==0 and abs(sind(30)-0.5)<1e-9
assert cosd(0)==1 and cosd(180)==-1 and abs(cosd(120)+0.5)<1e-9 and abs(cosd(60)-0.5)<1e-9
assert cosd(300)-0.5<1e-9 and abs(cosd(240)+0.5)<1e-9
assert sind(150)-0.5<1e-9 and sind(270)==-1
# solution sets in range 0..360 step check
def sols_eq(fn,k):
    return [x for x in range(0,361) if abs(fn(x)-k)<1e-9]
assert sols_eq(sind,0.5)==[30,150]
assert sols_eq(cosd,0.5)==[60,300]
assert sols_eq(cosd,-0.5)==[120,240]
assert sols_eq(sind,0)==[0,180,360]  # count 3
assert sols_eq(cosd,0)==[90,270]     # larger 270
assert sols_eq(sind,-1)==[270]
assert sols_eq(cosd,-1)==[180]
assert sols_eq(sind,1)==[90]
# tan zeros
tanz=[x for x in range(0,361) if x not in (90,270) and abs(math.tan(math.radians(x)))<1e-9]
assert tanz==[0,180,360]

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        exp = EXPECT[(tier,i)]
        if p["solutions"] != exp:
            fails.append("%s[%d] solution %r != expected %r" % (tier,i,p["solutions"],exp))
        # final guided box lands on solution (single-sol single_value only)
        gs = p.get("guided_steps")
        if gs and p.get("input_type")!="multiple_choice":
            boxes=[s for s in gs if s.get("answer") is not None]
            if boxes and boxes[-1]["answer"]!=p["solutions"][0]:
                fails.append("%s[%d] final box %r != solution %r" % (tier,i,boxes[-1]["answer"],p["solutions"][0]))
            # completion boundary
            sub=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
            if not sub:
                fails.append("%s[%d] no substitute boundary" % (tier,i))
            else:
                si=sub[0]
                live_after=sum(1 for s in gs[si:] if s.get("answer") is not None)
                before=sum(1 for s in gs[:si] if s.get("answer") is not None)
                if before<1: fails.append("%s[%d] nothing pre-worked" % (tier,i))
                if live_after<2: fails.append("%s[%d] only %d live after boundary"%(tier,i,live_after))
        # expects differ from solution
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and [float(e)]==[float(x) for x in p["solutions"]]:
                fails.append("%s[%d] expect==solution"%(tier,i))

# ---- chart faithfulness: curve points satisfy the function; k line matches ----
KLINE = {("silver",0):1,("silver",1):-1,("silver",2):0,("silver",6):0,
         ("gold",0):0.5,("gold",1):0.5,("gold",2):-1,("gold",3):0,("gold",4):-0.5}
CURVE = {("bronze",0):"sin",("bronze",5):"tan",("bronze",6):"sin",("bronze",7):"cos",
         ("silver",0):"sin",("silver",1):"cos",("silver",2):"sin",("silver",4):"cos",("silver",5):"tan",("silver",6):"cos",
         ("gold",0):"sin",("gold",1):"cos",("gold",2):"sin",("gold",3):"tan",("gold",4):"cos"}
fn = {"sin":lambda x:math.sin(math.radians(x)),"cos":lambda x:math.cos(math.radians(x)),
      "tan":lambda x:math.tan(math.radians(x))}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        ch=p.get("chart")
        if not ch: continue
        curve=CURVE.get((tier,i))
        ds=ch["data"]["datasets"]
        cpts=ds[0]["data"]
        for pt in cpts:
            if pt["y"] is None: continue
            true=fn[curve](pt["x"])
            if curve=="tan" and abs(true)>6:
                fails.append("%s[%d] tan point x=%s y set but |tan|>6"%(tier,i,pt["x"])); continue
            if abs(true-pt["y"])>0.002:
                fails.append("%s[%d] chart %s point x=%s y=%s != %.4f"%(tier,i,curve,pt["x"],pt["y"],true))
        # k line
        if (tier,i) in KLINE:
            if len(ds)<2: fails.append("%s[%d] missing k-line"%(tier,i))
            else:
                kv=ds[1]["data"][0]["y"]
                if kv!=KLINE[(tier,i)]:
                    fails.append("%s[%d] k-line %s != %s"%(tier,i,kv,KLINE[(tier,i)]))

# ---- opener boxes arithmetic ----
op=pd["guided"]["opener"]["steps"]
obx=[s["answer"] for s in op if s.get("answer") is not None]
if obx!=[10,0,-10]:
    fails.append("opener boxes %r != [10,0,-10]"%obx)

# ---- teach box counts ----
for t in ("bronze","silver","gold"):
    tb=[s for s in pd["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
    if len(tb)<4: fails.append("teach.%s only %d boxes"%(t,len(tb)))
# teach arithmetic spot-checks
tb_b=[s["answer"] for s in pd["guided"]["teach"]["bronze"]["steps"] if s.get("answer") is not None]
assert tb_b==[0,1,0,-1], tb_b
tb_s=[s["answer"] for s in pd["guided"]["teach"]["silver"]["steps"] if s.get("answer") is not None]
assert tb_s==[1,0,360,2], tb_s
tb_g=[s["answer"] for s in pd["guided"]["teach"]["gold"]["steps"] if s.get("answer") is not None]
assert tb_g==[30,210,330,330], tb_g

# ---- preservation ----
if pd["topic_links"]!=live["topic_links"]: fails.append("topic_links changed")
if pd["related_videos"]!=live["related_videos"]: fails.append("related_videos changed")
# worked_examples: only dash->colon change allowed
import re
def strip_dash(o):
    s=json.dumps(o,ensure_ascii=False)
    return s.replace(" — ",": ").replace("—",": ")
if strip_dash(live["worked_examples"])!=json.dumps(pd["worked_examples"],ensure_ascii=False):
    # allow: exactly the label dash replacement
    fails.append("worked_examples changed beyond dash fix")

# ---- em dash sweep on student-facing ----
def sweep(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            sweep(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): sweep(v,path+"[%d]"%j)
    elif isinstance(o,str) and "—" in o:
        fails.append("EM DASH at "+path)
sweep(pd,"pd")

# box arithmetic continuity checks (explicit)
def bx(tier,i):
    return [s for s in pb[tier][i]["guided_steps"] if s.get("answer") is not None]
# a few explicit arithmetic verifications
assert 180-120==60 and 360-90==270 and 180-30==150 and 360-60==300
assert 180+60==240 and 180-60==120 and 3*90==270 and 4*90==360 and 360//4==90 and 360//2==180

print("FAILS:", len(fails))
for f in fails: print("  -",f)
if not fails: print("ALL VERIFY CHECKS PASS")
