# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="fc1f101a-9d1b-4eab-8bf8-8159f78caea2"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-ocr_graphs-L03.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":KEY,"Authorization":f"Bearer {KEY}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status",r.status)

# verify round-trip
g=urllib.request.Request(url+"&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
with urllib.request.urlopen(g) as r:
    back=json.load(r)[0]["practice_data"]
print("guided present:", "guided" in back and "opener" in back["guided"])
print("tier_guides present:", "tier_guides" in back)
print("charts:", sum(1 for t in ("bronze","silver","gold") for p in back["problem_bank"][t] if "chart" in p))
print("bronze[5] display:", back["problem_bank"]["bronze"][5]["display"])
print("gold[2] solutions:", back["problem_bank"]["gold"][2]["solutions"])
