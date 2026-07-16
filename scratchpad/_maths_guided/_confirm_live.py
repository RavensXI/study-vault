# -*- coding: utf-8 -*-
import os, json, io, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "007f6c38-d280-4dd8-801d-5bb62c612eb2"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey":key,"Authorization":"Bearer "+key})
live = json.load(urllib.request.urlopen(req))[0]["practice_data"]
mine = json.load(io.open("lesson_number-L04.json", encoding="utf-8"))
print("MATCH" if json.dumps(live,sort_keys=True)==json.dumps(mine,sort_keys=True) else "DIFFERENT")
json.dump(live, io.open("_live_confirm_number-L04.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
