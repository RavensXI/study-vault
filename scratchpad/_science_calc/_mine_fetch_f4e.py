import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="1b30cd36-ea7e-4210-baa6-cc9f3f30072a"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
d=json.load(urllib.request.urlopen(req))
json.dump(d[0], open("_f4e_live.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("slug:", d[0].get("slug"), "| title:", d[0].get("title"))
pd=d[0]["practice_data"]
print("pd top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t,[])))
print("has guided:", "guided" in pd, "| has tier_guides:", "tier_guides" in pd)
