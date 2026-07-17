# -*- coding: utf-8 -*-
import os, json, io, urllib.request

LID = "fe589e29-485c-4272-94df-41687f398c1b"
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
KEY = os.environ["SUPABASE_SERVICE_KEY"]

pd = json.load(io.open("lesson_maths-ocr_number-L02.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(
    BASE + "?id=eq." + LID, data=body, method="PATCH",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
             "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)

# verify readback
vurl = BASE + "?id=eq." + LID + "&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
live = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
print("live top keys:", sorted(live.keys()))
print("bronze[5] display:", live["problem_bank"]["bronze"][5]["display"], live["problem_bank"]["bronze"][5]["solutions"])
print("bronze[7] display:", live["problem_bank"]["bronze"][7]["display"], live["problem_bank"]["bronze"][7]["solutions"])
print("has guided.opener:", "opener" in live.get("guided",{}))
print("tier_guides keys:", list(live.get("tier_guides",{}).keys()))
print("bronze[0] has guided_steps:", "guided_steps" in live["problem_bank"]["bronze"][0])
