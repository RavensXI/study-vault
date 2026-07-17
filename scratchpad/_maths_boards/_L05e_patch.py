import os, json, io, urllib.request
ID="2e75898f-577a-42bd-b94e-f1435e89ace3"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-eduqas_probability-statistics-L05.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:", r.status)
# verify roundtrip
g=urllib.request.Request(f"{url}&select=practice_data", headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("guided present:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("B4 cf:", live["problem_bank"]["bronze"][3]["chart"]["data"]["datasets"][0]["data"])
print("B8 display:", live["problem_bank"]["bronze"][7]["display"], "sol", live["problem_bank"]["bronze"][7]["solutions"])
print("gold[2] chart added:", "chart" in live["problem_bank"]["gold"][2])
