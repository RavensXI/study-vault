import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="3a0b41fb-d6d3-43ac-9d74-08abb8926e8a"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
r=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
d=json.load(urllib.request.urlopen(r))
pd=d[0]["practice_data"]
json.dump(pd, open("_u12_live.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(json.dumps(pd)))
print(list(pd.keys()))
