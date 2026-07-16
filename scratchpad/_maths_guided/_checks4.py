import json
# audit result
aud = json.load(open("_maths_audit/_audit_result.json", encoding="utf-8"))
print("audit top keys:", list(aud.keys()) if isinstance(aud,dict) else type(aud))
def scan(section):
    items = aud.get(section, [])
    hits=[]
    for it in items:
        s=json.dumps(it, ensure_ascii=False)
        if "geometry" in s.lower() and ("L02" in s or "l02" in s or "Area" in s or "fe5f6191" in s):
            hits.append(it)
    return hits
for sec in (aud.keys() if isinstance(aud,dict) else []):
    if isinstance(aud[sec], list):
        h=scan(sec)
        if h:
            print(f"\n--- {sec} ({len(h)}) ---")
            for x in h: print(json.dumps(x, ensure_ascii=False, indent=1))
