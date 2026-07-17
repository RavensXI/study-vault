import json
live=json.load(open("_ADV_ps01_live.json",encoding="utf-8"))["practice_data"]
predump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
ID="a28fddf4-3ee1-48dc-b138-aa17facad15d"
pre=None
for r in predump:
    if r.get("id")==ID: pre=r;break
ppd=pre["practice_data"]
a=ppd["worked_examples"]; b=live["worked_examples"]
print("len pre",len(a),"len live",len(b))
for i in range(max(len(a),len(b))):
    ea=json.dumps(a[i],sort_keys=True,ensure_ascii=False) if i<len(a) else None
    eb=json.dumps(b[i],sort_keys=True,ensure_ascii=False) if i<len(b) else None
    if ea!=eb:
        print(f"--- worked_examples[{i}] DIFFERS ---")
        print("PRE :",ea)
        print("LIVE:",eb)
