# -*- coding: utf-8 -*-
import json, io, re

pd = json.load(io.open("lesson_chemistry-calculations-L02@5b02ac14f2.json", encoding="utf-8"))
errs = []

# Expected fresh-solve answers (independently computed)
EXPECT = {
    ("bronze",0): 40,    # CuCO3 62/124=0.5 *80 =40
    ("bronze",1): 80,    # Mg 48/24=2 *40 =80
    ("bronze",2): 44,    # CaCO3 100/100=1 *44 =44
    ("bronze",3): 1,     # Fe 56/56=1
    ("bronze",4): 2,     # Na 4/2=2
    ("silver",0): 80,    # Fe 56/56=1 /2=0.5 *160 =80
    ("silver",1): 34,    # N2 28/28=1 *2=2 *17 =34
    ("silver",2): 68,    # H2 12/2=6 *2/3=4 *17 =68
    ("silver",3): 16.2,  # Zn 13/65=0.2 *81 =16.2
    ("gold",0): 133.5,   # Al 27/27=1 *133.5
    ("gold",1): 36,      # H2 4/2=2 *18 =36
    ("gold",2): 88,      # CH4 32/16=2 *44 =88
}

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pb[tier]):
        sol = p["solutions"][0]
        exp = EXPECT[(tier,i)]
        if abs(sol-exp) > 1e-9:
            errs.append("%s[%d] solution %s != fresh %s"%(tier,i,sol,exp))
        key=sol
        if key in seen:
            errs.append("%s[%d] DUPLICATE solution %s"%(tier,i,sol))
        seen.add(key)
        # expects outside accept window
        acc = p.get("accept", 0.005)
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            if abs(float(e)-sol) <= acc:
                errs.append("%s[%d].mc[%d] expect %s inside accept window of %s (acc %s)"%(tier,i,j,e,sol,acc))
        # recompute final box lands on solution
        gs=p["guided_steps"]
        finalboxes=[s for s in gs if s.get("answer") is not None]
        # the mass box (second to last box) should equal solution for mass problems
        # just check the solution appears as some box answer
        boxvals=[s["answer"] for s in finalboxes]
        if sol not in boxvals:
            errs.append("%s[%d] solution %s not reached by any box %s"%(tier,i,sol,boxvals))

# Recompute each mass_walk chain arithmetically from its pre-text numbers
def check_walk(tier,i,gs):
    for k,s in enumerate(gs):
        if s.get("answer") is None: continue
        pre=s.get("pre","")
        # extract an arithmetic expression like "a ÷ b =" or "a × b =" or "a op b op c ="
        expr=pre.split("=")[-2] if pre.count("=")>=1 else ""
        # find the segment right before the trailing '='
        m=re.findall(r'([\d\.]+)\s*([÷×\-])\s*([\d\.]+)(?:\s*([÷×])\s*([\d\.]+))?', pre)
        if not m: continue
        a,op,b,op2,c=m[-1]
        val=float(a)
        val = val/float(b) if op=='÷' else val*float(b) if op=='×' else val-float(b)
        if op2:
            val = val/float(c) if op2=='÷' else val*float(c)
        if abs(val - s["answer"])>1e-9:
            errs.append("%s[%d] box[%d] pre '%s' computes %s != answer %s"%(tier,i,k,pre.strip(),val,s["answer"]))

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        check_walk(tier,i,p["guided_steps"])

# teach walks
for tier,t in pd["guided"]["teach"].items():
    check_walk("teach-"+tier,0,t["steps"])
# opener
check_walk("opener",0,pd["guided"]["opener"]["steps"])

# em dash scan (excluding note/guided_skip_reason)
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+str(k))
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,path+"[%d]"%j)
    elif isinstance(o,str) and "—" in o:
        errs.append("EM DASH at "+path+": "+o[:60])
scan(pd,"pd")

print("ERRORS:" if errs else "ALL CLEAN")
for e in errs: print("  -",e)
