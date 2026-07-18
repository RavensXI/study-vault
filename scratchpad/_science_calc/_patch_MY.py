import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ROW_IDS=["d42fee71-d641-4f20-90c6-8bde5e185595"]
pd=json.load(io.open("lesson_higher-calculations-L01@8a0771bf50.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
base="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq."
hdr={"apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"}
for rid in ROW_IDS:
    req=urllib.request.Request(base+rid, data=body, headers=hdr, method="PATCH")
    r=urllib.request.urlopen(req)
    print("PATCH", rid, r.status)
# verify byte-identical readback for every row
for rid in ROW_IDS:
    req=urllib.request.Request(base+rid+"&select=practice_data", headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    live=json.load(urllib.request.urlopen(req))[0]["practice_data"]
    same=json.dumps(live,sort_keys=True,ensure_ascii=False)==json.dumps(pd,sort_keys=True,ensure_ascii=False)
    print("READBACK", rid, "identical:", same)
