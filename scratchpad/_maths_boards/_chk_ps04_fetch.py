import os, json, urllib.request

ID = "54d6fba0-9730-427b-917f-ca3487dc16e9"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_chk_ps04_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("wrote", out)
print("top keys:", list(pd.keys()))
