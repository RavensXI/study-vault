import json, re
live=json.load(open("_CK_geoL08_live.json",encoding="utf-8"))
pd=live["practice_data"]

# 1. em dash hunt in all strings
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        yield path,o
emdash=[]
for p,s in walk(pd):
    if "—" in s and ".note" not in p:
        emdash.append((p,s))
print("EM DASHES:",len(emdash))
for p,s in emdash[:20]: print("  ",p,repr(s[:80]))

# 2. compare preservation vs pre-dump
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
# pre-dump structure?
print("\nPREDUMP type:",type(pre))
if isinstance(pre,list):
    print("len",len(pre),"sample keys",list(pre[0].keys()) if pre else None)
elif isinstance(pre,dict):
    print("keys sample:",list(pre.keys())[:5])
