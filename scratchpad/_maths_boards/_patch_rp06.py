import os, json, urllib.request
ID="e15d6925-608b-4c05-aa82-c4782d1657b3"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-aqa_ratio-proportion-L06.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key,"Authorization":f"Bearer {key}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:", r.status)
# verify
url2=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req2=urllib.request.Request(url2, headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("live gold sols:", [p["solutions"] for p in live["problem_bank"]["gold"]])
print("live G1 display tail:", live["problem_bank"]["gold"][1]["display"][-20:])
print("worked_examples preserved:", live["worked_examples"]==pd["worked_examples"])
