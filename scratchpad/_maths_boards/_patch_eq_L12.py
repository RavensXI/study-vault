import os, json, urllib.request
ID="66a1ec53-d20f-4b82-b436-1b31fc88e998"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-eduqas_algebra-L12.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify round-trip
url2=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req2=urllib.request.Request(url2,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
got=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("has guided:","guided" in got,"| tier_guides:","tier_guides" in got)
print("bronze desc set:",bool(got["problem_bank"].get("bronze_description")))
print("gold[2] has guided_steps:","guided_steps" in got["problem_bank"]["gold"][2])
print("round-trip equal:", json.dumps(got,sort_keys=True)==json.dumps(pd,sort_keys=True))
