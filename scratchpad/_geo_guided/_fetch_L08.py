# -*- coding: utf-8 -*-
import json, os, io, urllib.request

ID = "e253d693-4f96-44fd-80e5-f62b89933bdf"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_live_L08.json")
io.open(out, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False, indent=1))
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze", "silver", "gold"):
    print(t, len(pb.get(t) or []))
print("wrote", out, os.path.getsize(out))
