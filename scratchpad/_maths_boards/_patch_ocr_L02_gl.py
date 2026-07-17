# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "1a8441e6-115c-473e-a9b7-a2276e5b7faa"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
F = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_guided/lesson_maths-ocr_probability-statistics-L02.json"
pd = json.load(io.open(F, encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)
# verify
req2 = urllib.request.Request(url+"&select=practice_data", headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
print("live keys", sorted(live.keys()))
print("has guided", "guided" in live, "tier_guides" in live)
print("gold sols", [p["solutions"] for p in live["problem_bank"]["gold"]])
