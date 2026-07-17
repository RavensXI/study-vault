# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "a48ad66b-78c0-46f9-9db0-828173e35d1f"
key = os.environ["SUPABASE_SERVICE_KEY"]
SHARD = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_ratio-proportion-L04.json"
pd = json.load(io.open(SHARD, encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": "Bearer " + key,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

# verify round-trip
gurl = url + "&select=practice_data"
greq = urllib.request.Request(gurl, headers={"apikey": key, "Authorization": "Bearer " + key})
live = json.load(urllib.request.urlopen(greq))[0]["practice_data"]
print("live keys:", sorted(live.keys()))
print("has tier_guides:", "tier_guides" in live, "| has guided:", "guided" in live)
print("g1 chart:", "chart" in live["problem_bank"]["gold"][1])
print("bronze[0] hint:", live["problem_bank"]["bronze"][0].get("hint"))
print("bronze[0] mc0 expect:", live["problem_bank"]["bronze"][0]["misconceptions"][0]["expect"])
s = json.dumps(live, ensure_ascii=False)
print("em dashes live:", s.count("—"))
