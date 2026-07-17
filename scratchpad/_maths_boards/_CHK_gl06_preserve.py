import json
ID="de6bd262-7fb6-4392-a5a3-e0cda56ea7ba"
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
# find entry
entry=None
if isinstance(pre,list):
    for r in pre:
        if r.get("id")==ID: entry=r; break
elif isinstance(pre,dict):
    entry=pre.get(ID) or (pre.get("data") and None)
print("type pre:", type(pre), "len" , len(pre) if hasattr(pre,'__len__') else '')
if entry is None and isinstance(pre,dict):
    print("dict keys sample:", list(pre.keys())[:5])
print("found entry:", entry is not None)
if entry:
    pd=entry.get("practice_data") or entry
    print("pre keys:", list(pd.keys()))
    live=json.load(open("_CHK_graphsL06_LIVE.json",encoding="utf-8"))
    for f in ["related_videos","topic_links","worked_examples"]:
        same = pd.get(f)==live.get(f)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE:", json.dumps(pd.get(f))[:400])
            print("  LIVE:", json.dumps(live.get(f))[:400])
