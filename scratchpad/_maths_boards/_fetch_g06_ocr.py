# -*- coding: utf-8 -*-
import os, json, urllib.request

LID = "fe05d231-ed67-4625-aa4d-791c6b1d9887"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % LID
req = urllib.request.Request(URL, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_g06_ocr.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("top keys:", sorted(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    ps = pb.get(tier, [])
    print("\n=== %s (%d) ===" % (tier, len(ps)))
    for i,p in enumerate(ps):
        print(" [%d] %s | sols=%s it=%s calc=%s" % (i, p.get("display","")[:90], p.get("solutions"), p.get("input_type"), p.get("calculator")))
