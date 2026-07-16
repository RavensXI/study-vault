import os, json, io, urllib.request
ID="a769c80a-697d-4ae1-a042-6299738f9021"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_algebra-L12_diagrams.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url, data=body, method="PATCH", headers={
  "apikey":key,"Authorization":f"Bearer {key}",
  "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status", r.status)
# verify
req2=urllib.request.Request(url+"&select=practice_data", headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
s0=live["problem_bank"]["silver"][0]
print("silver[0] has chart:", bool(s0.get("chart")))
print("silver[0] chart pts:", [(d["x"],d["y"]) for d in s0["chart"]["data"]["datasets"][0]["data"]])
for t in ["bronze","silver","gold"]:
    disp=live["guided"]["teach"][t]["display"]
    print(t,"teach svg:", "<svg" in disp, "len", len(disp))
