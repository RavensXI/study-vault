# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "a36e47ae-bd22-4127-af9d-5b37e34c0b64"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_eduqas_geoL06.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("top keys:", sorted(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze","silver","gold"):
    print(t, "count:", len(pb.get(t) or []))
