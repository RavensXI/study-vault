# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "7f991a30-4b90-4e0e-8cf8-f37a3210006e"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data,title,slug" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
row = data[0]
print("TITLE:", row.get("title"))
print("SLUG:", row.get("slug"))
pd = row["practice_data"]
with open("_live_geometry-L04.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("TOP KEYS:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    probs = pb.get(t, [])
    print("\n=== %s (%d) desc=%r ===" % (t, len(probs), pb.get(t+"_description")))
    for i,p in enumerate(probs):
        print("  [%d] it=%s calc=%s sol=%s" % (i, p.get("input_type"), p.get("calculator"), p.get("solutions")))
        print("      disp:", (p.get("display") or "")[:220])
