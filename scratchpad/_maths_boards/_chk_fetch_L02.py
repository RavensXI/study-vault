import os, json, urllib.request
ID="a1bdc834-74b8-41cf-8671-c1e3e5270619"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title,unit_id"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
json.dump(data[0], open("_chk_L02_live.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
pd=data[0]["practice_data"]
print("title:", data[0].get("title"), "slug:", data[0].get("slug"))
print("top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb,dict) else type(pb))
