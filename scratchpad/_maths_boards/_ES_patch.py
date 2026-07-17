# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="a28fddf4-3ee1-48dc-b138-aa17facad15d"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-eduqas_probability-statistics-L01.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:",r.status)
# verify round-trip
url2=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req2=urllib.request.Request(url2,headers={"apikey":key,"Authorization":f"Bearer {key}"})
got=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("has guided:", "guided" in got, "| has tier_guides:", "tier_guides" in got)
print("bronze n:", len(got["problem_bank"]["bronze"]), "| b7 sols:", got["problem_bank"]["bronze"][7]["solutions"])
print("gold[0] has svg:", "<svg" in got["problem_bank"]["gold"][0]["display"])
