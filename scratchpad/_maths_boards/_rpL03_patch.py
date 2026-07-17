# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "0ff5cf7c-3a9d-4854-b458-6d816b7df718"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
SHARD = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_ratio-proportion-L03.json"
pd = json.load(open(SHARD, encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify roundtrip
req2 = urllib.request.Request(URL + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
print("guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("bronze b7 sol:", live["problem_bank"]["bronze"][7]["solutions"])
print("gold count:", len(live["problem_bank"]["gold"]))
print("has cube svg:", "<svg" in live["problem_bank"]["gold"][1]["display"])
