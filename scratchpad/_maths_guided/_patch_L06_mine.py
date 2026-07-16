# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "62194f78-5bda-4cdb-81db-015760b58c7a"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
pd = json.load(io.open("lesson_ratio-proportion-L06.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": f"Bearer {key}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

# verify round-trip
vurl = f"{url}&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": key, "Authorization": f"Bearer {key}"})
got = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
same = json.dumps(got, sort_keys=True) == json.dumps(pd, sort_keys=True)
print("round-trip identical:", same)
print("has guided:", "guided" in got, "| has tier_guides:", "tier_guides" in got,
      "| bronze5 sol:", got["problem_bank"]["bronze"][5]["solutions"])
