import os, json, urllib.request
ID="014f2f50-be82-4870-a8e7-d15963b39e8f"
key=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data"%ID
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":"Bearer "+key})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
json.dump(pd, open("_L05_FRESH.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t,[])), "desc:", (t+"_description") in pb)
print("has guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd, "method_card:", "method_card" in pd)
