import json,os
d=os.path.dirname(os.path.abspath(__file__))
pre=json.load(open(os.path.join(d,"_CK12_pre.json"),encoding="utf-8"))
live=json.load(open(os.path.join(d,"_CK12_live.json"),encoding="utf-8"))
print("pre top keys:", list(pre.keys()))
ppd = pre.get("practice_data") or pre
print("pre pd keys:", list(ppd.keys()))
for t in ("bronze","silver","gold"):
    a=ppd["problem_bank"][t]; b=live["problem_bank"][t]
    print("---",t,len(a),len(b))
    for i,(x,y) in enumerate(zip(a,b)):
        for f in ("display","solutions","image","chart","ruler","options","input_type","calculator"):
            if x.get(f)!=y.get(f):
                print("  %s[%d].%s\n    PRE : %s\n    LIVE: %s"%(t,i,f,json.dumps(x.get(f),ensure_ascii=False),json.dumps(y.get(f),ensure_ascii=False)))
for f in ("worked_examples","topic_links","exam_context","related_videos"):
    print(f,"same" if ppd.get(f)==live.get(f) else "CHANGED")
