import os,urllib.request,json
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="55a5af04-f88a-4be7-b4c0-7f89c607e266"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
r=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
d=json.load(urllib.request.urlopen(r))
open("_live_algebra-L03.json","w",encoding="utf-8").write(json.dumps(d[0]["practice_data"],ensure_ascii=False,indent=1))
print("title",d[0]["title"],"slug",d[0].get("slug"))
pd=d[0]["practice_data"]
print("top keys:",list(pd.keys()))
pb=pd.get("problem_bank",{})
print("bank keys:",list(pb.keys()) if isinstance(pb,dict) else type(pb))
