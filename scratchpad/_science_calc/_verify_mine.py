# -*- coding: utf-8 -*-
import json, io, re

pd = json.load(io.open("lesson_chemistry-calculations-L04@b7b54666b8.json", encoding="utf-8"))
errs = []

# expected correct answers per (tier,index)
CORRECT = {
    ("bronze",0):0.8,("bronze",1):0.7,("bronze",2):0.006,("bronze",3):5,
    ("bronze",4):8,("bronze",5):1.4,("bronze",6):42,("bronze",7):50,
    ("silver",0):1.1,("silver",1):0.9,("silver",2):29.2,("silver",3):11.7,
    ("silver",4):0.007,("silver",5):100,
    ("gold",0):2.4,("gold",1):1.5,("gold",2):0,("gold",3):200,("gold",4):0.7,("gold",5):18,
}

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        want = CORRECT[(tier,i)]
        got = p["solutions"][0]
        if abs(got-want) > 1e-9:
            errs.append("%s[%d] solution %s != expected %s" % (tier,i,got,want))
        # guided_steps final live box lands on solution (for numeric non-MC)
        gs = p.get("guided_steps")
        if gs:
            # last box before check is the answer; verify the compute box equals solution
            box_answers = [s["answer"] for s in gs if s.get("answer") is not None]
            # the phase compute box should contain the solution value somewhere
            if p.get("input_type") != "multiple_choice":
                if want not in [round(a,6) for a in box_answers] and want != 0:
                    # allow: reading problems where solution is a box
                    errs.append("%s[%d] solution %s not among box answers %s" % (tier,i,want,box_answers))
        # expects outside 0.011 of correct
        for j,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is not None:
                ev = e if isinstance(e,list) else [e]
                if len(ev)==1 and abs(ev[0]-want) < 0.011:
                    errs.append("%s[%d].mc[%d] expect %s equals correct %s" % (tier,i,j,e,want))

# Independent recompute of every guided_step arithmetic where pre is 'a OP b = '
def check_walk(steps, path):
    for k,s in enumerate(steps):
        if s.get("answer") is None: continue
        pre = s.get("pre","")
        ans = s["answer"]
        # find patterns like "X ÷ Y =" or "X × Y =" or "A − B ="
        m = re.search(r'([\d.]+)\s*÷\s*([\d.]+)\s*=', pre)
        if m:
            a,b=float(m.group(1)),float(m.group(2))
            if abs(a/b - ans) > 1e-6:
                errs.append("%s[%d] %s : %s÷%s=%s not %s" % (path,k,pre,a,b,a/b,ans))
            continue
        m = re.search(r'([\d.]+)\s*×\s*([\d.]+)\s*=', pre)
        if m:
            a,b=float(m.group(1)),float(m.group(2))
            if abs(a*b - ans) > 1e-6:
                errs.append("%s[%d] %s : %s×%s=%s not %s" % (path,k,pre,a,b,a*b,ans))
            continue
        m = re.search(r'([\d.]+)\s*−\s*([\d.]+)\s*=', pre)
        if m:
            a,b=float(m.group(1)),float(m.group(2))
            if abs(a-b - ans) > 1e-6:
                errs.append("%s[%d] %s : %s−%s=%s not %s" % (path,k,pre,a,b,a-b,ans))
            continue

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("guided_steps"):
            check_walk(p["guided_steps"], "%s[%d].gs"%(tier,i))
for tier in ("bronze","silver","gold"):
    check_walk(pd["guided"]["teach"][tier]["steps"], "teach.%s"%tier)
check_walk(pd["guided"]["opener"]["steps"], "opener")

# expects: recompute the committed error
EXPECT_CHECK = {
    ("bronze",0,0):60/48, ("bronze",3,0):2/10, ("bronze",4,0):0.5/4, ("bronze",7,0):0.4/20,
    ("silver",1,1):30/20, ("silver",2,0):7.3/250, ("silver",3,0):5.85/500,
    ("gold",0,0):15/10, ("gold",1,0):24/10, ("gold",3,0):8/40, ("gold",4,0):42/70,
    ("gold",5,0):36*500, ("gold",5,1):36/0.5,
}
for (tier,i,j),val in EXPECT_CHECK.items():
    e = pb[tier][i]["misconceptions"][j].get("expect")
    ev = e if not isinstance(e,list) else e[0]
    if ev is None or abs(ev - val) > 0.001:
        errs.append("%s[%d].mc[%d] expect %s != committed-error %s" % (tier,i,j,e,val))

if errs:
    print("FAIL:")
    for e in errs: print("  -", e)
else:
    print("ALL VERIFIED CLEAN: 20 solutions, all walk boxes, all expects")
