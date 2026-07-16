# -*- coding: utf-8 -*-
import json, io, os, urllib.request
ID="a43f9613-dd40-45e2-b692-00ac9c01fb92"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data"%ID
H={"apikey":KEY,"Authorization":"Bearer "+KEY}
# fetch fresh (confirm current topic before overwrite)
req=urllib.request.Request(BASE,headers=H)
cur=json.load(urllib.request.urlopen(req))[0]["practice_data"]
print("LIVE method_card.title BEFORE:", cur.get("method_card",{}).get("title"))
pd=json.load(io.open("lesson_ratio-proportion-L04.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd}).encode("utf-8")
h2=dict(H); h2["Content-Type"]="application/json"; h2["Prefer"]="return=minimal"
pr=urllib.request.Request(BASE.split("&select")[0],data=body,headers=h2,method="PATCH")
resp=urllib.request.urlopen(pr)
print("PATCH status:", resp.status)
# verify
v=json.load(urllib.request.urlopen(urllib.request.Request(BASE,headers=H)))[0]["practice_data"]
print("LIVE method_card.title AFTER:", v.get("method_card",{}).get("title"))
print("bronze n:",len(v["problem_bank"]["bronze"]),"has guided:", "guided" in v, "has tier_guides:", "tier_guides" in v)
print("related_videos[0].title:", v["related_videos"][0]["title"])
print("match written == live:", json.dumps(v,sort_keys=True)==json.dumps(pd,sort_keys=True))
