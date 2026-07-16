import os, json, urllib.request
ID="007f6c38-d280-4dd8-801d-5bb62c612eb2"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_l04.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
print("top keys:", list(pd.keys()))
