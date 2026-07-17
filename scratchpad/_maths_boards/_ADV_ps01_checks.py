import json, re
from fractions import Fraction

live=json.load(open("_ADV_ps01_live.json",encoding="utf-8"))["practice_data"]

# write shard for validator (just the practice_data)
json.dump(live, open("_ADV_ps01_shard.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- preservation vs pre-dump ----
predump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# find the ps01 entry
ID="a28fddf4-3ee1-48dc-b138-aa17facad15d"
pre=None
if isinstance(predump,list):
    for r in predump:
        if r.get("id")==ID:
            pre=r; break
elif isinstance(predump,dict):
    pre=predump.get(ID)
print("PRE FOUND:", pre is not None)
if pre is not None:
    ppd=pre.get("practice_data",pre)
    for f in ["related_videos","topic_links","worked_examples","method_card"]:
        a=json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'SAME' if a==b else 'CHANGED'}")
        if a!=b:
            print("  PRE :",a[:300])
            print("  LIVE:",b[:300])

# ---- em dash / style scan on student-facing strings ----
EM="—"
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            # skip internal note fields
            if k=="note": continue
            walk(v,path+"/"+k)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,path+f"[{i}]")
    elif isinstance(o,str):
        if EM in o:
            print("EM DASH at",path,":",o[:80])
walk(live)
print("em-dash scan done")

# ---- fresh solve every problem numeric-only box check ----
print("\n--- box numeric check ---")
pb=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        for j,s in enumerate(p.get("guided_steps",[])):
            if "answer" in s and not isinstance(s["answer"],(int,float)):
                print(f"NON-NUMERIC {tier}[{i}].guided_steps[{j}]:",s["answer"])
print("numeric check done")
