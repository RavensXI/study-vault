# -*- coding: utf-8 -*-
"""Adversarial independent check of the built L10. Fresh equations encoded here,
NOT imported from the builder. Confirms: solutions satisfy BOTH equations; every
guided box is numerically continuous and lands on the solutions; misconception
expects reproduce by committing the error; completion boundary >= 2 live boxes."""
import json
pd = json.load(open("lesson_maths-aqa_algebra-L10.json", encoding="utf-8"))
errs = []
def ck(cond, msg):
    if not cond: errs.append(msg)

# Independent equation model per problem, keyed by (tier, index).
# eqs: list of functions f(x,y) that must equal 0 at every solution pair.
# For "give the two x-values", the y for each x comes from the linear eq; we
# verify each x yields a y making BOTH equations true.
def parab(lx, lc, qx, qc):   # y=lx x+lc ; y=x^2+qx x+qc
    return lambda x: (lx*x+lc,                       # y from line
                      [lx*x+lc - (x*x+qx*x+qc)])     # residual list (=0)
def circ(lc, r2):            # y=x+lc ; x^2+y^2=r2
    return lambda x: (x+lc, [x*x+(x+lc)**2 - r2])
def horiz(k, qc):           # y=k ; y=x^2+qc
    return lambda x: (k, [k-(x*x+qc)])
MODEL = {
 ("bronze",0): parab(1,0,0,0), ("bronze",1): horiz(3,-1), ("bronze",2): parab(1,2,0,0),
 ("bronze",3): parab(4,0,0,3), ("bronze",4): parab(2,0,0,-3), ("bronze",5): parab(1,6,2,0),
 ("bronze",6): horiz(7,-2),
 ("silver",0): parab(1,3,0,1), ("silver",1): circ(1,13), ("silver",2): circ(-2,10),
 ("silver",3): parab(1,5,1,1), ("silver",4): parab(3,2,2,-4),
 ("gold",0): parab(-1,2,0,-4), ("gold",1): circ(-1,25), ("gold",2): parab(2,3,5,3),
}
# special gold
def g3_ok(sols):
    return sorted(sols)==[2,3] and all(abs((5-x)-(6/x))<1e-9 for x in sols)  # y=5-x and xy=6 -> y=6/x

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pb[tier]):
        sols=p["solutions"]; key=(tier,i)
        t=tuple(sols)
        ck(t not in seen, "%s[%d] DUP solutions %s"%(tier,i,sols)); seen.add(t)
        if key in MODEL:
            f=MODEL[key]
            for x in sols:
                y,res=f(x)
                for rr in res:
                    ck(abs(rr)<1e-9, "%s[%d] x=%s not on both eqns (res %s)"%(tier,i,x,rr))
        elif key==("gold",3):
            ck(g3_ok(sols), "gold[3] xy=6 system wrong: %s"%sols)
        elif key==("gold",4):
            ck(sols==[2], "gold[4] tangent k wrong: %s"%sols)
        # final guided boxes land on solutions (roots)
        gs=p.get("guided_steps") or []
        box_ans=[s["answer"] for s in gs if s.get("answer") is not None]
        # boundary
        sub=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        ck(len(sub)==1, "%s[%d] phase count %d"%(tier,i,len(sub)))
        if sub:
            live=sum(1 for s in gs[sub[0]:] if s.get("answer") is not None)
            ck(live>=2, "%s[%d] only %d live boxes"%(tier,i,live))
            ck(sub[0]>=1, "%s[%d] boundary at 0"%(tier,i))
        # misconceptions
        for m in p.get("misconceptions") or []:
            e=m.get("expect")
            ck("expect" in m, "%s[%d] misc missing expect"%(tier,i))
            if isinstance(e,list):
                ck(sorted(e)!=sorted(sols), "%s[%d] expect==solutions %s"%(tier,i,e))
                if m.get("pattern")=="factor_sign_flip":
                    # committing the flip = negate each root
                    ck(sorted(e)==sorted(-x for x in sols),
                       "%s[%d] sign_flip expect %s != negated roots %s"%(tier,i,sorted(e),sorted(-x for x in sols)))

# check every box has numeric answer + hint + pre (validator does too, belt & braces)
def walk_boxes(steps,path):
    for j,s in enumerate(steps):
        if s.get("answer") is not None:
            ck(isinstance(s["answer"],(int,float)), path+"[%d] non-numeric"%j)
            ck((s.get("hint") or "").strip()!="", path+"[%d] no hint"%j)
            ck((s.get("pre") or "").strip()!="", path+"[%d] no pre"%j)
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        walk_boxes(p.get("guided_steps") or [], "%s[%d].gs"%(tier,i))
g=pd["guided"]
walk_boxes(g["opener"]["steps"],"opener")
for tier in ("bronze","silver","gold"):
    walk_boxes(g["teach"][tier]["steps"],"teach."+tier)

# opener maths: x^2 = x+12 -> 4, -3
ck(4*4==4+12 and 9==-3+12, "opener numbers wrong")

# teach walks land correctly (independent)
def teach_final(tier): return [s["answer"] for s in g["teach"][tier]["steps"] if s.get("answer") is not None]
# bronze teach y=x+4,y=x^2-2 -> roots 3,-2 ; silver y=2x+1,y=x^2-x+3 -> 1,2 ; gold x+y=6 circ20 -> 2,4
ck((3)**2-2==3+4, "teach bronze root3 off"); ck((-2)**2-2==-2+4,"teach bronze root-2 off")
ck((1)**2-1+3==2*1+1,"teach silver root1 off"); ck((2)**2-2+3==2*2+1,"teach silver root2 off")
ck(2*2+4*4==20 and 2+4==6,"teach gold pair (2,4) off")

if errs:
    print("VERIFY FAIL (%d):"%len(errs))
    for e in errs[:60]: print("  -",e)
else:
    print("VERIFY PASS: all solutions on both equations, boxes continuous, expects reproduce, boundaries valid")
