# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "d8937c21-f4ad-4d20-971a-03186a285b7f"
key = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-eduqas_number-L07.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": f"Bearer {key}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)

# verify round-trip
vurl = f"{url}&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": key, "Authorization": f"Bearer {key}"})
got = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
print("keys live:", sorted(got.keys()))
print("has guided:", "guided" in got, "| has tier_guides:", "tier_guides" in got)
print("bronze[2] display:", got["problem_bank"]["bronze"][2]["display"])
print("silver[1] options:", got["problem_bank"]["silver"][1]["options"])
print("gold[0] options:", got["problem_bank"]["gold"][0]["options"])
print("gold[2] has svg:", "<svg" in got["problem_bank"]["gold"][2]["display"])
print("worked_examples preserved:", len(got.get("worked_examples", [])))
