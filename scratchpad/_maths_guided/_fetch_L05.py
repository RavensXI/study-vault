import os, json, urllib.request
wl=json.load(open("_worklist.json",encoding="utf-8"))
gid=wl["geometry-L05"]["id"]
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{gid}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
op=pd.get("guided",{}).get("opener",{})
print("OPENER KEYS:", list(op.keys()))
print(json.dumps(op, ensure_ascii=False)[:2500])
