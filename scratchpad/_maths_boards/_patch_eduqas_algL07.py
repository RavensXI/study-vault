# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "5ead70d6-f265-4790-86b5-573b9b16606a"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-eduqas_algebra-L07.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
req2 = urllib.request.Request(url + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
checks = {
    "has_guided": "guided" in live,
    "has_tier_guides": "tier_guides" in live,
    "bronze_n": len(live["problem_bank"]["bronze"]),
    "silver_n": len(live["problem_bank"]["silver"]),
    "gold_n": len(live["problem_bank"]["gold"]),
    "b4_display": live["problem_bank"]["bronze"][4]["display"][:22],
    "g2_sol": live["problem_bank"]["gold"][2]["solutions"],
    "wex_preserved": len(live.get("worked_examples", [])),
}
print(json.dumps(checks, ensure_ascii=False))
