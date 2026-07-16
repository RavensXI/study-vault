import os, json, urllib.request
ID="bc1ac13e-1cc0-42b3-a805-a8a3f35cbabb"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_ratio-proportion-L01.json", encoding="utf-8"))
body=json.dumps({"practice_data": pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url, data=body, method="PATCH", headers={
  "apikey":key,"Authorization":f"Bearer {key}",
  "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:", r.status)
# verify
vurl=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
vreq=urllib.request.Request(vurl, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(vreq))
sv=d[0]["practice_data"]["problem_bank"]["silver"][0]
print("VERIFY display:", sv["display"])
print("VERIFY solutions:", sv["solutions"])
print("VERIFY expect:", sv["misconceptions"][0]["expect"])
