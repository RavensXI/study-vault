# -*- coding: utf-8 -*-
import os, json, urllib.request

ID="5ea35085-7e2c-4216-9829-f0eda94acb67"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-ocr_graphs-L07.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
  "apikey":key,"Authorization":f"Bearer {key}",
  "Content-Type":"application/json","Prefer":"return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status",r.status)

# verify round-trip
vurl=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
vreq=urllib.request.Request(vurl,headers={"apikey":key,"Authorization":f"Bearer {key}"})
with urllib.request.urlopen(vreq) as r:
    live=json.load(r)[0]["practice_data"]
print("live has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze[0] input_type:", live["problem_bank"]["bronze"][0]["input_type"])
print("gold[0] has chart:", "chart" in live["problem_bank"]["gold"][0])
print("match written:", live==pd)
