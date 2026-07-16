import os, json, urllib.request
ID="4e2bb5ad-e75a-48be-951a-0e8b8db75296"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
json.dump(pd, open("_recheck_L06_live.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))
