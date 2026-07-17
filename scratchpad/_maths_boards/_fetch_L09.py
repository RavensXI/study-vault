import os, json, urllib.request
ID="5ff3e1eb-2284-4096-af06-4bcb6754b0e1"
key=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data"%ID
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":"Bearer "+key})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
json.dump(pd, open("_live_L09_aqa.json","w"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, "n=", len(pb.get(t,[])))
    for i,p in enumerate(pb.get(t,[])):
        print("  [%d]"%i, p.get("display"), "sols=", p.get("solutions"), "it=", p.get("input_type"), "calc=", p.get("calculator"))
print("has guided:", "guided" in pd, "has tier_guides:", "tier_guides" in pd)
