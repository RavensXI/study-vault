# -*- coding: utf-8 -*-
"""Adversarial verify: fresh-solve each display, recompute guided boxes, check expects."""
import json, io
pd = json.load(io.open("lesson_maths-aqa_probability-statistics-L04.json", encoding="utf-8"))
errs = []

# independent fresh solves keyed by (tier,index)
def mean(xs): return sum(xs)/len(xs)
def median(xs):
    s=sorted(xs); n=len(s)
    return s[n//2] if n%2 else (s[n//2-1]+s[n//2])/2
solve = {
 ("bronze",0): mean([4,8,6,10,7]),
 ("bronze",1): median([3,9,1,7,5]),
 ("bronze",2): 2,  # mode of 7,2,8,2,5,2,9
 ("bronze",3): max([14,3,8,22,11])-min([14,3,8,22,11]),
 ("bronze",4): 8*5,
 ("bronze",5): median([10,4,15,7,9,3]),
 ("bronze",6): mean([12,15,18,21,24]),
 ("bronze",7): 60,  # mode
 ("silver",0): round((1*3+2*5+3*8+4*4)/(3+5+8+4),4),
 ("silver",1): (4*5+10*15+6*25)/(4+10+6),
 ("silver",2): 5*18-4*15,
 ("silver",3): 0,  # MC index modal class 20-40
 ("silver",4): 0,  # MC median class 10-20
 ("silver",5): 5,  # median from freq table
 ("silver",6): 0,  # MC
 ("gold",0): round((3*5+7*15+12*25+8*35)/(3+7+12+8),1),
 ("gold",1): (10*12-6*10)/4,
 ("gold",2): 3*15,
 ("gold",3): 20+5,
 ("gold",4): 10,
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        exp = solve[(tier,i)]
        got = p["solutions"][0]
        if abs(float(got)-float(exp))>0.011:
            errs.append("SOLVE %s[%d] stored %s but computed %s" % (tier,i,got,exp))
        # last live box lands on solution (skip MC)
        gs = p.get("guided_steps")
        if gs:
            boxes=[s for s in gs if s.get("answer") is not None]
            # find the box that equals the solution
            if p["input_type"]!="multiple_choice":
                if not any(abs(float(b["answer"])-float(got))<0.011 for b in boxes):
                    errs.append("WALK %s[%d] no box lands on solution %s" % (tier,i,got))
        # expect != solution and derivable-distinct
        for j,m in enumerate(p.get("misconceptions") or []):
            e=m.get("expect")
            if e is not None and abs(float(e)-float(got))<0.011 and p["input_type"]!="multiple_choice":
                errs.append("EXPECT %s[%d].m%d equals solution" % (tier,i,j))

# duplicate solutions within tier (single_value only)
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pd["problem_bank"][tier]):
        if p["input_type"]=="multiple_choice": continue
        k=tuple(p["solutions"])
        if k in seen: errs.append("DUP %s: %s at [%d] and [%d]"%(tier,k,seen[k],i))
        seen[k]=i

# recompute continuity of a few key walks: verify arithmetic of pre-strings that contain 'a op b ='
import re
# Evaluate the trailing arithmetic expression before '='. Subtraction uses U+2212;
# ASCII '-' only appears inside class ranges, so excluding it avoids range confusion.
def arith(pre):
    m=re.search(r"([0-9\.\s+×÷−]+)=\s*$", pre)
    if not m: return None
    expr=m.group(1).replace("×","*").replace("÷","/").replace("−","-").strip()
    if not re.search(r"[+\-*/]", expr): return None
    try: return eval(expr)
    except Exception: return None
def check_steps_arith(steps,label):
    for s in steps:
        if s.get("answer") is None: continue
        r=arith(s.get("pre",""))
        if r is not None and abs(r-float(s["answer"]))>0.011:
            errs.append("ARITH %s '%s' -> %s but answer %s"%(label,s['pre'].strip(),r,s["answer"]))
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        check_steps_arith(p.get("guided_steps",[]),"%s[%d]"%(tier,i))
for tier,t in pd["guided"]["teach"].items():
    check_steps_arith(t["steps"],"teach.%s"%tier)
check_steps_arith(pd["guided"]["opener"]["steps"],"opener")

# preservation
live=json.load(io.open("_live_ps04.json",encoding="utf-8"))
for f in ("related_videos","topic_links","worked_examples"):
    if json.dumps(pd[f],sort_keys=True)!=json.dumps(live[f],sort_keys=True):
        errs.append("PRESERVE %s changed"%f)

if errs:
    print("FAIL",len(errs))
    for e in errs: print("  -",e)
else:
    print("VERIFY OK: solves, walks land, expects distinct, no dups, arithmetic clean, preserved")
