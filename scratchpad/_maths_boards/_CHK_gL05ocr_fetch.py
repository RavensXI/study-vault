# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "acf8619c-92bc-4778-b29c-dd0cb973f59c"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data,title,slug" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
print("title:", data[0].get("title"), "slug:", data[0].get("slug"))
with open("_CHK_gL05ocr_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze", "silver", "gold"):
    print(t, len(pb.get(t, [])), "desc:", bool(pb.get(t+"_description")))
print("has guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd, "method_card:", "method_card" in pd)
