import os, json, urllib.request
ID="aae0e652-fbec-4f5d-b06a-abfea8eeb630"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=id,title,slug,practice_data"
r=urllib.request.Request(url, headers={"apikey":key,"Authorization":"Bearer "+key})
d=json.load(urllib.request.urlopen(r))
out=r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_adv14_live.json"
json.dump(d[0], open(out,"w",encoding="utf-8"), indent=1, ensure_ascii=False)
print(d[0]["title"], d[0]["slug"], len(json.dumps(d[0]["practice_data"])))
