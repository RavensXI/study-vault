# -*- coding: utf-8 -*-
import os, json, urllib.request
ID="47e48001-4c4f-45ab-a400-ba16648b2569"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-aqa_ratio-proportion-L05.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data": pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key,"Authorization":f"Bearer {key}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:", r.status)
# verify readback
url2=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req2=urllib.request.Request(url2, headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("bronze sols:", [p["solutions"] for p in live["problem_bank"]["bronze"]])
print("gold sols:", [p["solutions"] for p in live["problem_bank"]["gold"]])
print("B2 display:", live["problem_bank"]["bronze"][2]["display"])
print("G1 display:", live["problem_bank"]["gold"][1]["display"])
