import os, json, urllib.request
ID="27ec4539-cb68-4e60-ad0d-fa0828706d80"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
json.dump(pd, open("_CHK_L10_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("saved", len(json.dumps(pd)))
print("top keys:", list(pd.keys()))
