import json, io
ID="44ac4c68-828c-4d38-888a-37758fefde57"
pre=json.load(io.open("_pre_dump_maths-ocr.json",encoding="utf-8"))
live=json.load(io.open("_CHK_algL13ocr_live.json",encoding="utf-8"))

# pre-dump structure: could be dict keyed by id, or list
entry=None
if isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v; break
if isinstance(pre,list):
    for v in pre:
        if v.get("id")==ID: entry=v; break
print("entry found:", entry is not None)
if entry is None:
    print("TOP-LEVEL TYPE:", type(pre))
    if isinstance(pre,dict): print("keys sample:", list(pre.keys())[:5])
    raise SystemExit

pd = entry.get("practice_data", entry)
for f in ["related_videos","topic_links","worked_examples"]:
    a=json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
    b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "UNCHANGED" if a==b else "CHANGED")
    if a!=b:
        print("  PRE :", a[:500])
        print("  LIVE:", b[:500])
print("pre keys:", sorted(pd.keys()))
print("live keys:", sorted(live.keys()))
