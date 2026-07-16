import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
aud = json.load(open("_maths_audit/_audit_result.json", encoding="utf-8"))
for sec in ["issues","unconfirmed","confirmed","progression"]:
    items = aud.get(sec, [])
    if not isinstance(items,list): 
        print(sec, "->", items); continue
    for it in items:
        s=json.dumps(it, ensure_ascii=False)
        key = it.get("key") or it.get("lesson_key") or it.get("lesson") or ""
        if "geometry-L02" in s or "geometry-l02" in s or (isinstance(key,str) and "geometry" in key and ("2" in key)):
            print(f"[{sec}]", json.dumps(it, ensure_ascii=False))
# also print keys present to understand key format
print("\nsample issue:", json.dumps(aud["issues"][0], ensure_ascii=False) if aud["issues"] else "none")
print("sample unconfirmed:", json.dumps(aud["unconfirmed"][0], ensure_ascii=False) if aud["unconfirmed"] else "none")
