# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "4feee23f-c960-4264-a828-cde0f9080d45"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
pd = json.load(io.open("lesson_maths-eduqas_algebra-L04.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# read-back verify
req2 = urllib.request.Request(URL + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    got = json.load(r)[0]["practice_data"]
print("keys live:", sorted(got.keys()))
print("has guided:", "guided" in got, "| has tier_guides:", "tier_guides" in got)
print("bronze[1] starts with svg:", got["problem_bank"]["bronze"][1]["display"].lstrip().startswith("<svg"))
print("bronze[4] starts with svg:", got["problem_bank"]["bronze"][4]["display"].lstrip().startswith("<svg"))
print("match written:", json.dumps(got, sort_keys=True, ensure_ascii=False) == json.dumps(pd, sort_keys=True, ensure_ascii=False))
