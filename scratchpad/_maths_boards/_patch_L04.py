import os, json, urllib.request
ID="499de8ed-424f-4027-a013-e64b3b083820"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-eduqas_geometry-L04.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify
g=urllib.request.Request(url+"&select=practice_data",headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("live keys:",sorted(live.keys()))
print("has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze[0] hint:", live["problem_bank"]["bronze"][0].get("hint","MISSING")[:40])
print("gold[0] mis[0] expect:", live["problem_bank"]["gold"][0]["misconceptions"][0]["expect"])
print("silver[2] display starts svg:", live["problem_bank"]["silver"][2]["display"][:10])
