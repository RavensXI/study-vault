# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="6e383a58-7e5b-4917-a28d-2881938a3def"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-ocr_probability-statistics-L04.json", encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key, "Authorization":f"Bearer {key}",
    "Content-Type":"application/json", "Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status", r.status)
# verify readback
g=urllib.request.Request(url+"&select=practice_data", headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("readback keys:", sorted(live.keys()))
print("bronze/silver/gold:", len(live["problem_bank"]["bronze"]), len(live["problem_bank"]["silver"]), len(live["problem_bank"]["gold"]))
print("has guided:", "guided" in live, "has tier_guides:", "tier_guides" in live)
print("silver[2] mean sol:", live["problem_bank"]["silver"][2]["solutions"], "gold[0] sol:", live["problem_bank"]["gold"][0]["solutions"])
print("svg count:", json.dumps(live).count("<svg"))
