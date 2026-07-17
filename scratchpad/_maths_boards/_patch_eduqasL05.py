# -*- coding: utf-8 -*-
import os, json, urllib.request

LID = "295660a5-6ee6-40a4-9c32-c6aa0de7a590"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}"
SHARD = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_graphs-L05_diagrams.json"

pd = json.load(open(SHARD, encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# roundtrip verify
req2 = urllib.request.Request(URL + "&select=practice_data", headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("roundtrip equal:", json.dumps(live, sort_keys=True, ensure_ascii=False) == json.dumps(pd, sort_keys=True, ensure_ascii=False))
pbl = live["problem_bank"]
print("charts on silver 4/5/6:", [("chart" in pbl["silver"][i]) for i in (4,5,6)])
print("bronze order sols:", [p["solutions"] for p in pbl["bronze"]])
print("has guided.opener + teach:", bool(live.get("guided",{}).get("opener")), bool(live.get("guided",{}).get("teach")))
