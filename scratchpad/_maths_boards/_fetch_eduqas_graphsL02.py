import os, json, urllib.request

ID = "8cd3697d-8a79-488d-87f0-7e8f6a40ddbb"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
row = data[0]
pd = row["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_eduqas_graphsL02.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("title:", row["title"], "slug:", row.get("slug"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier, [])
    print(f"\n=== {tier}: {len(probs)} problems ===")
    for i,p in enumerate(probs):
        print(f"[{i}] itype={p.get('input_type')} calc={p.get('calculator')} sol={p.get('solutions')}")
        print("    disp:", p.get("display"))
