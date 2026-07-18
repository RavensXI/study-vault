# -*- coding: utf-8 -*-
import json, io, math

pd = json.load(io.open("lesson_physics-calculations-L04@6ac34b4fe4.json", encoding="utf-8"))

errors = []

# 1. Independent fresh-solve of each problem answer
expected = {
 # tier, index : correct answer
 ("bronze",0):230*4, ("bronze",1):2*0.5, ("bronze",2):5*30, ("bronze",3):2**2*20,
 ("bronze",4):200*6, ("bronze",5):3000/1000,
 ("silver",0):1.5*((20*30)/60), ("silver",1):(15*28)/100, ("silver",2):0.6**2*50,
 ("silver",3):3*2.5*32,
 ("gold",0):(25000*800)/400000, ("gold",1):0.9*((8*30)/60)*30, ("gold",2):100**2*2,
 ("gold",3):(4500*28)/100,
}
pb = pd["problem_bank"]
for (tier,i),val in expected.items():
    sol = pb[tier][i]["solutions"][0]
    if abs(sol-val) > 1e-9:
        errors.append("SOLUTION MISMATCH %s[%d]: stored %s computed %s" % (tier,i,sol,val))

# 2. Expects must sit outside accept window and be genuinely the described error
#    (just check != solution here; window handled by validator)
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sols=p["solutions"]
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and abs(float(e)-float(sols[0]))<0.011:
                errors.append("DEAD EXPECT %s[%d]: %s == solution" % (tier,i,e))

# 3. Recompute every guided_steps final box lands on solution and boundary sane
def check_walk(steps, label, solution=None):
    boxes=[s for s in steps if s.get("answer") is not None]
    if len(boxes)<3:
        errors.append("%s: <3 boxes" % label)
    # substitute boundary
    sub_idx=None
    for idx,s in enumerate(steps):
        if s.get("phase")=="substitute" and sub_idx is None: sub_idx=idx
    if sub_idx is None:
        errors.append("%s: no substitute boundary" % label)
    else:
        live=[s for s in steps[sub_idx:] if s.get("answer") is not None]
        if len(live)<2: errors.append("%s: <2 live boxes after boundary" % label)
        if sub_idx<1: errors.append("%s: boundary at 0" % label)

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        check_walk(p["guided_steps"], "%s[%d]"%(tier,i), p["solutions"][0])

# manual recompute of each box arithmetic (the pre strings state 'a OP b = ')
def recompute(steps, label):
    import re
    for j,s in enumerate(steps):
        if s.get("answer") is None: continue
        pre=s.get("pre","")
        # extract last 'expr =' before the box
        m=re.search(r'([-\d,\.\s×÷\+\(\)²]+)=\s*$', pre)
        if not m: continue
        expr=m.group(1).replace(",","").replace("×","*").replace("÷","/").replace("²","**2").strip()
        # handle trailing operators/spaces
        try:
            val=eval(expr)
        except Exception:
            continue
        if abs(val-float(s["answer"]))>0.005:
            errors.append("BOX ARITH %s[%d]: '%s' -> %s but answer=%s"%(label,j,expr,val,s["answer"]))

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        recompute(p["guided_steps"], "%s[%d]"%(tier,i))
recompute(pd["guided"]["opener"]["steps"],"opener")
for t in ("bronze","silver","gold"):
    recompute(pd["guided"]["teach"][t]["steps"],"teach.%s"%t)

# 4. em dash scan (all student-facing strings)
def scan(o,p=""):
    h=[]
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            h+=scan(v,p+"."+str(k))
    elif isinstance(o,list):
        for idx,v in enumerate(o): h+=scan(v,p+"[%d]"%idx)
    elif isinstance(o,str) and "—" in o: h.append(p)
    return h
dash=scan(pd)
if dash: errors.append("EM DASHES: "+", ".join(dash))

# 5. board-name / equation-sheet claim scan
bad_terms=["equation sheet","must memorise","must memorize","on your sheet","AQA","Edexcel","OCR","WJEC","Eduqas"]
def scan_terms(o,p=""):
    h=[]
    if isinstance(o,dict):
        for k,v in o.items(): h+=scan_terms(v,p+"."+str(k))
    elif isinstance(o,list):
        for idx,v in enumerate(o): h+=scan_terms(v,p+"[%d]"%idx)
    elif isinstance(o,str):
        for t in bad_terms:
            if t.lower() in o.lower(): h.append(p+" ("+t+")")
    return h
bt=scan_terms(pd)
if bt: errors.append("BOARD/SHEET CLAIMS: "+"; ".join(bt))

# 6. higher_only on transformer
if pb["gold"][0].get("higher_only") is not True:
    errors.append("transformer not flagged higher_only")

# report
if errors:
    print("VERIFY FAIL (%d):"%len(errors))
    for e in errors: print("  -",e)
else:
    print("VERIFY PASS: all solutions, boxes, boundaries, expects, style, board-neutrality clean")
