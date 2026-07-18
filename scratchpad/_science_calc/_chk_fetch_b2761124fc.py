# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

def fetch(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data,title,slug"
    req = urllib.request.Request(url, headers={
        "apikey": KEY,
        "Authorization": "Bearer " + KEY,
    })
    with urllib.request.urlopen(req) as r:
        return json.load(r)

rid = "7876f55a-694d-4932-9bb9-43372697d1d9"
data = fetch(rid)
row = data[0]
pd = row["practice_data"]
with open("_chk_live_canonical.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("title:", row.get("title"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze", "silver", "gold"):
    probs = pb.get(t, [])
    print("---", t, len(probs), "problems; desc:", repr(pb.get(t + "_description")))
