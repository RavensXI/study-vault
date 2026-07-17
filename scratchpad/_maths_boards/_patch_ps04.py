# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="9bf07c35-9977-4389-9fbb-7c9b3a67caea"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-aqa_probability-statistics-L04.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# read back and confirm
g=urllib.request.Request(url+"&select=practice_data",headers={"apikey":key,"Authorization":f"Bearer {key}"})
back=json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("readback keys:",sorted(back.keys()))
print("bronze[2] display starts:",back["problem_bank"]["bronze"][2]["display"][:40])
print("silver[0] has svg:","<svg" in back["problem_bank"]["silver"][0]["display"])
print("guided.opener boxes:",sum(1 for s in back["guided"]["opener"]["steps"] if s.get("answer") is not None))
print("bronze sols:",[p["solutions"] for p in back["problem_bank"]["bronze"]])
