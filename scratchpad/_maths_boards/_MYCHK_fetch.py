import os, json, urllib.request

ID = "ca643606-adf3-40c8-a4dd-8dfb8c25a21f"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_MYCHK_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("Top-level keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier)
    if isinstance(probs, list):
        print(f"  {tier}: {len(probs)} problems")
