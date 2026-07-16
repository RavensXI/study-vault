import json
KEY="algebra-L04"
ID="de190166-58bb-4edb-927f-1f2f3f3d8eb3"
a=json.load(open("../_maths_audit/_audit_result.json",encoding="utf-8"))
for sect in ("issues","unconfirmed"):
    items=a.get(sect,[])
    hits=[x for x in items if KEY in json.dumps(x) or ID in json.dumps(x)]
    print(f"=== {sect}: {len(hits)} hits ===")
    for h in hits: print(json.dumps(h,ensure_ascii=False))
