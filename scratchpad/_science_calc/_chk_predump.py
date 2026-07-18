import json, io, re
canon="e68bcd00-8b3f-47d3-9a5b-e327a9ddde48"
pd=json.load(open("_pre_dump_all.json",encoding="utf-8"))
# structure?
print("pre_dump top type:", type(pd))
if isinstance(pd,dict):
    print("has canon key:", canon in pd)
    keys=list(pd.keys())
    print("num entries:", len(keys), "sample keys:", keys[:3])
