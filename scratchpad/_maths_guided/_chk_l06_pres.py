# -*- coding: utf-8 -*-
import math, json

# method_card precision
x1=math.sqrt(23)
print("x1=%.8f -> 4dp %.4f"%(x1, round(x1,4)))
x2=math.sqrt(5*x1+3)
print("x2 full=%.8f -> 4dp %.4f"%(x2, round(x2,4)))
x2b=math.sqrt(26.979)  # using their shown 3dp intermediate
print("x2 from 26.979=%.8f -> 4dp %.4f"%(x2b, round(x2b,4)))
x3=math.sqrt(5*x2+3); print("x3 full=%.8f -> 4dp %.4f"%(x3, round(x3,4)))

# preservation
live=json.load(open("_CHK_L06_live.json",encoding="utf-8"))
dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
ID="62194f78-5bda-4cdb-81db-015760b58c7a"
pre=None
def find(o):
    if isinstance(o,dict):
        if o.get("id")==ID: return o
        for v in o.values():
            r=find(v)
            if r: return r
    if isinstance(o,list):
        for v in o:
            r=find(v)
            if r: return r
    return None
pre=find(dump)
if pre is None:
    print("PRE NOT FOUND; dump top keys:", list(dump.keys())[:20] if isinstance(dump,dict) else type(dump))
else:
    ppd=pre.get("practice_data") or pre.get("practice_data")
    print("pre keys:", list(pre.keys())[:10])
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "SAME" if a==b else "DIFFERENT")
        if a!=b:
            print("  PRE:",a[:400])
            print("  LIVE:",b[:400])
