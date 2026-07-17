import json, io
live=json.load(io.open("_CHK_L09_live.json",encoding="utf-8"))
dump=json.load(io.open("_pre_dump_maths-aqa.json",encoding="utf-8"))
ID="5ff3e1eb-2284-4096-af06-4bcb6754b0e1"
# find entry
entry=None
if isinstance(dump,list):
    for e in dump:
        if e.get("id")==ID or e.get("key")=="algebra-L09": entry=e
elif isinstance(dump,dict):
    entry=dump.get(ID) or dump.get("algebra-L09")
    if entry is None:
        # maybe keyed differently
        for k,v in dump.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v
print("dump type:", type(dump).__name__, "| top len:", len(dump) if hasattr(dump,'__len__') else '?')
if isinstance(dump,dict):
    print("dump sample keys:", list(dump.keys())[:5])
print("entry found:", entry is not None)
if entry is not None:
    pdold = entry.get("practice_data", entry)
    for f in ("related_videos","topic_links","worked_examples"):
        old=pdold.get(f); new=live.get(f)
        print(f"{f}: {'SAME' if old==new else '*** DIFFERENT ***'}")
        if old!=new:
            print("   OLD:", json.dumps(old,ensure_ascii=False)[:300])
            print("   NEW:", json.dumps(new,ensure_ascii=False)[:300])
