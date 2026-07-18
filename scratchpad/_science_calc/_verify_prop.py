import json, urllib.request, os, hashlib
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ids=["08e03207-3ecf-4964-81dc-a8b94002b3e2","599f6b2c-9f8e-4321-b8b0-7e6036ce1450","a19bb97b-86bd-46fd-8623-a309449c8166"]
base="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?select=practice_data&id=eq."
hdr={"apikey":KEY,"Authorization":f"Bearer {KEY}"}
hashes={}
canon=None
for i in ids:
    d=json.load(urllib.request.urlopen(urllib.request.Request(base+i,headers=hdr)))[0]["practice_data"]
    h=hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    hashes[i]=h
    if i==ids[0]:
        canon=d
        json.dump(d,open("_live_canon.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for i,h in hashes.items(): print(i[:8],h[:16])
print("ALL IDENTICAL:",len(set(hashes.values()))==1)
