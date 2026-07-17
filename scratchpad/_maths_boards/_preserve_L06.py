import json
ID="6e4a84ec-b6c4-489b-9d86-0cc1a7fb65b0"
live=json.load(open("_live_L06_fetched.json",encoding="utf-8"))
dump=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
# find entry
entry=None
if isinstance(dump,list):
    for e in dump:
        if e.get("id")==ID or (isinstance(e,dict) and e.get("lesson_id")==ID): entry=e
elif isinstance(dump,dict):
    entry=dump.get(ID)
print("dump type:",type(dump).__name__, "len" , len(dump) if hasattr(dump,'__len__') else '')
if entry is None and isinstance(dump,list):
    print("sample keys:", list(dump[0].keys())[:10] if dump else None)
if entry:
    pdold=entry.get("practice_data",entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(pdold.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f,"PRESERVED" if a==b else "CHANGED")
        if a!=b:
            print("  OLD:",a[:300]); print("  NEW:",b[:300])
else:
    print("entry NOT FOUND for",ID)
