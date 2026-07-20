import os, json, urllib.request
ID = "e253d693-4f96-44fd-80e5-f62b89933bdf"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
d = json.load(urllib.request.urlopen(req))
pd = d[0]["practice_data"]
out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_chk_L08_live.json"
json.dump(pd, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(json.dumps(pd)))
print(list(pd.keys()))
