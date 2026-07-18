import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ALL=["6dc6da50-6253-4e4d-9806-83c34bc567cb"]
pd=json.load(io.open("lesson_higher-calculations-L01@146c1cc6d7.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode()
for ID in ALL:
    url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
    req=urllib.request.Request(url,data=body,method="PATCH",headers={
        "apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
    r=urllib.request.urlopen(req); print("PATCH",ID,r.status)
# verify round-trip byte-identical
for ID in ALL:
    url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
    req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    live=json.load(urllib.request.urlopen(req))[0]["practice_data"]
    same=json.dumps(live,sort_keys=True)==json.dumps(pd,sort_keys=True)
    print("VERIFY",ID,"identical" if same else "MISMATCH")
