# -*- coding: utf-8 -*-
import os, io, json, urllib.request

ID = "df1cb4b9-09d1-4692-8674-2427dfe4c393"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-aqa_probability-statistics-L05.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
req2 = urllib.request.Request(url+"&select=practice_data",
    headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    got = json.load(r)[0]["practice_data"]
print("bronze[3] sol:", got["problem_bank"]["bronze"][3]["solutions"])
print("bronze[5] sol:", got["problem_bank"]["bronze"][5]["solutions"])
print("has guided:", "guided" in got, "| has tier_guides:", "tier_guides" in got)
print("gold[2] has chart:", "chart" in got["problem_bank"]["gold"][2])
print("silver[0] first single_value:", got["problem_bank"]["silver"][0].get("input_type"))
