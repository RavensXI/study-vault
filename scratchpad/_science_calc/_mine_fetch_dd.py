# -*- coding: utf-8 -*-
import os, json, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
CID = "8b8d72ed-5bdb-44b2-82e8-a7272e91d854"
url = BASE + "?id=eq." + CID + "&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
pd = json.load(urllib.request.urlopen(req))[0]["practice_data"]
with open("_mine_dd_canonical.json","w",encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t, [])))
