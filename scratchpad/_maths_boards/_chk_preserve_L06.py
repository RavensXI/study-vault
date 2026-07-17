import json
ID="32acb3ec-b5ac-410b-984c-d9008683af8e"
live=json.load(open("_live_algL06_eduqas.json",encoding="utf-8"))["practice_data"]
dump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# dump may be list or dict keyed by id
entry=None
if isinstance(dump,list):
    for r in dump:
        if r.get("id")==ID: entry=r; break
elif isinstance(dump,dict):
    if ID in dump: entry=dump[ID]
    else:
        # maybe {'lessons':[...]}
        for k,v in dump.items():
            if isinstance(v,list):
                for r in v:
                    if isinstance(r,dict) and r.get("id")==ID: entry=r
print("entry found:", entry is not None)
if entry:
    pre = entry.get("practice_data", entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "PRESERVED" if same else "CHANGED")
        if not same:
            print("  PRE :", json.dumps(pre.get(f),ensure_ascii=False)[:400])
            print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:400])
    print("pre keys:", list(pre.keys()))
