# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="a1bdc834-74b8-41cf-8671-c1e3e5270619"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("_L02exp_patched_pd.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":KEY,"Authorization":f"Bearer {KEY}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
print("PATCH status:", urllib.request.urlopen(req).status)
# round-trip verify
req2=urllib.request.Request(url+"&select=practice_data,title",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
live=json.load(urllib.request.urlopen(req2))[0]
lp=live["practice_data"]
print("title:", live["title"])
print("worked_examples now:")
for w in lp["worked_examples"]:
    print("   ", w["difficulty"], "->", w["question"], "=", w["steps"][-1]["content"])
print("related_videos count:", len(lp.get("related_videos") or []))
print("topic_links count:", len(lp.get("topic_links") or []))
print("top keys:", sorted(lp.keys()))
