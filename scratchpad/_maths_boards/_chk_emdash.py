import json
pd=json.load(open("_CHK_live_L03.json",encoding="utf-8"))["practice_data"]
# recursively find em dashes and en dashes in strings
hits=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        for ch,name in [("—","EM-DASH"),("–","EN-DASH")]:
            if ch in o: hits.append((path,name,o[:80]))
for k in pd: walk(pd[k],k)
print("EMDASH/ENDASH hits:", len(hits))
for h in hits: print(h)
