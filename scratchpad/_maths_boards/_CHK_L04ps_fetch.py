import os, json, urllib.request
ID="6e383a58-7e5b-4917-a28d-2881938a3def"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
row=data[0]
open("_CHK_L04ps_live.json","w",encoding="utf-8").write(json.dumps(row,ensure_ascii=False,indent=1))
print("title:",row["title"])
print("slug:",row["slug"])
pd=row["practice_data"]
print("top keys:",list(pd.keys()))
