import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="ddb5e897-f8ce-4c64-961a-7d6095d41a7c"
pd=json.load(open("lesson_algebra-L10_diagrams.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
  "apikey":KEY,"Authorization":f"Bearer {KEY}",
  "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify
vurl=f"{url}&select=practice_data"
vreq=urllib.request.Request(vurl, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
live=json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
n=sum(1 for g in live["problem_bank"]["gold"] if "<svg" in g["display"])
print("gold problems with svg live:",n)
