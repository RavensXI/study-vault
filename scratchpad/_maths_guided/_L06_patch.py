# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "4e2bb5ad-e75a-48be-951a-0e8b8db75296"
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
pd = json.load(io.open("lesson_geometry-L06_diagrams.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify: re-fetch and count svgs
g = urllib.request.Request(url + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(g) as r:
    live = json.loads(r.read().decode("utf-8"))[0]["practice_data"]
s = json.dumps(live, ensure_ascii=False)
print("live svg count:", s.count("<svg"))
print("live degree signs:", s.count(chr(176)))
