# -*- coding: utf-8 -*-
import json, os, io, urllib.request

ID = "e253d693-4f96-44fd-80e5-f62b89933bdf"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "lesson_L08.json"), encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

# verify
req2 = urllib.request.Request(url + "&select=practice_data",
                              headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("keys:", sorted(live.keys()))
print("identical to file:", json.dumps(live, sort_keys=True, ensure_ascii=False) ==
      json.dumps(pd, sort_keys=True, ensure_ascii=False))
print("tier descs:", all(live["problem_bank"].get(t + "_description") for t in ("bronze", "silver", "gold")))
n_wrong = json.dumps(live).count('"check": "wrong"')
print("surviving check-wrong:", n_wrong)
