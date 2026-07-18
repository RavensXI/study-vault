# -*- coding: utf-8 -*-
import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
pd=json.load(io.open("lesson_physics-calculations-L08@d964afae07.json",encoding="utf-8"))
ROWS=["af432bd7-94b6-4601-a30d-4356767061bb","578cc26a-c6ab-4e1f-b87d-f818dd50e901"]
body=json.dumps({"practice_data":pd}).encode("utf-8")
for rid in ROWS:
    req=urllib.request.Request(f"{BASE}?id=eq.{rid}",data=body,method="PATCH",
        headers={"apikey":KEY,"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"return=minimal"})
    with urllib.request.urlopen(req) as r:
        print("PATCH",rid,r.status)
