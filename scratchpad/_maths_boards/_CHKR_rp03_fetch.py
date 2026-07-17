import os, json, urllib.request
ID="2351f9ce-12fd-4b0e-95ac-c89fb8adc612"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_CHKR_rp03_live.json","w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=1))
print("title:",data[0].get("title"),"slug:",data[0].get("slug"))
pd=data[0]["practice_data"]
print("top keys:",list(pd.keys()))
