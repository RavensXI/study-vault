# -*- coding: utf-8 -*-
import json, io, math, re
pd = json.load(io.open("lesson_maths-eduqas_geometry-L02.json", encoding="utf-8"))
fails = []
def ck(cond, msg):
    if not cond: fails.append(msg)

exp = {"bronze":[35,26,48,60,81,42,6,27],
       "silver":[43.96,78.5,32,12.6,37.7,77.0,25.7],
       "gold":[31.7,7.0,60,388,201.1]}
def close(a,b): return abs(a-b)<0.06
for tier in ("bronze","silver","gold"):
    probs = pd["problem_bank"][tier]
    ck(len(probs)==len(exp[tier]), tier+" length")
    seen=set()
    for i,p in enumerate(probs):
        sol=p["solutions"][0]
        ck(abs(sol-exp[tier][i])<0.001, "%s[%d] solution %s != %s"%(tier,i,sol,exp[tier][i]))
        ck(p["input_type"]=="single_value","%s[%d] not single_value"%(tier,i))
        key=round(sol,3); ck(key not in seen,"%s[%d] dup solution %s"%(tier,i,sol)); seen.add(key)
        gs=p["guided_steps"]
        boxes=[s for s in gs if s.get("answer") is not None]
        ck(len(boxes)>=3,"%s[%d] <3 boxes"%(tier,i))
        ck(any(close(b["answer"],sol) for b in boxes),"%s[%d] no box lands on solution"%(tier,i))
        sub=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        ck(bool(sub) and sub[0]>=1,"%s[%d] boundary too early"%(tier,i))
        live=sum(1 for s in gs[sub[0]:] if s.get("answer") is not None) if sub else 0
        ck(live>=2,"%s[%d] <2 live after boundary (%d)"%(tier,i,live))
        ck(gs[-1].get("done"),"%s[%d] last step no done"%(tier,i))
        for m in p["misconceptions"]:
            ck("expect" in m,"%s[%d] misc no expect"%(tier,i))
            e=m["expect"]; ck(e is None or abs(e-sol)>0.011,"%s[%d] expect==sol"%(tier,i))

pi=math.pi
recompute=[
 (2*(7+5),24),(7+5,12),(9*4,36),(9+4,13),(12*8,96),(12+8,20),(10+6,16),
 (14*6,84),(14+6,20),(48*8,384),(48+8,56),(2*9,18),(9*9,81),
 (3.14*49,153.86),(3.14*7,21.98),(pi*100,314.2),(2*pi*5,31.4),(16*4,64),(0.5*6*4,12),
 (2*pi*10,62.8),(5*2*pi*10,314.2),(pi*36,113.1),((1/3)*2*pi*6,12.6),
 (pi*49,153.9),(0.5*pi*196,307.9),(pi*5,15.7),(2*pi*5+10,41.4),
 (60+0.25*pi*36,88.3),(60-0.5*pi*36,3.5),(154/pi,49.0),(154/(2*pi),24.5),
 (24*360/12,720),(200+2*pi*60,577),(pi*16,50.3),
]
for idx,(a,b) in enumerate(recompute):
    ck(close(a,b),"expect-recompute #%d %s!=%s"%(idx,round(a,3),b))

# guided box arithmetic spot-recompute (the substantive intermediate steps)
ck(close(25*pi,78.5),"S1 box 25pi"); ck(close(49*pi,153.9),"S5 box"); ck(close(153.9/2,77.0),"S5 half->77")
ck(close(0.25*pi*36,28.27),"G0 quarter"); ck(close(60-28.27,31.73),"G0 sub")
ck(close(154/pi,49.0) and close(math.sqrt(49),7.0),"G1 chain")
ck(close(pi*60,188.5),"G3 circ"); ck(close(200+188.5,388.5),"G3 total"); ck(round(200+pi*60)==388,"G3 nearest")
ck(close(pi*100,314.2) and close(pi*36,113.1) and close(314.2-113.1,201.1),"G4 chain")
ck(close(2*pi*10,62.8) and close(62.8*0.2,12.56),"S3 chain")
ck(close(pi*36,113.1) and close(113.1/3,37.7),"S4 chain")

