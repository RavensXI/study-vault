import os,json,urllib.request
key=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.0d2298c0-fb7d-447b-80ee-0cf8468366f2&select=practice_data"
r=urllib.request.Request(url,headers={"apikey":key,"Authorization":"Bearer "+key})
d=json.load(urllib.request.urlopen(r))
pd=d[0]["practice_data"]
json.dump(pd,open("_CHK_L03_live.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print(list(pd.keys()))
print({k:len(v) for k,v in pd.get("problem_bank",{}).items() if isinstance(v,list)})
