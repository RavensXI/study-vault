import os, json, urllib.request
ID="4fd08300-e0fe-44c5-93cd-76b6d900c72d"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_CHK_L05n_live.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("keys:",list(pd.keys()))
print("bank tiers:",{k:len(v) for k,v in pd.get("problem_bank",{}).items() if isinstance(v,list)})
