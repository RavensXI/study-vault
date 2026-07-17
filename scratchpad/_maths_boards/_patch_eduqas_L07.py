# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "660796ad-070d-4a2d-af11-900e5a5af1c1"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-eduqas_graphs-L07.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
req2 = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
print("has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze[2] sol:", live["problem_bank"]["bronze"][2]["solutions"],
      "| silver[4] sol:", live["problem_bank"]["silver"][4]["solutions"])
print("round-trip equal:", json.dumps(live, sort_keys=True) == json.dumps(pd, sort_keys=True))
