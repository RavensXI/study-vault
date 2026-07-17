# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "1d30ba6e-3b9a-41a9-b192-23cab4fd0d5f"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_gL08_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t, [])), "desc:", repr(pb.get(t+"_description")))
print("has guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd)
