# -*- coding: utf-8 -*-
import json, io, re
from fractions import Fraction
pd = json.load(io.open("lesson_maths-eduqas_probability-statistics-L01.json", encoding="utf-8"))
pb = pd["problem_bank"]
bad = []

def last_two_boxes(gs):
    boxes = [st for st in gs if st.get("answer") is not None]
    return boxes

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sols = p["solutions"]
        gs = p["guided_steps"]
        boxes = [st for st in gs if st.get("answer") is not None]
        # landing: for fraction, last two boxes should equal [num,den]; for single_value last meaningful == sol
        if p["input_type"]=="fraction":
            lastnum = boxes[-2]["answer"]; lastden = boxes[-1]["answer"]
            if [lastnum,lastden] != sols:
                # allow the case where a trailing check box exists; search for a box pair equal to sols
                found = any([boxes[j]["answer"],boxes[j+1]["answer"]]==sols for j in range(len(boxes)-1))
                if not found:
                    bad.append("%s[%d] landing %s != sols %s"%(tier,i,[lastnum,lastden],sols))
        # phase boundary present
        if not any(st.get("phase")=="substitute" for st in gs):
            bad.append("%s[%d] no phase"%(tier,i))
        live_after = 0; seen_phase=False
        for st in gs:
            if st.get("phase")=="substitute": seen_phase=True
            if seen_phase and st.get("answer") is not None: live_after+=1
        if live_after<2: bad.append("%s[%d] live_after<2"%(tier,i))
        # misconception expects != sols
        for j,m in enumerate(p.get("misconceptions") or []):
            e=m["expect"]
            if isinstance(e,list) and e==sols:
                bad.append("%s[%d].misc[%d] expect==sols"%(tier,i,j))
        # svg external refs / theme
        disp=p["display"]
        if "http" in disp.lower() or "xlink" in disp.lower():
            bad.append("%s[%d] svg external"%(tier,i))
        for tg in re.findall(r'<text[^>]*>', disp):
            if 'fill="currentColor"' not in tg:
                bad.append("%s[%d] text not currentColor"%(tier,i))

# independent probability recompute from display semantics (spot targets)
def F(a,b): return Fraction(a,b)
targets = {
 ("bronze",0):F(3,8),("bronze",1):F(1,2),("bronze",2):F(7,10),("bronze",3):F(2,5),
 ("bronze",4):F(1,4),("bronze",6):F(2,11),("bronze",7):F(5,12),
 ("silver",0):F(1,4),("silver",1):F(4,25),("silver",2):F(5,14),("silver",3):F(1,5),
 ("silver",4):F(7,10),("silver",5):F(8,27),("silver",6):F(16,45),
 ("gold",0):F(8,15),("gold",1):F(7,24),("gold",2):F(15,16),("gold",3):F(2,5),("gold",4):F(4,9),
}
for (t,i),fr in targets.items():
    sols=pb[t][i]["solutions"]
    if F(sols[0],sols[1])!=fr:
        bad.append("%s[%d] sols %s != independent %s"%(t,i,sols,fr))
# b5 single value
if pb["bronze"][5]["solutions"]!=[10]: bad.append("b5 expected 10")

# teach + opener boxes numeric & landing
gd=pd["guided"]
for tier,val in gd["teach"].items():
    nb=sum(1 for st in val["steps"] if st.get("answer") is not None)
    if nb<4: bad.append("teach.%s boxes<4"%tier)

print("DEFECTS:",len(bad))
for x in bad: print("  -",x)
# report a few sanity numbers
print("teach silver last box (should be 25):", [st.get("answer") for st in gd["teach"]["silver"]["steps"] if st.get("answer") is not None][-1])
print("teach gold last box (should be 2):", [st.get("answer") for st in gd["teach"]["gold"]["steps"] if st.get("answer") is not None][-1])
