import os, json, urllib.request
ID="d6cc3827-bbe2-42ae-b116-7c8398b1bf70"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_ps03e_live.json","w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=1))
pd=data[0]["practice_data"]
print("title:",data[0].get("title"),"slug:",data[0].get("slug"))
print("top keys:",list(pd.keys()))
print("has guided:", "guided" in pd, "| has tier_guides:", "tier_guides" in pd)
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    probs=pb.get(t) if isinstance(pb.get(t),list) else pb.get(t,{}).get("problems") if isinstance(pb.get(t),dict) else None
    print(t, "->", type(pb.get(t)).__name__)
