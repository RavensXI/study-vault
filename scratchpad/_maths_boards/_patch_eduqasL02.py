# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "bba25423-da94-4b3e-8415-2e9161014760"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + ID
pd = json.load(open("lesson_maths-eduqas_ratio-proportion-L02.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
req2 = urllib.request.Request(URL + "&select=practice_data", headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
print("live silver5[0]:", live["problem_bank"]["silver"][5]["options"][0])
print("live gold4[0]:", live["problem_bank"]["gold"][4]["options"][0])
print("live has tier_guides:", "tier_guides" in live, "| guided:", "guided" in live)
print("live bronze0 hint:", live["problem_bank"]["bronze"][0].get("hint"))
