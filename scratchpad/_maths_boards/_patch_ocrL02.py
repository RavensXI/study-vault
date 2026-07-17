# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="330ee5b7-1c7b-4990-861a-b9de40f4c2a9"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-ocr_ratio-proportion-L02.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify readback
req2=urllib.request.Request(url+"&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("readback gold[3] expect:",live["problem_bank"]["gold"][3]["misconceptions"][0]["expect"])
print("readback bronze[2] display:",live["problem_bank"]["bronze"][2]["display"])
print("has guided.opener:", "opener" in live.get("guided",{}))
print("has tier_guides:", set(live.get("tier_guides",{}).keys()))
print("method_card steps:", len(live["method_card"]["steps"]))
