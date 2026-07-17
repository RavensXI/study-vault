import os, json, urllib.request

LID = "295660a5-6ee6-40a4-9c32-c6aa0de7a590"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data,title,slug,unit_id"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_eduqas_graphs-L05.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(row["practice_data"], f, ensure_ascii=False, indent=1)
print("title:", row.get("title"), "| slug:", row.get("slug"))
pd = row["practice_data"]
pb = pd.get("problem_bank", {})
for tier in ["bronze","silver","gold"]:
    probs = pb.get(tier, [])
    print(f"\n=== {tier}: {len(probs)} problems ===")
    for i,p in enumerate(probs):
        print(f"  [{i}] sol={p.get('solutions')} calc={p.get('calculator')} it={p.get('input_type')} chart={'Y' if p.get('chart') else '-'}")
        print(f"       display: {p.get('display','')[:120]}")
print("\nTop-level keys:", list(pd.keys()))
