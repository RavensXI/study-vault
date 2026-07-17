import json
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
live=json.load(open("_live_ratio-L04.json",encoding="utf-8"))
lid="f4a69507-b194-4751-ae27-c657ddd23113"
# pre may be list of rows
def find(pre):
    if isinstance(pre,list):
        for r in pre:
            if r.get("id")==lid: return r
    if isinstance(pre,dict):
        if lid in pre: return pre[lid]
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==lid: return v
    return None
row=find(pre)
print("found pre row:", row is not None)
if row:
    pd=row.get("practice_data") or row
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "SAME" if a==b else "DIFF")
        if a!=b:
            print("  PRE:",a[:400])
            print("  LIVE:",b[:400])
    print("pre keys:", list(pd.keys()))
