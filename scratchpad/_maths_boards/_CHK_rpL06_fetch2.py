import os, json, urllib.request

LID = "ca643606-adf3-40c8-a4dd-8dfb8c25a21f"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": key,
    "Authorization": f"Bearer {key}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)

out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK_rpL06_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=2, ensure_ascii=False)
print("title:", data[0].get("title"))
print("slug:", data[0].get("slug"))
print("written", out)
