# -*- coding: utf-8 -*-
import json, io, os, urllib.request
ID="3e214279-84c2-41dc-a639-94bda78e2da8"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(data, io.open("_fresh_L08.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("problem_bank tiers:", {k:len(v) for k,v in data["problem_bank"].items() if isinstance(v,list)})
print("has guided:", "guided" in data, "has tier_guides:", "tier_guides" in data)
print("top keys:", sorted(data.keys()))
