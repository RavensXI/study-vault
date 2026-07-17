import json
ID = "5f629e65-9b8c-4fcb-a334-93ee7e25d4ff"
pre = json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# figure out structure
if isinstance(pre, dict):
    print("pre is dict, keys sample:", list(pre.keys())[:5])
    entry = pre.get(ID)
    if entry is None:
        # maybe keyed differently
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID:
                entry=v; break
elif isinstance(pre, list):
    entry = next((e for e in pre if e.get("id")==ID), None)
    print("pre is list, len", len(pre))
print("ENTRY FOUND:", entry is not None)
if entry:
    print("entry keys:", list(entry.keys()))
    pd = entry.get("practice_data") or entry
    for f in ("related_videos","topic_links","worked_examples"):
        print("HAS", f, ":", f in pd)
    json.dump(pd, open("_pre_numL03_pd.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
