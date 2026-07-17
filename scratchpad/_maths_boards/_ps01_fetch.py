# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "32c2c2c1-056b-4d78-b025-7e1e6f7ab3f3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
url = BASE + "?id=eq." + ID + "&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_ps01_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze","silver","gold"):
    probs = pb.get(t) or []
    print(t, len(probs), "desc:", repr((pb.get(t+"_description") or ""))[:80])
print("has guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd)
print("has method_card:", "method_card" in pd)
# pre-dump
try:
    predump = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
    if isinstance(predump, dict) and ID in predump:
        entry = predump[ID]
    elif isinstance(predump, dict) and "probability-statistics-L01" in predump:
        entry = predump["probability-statistics-L01"]
    else:
        entry = None
    print("predump type", type(predump), "top keys sample:", list(predump.keys())[:5] if isinstance(predump,dict) else len(predump))
except Exception as e:
    print("predump err", e)
