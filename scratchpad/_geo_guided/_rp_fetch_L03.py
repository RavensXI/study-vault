import os, json, urllib.request
K = os.environ["SUPABASE_SERVICE_KEY"]
ID = "0d2298c0-fb7d-447b-80ee-0cf8468366f2"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
r = urllib.request.Request(url, headers={"apikey": K, "Authorization": "Bearer " + K})
d = json.load(urllib.request.urlopen(r))[0]["practice_data"]
out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\_rp_L03_live.json"
json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", list(d.keys()))
