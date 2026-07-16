import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="ddb5e897-f8ce-4c64-961a-7d6095d41a7c"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
json.dump(pd, open("_L10_live_fresh.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("fetched, keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t,[])))
