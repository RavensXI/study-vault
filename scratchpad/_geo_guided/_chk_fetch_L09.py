import os, json, urllib.request
ID = "2aeee60b-5e2f-4781-8455-e81739317bf9"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
r = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
d = json.load(urllib.request.urlopen(r))
pd = d[0]["practice_data"]
out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_CHK_L09_live.json"
json.dump(pd, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(json.dumps(pd)))
print(list(pd.keys()))
