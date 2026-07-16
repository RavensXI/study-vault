import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="d9df7fae-d515-4c06-94b6-9068029bd037"
pd=json.load(io.open("lesson_ratio-proportion-L03.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":KEY,"Authorization":f"Bearer {KEY}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
resp=urllib.request.urlopen(req)
print("PATCH status:", resp.status)
# verify readback
req2=urllib.request.Request(url+"&select=practice_data", headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("readback keys:", sorted(back.keys()))
print("bronze6 display:", back["problem_bank"]["bronze"][6]["display"])
print("bronze7 sol:", back["problem_bank"]["bronze"][7]["solutions"])
print("has guided.opener:", "opener" in back.get("guided",{}))
print("roundtrip equal:", back==pd)
