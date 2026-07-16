import os, json, urllib.request

key = os.environ["SUPABASE_SERVICE_KEY"]
lid = "1d34f8fe-3649-4053-8b54-1c4e843d7669"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{lid}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": key,
    "Authorization": f"Bearer {key}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)

pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_guided/_live_graphs_l05.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("top keys:", list(pd.keys()))
