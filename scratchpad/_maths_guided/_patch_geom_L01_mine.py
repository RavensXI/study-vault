import os, json, urllib.request
ID="65f2d938-335c-4d09-9917-f888f5a7c23e"
key=os.environ["SUPABASE_SERVICE_KEY"]
with open("lesson_geometry-L01.json",encoding="utf-8") as f:
    pd=json.load(f)
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key,"Authorization":f"Bearer {key}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
resp=urllib.request.urlopen(req)
print("PATCH status:",resp.status)
# verify
vurl=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
vreq=urllib.request.Request(vurl, headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
print("live has keys:", sorted(live.keys()))
print("gold count:", len(live["problem_bank"]["gold"]), "gold[2]:", live["problem_bank"]["gold"][2]["display"][:40])
print("guided present:", "guided" in live, "tier_guides present:", "tier_guides" in live)
print("bronze[1] sol:", live["problem_bank"]["bronze"][1]["solutions"])
