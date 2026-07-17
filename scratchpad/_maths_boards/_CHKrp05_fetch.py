import os, json, urllib.request

ID = "ddbb6863-36ab-4898-8090-16df440a9d85"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,lesson_key,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHKrp05_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("rows:", len(data))
print("keys:", list(data[0].keys()) if data else None)
pd = data[0]["practice_data"]
print("pd keys:", list(pd.keys()))
