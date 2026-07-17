import os, json, urllib.request
ID="66a1ec53-d20f-4b82-b436-1b31fc88e998"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_LIVE_eduqas_L12.json","w",encoding="utf-8").write(json.dumps(data[0], ensure_ascii=False, indent=2))
print("title:", data[0].get("title"), "slug:", data[0].get("slug"))
pd=data[0]["practice_data"]
print("top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb,dict) else type(pb))
