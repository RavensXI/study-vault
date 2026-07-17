import os,json,urllib.request
ID="b73c61cf-00b8-44c8-9e08-9f7f6f84c60a"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]["practice_data"]
json.dump(pd,open("_CHK_graphsL04_LIVE.json","w"),indent=1)
print("title:",d[0].get("title"),"slug:",d[0].get("slug"))
print("keys:",sorted(pd.keys()))
pb=pd.get("problem_bank",{})
print("pb keys:",list(pb.keys()))
for t in ["bronze","silver","gold"]:
    arr=pb.get(t,[])
    print(t,"n=",len(arr))
