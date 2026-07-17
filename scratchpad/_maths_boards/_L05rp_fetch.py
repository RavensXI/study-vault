# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "ddbb6863-36ab-4898-8090-16df440a9d85"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug,unit_id"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
row = json.load(urllib.request.urlopen(req))[0]
with open("_L05rp_live.json", "w", encoding="utf-8") as f:
    json.dump(row["practice_data"], f, indent=2, ensure_ascii=False)
print("title:", row.get("title"), "| slug:", row.get("slug"))
pd = row["practice_data"]
print("TOP KEYS:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb, dict) else type(pb))
for t in ["bronze","silver","gold"]:
    v = pb.get(t) if isinstance(pb, dict) else None
    if isinstance(v, list):
        print(f"--- {t}: {len(v)} problems ---")
        for i,p in enumerate(v):
            print(f"  [{i}] disp={p.get('display','')[:90]!r}")
            print(f"       sol={p.get('solutions')} input={p.get('input_type')} calc={p.get('calculator')}")
