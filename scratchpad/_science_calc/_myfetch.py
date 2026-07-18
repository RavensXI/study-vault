import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="d42fee71-d641-4f20-90c6-8bde5e185595"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title,unit_id"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
d=json.load(urllib.request.urlopen(req))
json.dump(d[0], open("_MY_canonical.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("slug:", d[0]["slug"], "| title:", d[0]["title"])
pd=d[0]["practice_data"]
print("pd keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t,[])))
