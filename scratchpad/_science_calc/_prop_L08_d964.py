# -*- coding: utf-8 -*-
import os,json,io,urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def get(rid):
    req=urllib.request.Request(f"{BASE}?id=eq.{rid}&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r: return json.load(r)[0]["practice_data"]
a=get("af432bd7-94b6-4601-a30d-4356767061bb")
b=get("578cc26a-c6ab-4e1f-b87d-f818dd50e901")
loc=json.load(io.open("lesson_physics-calculations-L08@d964afae07.json",encoding="utf-8"))
ja=json.dumps(a,sort_keys=True,ensure_ascii=False)
jb=json.dumps(b,sort_keys=True,ensure_ascii=False)
jl=json.dumps(loc,sort_keys=True,ensure_ascii=False)
print("live A == live B :",ja==jb)
print("live A == my file:",ja==jl)
json.dump(a,io.open("_live_after_L08.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
