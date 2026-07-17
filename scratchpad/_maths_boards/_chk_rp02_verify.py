# -*- coding: utf-8 -*-
import json, re

base = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards"
live = json.load(open(base + r"\_chk_rp02_live.json", encoding="utf-8"))
pb = live["problem_bank"]

def r2(x): return round(x + 1e-9, 2)
def approx(a,b,tol=0.005): return abs(a-b)<=tol

# ---- fresh-solve solutions ----
errs=[]
def solve_gold(i):
    return {0:340/0.85, 1:4, 2:round(12000*0.92**5), 3:495/(1.1*0.9), 4:r2(6000*1.035**4)-6000}[i]
def solve_bronze(i):
    return {0:0.25*80,1:0.1*350,2:60*1.2,3:200*0.85,4:1.3,5:0.95,6:40*0.9,7:0.5*84}[i]
def solve_silver(i):
    return {0:100*3,1:200000*1.1**2,2:96/1.2,3:round((15000-9600)/15000*100),
            4:round(5000*1.02**3),5:84/1.2,6:800*0.75**2}[i]
for tier,solver in [("gold",solve_gold),("bronze",solve_bronze),("silver",solve_silver)]:
    for i,p in enumerate(pb[tier]):
        got=solver(i); stored=p["solutions"][0]
        if abs(got-stored)>0.005:
            errs.append(f"{tier}[{i}] SOLUTION fresh={got} stored={stored} :: {p['display']}")
        # non-calc clean check
        if p.get("calculator")==False and abs(stored-round(stored,2))>1e-9:
            errs.append(f"{tier}[{i}] non-calc messy answer {stored}")
print("=== SOLUTION MISMATCHES ==="); [print(" ",e) for e in errs] or (not errs and print("  none"))

# ---- box recompute ----
boxchecks=[]
def bc(label,expr,stored):
    if not approx(expr,stored,0.005): boxchecks.append(f"{label}: computed={expr} stored={stored}")
