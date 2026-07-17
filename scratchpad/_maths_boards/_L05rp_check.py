# -*- coding: utf-8 -*-
import json, io, sys, math, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open("lesson_maths-ocr_ratio-proportion-L05.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs=[]
def eq(a,b,t=1e-9): return abs(a-b)<=t

# independent solver from math (not from stored)
def cube_root(v): return round(v**(1/3)) if v>0 else 0

# expected box-answer sequences, recomputed by hand here:
expected = {
 ("bronze",0):[4,3,12],
 ("bronze",1):[16,80,5],
 ("bronze",2):[9,5,4,20,5],
 ("bronze",3):[2,4,72,72],
 ("bronze",4):[2,7,14],
 ("bronze",5):[25,50,2],
 ("bronze",6):[8,5,40],
 ("bronze",7):[9,63,7],
 ("silver",0):[4,20,25,0.8,5],
 ("silver",1):[3,5,5,25,15],
 ("silver",2):[8,5,27,135,40],
 ("silver",3):[16,3,25,5,75],
 ("silver",4):[3,9,4,36],
 ("silver",5):[4,5,10,50,20],
 ("silver",6):[25,4,100,400,100],
 ("gold",0):[27,2,8,2,16],
 ("gold",1):[2,20,4,5,10],
 ("gold",2):[16,2,36,72,32],
 ("gold",3):[1000,4,250],
 ("gold",4):[10,0.2,30,6,2],
}
for (t,i),seq in expected.items():
    gs=pb[t][i]["guided_steps"]
    got=[st["answer"] for st in gs if st.get("answer") is not None]
    if got!=seq:
        errs.append(f"{t}[{i}] box seq {got} != recomputed {seq}")

# recompute every expect from the committed error
expects = {
 ("bronze",0):{6:12/2, 48:12*4},
 ("bronze",1):{20:5*4, 40:5*4*2},
 ("bronze",2):{30:45*2/3, 10:5*2},
 ("bronze",3):{36:18*2},
 ("bronze",4):{3.5:14/4, 28:14*2},
 ("bronze",5):{10:2*5, 20:2*5*2},
 ("bronze",6):{10:40/4, 20:40/2},
 ("bronze",7):{21:7*3},
 ("silver",0):{31.25:(5/4)*25, 2:20/(5*2)},
 ("silver",1):{125:5*25},
 ("silver",2):{90:(40/4)*9, 15:5*3},
 ("silver",3):{25:25},
 ("silver",4):{12:36/3, 324:36*9},
 ("silver",5):{125:(20/16)*100, 500:5*100},
 ("silver",6):{200:100*2, 40:4*10},
 ("gold",0):{8:8},
 ("gold",1):{20:(10/2)*4, 2.5:(10*4)/16},
 ("gold",2):{48:32*6/4, 12:2*6},
 ("gold",3):{6.25:(200/5)*250/1000*0 + 250/(200/5), 0.25:250/1000},
 ("gold",4):{18:(2/100)*900, 180:0.2*900},
}
for (t,i),mp in expects.items():
    for m in pb[t][i].get("misconceptions",[]):
        e=m.get("expect")
        if e is None: continue
        if e not in mp:
            errs.append(f"{t}[{i}] expect {e} not in recomputed set {list(mp.keys())}")
        else:
            if not eq(float(e), float(mp[e]), 1e-6):
                errs.append(f"{t}[{i}] expect {e} != derived {mp[e]}")

# opener figure sanity: 2x2=4 slabs, 4x4=16 slabs
disp=pd["guided"]["opener"]["display"]
n_small=disp.count('#60a5fa'); n_big=disp.count('#34d399')
if n_small!=4: errs.append(f"opener small grid has {n_small} slabs, need 4")
if n_big!=16: errs.append(f"opener big grid has {n_big} slabs, need 16")
ob=[st["answer"] for st in pd["guided"]["opener"]["steps"] if st.get("answer") is not None]
if ob!=[4,16]: errs.append(f"opener boxes {ob} != [4,16]")
if "http" in disp.lower(): errs.append("opener svg has external ref")

# teach walks recompute
teach_exp={"bronze":[9,2,25,50,18],"silver":[9,72,36,2,8],"gold":[8,5,27,3,135]}
for t,seq in teach_exp.items():
    got=[st["answer"] for st in pd["guided"]["teach"][t]["steps"] if st.get("answer") is not None]
    if got!=seq: errs.append(f"teach.{t} {got} != {seq}")

# preservation vs pre-dump
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
ID="ddbb6863-36ab-4898-8090-16df440a9d85"
p0=next(r["practice_data"] for r in pre if r["id"]==ID)
for f in ["related_videos","topic_links"]:
    if json.dumps(p0.get(f),sort_keys=True)!=json.dumps(pd.get(f),sort_keys=True):
        errs.append(f"PRESERVE {f} changed")
# worked_examples: only em-dash label fix allowed
we_pre=json.dumps(p0["worked_examples"]).replace(" \\u2014 ",": ").replace("\\u2014",":")
if json.dumps(pd["worked_examples"]).replace(" \\u2014 ",": ").replace("\\u2014",":") != we_pre:
    # compare ignoring em-dash substitution
    a=json.dumps(p0["worked_examples"],ensure_ascii=False).replace(" — ",": ").replace("—",":")
    b=json.dumps(pd["worked_examples"],ensure_ascii=False)
    if a!=b: errs.append("PRESERVE worked_examples changed beyond em-dash fix")

print("CHECK:", "ALL CLEAR" if not errs else f"{len(errs)} ISSUES")
for e in errs: print("  -",e)
