import os, json, urllib.request
ID="e0a5f715-f25c-4afd-b0c1-c71ea7f743e3"
sk=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("_maths_boards/lesson_maths-aqa_algebra-L13.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":sk,"Authorization":f"Bearer {sk}","Content-Type":"application/json",
    "Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:",r.status)
# verify
vurl=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
vreq=urllib.request.Request(vurl,headers={"apikey":sk,"Authorization":f"Bearer {sk}"})
live=json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
print("live top keys:",sorted(live.keys()))
print("has guided:","guided" in live,"| has tier_guides:","tier_guides" in live)
print("bronze n:",len(live["problem_bank"]["bronze"]),"silver n:",len(live["problem_bank"]["silver"]),"gold n:",len(live["problem_bank"]["gold"]))
print("svg in opener:","<svg" in live["guided"]["opener"]["display"])
print("svg in teach.bronze:","<svg" in live["guided"]["teach"]["bronze"]["display"])
print("bronze[0] sol:",live["problem_bank"]["bronze"][0]["solutions"],"input:",live["problem_bank"]["bronze"][0]["input_type"])
print("bronze[7] display tail:",live["problem_bank"]["bronze"][7]["display"][-30:],"sol:",live["problem_bank"]["bronze"][7]["solutions"])
