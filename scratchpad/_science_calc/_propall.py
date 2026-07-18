import os, json, urllib.request, hashlib
KEY=os.environ.get('SUPABASE_SERVICE_KEY')
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids=["43820341-3858-411e-83f2-3eb799cb438c","db581cb0-0599-4bac-bca2-dfddabc7efdb",
"6e81a06c-c3bc-4d34-babe-494e118ff014","4ab2dfb0-a3ad-4e8d-960d-131a442f6950",
"72aa308d-5780-4998-bd5f-9cfe80d9cf07","8f8ace87-ba2d-4ae9-a188-75a66d4f4a9a",
"48e3458e-73a0-4558-8ddb-86bbb03ad7d5"]
h=set()
for i in ids:
    req=urllib.request.Request(f"{BASE}?id=eq.{i}&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    d=json.load(urllib.request.urlopen(req))
    pd=d[0]["practice_data"] if d else None
    dig=hashlib.sha256(json.dumps(pd,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:16] if pd else "MISSING"
    print(i, dig)
    h.add(dig)
print("ALL IDENTICAL" if len(h)==1 else "MISMATCH!!!")
