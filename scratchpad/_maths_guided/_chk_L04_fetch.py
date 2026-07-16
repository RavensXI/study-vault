import os, json, urllib.request
ID="1d039d5e-b358-4864-b935-b3334ba99d20"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data=json.load(urllib.request.urlopen(req))
open("_CHK_L04_live.json","w",encoding="utf-8").write(json.dumps(data[0], ensure_ascii=False, indent=2))
print("slug", data[0].get("slug"), "title", data[0].get("title"))
pd=data[0]["practice_data"]
print("top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb,dict) else type(pb))
