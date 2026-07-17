import os, json, io, urllib.request
ID="fe1de83d-e81d-4f39-bc83-036f91da46f0"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_geometry-L01.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":key,"Authorization":f"Bearer {key}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify roundtrip
gu=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
g=urllib.request.Request(gu,headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("roundtrip equal:", live==pd)
print("keys:", sorted(live.keys()))
