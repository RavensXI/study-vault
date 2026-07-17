import json, io
KEY="algebra-L12"
ID="971cfba0-badb-4c6b-b0f8-e9d33d450b8c"
live=json.load(io.open("_CHK_algL12ocr_live.json","r",encoding="utf-8"))
dump=json.load(io.open("_pre_dump_maths-ocr.json","r",encoding="utf-8"))
# dump structure?
if isinstance(dump, dict):
    keys=list(dump.keys())
    print("dump top keys sample:", keys[:5], "n=", len(keys))
    # find entry by id or key
    entry=None
    for k,v in dump.items():
        if k==ID or k==KEY:
            entry=v; break
        if isinstance(v,dict) and (v.get("id")==ID or v.get("key")==KEY or v.get("lesson_key")==KEY):
            entry=v; break
    if entry is None and ID in dump: entry=dump[ID]
    print("entry found:", entry is not None)
elif isinstance(dump, list):
    print("dump is list n=", len(dump))
    entry=None
    for v in dump:
        if v.get("id")==ID or v.get("key")==KEY or v.get("lesson_key")==KEY or v.get("slug")==KEY:
            entry=v; break
    print("entry found:", entry is not None)
    if entry: print("entry keys:", list(entry.keys()))
