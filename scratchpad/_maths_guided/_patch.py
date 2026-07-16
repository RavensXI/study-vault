import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="a769c80a-697d-4ae1-a042-6299738f9021"
pd=json.load(io.open("lesson_algebra-L12.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
 "apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status", r.status)
# read back
req2=urllib.request.Request(url+"&select=practice_data", headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("readback keys:", sorted(back.keys()))
print("bronze n=%d silver n=%d gold n=%d"%(len(back["problem_bank"]["bronze"]),len(back["problem_bank"]["silver"]),len(back["problem_bank"]["gold"])))
print("has guided:", "guided" in back, "has tier_guides:", "tier_guides" in back)
print("match written:", back==pd)
