import os, json, urllib.request
ID="6e4a84ec-b6c4-489b-9d86-0cc1a7fb65b0"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-aqa_geometry-L06.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status",r.status)
# verify readback
req2=urllib.request.Request(url+"&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    got=json.load(r)[0]["practice_data"]
print("readback keys:",list(got.keys()))
print("bronze[1] sol (was 49.5):",got["problem_bank"]["bronze"][1]["solutions"])
print("silver[1] sol (was 35.2):",got["problem_bank"]["silver"][1]["solutions"])
print("bronze[3] sol (was 10, now 12):",got["problem_bank"]["bronze"][3]["solutions"])
print("has guided:",("guided" in got),"has tier_guides:",("tier_guides" in got))
import json as _j
print("svg count:",_j.dumps(got).count("<svg"))
