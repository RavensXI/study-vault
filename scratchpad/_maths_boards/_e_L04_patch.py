# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="83d542e3-c94b-4365-b8a9-070845b779ec"
live=json.load(io.open("_e_L04_live.json",encoding="utf-8"))["practice_data"]
new=json.load(io.open("lesson_maths-eduqas_number-L04.json",encoding="utf-8"))
# preservation check
for k in ("method_card","topic_links","worked_examples","related_videos"):
    assert json.dumps(live[k],sort_keys=True,ensure_ascii=False)==json.dumps(new[k],sort_keys=True,ensure_ascii=False), "CHANGED: "+k
print("preserved: method_card, topic_links, worked_examples, related_videos")
# PATCH
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":new},ensure_ascii=False).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status:",r.status)
