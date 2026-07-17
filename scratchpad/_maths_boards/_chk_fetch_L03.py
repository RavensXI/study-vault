import os, json, urllib.request
ID="7ccfb7aa-adfd-4f9d-9679-35d805ddd77a"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
json.dump(data[0], open("_CHK_live_L03.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("title:", data[0].get("title"))
print("slug:", data[0].get("slug"))
pd=data[0]["practice_data"]
print("top keys:", list(pd.keys()))
print("bank tiers:", list(pd.get("problem_bank",{}).keys()) if "problem_bank" in pd else "NO BANK")
