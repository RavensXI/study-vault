import os, json, urllib.request

ID = "bbbab852-7730-4d87-a2db-9ba6413f97b1"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
row = data[0]
pd = row["practice_data"]
print("slug:", row.get("slug"), "title:", row.get("title"))
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK_algL02ocr_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ["bronze","silver","gold"]:
    probs = pb.get(tier)
    if isinstance(probs, list):
        print(f"{tier}: {len(probs)} problems")
g = pd.get("guided", {})
print("guided keys:", list(g.keys()) if isinstance(g,dict) else type(g))
print("tier_guides keys:", list(pd.get("tier_guides",{}).keys()))
