import os, json, urllib.request
ID="d84411dc-60b7-4f96-8f42-35486f5d7129"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-eduqas_algebra-L13.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key,"Authorization":f"Bearer {key}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:", r.status)

# verify round-trip
gurl=f"{url}&select=practice_data"
greq=urllib.request.Request(gurl, headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(greq))[0]["practice_data"]
bd=live["guided"]["teach"]["bronze"]["display"]
s2=live["problem_bank"]["silver"][2]
print("viewBox 300:", '0 0 300 78' in bd)
print("silver[2] options:", s2["options"])
print("distinct options:", len(set(s2["options"]))==4)
print("expects:", [m["expect"] for m in s2["misconceptions"]])
print("solutions:", s2["solutions"])
