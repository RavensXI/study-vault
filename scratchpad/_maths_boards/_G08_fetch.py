# -*- coding: utf-8 -*-
import os, io, json, urllib.request

ID = "cdee2760-731b-4056-9231-cfd7327b0ed4"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data,title,lesson_number" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
row = data[0]
io.open("_G08_live.json", "w", encoding="utf-8").write(json.dumps(row, ensure_ascii=False, indent=1))
pd = row["practice_data"]
print("title:", row["title"], "n:", row["lesson_number"])
print("top keys:", sorted(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze","silver","gold"):
    print(t, "count:", len(pb.get(t) or []), "desc:", (pb.get(t+"_description") or "")[:60])
print("has guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd, "method_card:", "method_card" in pd)
