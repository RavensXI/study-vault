import os, json, urllib.request
ID="2e75898f-577a-42bd-b94e-f1435e89ace3"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))[0]
json.dump(d, open("_L05e_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
pd=d["practice_data"]
print("title:", d["title"], "| slug:", d.get("slug"))
print("top keys:", list(pd.keys()))
print("has guided:", "guided" in pd, "| has tier_guides:", "tier_guides" in pd)
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb,dict) else type(pb))
for t in ["bronze","silver","gold"]:
    probs = pb.get(t) if isinstance(pb,dict) else None
    if isinstance(probs,list):
        print(f"  {t}: {len(probs)} problems")
