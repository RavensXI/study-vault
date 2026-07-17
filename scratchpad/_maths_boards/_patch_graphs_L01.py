# -*- coding: utf-8 -*-
import json, io, os, urllib.request
ID="cc326bc8-362b-4a54-875c-f7a7ffc1b77d"
URL="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq."+ID
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_graphs-L01.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(URL+"&select=practice_data", data=body, method="PATCH",
    headers={"apikey":KEY,"Authorization":"Bearer "+KEY,"Content-Type":"application/json","Prefer":"return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status",r.status)
# verify
req2=urllib.request.Request(URL+"&select=practice_data",headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
with urllib.request.urlopen(req2) as r:
    live=json.loads(r.read())[0]["practice_data"]
print("live has guided?", "guided" in live, "tier_guides?", "tier_guides" in live)
print("bronze count", len(live["problem_bank"]["bronze"]), "silver", len(live["problem_bank"]["silver"]), "gold", len(live["problem_bank"]["gold"]))
print("B6 sol", live["problem_bank"]["bronze"][5]["solutions"], "S5 sol", live["problem_bank"]["silver"][4]["solutions"], "G3 sol", live["problem_bank"]["gold"][2]["solutions"])
print("match written?", live==pd)
