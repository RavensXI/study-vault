import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="4e8ba0ab-6dca-4615-98e2-2fac39408f5c"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data=json.load(urllib.request.urlopen(req))
open("_CHK_rpL06_live.json","w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=1))
pd=data[0]["practice_data"]
print("TITLE:",data[0].get("title"),"SLUG:",data[0].get("slug"))
print("TOP KEYS:",list(pd.keys()))
print("PROBLEM_BANK KEYS:",list(pd.get("problem_bank",{}).keys()) if isinstance(pd.get("problem_bank"),dict) else "N/A")
