import os, json, urllib.request
ID="64b88a88-ec47-40c2-9478-1f7ba7572096"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
r=urllib.request.Request(url, headers={"apikey":key,"Authorization":"Bearer "+key})
d=json.load(urllib.request.urlopen(r))
pd=d[0]["practice_data"]
out=r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_CHK_L06_live.json"
json.dump(pd, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(json.dumps(pd)))
print(list(pd.keys()))
