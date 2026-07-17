# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "47a41e5d-3d22-45fd-a1c0-b29405585d87"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_geoL08_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("top keys:", sorted(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze", "silver", "gold"):
    print(t, len(pb.get(t) or []), "problems")
