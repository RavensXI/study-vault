# -*- coding: utf-8 -*-
import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS=["e68bcd00-8b3f-47d3-9a5b-e327a9ddde48","3848d92a-26c5-4ebf-a4d4-7f55b392e888"]
pd=json.load(io.open("lesson_physics-calculations-L01@087ba4e3f7.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
for i in IDS:
    url=f"{BASE}?id=eq.{i}"
    req=urllib.request.Request(url,data=body,method="PATCH",headers={
        "apikey":KEY,"Authorization":f"Bearer {KEY}",
        "Content-Type":"application/json","Prefer":"return=minimal"})
    r=urllib.request.urlopen(req)
    print("PATCH",i,r.status)
# verify propagation byte-identical to authored file
canon=json.dumps(pd,sort_keys=True,ensure_ascii=False)
for i in IDS:
    url=f"{BASE}?id=eq.{i}&select=practice_data"
    req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    d=json.load(urllib.request.urlopen(req))
    live=json.dumps(d[0]["practice_data"],sort_keys=True,ensure_ascii=False)
    print("VERIFY",i,"identical-to-authored:",live==canon)
