# -*- coding: utf-8 -*-
import json, os, io, urllib.request

ID = "4d1cbe2a-483a-400a-9fee-5166ebde6a1b"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-aqa_algebra-L11.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
url2 = url + "&select=practice_data"
req2 = urllib.request.Request(url2, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    got = json.load(r)[0]["practice_data"]
print("round-trip keys:", sorted(got.keys()))
print("guided present:", "guided" in got, "| tier_guides:", "tier_guides" in got)
print("bronze desc:", repr(got["problem_bank"]["bronze_description"]))
print("bronze[7] display:", got["problem_bank"]["bronze"][7]["display"])
print("match:", json.dumps(got,sort_keys=True)==json.dumps(pd,sort_keys=True))
