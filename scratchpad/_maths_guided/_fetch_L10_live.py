import os, json, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "ddb5e897-f8ce-4c64-961a-7d6095d41a7c"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
open("_live_algebra_L10.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
print("keys:", list(pd.keys()))
