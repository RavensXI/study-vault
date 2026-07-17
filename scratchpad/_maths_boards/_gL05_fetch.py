# -*- coding: utf-8 -*-
import os, json, urllib.request, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ID = "acf8619c-92bc-4778-b29c-dd0cb973f59c"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug,unit_id"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
row = json.load(urllib.request.urlopen(req))[0]
with open("_gL05_live.json", "w", encoding="utf-8") as f:
    json.dump(row["practice_data"], f, indent=2, ensure_ascii=False)
print("title:", row.get("title"), "slug:", row.get("slug"))
pd = row["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()) if isinstance(pb, dict) else type(pb))
for t in ["bronze","silver","gold"]:
    v = pb.get(t) if isinstance(pb, dict) else None
    if isinstance(v, list):
        print(t, "count:", len(v))
print("has guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd)