g=pb["gold"]; b=pb["bronze"]; s=pb["silver"]
bc("gold[0].m",0.85,g[0]["guided_steps"][1]["answer"])
bc("gold[0].rev",340/0.85,g[0]["guided_steps"][2]["answer"])
bc("gold[0].chk",400*0.85,g[0]["guided_steps"][3]["answer"])
bc("gold[1].m",1.04,g[1]["guided_steps"][1]["answer"])
bc("gold[1].y1",8000*1.04,g[1]["guided_steps"][2]["answer"])
bc("gold[1].y2",8320*1.04,g[1]["guided_steps"][3]["answer"])
bc("gold[1].y3",r2(8652.8*1.04),g[1]["guided_steps"][4]["answer"])
bc("gold[1].y4",r2(8998.91*1.04),g[1]["guided_steps"][5]["answer"])
bc("gold[1].fin",4,g[1]["guided_steps"][6]["answer"])
bc("gold[2].m",0.92,g[2]["guided_steps"][1]["answer"])
bc("gold[2].a5",r2(12000*0.92**5),g[2]["guided_steps"][2]["answer"])
bc("gold[2].rnd",round(12000*0.92**5),g[2]["guided_steps"][3]["answer"])
bc("gold[2].revchk",r2(7908.98/0.92),g[2]["guided_steps"][4]["answer"])
bc("gold[3].r",1.1,g[3]["guided_steps"][1]["answer"])
bc("gold[3].f",0.9,g[3]["guided_steps"][2]["answer"])
bc("gold[3].c",0.99,g[3]["guided_steps"][3]["answer"])
bc("gold[3].rev",495/0.99,g[3]["guided_steps"][4]["answer"])
bc("gold[3].chk",500*0.99,g[3]["guided_steps"][5]["answer"])
bc("gold[4].m",1.035,g[4]["guided_steps"][1]["answer"])
bc("gold[4].tot",r2(6000*1.035**4),g[4]["guided_steps"][2]["answer"])
bc("gold[4].int",r2(6000*1.035**4)-6000,g[4]["guided_steps"][3]["answer"])
bc("gold[4].chk",6000+885.14,g[4]["guided_steps"][4]["answer"])
bc("b0.d",0.25,b[0]["guided_steps"][1]["answer"]); bc("b0.m",20,b[0]["guided_steps"][2]["answer"]); bc("b0.c",80,b[0]["guided_steps"][3]["answer"])
bc("b1.d",0.1,b[1]["guided_steps"][1]["answer"]); bc("b1.m",35,b[1]["guided_steps"][2]["answer"]); bc("b1.c",350,b[1]["guided_steps"][3]["answer"])
bc("b2.p",12,b[2]["guided_steps"][1]["answer"]); bc("b2.a",72,b[2]["guided_steps"][2]["answer"]); bc("b2.f",72,b[2]["guided_steps"][3]["answer"])
bc("b3.p",30,b[3]["guided_steps"][1]["answer"]); bc("b3.s",170,b[3]["guided_steps"][2]["answer"]); bc("b3.f",170,b[3]["guided_steps"][3]["answer"])
bc("b4.d",0.3,b[4]["guided_steps"][1]["answer"]); bc("b4.a",1.3,b[4]["guided_steps"][2]["answer"]); bc("b4.c",13,b[4]["guided_steps"][3]["answer"])
bc("b5.d",0.05,b[5]["guided_steps"][1]["answer"]); bc("b5.s",0.95,b[5]["guided_steps"][2]["answer"]); bc("b5.c",190,b[5]["guided_steps"][3]["answer"])
bc("b6.p",4,b[6]["guided_steps"][1]["answer"]); bc("b6.s",36,b[6]["guided_steps"][2]["answer"]); bc("b6.f",36,b[6]["guided_steps"][3]["answer"])
bc("b7.d",0.5,b[7]["guided_steps"][1]["answer"]); bc("b7.h",42,b[7]["guided_steps"][2]["answer"]); bc("b7.c",84,b[7]["guided_steps"][3]["answer"])
bc("s0.y",100,s[0]["guided_steps"][1]["answer"]); bc("s0.3",300,s[0]["guided_steps"][2]["answer"]); bc("s0.t",2300,s[0]["guided_steps"][3]["answer"])
bc("s1.m",1.1,s[1]["guided_steps"][1]["answer"]); bc("s1.y1",220000,s[1]["guided_steps"][2]["answer"]); bc("s1.y2",242000,s[1]["guided_steps"][3]["answer"]); bc("s1.p",242000,s[1]["guided_steps"][4]["answer"])
bc("s2.m",1.2,s[2]["guided_steps"][1]["answer"]); bc("s2.r",80,s[2]["guided_steps"][2]["answer"]); bc("s2.c",96,s[2]["guided_steps"][3]["answer"])
bc("s3.l",5400,s[3]["guided_steps"][1]["answer"]); bc("s3.p",36,s[3]["guided_steps"][2]["answer"]); bc("s3.c",5400,s[3]["guided_steps"][3]["answer"])
bc("s4.m",1.02,s[4]["guided_steps"][1]["answer"]); bc("s4.y1",5100,s[4]["guided_steps"][2]["answer"]); bc("s4.y2",5202,s[4]["guided_steps"][3]["answer"]); bc("s4.y3",r2(5202*1.02),s[4]["guided_steps"][4]["answer"]); bc("s4.rnd",5306,s[4]["guided_steps"][5]["answer"]); bc("s4.p",r2(5000*1.02**3),s[4]["guided_steps"][6]["answer"])
bc("s5.m",1.2,s[5]["guided_steps"][1]["answer"]); bc("s5.r",70,s[5]["guided_steps"][2]["answer"]); bc("s5.c",84,s[5]["guided_steps"][3]["answer"])
bc("s6.m",0.75,s[6]["guided_steps"][1]["answer"]); bc("s6.y1",600,s[6]["guided_steps"][2]["answer"]); bc("s6.y2",450,s[6]["guided_steps"][3]["answer"]); bc("s6.p",450,s[6]["guided_steps"][4]["answer"])
t=live["guided"]["teach"]
bc("t.g.m",1.04,t["gold"]["steps"][1]["answer"]); bc("t.g.tot",r2(2500*1.04**3),t["gold"]["steps"][2]["answer"]); bc("t.g.int",r2(2500*1.04**3)-2500,t["gold"]["steps"][3]["answer"]); bc("t.g.chk",2812.16,t["gold"]["steps"][4]["answer"])
bc("t.b.d",0.4,t["bronze"]["steps"][1]["answer"]); bc("t.b.a",1.4,t["bronze"]["steps"][2]["answer"]); bc("t.b.m",70,t["bronze"]["steps"][3]["answer"]); bc("t.b.l",20,t["bronze"]["steps"][4]["answer"]); bc("t.b.s",70,t["bronze"]["steps"][5]["answer"])
bc("t.s.m",0.8,t["silver"]["steps"][1]["answer"]); bc("t.s.y1",960,t["silver"]["steps"][2]["answer"]); bc("t.s.y2",768,t["silver"]["steps"][3]["answer"]); bc("t.s.p",768,t["silver"]["steps"][4]["answer"])
o=live["guided"]["opener"]["steps"]
bc("op.1",4,o[0]["answer"]); bc("op.2",16,o[1]["answer"])
print("\n=== BOX RECOMPUTE MISMATCHES ==="); [print(" ",e) for e in boxchecks] or (not boxchecks and print("  none"))

# ---- misconception expects ----
mis=[]
def me(label,commit,stored):
    if not approx(commit,stored,0.02): mis.append(f"{label}: committed={commit} expect={stored}")
