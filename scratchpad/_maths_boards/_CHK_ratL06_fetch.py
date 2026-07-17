import os, json, urllib.request

ID = "e15d6925-608b-4c05-aa82-c4782d1657b3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK_ratL06_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=1, ensure_ascii=False)
pd = data[0]["practice_data"]
print("title:", data[0].get("title"), "| slug:", data[0].get("slug"))
print("top keys:", list(pd.keys()))
