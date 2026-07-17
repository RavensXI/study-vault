# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_maths-ocr_graphs-L04.json", encoding="utf-8"))
pre = json.load(io.open("_gL04_pre.json", encoding="utf-8"))
issues = []

# expected fresh solutions per tier (independently recomputed)
expect_sol = {
 "bronze": [[60],[1],[40],[30],[20],[24],[4],[90]],
 "silver": [[5],[140],[8],[60],[230],[120],[25]],
 "gold":   [[105],[5],[30],[20],[40]],
}
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    probs = pb[tier]
    if [p["solutions"] for p in probs] != expect_sol[tier]:
        issues.append("%s solutions mismatch: %s" % (tier, [p["solutions"] for p in probs]))
    # duplicate check
    seen=set()
    for i,p in enumerate(probs):
        k=tuple(p["solutions"])
        if k in seen and p.get("input_type")!="multiple_choice":
            issues.append("%s[%d] dup %s" % (tier,i,k))
        seen.add(k)
    # guided_steps: final box lands on solution; boundary
    for i,p in enumerate(probs):
        gs=p.get("guided_steps")
        if not gs:
            if p.get("input_type")!="multiple_choice": issues.append("%s[%d] no gs"%(tier,i))
            continue
        boxes=[st for st in gs if st.get("answer") is not None]
        if len(boxes)<3: issues.append("%s[%d] <3 boxes"%(tier,i))
        # phase boundary
        sub=[j for j,st in enumerate(gs) if st.get("phase")=="substitute"]
        if not sub: issues.append("%s[%d] no phase"%(tier,i))
        else:
            live=sum(1 for st in gs[sub[0]:] if st.get("answer") is not None)
            if live<2: issues.append("%s[%d] <2 live after phase"%(tier,i))
            if sub[0]<1: issues.append("%s[%d] phase at 0"%(tier,i))
        # every box answer numeric
        for st in boxes:
            if not isinstance(st["answer"],(int,float)): issues.append("%s[%d] nonnum"%(tier,i))
        # expects != solution
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None:
                ev=e if isinstance(e,list) else [e]
                sv=[float(x) for x in p["solutions"]]
                if len(ev)==len(sv) and all(abs(float(a)-b)<0.011 for a,b in zip(ev,sv)):
                    issues.append("%s[%d] expect==sol"%(tier,i))

# --- verify specific arithmetic of key boxes (continuity) ---
def boxvals(tier,i):
    return [st["answer"] for st in pb[tier][i]["guided_steps"] if st.get("answer") is not None]

checks = {
 ("bronze",0):[30,60,60], ("bronze",1):[2,3,1,60], ("bronze",2):[120,40,120],
 ("bronze",3):[15,30,15], ("bronze",4):[50,20,50], ("bronze",5):[1.6,24,15],
 ("bronze",6):[800,4,800], ("bronze",7):[60,90,60],
 ("silver",0):[25,5,25], ("silver",1):[40,80,20,140,10], ("silver",2):[24,8,24],
 ("silver",3):[90,60,90], ("silver",4):[1.15,230,200], ("silver",5):[15,120,15],
 ("silver",6):[0.625,25,40],
 ("gold",0):[20,60,25,105,15], ("gold",1):[30,5,30], ("gold",2):[60,2,30,60],
 ("gold",3):[4,20,80], ("gold",4):[40,40,40],
}
for (tier,i),exp in checks.items():
    got=boxvals(tier,i)
    if got!=exp: issues.append("box vals %s[%d] got %s exp %s"%(tier,i,got,exp))

# --- expect reproduction (commit the error) ---
exp_checks = [
 ("bronze",0,90),("bronze",1,3),("bronze",2,round(3/120,4)),("bronze",3,15/2),
 ("bronze",4,2.5/50),("bronze",5,15/8*5),("bronze",6,200/800),("bronze",7,60/1.5),
 ("silver",0,5/25),("silver",1,10*20),("silver",2,3/24),("silver",3,90),
 ("silver",4,200),("silver",5,0.5*8*15),("silver",6,40/5*8),
 ("gold",0,40+60+50),("gold",1,30*6),("gold",2,60/5),("gold",3,80/8),("gold",4,10/4),
]
for tier,i,val in exp_checks:
    e=pb[tier][i]["misconceptions"][0]["expect"]
    if abs(float(e)-float(val))>0.001:
        issues.append("expect %s[%d] stored %s recomputed %s"%(tier,i,e,val))

# --- chart / svg label sanity ---
# B0/B1 chart data
c=pb["bronze"][0]["chart"]
if c["data"]["datasets"][0]["data"]!=[0,30,60,60,90]: issues.append("B0 chart data changed")
# G0 chart points -> area 105
g0=pb["gold"][0]["chart"]["data"]["datasets"][0]["data"]
pts=[(d["x"],d["y"]) for d in g0]
if pts!=[(0,0),(4,10),(10,10),(15,0)]: issues.append("G0 chart pts %s"%pts)
area=0.5*4*10+6*10+0.5*5*10
if area!=105: issues.append("G0 area %s"%area)
# G2 chart pts -> final section speed 30
g2=[(d["x"],d["y"]) for d in pb["gold"][2]["chart"]["data"]["datasets"][0]["data"]]
if g2!=[(0,0),(2,40),(3,40),(5,100)]: issues.append("G2 chart pts %s"%g2)
if (100-40)/(5-3)!=30: issues.append("G2 speed")
# G3 svg mentions 8 s and 80 m and v; area check
d3=pb["gold"][3]["display"]
for tok in ["8 s","area = 80 m",">v<","8 seconds","80 m"]:
    if tok not in d3: issues.append("G3 svg missing %r"%tok)
if 0.5*8*20!=80: issues.append("G3 area")

# --- preservation vs pre-dump ---
if pd["related_videos"]!=pre.get("related_videos"): issues.append("related_videos changed")
if pd["topic_links"]!=pre.get("topic_links"): issues.append("topic_links changed")
# worked_examples: only labels' em dash replaced; questions/content preserved
prewe=pre.get("worked_examples")
nowwe=pd["worked_examples"]
if len(prewe)!=len(nowwe): issues.append("we count changed")
for a,b in zip(prewe,nowwe):
    if a["question"]!=b["question"]: issues.append("we question changed")
    for sa,sb in zip(a["steps"],b["steps"]):
        if sa["content"]!=sb["content"]: issues.append("we content changed")
        if sa["label"].replace(" — ",": ").replace("—",":")!=sb["label"]:
            issues.append("we label changed beyond em dash: %r -> %r"%(sa["label"],sb["label"]))

print("ISSUES:" if issues else "ALL CLEAR")
for x in issues: print("  -",x)
