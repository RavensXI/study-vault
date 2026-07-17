# -*- coding: utf-8 -*-
import os, io, json, urllib.request

ID = "a4c149cd-abd5-4180-9ea3-449d4ac37f88"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-aqa_number-L06.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify round-trip
vurl = f"{URL}&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
back = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
print("live has tier_guides:", "tier_guides" in back)
print("live has guided.opener:", bool(back.get("guided", {}).get("opener")))
print("live gold[0] has guided_steps:", bool(back["problem_bank"]["gold"][0].get("guided_steps")))
print("live bronze_description:", bool(back["problem_bank"].get("bronze_description")))
print("round-trip equal to shard:", back == pd)
