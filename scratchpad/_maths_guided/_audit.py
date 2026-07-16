import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="68997180-8486-4551-ab42-0a1b98384336"
a=json.load(open("_maths_audit/_audit_result.json",encoding="utf-8"))
def rel(o):
    hits=[]
    if isinstance(o,dict):
        s=json.dumps(o)
        if ID in s or "number" in json.dumps(o.get("key","")) or "L01" in json.dumps(o.get("key","")):
            pass
        for k in ("issues","unconfirmed"):
            pass
    return o
print("top keys:", list(a.keys()) if isinstance(a,dict) else type(a))
for sec in ("issues","unconfirmed"):
    items=a.get(sec,[]) if isinstance(a,dict) else []
    for it in items:
        key=json.dumps(it)
        if ID in key or "number" in str(it.get("key","")).lower() and "L01" in str(it.get("key","")):
            print(sec, json.dumps(it,ensure_ascii=False))
# also just print any entry mentioning this lesson id or number-L01
allstr=json.dumps(a,ensure_ascii=False)
print("ID present in audit:", ID in allstr)
