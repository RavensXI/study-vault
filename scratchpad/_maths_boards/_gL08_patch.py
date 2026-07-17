# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "1d30ba6e-3b9a-41a9-b192-23cab4fd0d5f"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open(os.path.join(os.path.dirname(__file__), "lesson_maths-eduqas_graphs-L08.json"), encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
vurl = url + "&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(vreq) as r:
    got = json.load(r)[0]["practice_data"]
print("live has guided:", "guided" in got, "tier_guides:", "tier_guides" in got)
print("bronze n:", len(got["problem_bank"]["bronze"]), "silver[0] chart:", "chart" in got["problem_bank"]["silver"][0])
print("bronze[1] sol:", got["problem_bank"]["bronze"][1]["solutions"])
