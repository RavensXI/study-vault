import os,json,urllib.request
ID="74e144eb-d320-44e4-afed-c9a263b3af36"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
row=d[0]
pd=row["practice_data"]
json.dump(pd,open("_live_graphsL05.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print("title:",row.get("title"),"slug:",row.get("slug"))
print("keys:",list(pd.keys()))
pb=pd.get("problem_bank",{})
print("pb keys:",list(pb.keys()))
for t in ["bronze","silver","gold"]:
    arr=pb.get(t,[])
    print(t,"n=",len(arr))
print("has guided:", "guided" in pd)
print("has tier_guides:", "tier_guides" in pd)
