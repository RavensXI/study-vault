import os, json, urllib.request
ID="55ede5fd-81e7-43de-95ed-d0b3bb681d06"
k=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=id,title,slug,practice_data"
r=urllib.request.Request(url, headers={"apikey":k,"Authorization":"Bearer "+k})
d=json.load(urllib.request.urlopen(r))
json.dump(d[0], open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_zz13_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(d[0]["practice_data"], open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_zz13_pd.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print(d[0]["title"], d[0]["slug"])
pd=d[0]["practice_data"]
print(list(pd.keys()))
