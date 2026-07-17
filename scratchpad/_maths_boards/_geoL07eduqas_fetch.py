import os, json, urllib.request
LID="f3574e2a-651d-42a7-af75-8ee52eeb48d8"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data,title,slug"%LID
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
data=json.load(urllib.request.urlopen(req))
open("_geoL07eduqas_live.json","w",encoding="utf-8").write(json.dumps(data[0], indent=1, ensure_ascii=False))
print("title:", data[0].get("title"), "| slug:", data[0].get("slug"))
pd=data[0]["practice_data"]
print("top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t,[])), "problems; has guided:", "guided" in pd, "; tier_guides:", "tier_guides" in pd)
