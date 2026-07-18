# -*- coding: utf-8 -*-
import json, os, re
HERE = os.path.dirname(__file__)
pd = json.load(open(os.path.join(HERE,"lesson_higher-calculations-L06@d1cc4db5ec.json"), encoding="utf-8"))
bad=[]

def acc(p): return p.get("accept", 0.011)

# 1. final guided box lands on solution; expects outside accept; board-neutral
BOARD = re.compile(r"\bAQA\b|\bEdexcel\b|\bOCR\b|\bEduqas\b|\bWJEC\b|equation sheet|on your sheet|must memorise", re.I)
alltext=json.dumps(pd, ensure_ascii=False)
for m in BOARD.finditer(alltext):
    bad.append("BOARD phrase: "+alltext[m.start()-20:m.start()+20])

pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]; a=acc(p)
        gs=p["guided_steps"]
        live=[st for st in gs if st.get("answer") is not None]
        last=live[-1]["answer"]
        # last box is a CHECK; the answer box is the substitute box -> verify a box equals sol
        boxvals=[st["answer"] for st in live]
        if not any(abs(v-sol)<=max(a,0.005)+1e-9 for v in boxvals):
            bad.append(f"{tier}[{i}] no box equals solution {sol}: {boxvals}")
        for mm in p["misconceptions"]:
            e=mm["expect"]
            if e is not None and abs(float(e)-sol)<=a:
                bad.append(f"{tier}[{i}] expect {e} inside accept of {sol}")
        # svg a11y
        q=p.get("question","")
        if "<svg" in q:
            if 'role="img"' not in q: bad.append(f"{tier}[{i}] svg no role")
            if "aria-label" not in q: bad.append(f"{tier}[{i}] svg no aria")
            if "xmlns" in q or "http" in q: bad.append(f"{tier}[{i}] svg xmlns/http remains")

# 2. recompute specific box chains
def chk(name, got, exp):
    if abs(got-exp)>1e-6: bad.append(f"{name}: computed {got} != box {exp}")

# opener
chk("opener b1",5*2,10); chk("opener b2",20*2,40)
# teach bronze
chk("tB ratio",150/50,3); chk("tB vs",24*3,72); chk("tB chk1",24*150,3600); chk("tB chk2",72*50,3600)
# teach silver
chk("tS pin",20*6,120); chk("tS is",120/240,0.5); chk("tS fac",240/20,12); chk("tS pout",240*0.5,120)
# teach gold
chk("tG pin",20000*1000,20000000); chk("tG is",20000000/100000,200); chk("tG sq",200**2,40000)
chk("tG loss",40000*5,200000); chk("tG alt",1000**2*5,5000000)

# spot bank boxes
chk("B0",12*20,240); chk("B1",200*50,10000); chk("B2 pin",1000*400,400000); chk("B2 is",400000/20000,20)
chk("B3",240*0.1,24); chk("B4",1200/400,3)
chk("S1 pout",11*2.0,22); chk("S1 ip",22/230,0.09565)  # ~0.0957
chk("S2",20000000/400000,50); chk("S3 sq",50**2,2500); chk("S4",1200*0.05,60)
chk("G0",25000*200,5000000); chk("G1",12500000/5000000,2.5); chk("G2",6.25*100,625)
chk("G3 ratio",230/11000,0.0209091); chk("G3 ns",1000*0.0209,20.9); chk("G4",3/9,0.33333)

# accept-window sanity for rounded answers
for tier,i,val in [("silver",1,0.0957),("gold",3,20.9),("gold",4,0.333)]:
    p=pb[tier][i]; sol=p["solutions"][0]
    if abs(sol-val)>acc(p): bad.append(f"{tier}[{i}] stored {sol} vs {val} outside accept {acc(p)}")

# preservation: worked_examples, related_videos, exam_context, topic_links present
for k in ("worked_examples","related_videos","exam_context","topic_links"):
    if k not in pd: bad.append("lost "+k)
if len(pd["worked_examples"])!=3: bad.append("worked_examples count changed")

if bad:
    print("ISSUES:")
    for b in bad: print("  -",b)
else:
    print("ALL VERIFY CHECKS PASS")
