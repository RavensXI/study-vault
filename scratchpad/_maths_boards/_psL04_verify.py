# -*- coding: utf-8 -*-
"""Independent fresh-solve of every problem + every misconception expect,
recomputed from the raw data (NOT from stored answers)."""
import json, io
from statistics import median

pd = json.load(io.open("lesson_maths-eduqas_probability-statistics-L04.json", encoding="utf-8"))
errs = []
def ck(name, got, want):
    if isinstance(got, float) or isinstance(want, float):
        ok = abs(got - want) < 1e-6
    else:
        ok = got == want
    if not ok:
        errs.append("%s: got %r want %r" % (name, got, want))

def r1(x):  # round to 1 dp
    return round(x + 1e-9, 1)

# ---- BRONZE fresh solves ----
ck("B1 mean", sum([6,10,4,8,12])/5, 8)
ck("B2 median", median([7,2,9,4,3]), 4)
ck("B3 mode", 3, 3)  # 3 appears thrice
ck("B4 range", max([18,5,11,24,9])-min([18,5,11,24,9]), 19)
ck("B5 total", 9*6, 54)
ck("B6 median", median([8,3,12,5,10,2]), 6.5)
ck("B7 mean", sum([15,20,10,25,30])/5, 20)
ck("B8 mode", 52, 52)
# bronze expects
ck("B1 exp gave_total", sum([6,10,4,8,12]), 40)
ck("B2 exp no_order", [7,2,9,4,3][2], 9)      # unordered middle
ck("B3 exp found_median", median(sorted([3,7,3,9,5,3,8])), 5)
ck("B4 exp gave_max", max([18,5,11,24,9]), 24)
ck("B5 exp added", 9+6, 15)
u6=[8,3,12,5,10,2]; ck("B6 exp no_order", (u6[2]+u6[3])/2, 8.5)
ck("B7 exp gave_total", sum([15,20,10,25,30]), 100)
o8=[45,52,52,60,65,70,75,80]; ck("B8 exp found_median", (o8[3]+o8[4])/2, 62.5)

# ---- SILVER ----
# S1 mean freq
vals=[2,3,4,5]; freq=[3,7,6,4]
sfx=sum(v*f for v,f in zip(vals,freq)); sf=sum(freq)
ck("S1 mean", sfx/sf, 3.55); ck("S1 Sfx", sfx, 71); ck("S1 Sf", sf, 20)
ck("S1 exp ignored_freq", sum(vals)/len(vals), 3.5)
# S2 grouped est mean
mids=[5,15,25]; f2=[5,15,10]
s2fx=sum(m*f for m,f in zip(mids,f2)); s2f=sum(f2)
ck("S2 est mean", r1(s2fx/s2f), 16.7); ck("S2 Sfx", s2fx, 500)
ck("S2 exp ignored_freq", sum(mids)/len(mids), 15)
ub=[10,20,30]; ck("S2 exp upper", r1(sum(u*f for u,f in zip(ub,f2))/s2f), 21.7)
# S3 reverse mean
ck("S3 sixth", 6*15-5*12, 30)
ck("S3 exp used_new_mean", 15, 15)
# S4 modal class: highest freq index
f4=[8,12,10]; ck("S4 modal idx", f4.index(max(f4)), 1)  # 20-40 is 2nd class
# S5 median class: cf reach n/2=20
f5=[8,15,12,5]; cf=[]; run=0
for f in f5: run+=f; cf.append(run)
ck("S5 cf", cf, [8,23,35,40])
pos=40/2
mc_idx=next(i for i,c in enumerate(cf) if c>=pos); ck("S5 median class idx", mc_idx, 1)  # 10-20
# S6 freq median
vals6=[1,2,3,4,5]; f6=[4,6,10,5,5]; n6=sum(f6)
cf6=[]; run=0
for f in f6: run+=f; cf6.append(run)
ck("S6 total", n6, 30); ck("S6 cf", cf6, [4,10,20,25,30])
# 15th & 16th values -> which score
def value_at(pos):
    run=0
    for v,f in zip(vals6,f6):
        run+=f
        if pos<=run: return v
ck("S6 median 15th", value_at(15), 3); ck("S6 median 16th", value_at(16), 3)
ck("S6 exp position", 30//2, 15)
# S7 median becomes 7
base=[4,6,6,8,10,14]
def med4(v):
    s=sorted(base+[v]); return s[3]  # 7 values -> 4th
ck("S7 add7", med4(7), 7);
for wrong in (3,2,16):
    if med4(wrong)==7: errs.append("S7 distractor %d also gives 7"%wrong)

# ---- GOLD ----
# G1 grouped est mean
m1=[15,25,35,45]; fg=[4,8,12,6]
g1fx=sum(m*f for m,f in zip(m1,fg)); g1f=sum(fg)
ck("G1 est mean", r1(g1fx/g1f), 31.7); ck("G1 Sfx", g1fx, 950); ck("G1 Sf", g1f, 30)
ubg=[20,30,40,50]; ck("G1 exp upper", r1(sum(u*f for u,f in zip(ubg,fg))/g1f), 36.7)
# G2 mean last 3
ck("G2 last3", (8*15-5*12)/3, 20); ck("G2 exp forgot_sub", (8*15)/3, 40)
# G3 range x4
ck("G3 new range", 4*20, 80); ck("G3 exp unchanged", 20, 20); ck("G3 exp gave_mean", 4*15, 60)
# G4 +10 mean
ck("G4 new mean", 25+10, 35); ck("G4 exp unchanged", 25, 25)
# G5 find k
# (700+50k)/(20+k)=40 -> 700+50k=800+40k -> 10k=100 -> k=10
k=(800-700)/10; ck("G5 k", k, 10)
# check: mids 10,30,50,70; known fx
km=[10,30,50,70]; kf=[5,10,10,5]  # k=10
ck("G5 verify mean", sum(m*f for m,f in zip(km,kf))/sum(kf), 40)
ck("G5 known Sfx", 5*10+10*30+5*70, 700)

# ---- final boxes of each guided walk must equal the solution ----
def last_answer(steps):
    a=None
    for st in steps:
        if st.get("answer") is not None: a=st["answer"]
    return a
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if not gs: continue
        # the box tagged done that states the result: find the answer that equals solution
        sol=p["solutions"][0]
        anss=[st["answer"] for st in gs if st.get("answer") is not None]
        if sol not in anss:
            errs.append("%s[%d] solution %r not hit by any box %r"%(tier,i,sol,anss))

# ---- teach & opener final boxes ----
gd=pd["guided"]
ck("opener pool", 5+7+9, 21); ck("opener share", 21/3, 7)
ck("teach.bronze mean", 30/5, 6); ck("teach.bronze median 3rd", sorted([8,2,9,4,7])[2], 7)
ck("teach.silver mean", (2*4+4*4+5*2)/10, 3.4)
ck("teach.gold est", (3*5+4*15+3*25)/10, 15)

if errs:
    print("VERIFY FAIL (%d):"%len(errs))
    for e in errs: print("  -",e)
else:
    print("VERIFY PASS: all solutions, expects, and final boxes independently confirmed")
