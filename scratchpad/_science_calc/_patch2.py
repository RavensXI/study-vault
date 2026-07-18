# -*- coding: utf-8 -*-
import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS=["bbd5ca5d-b290-4754-9d0a-bd5f5085c82c","8d58d615-1b59-4271-9df0-c2ddc1d0c030"]
pd=json.load(io.open("lesson_physics-calculations-L02@ffe1cce606.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
for rid in IDS:
    req=urllib.request.Request(BASE+"?id=eq."+rid,data=body,method="PATCH",
        headers={"apikey":KEY,"Authorization":"Bearer "+KEY,
                 "Content-Type":"application/json","Prefer":"return=minimal"})
    r=urllib.request.urlopen(req)
    print("PATCH",rid,r.status)
def get(rid):
    req=urllib.request.Request(BASE+"?id=eq."+rid+"&select=practice_data",
        headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
    return json.load(urllib.request.urlopen(req))[0]["practice_data"]
a=json.dumps(get(IDS[0]),sort_keys=True)
b=json.dumps(get(IDS[1]),sort_keys=True)
want=json.dumps(pd,sort_keys=True)
print("row0==shard:",a==want)
print("row1==shard:",b==want)
print("row0==row1 (byte-identical propagation):",a==b)