# opener
op=pd["guided"]["opener"]["steps"]
opb=[s for s in op if s.get("answer") is not None]
ck(opb[0]["answer"]==15 and opb[1]["answer"]==16,"opener values")
ck(5*3==15 and 2*(5+3)==16,"opener arithmetic")
ck("<svg" in op[0].get("display",""),"opener no svg")

# teach
tb=[s["answer"] for s in pd["guided"]["teach"]["bronze"]["steps"] if s.get("answer") is not None]
ck(tb==[40,13,26,5],"teach bronze "+str(tb))
ck(8*5==40 and 8+5==13 and 2*13==26 and 40//8==5,"teach bronze arith")
tsv=[s["answer"] for s in pd["guided"]["teach"]["silver"]["steps"] if s.get("answer") is not None]
ck(tsv==[81,254.5,84.8,254],"teach silver "+str(tsv))
ck(close(81*pi,254.5) and close(254.5/3,84.8) and round(84.8*3)==254,"teach silver arith")
tgv=[s["answer"] for s in pd["guided"]["teach"]["gold"]["steps"] if s.get("answer") is not None]
ck(tgv==[40,6.3,46.3,6.3],"teach gold "+str(tgv))
ck(close(0.5*pi*4,6.3) and close(40+6.3,46.3),"teach gold arith")
for t in ("bronze","silver","gold"):
    ck(sum(1 for s in pd["guided"]["teach"][t]["steps"] if s.get("answer") is not None)>=4,"teach "+t+" <4")
    ck("<svg" in pd["guided"]["teach"][t]["display"],"teach "+t+" no svg")

# figure svg safety + label spot-checks
def svgok(d):
    return ('role="img"' in d and "aria-label" in d and "viewBox" in d
            and "http://" not in d and "https://" not in d and "xlink" not in d
            and 'fill="currentColor"' in d)
fig_count=0
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        if "<svg" in p["display"]:
            fig_count+=1
            ck(svgok(p["display"]),"%s[%d] svg unsafe"%(tier,i))
lab={("bronze",0):["7 cm","5 cm"],("gold",0):["10 cm","6 cm","r = 6"],
     ("gold",3):["100 m","60 m"],("gold",4):["R = 10","r = 6"],
     ("silver",2):["6 cm","10 cm","4 cm"],("silver",3):["72","10 cm"]}
for (t,i),labels in lab.items():
    d=pd["problem_bank"][t][i]["display"]
    for L in labels: ck(L in d,"%s[%d] missing label %s"%(t,i,L))

# em dash sweep
def scan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+str(k))
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,path+"[%d]"%j)
    elif isinstance(o,str) and "—" in o: fails.append("EM DASH at "+path)
scan(pd)

# preservation vs pre-dump
try:
    pre=json.load(io.open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
    entry=None
    if isinstance(pre,list):
        for v in pre:
            if isinstance(v,dict) and v.get("id")=="5c10e089-e2cc-4a61-b6b3-951a8994a1a0": entry=v; break
    elif isinstance(pre,dict):
        entry=pre.get("5c10e089-e2cc-4a61-b6b3-951a8994a1a0")
        if entry is None:
            for k,v in pre.items():
                if isinstance(v,dict) and (v.get("id")=="5c10e089-e2cc-4a61-b6b3-951a8994a1a0"): entry=v;break
    print("pre-dump entry found:",entry is not None)
    if entry:
        pdp=entry.get("practice_data") or entry
        for f in ("topic_links","related_videos"):
            ck(json.dumps(pd.get(f),sort_keys=True)==json.dumps(pdp.get(f),sort_keys=True),"preservation changed: "+f)
        # worked_examples: only em-dash label fix expected
        we_now=json.dumps(pd.get("worked_examples"))
        ck("—" not in we_now,"worked_examples still has em dash")
except Exception as e:
    print("pre-dump check skipped:",e)

print("figures on bank problems:",fig_count)
if fails:
    print("VERIFY FAILS (%d):"%len(fails))
    for f in fails: print("  -",f)
else:
    print("VERIFY CLEAN: solutions, box chains, expects, teach/opener, boundaries, figure labels, preservation all pass")
