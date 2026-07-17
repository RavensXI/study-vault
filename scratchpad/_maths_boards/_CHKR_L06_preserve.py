import json
ID="fe05d231-ed67-4625-aa4d-791c6b1d9887"
live=json.load(open("_CHKR_L06_live.json",encoding="utf-8"))
dump=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# find entry
entry=None
if isinstance(dump,list):
    for r in dump:
        if r.get("id")==ID: entry=r; break
elif isinstance(dump,dict):
    entry=dump.get(ID) or dump.get("data") 
print("dump type",type(dump), "found entry:", entry is not None)
if entry is None:
    # maybe dict keyed
    print("sample keys", list(dump)[:3] if isinstance(dump,dict) else [r.get('id') for r in dump[:3]])
else:
    pre=entry.get("practice_data") if "practice_data" in entry else entry
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "PRESERVED" if a==b else "CHANGED")
        if a!=b:
            print("  PRE :",a[:300])
            print("  LIVE:",b[:300])
