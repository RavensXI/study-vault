# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "4e2bb5ad-e75a-48be-951a-0e8b8db75296"
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode("utf-8"))
pd = data[0]["practice_data"]
with open("_L06_diag_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("saved bytes:", len(json.dumps(pd)))
print("top keys:", list(pd.keys()))
