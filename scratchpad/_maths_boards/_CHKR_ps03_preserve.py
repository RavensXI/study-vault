import json
ID="65e7a745-9820-431a-8b99-d96cd7514bf3"
live=json.load(open("_CHKR_ps03_live.json",encoding="utf-8"))["practice_data"]
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre may be list or dict
entry=None
if isinstance(pre,list):
    for e in pre:
        if e.get("id")==ID: entry=e; break
elif isinstance(pre,dict):
    entry = pre.get(ID) or (pre.get("data") and None)
    if entry is None and "practice_data" in pre and pre.get("id")==ID: entry=pre
print("pre type:",type(pre).__name__, "found entry:",entry is not None)
if entry is None:
    # try structure
    print("keys sample:", list(pre.keys())[:5] if isinstance(pre,dict) else [e.get('id') for e in pre[:3]])
else:
    ppd=entry.get("practice_data",entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(ppd.get(f),ensure_ascii=False,sort_keys=True)
        b=json.dumps(live.get(f),ensure_ascii=False,sort_keys=True)
        print(f"{f}: {'SAME' if a==b else 'DIFF'} (pre_present={f in ppd}, live_present={f in live})")
    # method_card compare
    print("method_card pre keys:", list(ppd.get("method_card",{}).keys()) if ppd.get("method_card") else None)
    print("method_card live keys:", list(live.get("method_card",{}).keys()) if live.get("method_card") else None)
    # what top-level keys existed pre vs live
    print("pre top keys:", sorted(ppd.keys()))
    print("live top keys:", sorted(live.keys()))
