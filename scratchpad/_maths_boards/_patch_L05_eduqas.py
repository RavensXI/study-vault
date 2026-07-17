# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "769be867-fe49-4cf1-b45f-1308b21e81dd"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
pd = json.load(io.open("../_maths_guided/lesson_maths-eduqas_number-L05.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)
req2 = urllib.request.Request(URL + "&select=practice_data", headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
got = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live guided:", list(got.get("guided", {}).keys()), "| tier_guides:", list(got.get("tier_guides", {}).keys()))
print("bronze[6]:", got["problem_bank"]["bronze"][6]["solutions"], got["problem_bank"]["bronze"][6]["display"])
print("gold[3]:", got["problem_bank"]["gold"][3]["solutions"], got["problem_bank"]["gold"][3]["display"])
print("worked_examples:", len(got.get("worked_examples", [])), "| bronze[0] guided_steps:", bool(got["problem_bank"]["bronze"][0].get("guided_steps")))
