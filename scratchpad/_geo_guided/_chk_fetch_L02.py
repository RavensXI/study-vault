import os, json, urllib.request
ID = "a5a6dc3b-3a48-451b-b2ae-ade19de98d14"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
d = json.load(urllib.request.urlopen(req))
pd = d[0]["practice_data"]
out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_CHK_L02_live.json"
json.dump(pd, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(json.dumps(pd)))
print(list(pd.keys()))
