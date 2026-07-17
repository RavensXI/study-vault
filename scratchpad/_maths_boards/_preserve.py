import json
ID="d6cc3827-bbe2-42ae-b116-7c8398b1bf70"
KEY="probability-statistics-L03"
live=json.load(open("_live_L03.json",encoding="utf-8"))
dump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# find entry
entry=None
if isinstance(dump,list):
    for e in dump:
        if e.get("id")==ID or e.get("key")==KEY or e.get("lesson_key")==KEY:
            entry=e;break
elif isinstance(dump,dict):
    entry=dump.get(ID) or dump.get(KEY)
    if entry is None:
        for k,v in dump.items():
            if isinstance(v,dict) and (v.get("id")==ID or v.get("key")==KEY):
                entry=v;break
print("entry found:", entry is not None, "| dump type:", type(dump).__name__)
if entry is not None:
    print("entry keys:", list(entry.keys())[:10])
