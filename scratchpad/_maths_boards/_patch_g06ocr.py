import os, json, io, urllib.request
ID="9f0126b9-ab85-4cbc-bc94-5d1214d5c4c2"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-ocr_graphs-L06.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
  "apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req); print("PATCH status:",r.status)
# verify round-trip
u2=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req2=urllib.request.Request(u2,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("live counts:", {t:len(live["problem_bank"][t]) for t in ("bronze","silver","gold")})
print("live gold[0] sol:", live["problem_bank"]["gold"][0]["solutions"], "| has chart:", "chart" in live["problem_bank"]["gold"][0])
