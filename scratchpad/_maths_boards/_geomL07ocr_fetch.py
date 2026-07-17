# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "813488f9-f52c-4d54-8b53-c95eded2df12"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_geomL07ocr_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t) or []))
    for i,p in enumerate(pb.get(t) or []):
        print("  ", t, i, "sols=", p.get("solutions"), "it=", p.get("input_type"), "calc=", p.get("calculator"))
        print("     disp:", (p.get("display") or "")[:160])
print("has guided?", "guided" in pd, "tier_guides?", "tier_guides" in pd, "method_card?", "method_card" in pd)
