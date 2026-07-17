import os, json, urllib.request
ID="9f0126b9-ab85-4cbc-bc94-5d1214d5c4c2"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
d=json.load(urllib.request.urlopen(req))[0]
json.dump(d["practice_data"], open("_g06ocr_live.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("title:", d.get("title"), "| slug:", d.get("slug"))
pd=d["practice_data"]
print("top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, "count:", len(pb.get(t,[])), "| desc:", (pb.get(t+"_description") or "")[:60])
print("has guided:", "guided" in pd, "| has tier_guides:", "tier_guides" in pd, "| has method_card:", "method_card" in pd)
