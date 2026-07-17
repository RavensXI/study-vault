import os, json, urllib.request
ID="1ee92530-13a8-48bd-901d-f8c28e6bf899"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
open("_geoL05_live.json","w",encoding="utf-8").write(json.dumps(d[0], ensure_ascii=False, indent=1))
pd=d[0]["practice_data"]
print("TITLE:", d[0].get("title"), "| SLUG:", d[0].get("slug"))
print("TOP KEYS:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb,dict) else type(pb))
for tier in ("bronze","silver","gold"):
    t=pb.get(tier)
    if isinstance(t,list): print(tier, "->", len(t), "problems")
