import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="68997180-8486-4551-ab42-0a1b98384336"
live=json.load(open("_live_L01.json",encoding="utf-8"))
dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
def locate(o):
    if isinstance(o,dict):
        if o.get("id")==ID: return o
        for v in o.values():
            r=locate(v)
            if r: return r
    if isinstance(o,list):
        for x in o:
            r=locate(x)
            if r: return r
    return None
pre=locate(dump)["practice_data"]
print("=== PRE worked_examples ===")
print(json.dumps(pre["worked_examples"],ensure_ascii=False,indent=1))
print("=== PRE bank ===")
for t in ["bronze","silver","gold"]:
    print(t, len(pre["problem_bank"][t]), [p["display"] for p in pre["problem_bank"][t]])
print("=== LIVE bank ===")
for t in ["bronze","silver","gold"]:
    print(t, len(live["problem_bank"][t]), [p["display"] for p in live["problem_bank"][t]])
