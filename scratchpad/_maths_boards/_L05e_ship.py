# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="014f2f50-be82-4870-a8e7-d15963b39e8f"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-eduqas_algebra-L05.json",encoding="utf-8"))
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s"%ID
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key,"Authorization":"Bearer "+key,
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:", r.status)
u2="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data"%ID
req2=urllib.request.Request(u2, headers={"apikey":key,"Authorization":"Bearer "+key})
got=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live keys:", sorted(got.keys()))
print("guided?", "guided" in got, "tier_guides?", "tier_guides" in got)
print("gold[3] sol:", got["problem_bank"]["gold"][3]["solutions"])
print("match local:", got==pd)
