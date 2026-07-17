# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "5ead70d6-f265-4790-86b5-573b9b16606a"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data,title,slug" % ID
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
row = data[0]
pd = row["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_ADVCHK_L07eq_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("title:", row.get("title"), "| slug:", row.get("slug"))
print("wrote", out)
print("Top keys:", sorted(pd.keys()))
print("has guided:", "guided" in pd, "| tier_guides:", "tier_guides" in pd, "| method_card:", "method_card" in pd)
