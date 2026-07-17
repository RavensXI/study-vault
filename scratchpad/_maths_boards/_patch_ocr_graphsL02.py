# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "e40e80e4-666f-4cce-a8b3-5f7bb6b5c490"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-ocr_graphs-L02.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)

vurl = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
print("live gold count:", len(live["problem_bank"]["gold"]))
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("live G3 sol:", live["problem_bank"]["gold"][2]["solutions"],
      "S7 sol:", live["problem_bank"]["silver"][6]["solutions"])
print("roundtrip match:", json.dumps(live, sort_keys=True) == json.dumps(pd, sort_keys=True))
