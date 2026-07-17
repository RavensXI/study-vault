# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="83d542e3-c94b-4365-b8a9-070845b779ec"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(req))[0]["practice_data"]
local=json.load(io.open("lesson_maths-eduqas_number-L04.json",encoding="utf-8"))
same=json.dumps(live,sort_keys=True,ensure_ascii=False)==json.dumps(local,sort_keys=True,ensure_ascii=False)
print("live == shard:", same)
json.dump(live, io.open("_e_L04_livecheck.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
