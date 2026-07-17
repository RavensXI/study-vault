import os, json, urllib.request
ID="dd0172cd-6a81-41c6-ae9b-98de9328eb77"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-ocr_algebra-L10.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify readback
u2=f"{url}&select=practice_data"
r2=urllib.request.Request(u2,headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(r2))[0]["practice_data"]
print("keys:",sorted(live.keys()))
print("bronze/silver/gold:",len(live["problem_bank"]["bronze"]),len(live["problem_bank"]["silver"]),len(live["problem_bank"]["gold"]))
print("has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("gold[0] input_type:", live["problem_bank"]["gold"][0]["input_type"], "sols:", live["problem_bank"]["gold"][0]["solutions"])
