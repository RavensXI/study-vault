import json
ID="da768b8a-d62b-4701-8423-7988dc8325a7"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre may be list or dict
entry=None
if isinstance(pre,list):
    for r in pre:
        if r.get("id")==ID: entry=r; break
elif isinstance(pre,dict):
    entry=pre.get(ID) or pre
print("pre type:",type(pre).__name__, "found entry:", entry is not None)
if entry and "practice_data" in entry: entry=entry["practice_data"]
live=json.load(open("_live_L14.json",encoding="utf-8"))
if entry:
    for f in ["related_videos","topic_links","worked_examples","method_card"]:
        pv=json.dumps(entry.get(f),ensure_ascii=False,sort_keys=True)
        lv=json.dumps(live.get(f),ensure_ascii=False,sort_keys=True)
        print(f"{f}: {'SAME' if pv==lv else 'CHANGED'}")
    print("pre keys:",list(entry.keys()))
