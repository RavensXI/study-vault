# -*- coding: utf-8 -*-
import json, io
d = json.load(io.open("lesson_maths-eduqas_algebra-L14.json", encoding="utf-8"))
pb = d["problem_bank"]
errs = []

def nth_from_seq(seq):
    d1 = [seq[i+1]-seq[i] for i in range(len(seq)-1)]
    d2 = [d1[i+1]-d1[i] for i in range(len(d1)-1)]
    a = d2[0]/2
    rem = [seq[i]-a*(i+1)**2 for i in range(len(seq))]
    b = rem[1]-rem[0]; c = rem[0]-b
    return a, b, c

checks = []
checks.append(("G0 nth", nth_from_seq([2,9,20,35,54]), (2,1,-1)))
checks.append(("G1 fg solve", (19-13)/3, 2))
x=1; x=(x**2+3)/5; x=(x**2+3)/5
checks.append(("G2 x2", round(x,3), 0.728))
checks.append(("G3 inv check f(4)->9->4", (3*9+1)/(9-2), 4))
checks.append(("G4 nth", nth_from_seq([5,12,23,38]), (2,1,2)))
a,b,c = nth_from_seq([5,12,23,38]); checks.append(("G4 10th", a*100+b*10+c, 212))
d1=[4-1,9-4,16-9,25-16]; checks.append(("B0 2nd diff", d1[1]-d1[0], 2))
checks.append(("B1 a", 6/2, 3))
checks.append(("B2 f4", 2*4+3, 11))
checks.append(("B3 f3", 3**2-1, 8))
checks.append(("B4 fneg1", 2*(-1)+3, 1))
checks.append(("B5 x3", 1+3+3, 7))
checks.append(("B6 squares", [i*i for i in range(1,5)], [1,4,9,16]))
checks.append(("B7 f3", 5*3, 15))
checks.append(("S0 nth", nth_from_seq([3,8,15,24,35]), (1,2,0)))
checks.append(("S1 fg2", 3*(2**2)+1, 13))
checks.append(("S2 gf2", (3*2+1)**2, 49))
checks.append(("S3 inv check f(3)->1->3", (1+5)/2, 3))
checks.append(("S4 nth", nth_from_seq([0,3,8,15,24]), (1,0,-1)))
x=1; x=(x+5)/2; x=(x+5)/2
checks.append(("S5 x2", x, 4))
checks.append(("S6 inv check f(5)->2->5", 3*2-1, 5))

for name, got, want in checks:
    ok = got == want or (isinstance(got,tuple) and tuple(round(g,6) for g in got)==tuple(want))
    if not ok:
        errs.append("%s got %r want %r" % (name, got, want))

# landing box == solution for every non-MC problem
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")=="multiple_choice": continue
        live=[s for s in (p.get("guided_steps") or []) if s.get("answer") is not None]
        last=live[-1]["answer"]; sol=p["solutions"][0]
        if abs(float(last)-float(sol))>1e-9:
            errs.append("%s[%d] last box %r != sol %r"%(tier,i,last,sol))

# MC expects valid distractor indices (1..n-1), never 0
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")!="multiple_choice": continue
        n=len(p["options"])
        for mm in p["misconceptions"]:
            e=mm["expect"]
            if not (isinstance(e,int) and 1<=e<=n-1):
                errs.append("%s[%d] bad MC expect %r"%(tier,i,e))

# single_value expect must not equal solution and must be plausibly the error's value (just non-equal check)
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")=="multiple_choice": continue
        for mm in p["misconceptions"]:
            e=mm["expect"]
            if e is not None and abs(float(e)-float(p["solutions"][0]))<1e-9:
                errs.append("%s[%d] expect equals sol"%(tier,i))

# duplicate solutions within tier
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")=="multiple_choice": continue
        k=tuple(p["solutions"])
        if k in seen: errs.append("%s dup sol %r (%d,%d)"%(tier,k,seen[k],i))
        seen[k]=i

# em dash scan
import re
def scan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note",): continue
            scan(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,path+"[%d]"%j)
    elif isinstance(o,str) and "—" in o:
        errs.append("EM DASH at "+path)
scan(d)

if errs:
    print("VERIFY FAIL:")
    for e in errs: print("  -",e)
else:
    print("VERIFY OK: fresh-solves, landing boxes, MC/SV expects, uniqueness, no em dash")
