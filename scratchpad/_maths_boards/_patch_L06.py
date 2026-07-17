# -*- coding: utf-8 -*-
import os, json, io, urllib.request, shutil

ID="4e8ba0ab-6dca-4615-98e2-2fac39408f5c"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
SRC="lesson_maths-ocr_ratio-proportion-L06.json"
# diagrams shard is identical final object
shutil.copyfile(SRC, "lesson_maths-ocr_ratio-proportion-L06_diagrams.json")

pd=json.load(io.open(SRC,encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":KEY,"Authorization":f"Bearer {KEY}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status:",r.status)

# re-fetch to confirm
g=urllib.request.Request(url+"&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
with urllib.request.urlopen(g) as r:
    live=json.load(r)[0]["practice_data"]
pb=live["problem_bank"]
print("live silver[2] sol:",pb["silver"][2]["solutions"])
print("live gold[0] sol:",pb["gold"][0]["solutions"])
print("live bronze sols:",[p["solutions"] for p in pb["bronze"]])
print("live has guided:","guided" in live,"tier_guides:","tier_guides" in live)
print("live bronze[0] has svg:","<svg" in pb["bronze"][0]["display"])
print("match built==live:", json.dumps(live,sort_keys=True)==json.dumps(pd,sort_keys=True))
