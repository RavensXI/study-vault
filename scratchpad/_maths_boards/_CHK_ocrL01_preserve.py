import json
ID="9a6f1e85-41b4-4b82-87c6-e919e48362a9"
live=json.load(open("_CHK_ocrL01_live.json", encoding="utf-8"))
dump=json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
# dump structure?
print("dump type:", type(dump))
if isinstance(dump, list):
    print("len", len(dump), "sample keys", list(dump[0].keys())[:6])
    entry=[r for r in dump if r.get("id")==ID]
elif isinstance(dump, dict):
    print("keys sample:", list(dump.keys())[:4])
    entry=dump.get(ID)
    entry=[{"id":ID,"practice_data":entry}] if entry else []
print("found entry:", bool(entry))
if entry:
    pre = entry[0].get("practice_data") if "practice_data" in entry[0] else entry[0]
    for field in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(pre.get(field),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(field),sort_keys=True,ensure_ascii=False)
        print(f"{field}: {'SAME' if a==b else 'CHANGED'}")
        if a!=b:
            print("  PRE :", a[:300])
            print("  LIVE:", b[:300])
    print("pre top keys:", sorted(pre.keys()))
    print("live top keys:", sorted(live.keys()))
