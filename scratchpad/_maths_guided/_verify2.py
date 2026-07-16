import json, io
new=json.load(io.open("lesson_geometry-L07.json",encoding="utf-8"))
dump=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
print("type",type(dump), "len", len(dump))
entry=None
for v in dump:
    if isinstance(v,dict) and (v.get("id")=="aee11210-c33f-4e61-a25e-1ef101e95ab3"):
        entry=v; break
print("found by id:", entry is not None)
if entry is None:
    # maybe keyed differently; sample
    print("sample keys:", list(dump[0].keys())[:8])
else:
    pdp=entry.get("practice_data",entry)
    for f in ("related_videos","topic_links","worked_examples"):
        same=json.dumps(pdp.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(new.get(f),sort_keys=True,ensure_ascii=False)
        print(f,"preserved:",same)
