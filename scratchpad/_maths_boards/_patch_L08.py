# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "3e214279-84c2-41dc-a639-94bda78e2da8"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
pd = json.load(io.open("lesson_maths-aqa_geometry-L08.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
gurl = URL + "&select=practice_data"
greq = urllib.request.Request(gurl, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(greq) as r:
    got = json.load(r)[0]["practice_data"]
print("live has guided:", "guided" in got, "| tier_guides:", "tier_guides" in got)
print("live bronze[0] sol:", got["problem_bank"]["bronze"][0]["solutions"])
print("live gold[1] display starts:", got["problem_bank"]["gold"][1]["display"][:60])
print("round-trip equal:", json.dumps(got, sort_keys=True) == json.dumps(pd, sort_keys=True))
