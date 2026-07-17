# -*- coding: utf-8 -*-
import os,json,urllib.request
ID="74e144eb-d320-44e4-afed-c9a263b3af36"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-aqa_graphs-L05.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:",r.status)
# roundtrip verify
g=urllib.request.Request(url+"&select=practice_data",headers={"apikey":key,"Authorization":f"Bearer {key}"})
back=json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("roundtrip has guided:", "guided" in back, "tier_guides:", "tier_guides" in back)
print("bronze[4] sol:", back["problem_bank"]["bronze"][4]["solutions"], "disp:", back["problem_bank"]["bronze"][4]["display"])
print("silver[5] sol:", back["problem_bank"]["silver"][5]["solutions"])
print("charts live:", sum('chart' in p for t in ('bronze','silver','gold') for p in back['problem_bank'][t]))
print("opener svg live:", "<svg" in back["guided"]["opener"]["display"])
print("match written == live:", back==pd)
