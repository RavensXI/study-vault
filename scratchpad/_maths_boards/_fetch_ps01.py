# -*- coding: utf-8 -*-
import os, json, urllib.request

LID = "aa2fb8d9-f47f-4412-8231-28085ce43740"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % LID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_live_ps01.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier) or []
    print("== %s (%d) ==" % (tier, len(probs)))
    for i,p in enumerate(probs):
        print("  [%d] it=%s calc=%s sols=%s" % (i, p.get("input_type"), p.get("calculator"), p.get("solutions")))
        print("      D:", (p.get("display") or "")[:200])
