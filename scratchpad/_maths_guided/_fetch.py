import os, json, urllib.request
ID="23b05854-d943-42b3-85e3-de479ce8aaa0"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data"%ID
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
json.dump(pd, open("_live_L02.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK keys:", list(pd.keys()))
