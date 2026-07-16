import os, json, io, urllib.request
ID="65f2d938-335c-4d09-9917-f888f5a7c23e"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_geometry-L01_diagrams.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url, data=body, method="PATCH", headers={
 "apikey":key,"Authorization":f"Bearer {key}",
 "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:", r.status)
# verify roundtrip
gurl=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
g=urllib.request.Request(gurl, headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(g))[0]["practice_data"]
cnt=sum(1 for t in ("bronze","silver","gold") for p in live["problem_bank"][t] if "<svg" in p["display"])
print("live bank svgs:", cnt)
print("opener svg:", "<svg" in live["guided"]["opener"].get("display",""))
print("teach bronze svg:", "<svg" in live["guided"]["teach"]["bronze"]["display"])
print("teach silver svg:", "<svg" in live["guided"]["teach"]["silver"]["display"])
