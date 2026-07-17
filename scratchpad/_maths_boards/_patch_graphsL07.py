# -*- coding: utf-8 -*-
import os,json,io,urllib.request
ID="063c867c-7ba6-4879-9747-c3546382aaf2"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-aqa_graphs-L07.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
  "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
# roundtrip
url2=url+"&select=practice_data"
req2=urllib.request.Request(url2,headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("roundtrip equal:", json.dumps(live,sort_keys=True,ensure_ascii=False)==json.dumps(pd,sort_keys=True,ensure_ascii=False))
print("has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
