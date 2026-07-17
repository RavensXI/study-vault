import json
ID="0ff5cf7c-3a9d-4854-b458-6d816b7df718"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre may be list of rows or dict
def find(pre):
    if isinstance(pre,list):
        for r in pre:
            if r.get("id")==ID: return r
    elif isinstance(pre,dict):
        if ID in pre: return pre[ID]
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: return v
    return None
row=find(pre)
print("found pre row:", row is not None)
if row is None:
    print("type:",type(pre))
    if isinstance(pre,list): print("first ids:",[r.get("id") for r in pre[:3]])
    if isinstance(pre,dict): print("keys sample:",list(pre.keys())[:5])
    raise SystemExit
prepd=row.get("practice_data") if "practice_data" in row else row
live=json.load(open("_CHK_L03rp_live.json",encoding="utf-8"))["practice_data"]
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(prepd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "PRESERVED" if same else "CHANGED")
    if not same:
        print("  PRE :",json.dumps(prepd.get(f),ensure_ascii=False)[:400])
        print("  LIVE:",json.dumps(live.get(f),ensure_ascii=False)[:400])
print("--- pre top keys:",list(prepd.keys()))
print("--- pre method_card:",json.dumps(prepd.get("method_card"),ensure_ascii=False)[:500])
