# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "90c8606a-f24d-4140-91ff-20adf463a3f0"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-ocr_algebra-L07.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

# verify round-trip
vurl = f"{url}&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
g0 = live["problem_bank"]["gold"][0]
print("live gold[0]:", g0["display"], g0["solutions"])
print("has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze[0] has guided_steps:", bool(live["problem_bank"]["bronze"][0].get("guided_steps")))
print("worked_examples preserved:", len(live.get("worked_examples", [])))
