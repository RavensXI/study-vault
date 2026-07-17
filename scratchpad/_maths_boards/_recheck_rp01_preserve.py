import json
SID = "a6f6c5da-0aa8-437c-b3fe-75b8a48d6714"
live = json.load(open("_recheck_rp01_live.json", encoding="utf-8"))
pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))

# find matching entry in pre-dump
def find(pre):
    if isinstance(pre, dict):
        if SID in pre: return pre[SID]
        for k,v in pre.items():
            if isinstance(v, dict) and v.get("id")==SID: return v
        # maybe list under a key
        for k,v in pre.items():
            r = find(v)
            if r: return r
    if isinstance(pre, list):
        for e in pre:
            if isinstance(e, dict) and e.get("id")==SID: return e
    return None
entry = find(pre)
print("pre-dump type:", type(pre).__name__)
if isinstance(pre, dict):
    print("pre-dump top keys sample:", list(pre.keys())[:5])
print("found entry:", entry is not None)
if entry is not None:
    pd = entry.get("practice_data", entry)
    print("pre keys:", list(pd.keys()) if isinstance(pd,dict) else type(pd))
    for f in ["related_videos","worked_examples","topic_links","method_card"]:
        pv = pd.get(f) if isinstance(pd,dict) else None
        lv = live.get(f)
        same = json.dumps(pv,sort_keys=True,ensure_ascii=False)==json.dumps(lv,sort_keys=True,ensure_ascii=False)
        print(f"  {f}: preserved={same}")
    json.dump(pd, open("_recheck_rp01_pre.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
