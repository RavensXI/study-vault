# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="e58f9467-dd87-4589-9b18-b603c1966291"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-eduqas_number-L01.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# verify readback
g=urllib.request.Request(url+"&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
live=json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("readback keys:",sorted(live.keys()))
print("bronze n:",len(live["problem_bank"]["bronze"]),"silver n:",len(live["problem_bank"]["silver"]),"gold n:",len(live["problem_bank"]["gold"]))
print("has guided.opener:", "opener" in live.get("guided",{}), "has tier_guides:", "tier_guides" in live)
print("match written:", json.dumps(live,sort_keys=True)==json.dumps(pd,sort_keys=True))
