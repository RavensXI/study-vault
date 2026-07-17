import json
pd = json.load(open("_CHK_gL02ocr_live.json", encoding="utf-8"))["practice_data"]
json.dump(pd, open("_CHK_gL02ocr_shard.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

# preservation check vs pre-dump
import os
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
ID="7134e062-5209-4de5-894e-c315dc3ee9d0"
row=None
if isinstance(pre,list):
    for r in pre:
        if r.get("id")==ID: row=r; break
elif isinstance(pre,dict):
    row=pre.get(ID) or (pre.get("data") if False else None)
    if row is None:
        # maybe keyed differently
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: row=v; break
print("pre-dump row found:", row is not None)
if row:
    ppd=row.get("practice_data",{})
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
        print(f"  {f}: {'UNCHANGED' if same else 'CHANGED'}")
        if not same:
            print("    PRE:", json.dumps(ppd.get(f),ensure_ascii=False)[:300])
            print("    NOW:", json.dumps(pd.get(f),ensure_ascii=False)[:300])
