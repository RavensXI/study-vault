import json, os, urllib.request
ID="1e9d6465-1ec1-40a3-8138-958197366837"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
json.dump(d[0]["practice_data"], open("_chk_live_geoL03.json","w"), indent=1)
print("ok", len(json.dumps(d[0]["practice_data"])))
