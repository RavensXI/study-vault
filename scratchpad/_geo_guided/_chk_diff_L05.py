import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="64a15c1c-c8d3-4eee-af4d-7d6d0342ac29"
pre=json.load(open("../_geo_audit/_pre_dump_all.json",encoding="utf-8"))
print("predump type",type(pre))
if isinstance(pre,dict):
    keys=list(pre.keys())[:5]; print(keys)
    entry=pre.get(ID)
else:
    entry=None
    for r in pre:
        if r.get("id")==ID: entry=r
print("found:", entry is not None)
if entry is not None:
    json.dump(entry,open("_CHK_L05_pre.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print("entry keys",list(entry.keys())[:20])
