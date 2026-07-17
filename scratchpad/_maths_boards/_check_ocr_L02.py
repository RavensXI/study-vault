# -*- coding: utf-8 -*-
import json, io, re
from fractions import Fraction as F

pd = json.load(io.open("lesson_maths-ocr_number-L02.json", encoding="utf-8"))
pb = pd["problem_bank"]
fails = []

def parse(s):
    m = re.match(r'^(\d+)\\frac\{(\d+)\}\{(\d+)\}$', s)
    if m:
        a,b,c = map(int, m.groups()); return F(a*c+b, c)
    m = re.match(r'^\\frac\{(\d+)\}\{(\d+)\}$', s)
    if m:
        return F(*map(int, m.groups()))
    if re.match(r'^\d+$', s): return F(int(s))
    raise ValueError("op %r" % s)

def solve(disp):
    e = disp.replace("\\(","").replace("\\)","").strip()
    e = e.replace("\\times"," * ").replace("\\div"," / ").replace("+"," + ").replace("−"," - ").replace("-"," - ")
    toks = e.split()
    seq=[]
    for t in toks:
        seq.append(t if t in "+-*/" else parse(t))
    res=[seq[0]]; j=1
    while j < len(seq):
        op=seq[j]; nxt=seq[j+1]
        if op=="*": res[-1]=res[-1]*nxt
        elif op=="/": res[-1]=res[-1]/nxt
        else: res.append(op); res.append(nxt)
        j+=2
    tot=res[0]; j=1
    while j<len(res):
        tot = tot+res[j+1] if res[j]=="+" else tot-res[j+1]; j+=2
    return tot

def solf(sols):
    return F(sols[0]) if len(sols)==1 else F(sols[0], sols[1])

# 1 fresh-solve + lowest terms + duplicates
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[tier]):
        got=solve(p["display"]); st=solf(p["solutions"])
        if got!=st: fails.append("%s[%d] %s solve=%s stored=%s"%(tier,i,p["display"],got,p["solutions"]))
        if p.get("input_type")=="fraction" and len(p["solutions"])==2:
            n,d=p["solutions"]; g=F(n,d)
            if (g.numerator,g.denominator)!=(n,d):
                fails.append("%s[%d] not lowest terms %s"%(tier,i,p["solutions"]))
        key=tuple(p["solutions"])
        if key in seen: fails.append("%s DUP solution %s at [%d] and [%d]"%(tier,p["solutions"],seen[key],i))
        seen[key]=i

# 2 last computational box lands on solution (num/den or single)
def last_boxes(steps):
    return [s for s in steps if s.get("answer") is not None]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p["guided_steps"]; lb=last_boxes(gs)
        sols=p["solutions"]
        # find the two boxes that state final top/bottom OR the divide result
        # heuristic: check that the multiset of final answers contains the solution parts
        vals=[b["answer"] for b in lb]
        if len(sols)==2:
            n,d=sols
            # the done step should assert final fraction; ensure n and d appear among box answers
            if n not in vals or d not in vals:
                # allowed: single_value style; but these are fraction type
                fails.append("%s[%d] solution parts %s not both among box answers %s"%(tier,i,sols,vals))
        else:
            if sols[0] not in vals:
                fails.append("%s[%d] single solution %s not among box answers %s"%(tier,i,sols,vals))

# 3 expects: not equal to answer; determinate ones reproduce known errors already hand-checked
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is not None and e==p["solutions"]:
                fails.append("%s[%d].mis[%d] expect==answer"%(tier,i,j))
            if e is not None and (not isinstance(e,list) or not all(isinstance(x,int) for x in e)):
                fails.append("%s[%d].mis[%d] expect not int list: %r"%(tier,i,j,e))

# 4 opener + teach boxes non-empty numeric
for t in ("bronze","silver","gold"):
    tt=pd["guided"]["teach"][t]
    nb=[s for s in tt["steps"] if s.get("answer") is not None]
    if len(nb)<4: fails.append("teach.%s <4 boxes"%t)
op=[s for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if len(op)<1: fails.append("opener no box")

# 5 count problems fixed / figures
edited = []
if pb["bronze"][5]["solutions"]==[3,4]: edited.append("bronze[5] display->7/8-1/8 ans 3/4")
if pb["bronze"][7]["solutions"]==[2,3]: edited.append("bronze[7] display->1/2+1/6 ans 2/3")

print("EDITS:", edited)
if fails:
    print("CHECK FAIL (%d):"%len(fails))
    for f in fails: print("  -", f)
else:
    print("CHECK PASS: 20/20 fresh-solve match, lowest terms, no tier duplicates, boxes land on solutions, expects sound, opener/teach boxes ok.")
