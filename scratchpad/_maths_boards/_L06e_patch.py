# -*- coding: utf-8 -*-
import os, json, urllib.request
ID="d15fddc3-0766-4882-bfc8-15a0b7208d89"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-eduqas_number-L06.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status",r.status)
# verify round-trip
req2=urllib.request.Request(url+"&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    got=json.load(r)[0]["practice_data"]
print("round-trip guided.opener present:", "opener" in got.get("guided",{}))
print("round-trip tier_guides present:", set(got.get("tier_guides",{}).keys()))
print("bronze problems:", len(got["problem_bank"]["bronze"]), "gold:", len(got["problem_bank"]["gold"]))
print("match written:", json.dumps(got,sort_keys=True)==json.dumps(pd,sort_keys=True))
