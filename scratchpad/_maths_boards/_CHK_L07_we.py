import json
live = json.load(open("_CHK_L07_live.json", encoding="utf-8"))
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
ID = "e16ccba1-6dc0-4321-835b-98ec18acce00"
entry = None
if isinstance(pre, dict):
    entry = pre.get(ID)
    if entry is None:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v;break
elif isinstance(pre,list):
    for v in pre:
        if isinstance(v,dict) and v.get("id")==ID: entry=v;break
pd_pre = entry.get("practice_data", entry)
out = {
 "pre_worked_examples": pd_pre.get("worked_examples"),
 "now_worked_examples": live.get("worked_examples"),
 "pre_method_card": pd_pre.get("method_card"),
 "now_method_card": live.get("method_card"),
 "pre_has_guided": "guided" in pd_pre,
 "pre_has_tier_guides": "tier_guides" in pd_pre,
 "pre_keys": list(pd_pre.keys()),
}
json.dump(out, open("_CHK_L07_we_out.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("equal worked_examples:", json.dumps(pd_pre.get("worked_examples"),sort_keys=True,ensure_ascii=False)==json.dumps(live.get("worked_examples"),sort_keys=True,ensure_ascii=False))
