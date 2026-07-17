# -*- coding: utf-8 -*-
import os, io, json, urllib.request

ID = "cdee2760-731b-4056-9231-cfd7327b0ed4"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_graphs-L08.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
req2 = urllib.request.Request(url + "&select=practice_data", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("bronze desc:", (live["problem_bank"].get("bronze_description") or "")[:40])
print("silver[3] sol:", live["problem_bank"]["silver"][3]["solutions"],
      "gold[0] sol:", live["problem_bank"]["gold"][0]["solutions"])
nfig = sum(1 for t in ("bronze", "silver", "gold") for p in live["problem_bank"][t]
           if p.get("chart") or "<svg" in (p.get("display") or ""))
print("figures on bank problems:", nfig)
