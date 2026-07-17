import json
ID="70586def-170c-4aa7-947b-2b961cfadec2"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre may be list or dict
if isinstance(pre,dict) and "practice_data" not in pre:
    # find entry
    entries=pre.get("lessons") or pre.get("data") or list(pre.values())
else:
    entries=pre
def find(entries):
    if isinstance(entries,list):
        for e in entries:
            if isinstance(e,dict) and e.get("id")==ID: return e
    if isinstance(entries,dict):
        if entries.get("id")==ID: return entries
        for v in entries.values():
            r=find(v) if isinstance(v,(list,dict)) else None
            if r: return r
    return None
e=find(pre)
print("found pre entry:",bool(e))
live=json.load(open("_CHK_geoL03_live.json",encoding="utf-8"))["practice_data"]
if e:
    ppd=e.get("practice_data",e)
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE:",json.dumps(ppd.get(f),ensure_ascii=False)[:300])
            print("  LIVE:",json.dumps(live.get(f),ensure_ascii=False)[:300])
    print("pre top keys:",list(ppd.keys()))
