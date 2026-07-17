# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "2351f9ce-12fd-4b0e-95ac-c89fb8adc612"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-eduqas_ratio-proportion-L03.json", encoding="utf-8"))

url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify round-trip
req2 = urllib.request.Request(url + "&select=practice_data", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("live gold[2] opt0:", live["problem_bank"]["gold"][2]["options"][0])
print("live bronze[0] hint set:", bool(live["problem_bank"]["bronze"][0].get("hint")))
