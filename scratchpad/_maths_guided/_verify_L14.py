# -*- coding: utf-8 -*-
"""Independent adversarial check of the built L14 file."""
import json, io
pd = json.load(io.open("lesson_algebra-L14.json", encoding="utf-8"))
pre = None
for e in json.load(io.open("_pre_fanout_dump.json", encoding="utf-8")):
    if e.get("id") == "ab716e12-4427-45e8-9796-a9343073968a":
        pre = e["practice_data"]; break
errs = []

# --- fresh-solve every non-MC problem from its display -------------------
expected = {
    ("bronze",0):17, ("bronze",2):10, ("bronze",4):5, ("bronze",6):-3,
    ("silver",0):11, ("silver",1):-3.5, ("silver",2):81, ("silver",4):6,
    ("silver",5):18, ("silver",6):47,
    ("gold",0):1.516, ("gold",1):-2, ("gold",2):1, ("gold",3):-1, ("gold",4):1.679,
}
pb = pd["problem_bank"]
for (tier,i),val in expected.items():
    got = pb[tier][i]["solutions"]
    if got != [val]:
        errs.append("%s[%d] solution %r != expected %r" % (tier,i,got,val))

# --- MC correctness: option[0] must fit the sequence ---------------------
import re
def seqfit(terms, rule):
    return all(abs(rule(n+1)-t) < 1e-9 for n,t in enumerate(terms))
mc_checks = [
    ("bronze",1,[2,5,10,17,26], lambda n:n*n+1),
    ("bronze",3,[3,12,27,48],   lambda n:3*n*n),
    ("bronze",5,[0,3,8,15,24],  lambda n:n*n-1),
    ("bronze",7,[4,7,12,19,28], lambda n:n*n+3),
    ("silver",3,[5,12,23,38,57],lambda n:2*n*n+n+2),
]
for tier,i,terms,rule in mc_checks:
    p=pb[tier][i]
    if p["solutions"]!=[0]: errs.append("%s[%d] MC sol not 0"%(tier,i))
    if not seqfit(terms,rule): errs.append("%s[%d] rule mismatch"%(tier,i))

# --- expect != answer, and expect present --------------------------------
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"]
        for j,m in enumerate(p.get("misconceptions",[])):
            if "expect" not in m: errs.append("%s[%d].mis[%d] no expect"%(tier,i,j))
            e=m["expect"]
            if e is not None and len(sol)==1 and abs(float(e)-float(sol[0]))<0.011:
                errs.append("%s[%d].mis[%d] expect==answer"%(tier,i,j))

# --- recompute final box lands on solution for every guided walk ---------
def last_box(steps):
    v=None
    for st in steps:
        if st.get("answer") is not None: v=st["answer"]
    return v
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if not gs: continue
        lb=last_box(gs)
        # final box should equal solution OR be a check landing on a verify value;
        # our design: answer box is second-last for some; assert solution appears among boxes
        vals=[st["answer"] for st in gs if st.get("answer") is not None]
        if p["solutions"][0] not in vals:
            errs.append("%s[%d] solution %r not among box values %r"%(tier,i,p["solutions"],vals))

# --- specific box recomputation for gold iterations ----------------------
cbrt=lambda v: v**(1/3) if v>=0 else -((-v)**(1/3))
g1=cbrt(6); g2=cbrt(8-2*g1); g3=cbrt(8-2*g2)
if round(g3,3)!=1.679: errs.append("G4 recompute %r"%g3)

# --- preservation vs pre-dump (allow worked_examples label em-dash fix) --
if pre is not None:
    if pd["related_videos"] != pre["related_videos"]:
        errs.append("related_videos changed")
    if pd["topic_links"] != pre["topic_links"]:
        errs.append("topic_links changed")
    # worked_examples: only labels changed (em dash -> colon); content/question same
    for a,b in zip(pd["worked_examples"], pre["worked_examples"]):
        if a.get("question")!=b.get("question") or a.get("difficulty")!=b.get("difficulty"):
            errs.append("worked_example question/difficulty changed")
        for sa,sb in zip(a["steps"], b["steps"]):
            if sa.get("content")!=sb.get("content"):
                errs.append("worked_example content changed: %r"%sa.get("label"))

# --- em dash scan on student-facing (exclude note) -----------------------
def scan(o,p):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,p+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,p+"[%d]"%i)
    elif isinstance(o,str) and "—" in o:
        errs.append("EM DASH at "+p)
scan(pd,"pd")

print("ERRORS:", len(errs))
for e in errs: print("  -", e)
if not errs: print("ALL CHECKS CLEAN")
