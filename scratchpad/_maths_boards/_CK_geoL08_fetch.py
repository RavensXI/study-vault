import os, json, urllib.request
ID="3e214279-84c2-41dc-a639-94bda78e2da8"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
json.dump(d[0], open("_CK_geoL08_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("title:",d[0]["title"],"slug:",d[0]["slug"])
pd=d[0]["practice_data"]
print("keys:",list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ["bronze","silver","gold"]:
    print(t, len(pb.get(t,[])) if isinstance(pb.get(t),list) else "n/a")