me("g0 added_back",340+0.15*340,g[0]["misconceptions"][0]["expect"])
me("g1 stopped_at_3",3,g[1]["misconceptions"][0]["expect"])
me("g2 subtracted_40pc",12000*0.6,g[2]["misconceptions"][0]["expect"])
me("g3 net_zero",495,g[3]["misconceptions"][0]["expect"])
me("g4 gave_total",r2(6000*1.035**4),g[4]["misconceptions"][0]["expect"])
me("g4 simple",6000*0.035*4,g[4]["misconceptions"][1]["expect"])
me("b0 dec_place",0.025*80,b[0]["misconceptions"][0]["expect"])
me("b1 div_100",350/100,b[1]["misconceptions"][0]["expect"])
me("b2 inc_only",0.2*60,b[2]["misconceptions"][0]["expect"])
me("b3 dec_only",0.15*200,b[3]["misconceptions"][0]["expect"])
me("b4 forgot_one",0.3,b[4]["misconceptions"][0]["expect"])
me("b5 five_half",0.5,b[5]["misconceptions"][0]["expect"])
me("b6 disc_only",0.1*40,b[6]["misconceptions"][0]["expect"])
me("s0 gave_total",2300,s[0]["misconceptions"][0]["expect"])
me("s0 one_year",100,s[0]["misconceptions"][1]["expect"])
me("s1 added_20",200000*1.2,s[1]["misconceptions"][0]["expect"])
me("s1 one_year",220000,s[1]["misconceptions"][1]["expect"])
me("s2 sub_new",96-0.2*96,s[2]["misconceptions"][0]["expect"])
me("s3 base_new",5400/9600*100,s[3]["misconceptions"][0]["expect"])
me("s3 remaining",9600/15000*100,s[3]["misconceptions"][1]["expect"])
me("s4 added_6",5000*1.06,s[4]["misconceptions"][0]["expect"])
me("s5 sub_new",84-0.2*84,s[5]["misconceptions"][0]["expect"])
me("s6 halved",800*0.5,s[6]["misconceptions"][0]["expect"])
me("s6 one_year",600,s[6]["misconceptions"][1]["expect"])
print("\n=== MISCONCEPTION EXPECT MISMATCHES ==="); [print(" ",e) for e in mis] or (not mis and print("  none"))

# ---- boundary ----
bnd=[]
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps",[])
        pidx=[j for j,x in enumerate(gs) if x.get("phase")=="substitute"]
        if not pidx: bnd.append(f"{tier}[{i}] NO phase"); continue
        pj=pidx[0]
        before=sum(1 for x in gs[:pj] if "answer" in x)
        after=sum(1 for x in gs[pj:] if "answer" in x)
        if before<1: bnd.append(f"{tier}[{i}] before={before}")
        if after<2: bnd.append(f"{tier}[{i}] at/after={after}")
print("\n=== BOUNDARY ==="); [print(" ",e) for e in bnd] or (not bnd and print("  none"))

# ---- non-numeric boxes ----
nn=[]
def sb(steps,path):
    for j,x in enumerate(steps):
        if isinstance(x,dict) and "answer" in x and not isinstance(x["answer"],(int,float)):
            nn.append(f"{path}[{j}]={x['answer']!r}")
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(pb[tier]): sb(p.get("guided_steps",[]),f"{tier}[{i}]")
    sb(t[tier]["steps"],f"teach.{tier}")
sb(o,"opener")
print("\n=== NON-NUMERIC BOXES ==="); [print(" ",e) for e in nn] or (not nn and print("  none"))

# ---- em dash ----
em=[]
def walk(obj,path):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k=="note": continue
            walk(v,f"{path}.{k}")
    elif isinstance(obj,list):
        for i2,v in enumerate(obj): walk(v,f"{path}[{i2}]")
    elif isinstance(obj,str):
        if "—" in obj or "–" in obj: em.append(path+" :: "+obj[:70])
walk(live,"")
print("\n=== EM/EN DASHES ==="); [print(" ",e) for e in em] or (not em and print("  none"))

# ---- dup solutions ----
print("\n=== DUP SOLUTIONS ===")
for tier in ["gold","bronze","silver"]:
    sols=[tuple(p["solutions"]) for p in pb[tier]]
    print(f"  {tier}: dupes={[x for x in set(sols) if sols.count(x)>1]}")

# ---- tier guide words ----
print("\n=== TIER GUIDE WORDS (<=115) ===")
for tier in ["bronze","silver","gold"]:
    tg=live["tier_guides"][tier]
    wc=sum(len(re.sub(r'<[^>]+>','',x).split()) for x in tg["steps"])
    print(f"  {tier}: {wc} title={tg['title']!r}")
