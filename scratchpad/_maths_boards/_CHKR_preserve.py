import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="fc1f101a-9d1b-4eab-8bf8-8159f78caea2"
live=json.load(open("_CHKR_live.json",encoding="utf-8"))["practice_data"]
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre could be dict keyed by id or list
entry=None
if isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    elif "practice_data" in pre: entry=pre
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v
elif isinstance(pre,list):
    for v in pre:
        if v.get("id")==ID: entry=v
print("pre type:",type(pre), "found entry:",entry is not None)
if entry and "practice_data" in entry: entry=entry["practice_data"]
if entry is None:
    print("keys in pre:", list(pre.keys())[:10] if isinstance(pre,dict) else len(pre))
else:
    for f in ["related_videos","topic_links","worked_examples"]:
        pv=json.dumps(entry.get(f),ensure_ascii=False,sort_keys=True)
        lv=json.dumps(live.get(f),ensure_ascii=False,sort_keys=True)
        print(f"{f}: {'SAME' if pv==lv else 'CHANGED'}  (pre {len(str(entry.get(f)))} / live {len(str(live.get(f)))})")
    print("pre top keys:",list(entry.keys()))
    print("live top keys:",list(live.keys()))
