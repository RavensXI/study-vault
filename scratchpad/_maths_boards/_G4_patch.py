# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "0334612d-1b10-4495-8d37-21ef41d3a925"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
F = r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_graphs-L04.json"
pd = json.load(io.open(F, encoding="utf-8"))

URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

# re-fetch and confirm
g = urllib.request.Request(URL + "&select=practice_data", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(g))[0]["practice_data"]
pbl = live["problem_bank"]
print("live tiers:", len(pbl["bronze"]), len(pbl["silver"]), len(pbl["gold"]))
print("has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze journey data:", pbl["bronze"][0]["chart"]["data"]["datasets"][0]["data"])
print("S5 solution:", pbl["silver"][5]["solutions"], "| display:", pbl["silver"][5]["display"][:40])
print("gold charts:", sum(1 for p in pbl["gold"] if "chart" in p), "/5")
print("silver charts:", sum(1 for p in pbl["silver"] if "chart" in p), "/7")
print("match written == live:", json.dumps(pd, sort_keys=True) == json.dumps(live, sort_keys=True))
