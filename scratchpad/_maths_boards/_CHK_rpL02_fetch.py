import os, json, urllib.request

ID = "330ee5b7-1c7b-4990-861a-b9de40f4c2a9"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK_rpL02_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=2, ensure_ascii=False)
print("slug:", data[0].get("slug"), "| title:", data[0].get("title"))
pd = data[0]["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb,dict) else type(pb))
for tier in ("bronze","silver","gold"):
    t = pb.get(tier) if isinstance(pb,dict) else None
    if isinstance(t, list):
        print(f"{tier}: {len(t)} problems")
