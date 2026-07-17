import os, json, urllib.request
ID="320a6b1d-a96c-400f-8807-5828376373ea"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("../_maths_guided/lesson_algebra-L05.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
 "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status", r.status)
# verify readback
url2=f"{url}&select=practice_data"
req2=urllib.request.Request(url2, headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("live bronze sols:", [p["solutions"] for p in live["problem_bank"]["bronze"]])
print("live silver[2] display:", live["problem_bank"]["silver"][2]["display"])
print("live gold[3] gsteps boxes:", sum(1 for s in live["problem_bank"]["gold"][3]["guided_steps"] if s.get("answer") is not None))
print("worked_examples preserved count:", len(live.get("worked_examples",[])))
