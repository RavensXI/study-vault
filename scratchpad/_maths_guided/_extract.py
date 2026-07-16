import json
ID = "ea8d68a2-63b8-40e9-87de-f879156e0d93"
# worklist
wl = json.load(open("_worklist.json",encoding="utf-8"))
def find(o):
    s=json.dumps(o)
    return ID in s
# print worklist entry matching
def walk(x,path=""):
    pass
print("=== WORKLIST matches ===")
def search(obj):
    results=[]
    if isinstance(obj,dict):
        if obj.get("id")==ID or obj.get("lesson_id")==ID:
            results.append(obj)
        for v in obj.values():
            results+=search(v)
    elif isinstance(obj,list):
        for v in obj:
            results+=search(v)
    return results
for m in search(wl):
    print(json.dumps(m,indent=1)[:800])
