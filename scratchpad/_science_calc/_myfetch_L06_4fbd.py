# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
CID = "8e511d1b-d282-4835-9969-c20a995cc72e"

url = BASE + "?id=eq." + CID + "&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    data = json.load(r)

pd = data[0]["practice_data"]
with open("_my_L06_4fbd_canonical.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("saved. top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t,[])))
