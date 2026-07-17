import os, json, urllib.request

ID = "09c2b39e-ac37-4058-8de3-22b163764aa7"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_chk_num02_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=2, ensure_ascii=False)
print("title:", data[0].get("title"), "slug:", data[0].get("slug"))
pd = data[0]["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ("bronze","silver","gold"):
    if tier in pb:
        print(tier, "->", len(pb[tier]), "problems")
