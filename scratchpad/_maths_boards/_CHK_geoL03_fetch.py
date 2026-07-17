import os, json, urllib.request
ID="70586def-170c-4aa7-947b-2b961cfadec2"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
out="C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK_geoL03_live.json"
open(out,"w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=1))
print("title:",data[0]["title"])
print("slug:",data[0]["slug"])
pd=data[0]["practice_data"]
print("top keys:",list(pd.keys()))
