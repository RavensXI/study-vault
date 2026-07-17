# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "6589946a-1739-4d22-add3-1a9081309921"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_live_alg8.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for tier in ("bronze", "silver", "gold"):
    probs = pb.get(tier) or []
    print("\n==== %s (%d) desc=%r ====" % (tier, len(probs), pb.get(tier + "_description")))
    for i, p in enumerate(probs):
        print(" [%d] %s | sols=%s | it=%s calc=%s" % (
            i, p.get("display"), p.get("solutions"), p.get("input_type"), p.get("calculator")))
