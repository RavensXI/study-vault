import os, json, urllib.request
ID="bba25423-da94-4b3e-8415-2e9161014760"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_CHK_L02_live.json","w",encoding="utf-8").write(json.dumps(data[0]["practice_data"],ensure_ascii=False,indent=1))
print("slug:",data[0].get("slug"),"| title:",data[0].get("title"))
pd=data[0]["practice_data"]
print("top keys:",list(pd.keys()))
