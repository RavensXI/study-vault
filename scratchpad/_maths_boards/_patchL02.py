# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="cbc91397-a67c-472a-b0da-308aa9da1653"
sk=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_number-L02.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s"%ID
req=urllib.request.Request(url, data=body, method="PATCH", headers={
  "apikey":sk,"Authorization":"Bearer "+sk,
  "Content-Type":"application/json","Prefer":"return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)
# verify round-trip
req2=urllib.request.Request(url+"&select=practice_data", headers={"apikey":sk,"Authorization":"Bearer "+sk})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live has guided:", "guided" in back, "tier_guides:", "tier_guides" in back)
print("bronze[7] sol:", back["problem_bank"]["bronze"][7]["solutions"], "disp:", back["problem_bank"]["bronze"][7]["display"])
print("match written:", back==pd)
