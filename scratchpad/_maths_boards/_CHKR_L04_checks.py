import json, re, subprocess, sys

ID="6e383a58-7e5b-4917-a28d-2881938a3def"
live=json.load(open("_CHKR_L04_live.json",encoding="utf-8"))
pd=live["practice_data"]

# 1. Write shard for validator
open("_CHKR_L04_shard.json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=1))

# 2. em dash search in student-facing strings
emdash=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note":  # internal exempt
                continue
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o:
            emdash.append(path)
walk(pd,"pd")
print("EM DASHES:",emdash)

# 3. entity search (&pound; etc) in student-facing
ents=[]
def walk2(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            walk2(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk2(v,f"{path}[{i}]")
    elif isinstance(o,str):
        for m in re.findall(r"&[a-z]+;",o):
            ents.append((path,m))
walk2(pd,"pd")
from collections import Counter
print("ENTITIES:",Counter([e[1] for e in ents]))
print("ENTITY PATHS:")
for p,m in ents:
    print("  ",m,p)
