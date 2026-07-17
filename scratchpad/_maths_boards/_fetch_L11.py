# -*- coding: utf-8 -*-
import json, os, urllib.request

ID = "4d1cbe2a-483a-400a-9fee-5166ebde6a1b"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_aqa_algL11.json"
json.dump(pd, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze", "silver", "gold"):
    print(t, "->", len(pb.get(t) or []), "problems; desc:", repr((pb.get(t+"_description") or "")[:60]))
print("has guided:", "guided" in pd, "| tier_guides:", "tier_guides" in pd, "| method_card:", "method_card" in pd)
