import json
ID="9f5d0097-caa6-464c-9f1c-05ce6b836cc9"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre may be list of rows
rows = pre if isinstance(pre,list) else pre.get("data",pre)
entry=None
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
entry=find(pre)
print("found pre entry:", bool(entry))
if entry:
    pd=entry.get("practice_data") or entry
    print("pre keys:", list(pd.keys()))
    open("_pre_pd.json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=2))
    live=json.load(open("_checker_live.json",encoding="utf-8"))
    for f in ["related_videos","worked_examples","topic_links","method_card"]:
        same = json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE:", json.dumps(pd.get(f),ensure_ascii=False)[:300])
            print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:300])
