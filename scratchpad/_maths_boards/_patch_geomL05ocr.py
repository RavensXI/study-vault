import os, json, urllib.request
ID="2d827ad4-80ab-4327-81f8-a2e5cec4f50a"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-ocr_geometry-L05.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":KEY,"Authorization":f"Bearer {KEY}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify readback
u2=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
r2=urllib.request.Request(u2,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
live=json.load(urllib.request.urlopen(r2))[0]["practice_data"]
print("live has guided:","guided" in live,"tier_guides:","tier_guides" in live)
print("silver[6] sol:",live["problem_bank"]["silver"][6]["solutions"])
print("gold[3] sol:",live["problem_bank"]["gold"][3]["solutions"])
print("bronze[0] has svg:","<svg" in live["problem_bank"]["bronze"][0]["display"])
