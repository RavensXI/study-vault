# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "0c881c07-49bb-49cd-8c89-41b971335061"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_aqa_L10_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier, [])
    print("\n=== %s (%d) ===" % (tier, len(probs)))
    for i,p in enumerate(probs):
        print(i, "|", p.get("input_type"), "| sols:", p.get("solutions"), "| calc:", p.get("calculator"))
        print("     display:", p.get("display"))
