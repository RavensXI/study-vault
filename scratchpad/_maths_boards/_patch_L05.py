# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="4fd08300-e0fe-44c5-93cd-76b6d900c72d"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("../_maths_guided/lesson_number-L05.json", encoding="utf-8"))
body=json.dumps({"practice_data":pd}, ensure_ascii=False).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status", r.status)
# verify readback
req2=urllib.request.Request(url+"&select=practice_data", headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("guided keys:", list(d.get("guided",{}).keys()), "tier_guides:", list(d.get("tier_guides",{}).keys()))
print("bronze[0] has guided_steps:", bool(d["problem_bank"]["bronze"][0].get("guided_steps")),
      "hint:", bool(d["problem_bank"]["bronze"][0].get("hint")))
print("gold[4] sol:", d["problem_bank"]["gold"][4]["solutions"],
      "worked_examples preserved:", len(d.get("worked_examples",[])),
      "related_videos:", len(d.get("related_videos",[])))
