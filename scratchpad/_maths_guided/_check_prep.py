import json
ID="de190166-58bb-4edb-927f-1f2f3f3d8eb3"
# worklist
wl=json.load(open("_worklist.json",encoding="utf-8"))
def find(o):
    if isinstance(o,dict):
        for v in o.values(): 
            r=find(v)
            if r: return r
    elif isinstance(o,list):
        for v in o:
            r=find(v)
            if r: return r
    return None
# print worklist structure
print("WORKLIST TYPE:", type(wl))
import json as j
s=j.dumps(wl)
# find entry with our ID
def walk(o,path=""):
    out=[]
    if isinstance(o,dict):
        if o.get("id")==ID or o.get("lesson_id")==ID:
            out.append((path,o))
        for k,v in o.items(): out+=walk(v,path+"/"+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): out+=walk(v,path+f"[{i}]")
    return out
for p,e in walk(wl):
    print("WL ENTRY:", p, {k:e[k] for k in e if k!='practice_data'})
