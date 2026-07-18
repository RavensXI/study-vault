# -*- coding: utf-8 -*-
import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
IDS=["1b30cd36-ea7e-4210-baa6-cc9f3f30072a"]
pd=json.load(io.open("lesson_higher-calculations-L04@f4e0c074d0.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
base="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq."
hdr={"apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"}
for i in IDS:
    req=urllib.request.Request(base+i,data=body,headers=hdr,method="PATCH")
    r=urllib.request.urlopen(req); print("PATCH",i,r.status)
# verify live == shard
import hashlib
def canon(o): return json.dumps(o,sort_keys=True,ensure_ascii=False)
shard_h=hashlib.md5(canon(pd).encode()).hexdigest()
for i in IDS:
    req=urllib.request.Request(base+i+"&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    live=json.load(urllib.request.urlopen(req))[0]["practice_data"]
    print(i,"MATCH" if hashlib.md5(canon(live).encode()).hexdigest()==shard_h else "MISMATCH")
