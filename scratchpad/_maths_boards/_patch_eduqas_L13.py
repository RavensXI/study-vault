# -*- coding: utf-8 -*-
import os, io, json, shutil, urllib.request
ID = "d84411dc-60b7-4f96-8f42-35486f5d7129"
key = os.environ["SUPABASE_SERVICE_KEY"]

# diagrams shard = final object (figures built into opener + bronze teach)
shutil.copyfile("lesson_maths-eduqas_algebra-L13.json", "lesson_maths-eduqas_algebra-L13_diagrams.json")

pd = json.load(io.open("lesson_maths-eduqas_algebra-L13.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
 "apikey": key, "Authorization": f"Bearer {key}",
 "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify round-trip
url2 = f"{url}&select=practice_data"
req2 = urllib.request.Request(url2, headers={"apikey": key, "Authorization": f"Bearer {key}"})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("round-trip equal:", live == pd)
print("bronze[0] display:", live["problem_bank"]["bronze"][0]["display"])
print("gold[3] display:", live["problem_bank"]["gold"][3]["display"])
print("has opener svg:", "<svg" in live["guided"]["opener"]["display"])
print("has bronze teach svg:", "<svg" in live["guided"]["teach"]["bronze"]["display"])
