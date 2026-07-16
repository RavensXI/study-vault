import os, json, urllib.request, io
KEY=os.environ['SUPABASE_SERVICE_KEY']
ID="fe5f6191-4452-4313-934d-8e5d16ba1032"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
with io.open("_CHK_geomL02_live.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("saved", len(json.dumps(pd)))
print("top keys:", list(pd.keys()))
