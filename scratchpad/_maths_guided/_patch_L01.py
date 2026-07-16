# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="560ef2dd-cbbd-4c48-a03c-192449cc74a6"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_probability-statistics-L01.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
  "apikey":key,"Authorization":f"Bearer {key}",
  "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# re-fetch to confirm
req2=urllib.request.Request(f"{url}&select=practice_data",headers={"apikey":key,"Authorization":f"Bearer {key}"})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("round-trip guided present:", "guided" in back and "tier_guides" in back)
print("gold[4] solutions:", back["problem_bank"]["gold"][4]["solutions"])
print("silver[5] display:", back["problem_bank"]["silver"][5]["display"])
