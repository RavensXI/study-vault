# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "769be867-fe49-4cf1-b45f-1308b21e81dd"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(URL, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_live_L05.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("TOP KEYS:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier, [])
    print("\n===", tier, "(%d)" % len(probs), "desc:", repr(pb.get(tier+"_description")))
    for i,p in enumerate(probs):
        print(" [%d] %s | sols=%s calc=%s it=%s" % (
            i, p.get("display"), p.get("solutions"), p.get("calculator"), p.get("input_type")))
print("\nHAS guided:", "guided" in pd, "| tier_guides:", "tier_guides" in pd, "| method_card:", "method_card" in pd)
