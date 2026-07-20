import json,os
d=os.path.dirname(os.path.abspath(__file__))
pd=json.load(open(os.path.join(d,"_CK12_live.json"),encoding="utf-8"))
out=[]
def w(s=""): out.append(s)
g=pd["guided"]
w("=== OPENER ===")
w(json.dumps(g.get("opener"),ensure_ascii=False,indent=1))
for t in ("bronze","silver","gold"):
    w("=== TEACH %s ==="%t)
    w(json.dumps(g["teach"][t],ensure_ascii=False,indent=1))
w("=== TIER GUIDES ===")
w(json.dumps(pd["tier_guides"],ensure_ascii=False,indent=1))
pb=pd["problem_bank"]
w("=== DESCRIPTIONS ===")
for k,v in pb.items():
    if k.endswith("_description"): w("%s: %s"%(k,v))
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        w("\n##### %s[%d] #####"%(t,i))
        w(json.dumps(p,ensure_ascii=False,indent=1))
w("=== METHOD CARD ===")
w(json.dumps(pd["method_card"],ensure_ascii=False,indent=1))
w("=== WORKED EXAMPLES ===")
w(json.dumps(pd.get("worked_examples"),ensure_ascii=False,indent=1))
open(os.path.join(d,"_CK12_dump.txt"),"w",encoding="utf-8").write("\n".join(out))
print(len("\n".join(out)))
