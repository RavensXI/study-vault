# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "90c8606a-f24d-4140-91ff-20adf463a3f0"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_algL07ocr_live.json"
json.dump(pd, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier) or pd.get(tier)
    if isinstance(probs, list):
        print(tier, "count:", len(probs))
