import json
ID = "4aa9afe1-7e47-4f0f-b7e6-da22be472716"
live = json.load(open("_CHK_L06_LIVE_fresh.json", encoding="utf-8"))
pre_all = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
entry = [e for e in pre_all if e.get("id")==ID][0]
pre = entry["practice_data"]["worked_examples"]
lv = live["worked_examples"]
print("counts pre/live:", len(pre), len(lv))
def walk(a,b,path=""):
    if isinstance(a,dict):
        for k in set(a)|set(b):
            if k not in a: print("ADDED",path,k)
            elif k not in b: print("REMOVED",path,k)
            else: walk(a[k],b[k],path+"/"+k)
    elif isinstance(a,list):
        for i in range(max(len(a),len(b))):
            walk(a[i] if i<len(a) else None, b[i] if i<len(b) else None, f"{path}[{i}]")
    else:
        if a!=b:
            print(f"CHANGED {path}:\n   PRE : {repr(a)}\n   LIVE: {repr(b)}")
walk(pre,lv)
