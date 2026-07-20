import os, json, urllib.request
ID = "2aeee60b-5e2f-4781-8455-e81739317bf9"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
p = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_rp9_live.json"
json.dump(pd, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(json.dumps(pd)))
